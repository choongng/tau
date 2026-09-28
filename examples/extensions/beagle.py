"""Beagle's engineering-practice skills and pursuit-mode support for Tau.

Beagle ships as a Claude Code plugin, but Tau does not run Claude Code's
`.claude/settings.json` hooks — its hooks are this Python extension API. This
module is therefore the port point: it loads Beagle's skills and re-implements,
on Tau's own seams, the small set of behaviours pursuit mode needs.

Campaign mode is on its way out, so nothing here reintroduces it: no run record,
no slots, no counted loop. A pursuit is a goal, a task tree grown by doing the
work, and a `done_when` command bound before the work it judges. The pieces
below exist because a specific part of that model has no Tau equivalent:

- **Skills** — a pursuit's own guidance arrives only if it is loaded. Beagle's
  pursuit skills live in the (deprecated) `beagle-campaign` plugin, beside the
  engineering-practice skills in `beagle-dev`, and both sets run scripts from
  `${CLAUDE_PLUGIN_ROOT}/skills/<name>/...`. Claude Code sets that variable per
  plugin; a shell has one. So the extension links every skill it loads into
  one merged plugin root under the Tau home, points `CLAUDE_PLUGIN_ROOT` at it,
  and registers its `skills/` — every script path then resolves, whichever
  plugin shipped it, without dragging the campaign skills into every pursuit.
- **`/pursuit`** — the driver. Injects the command's own text as the turn,
  with `${CLAUDE_PLUGIN_ROOT}` spelled out as the merged root.
- **`pursuit_dispatch`** — a headless `step-executor`. Tau has no Task tool, so
  delegation is a nested `tau -p` run: the step-executor persona appended, the
  target dir set with `--cwd`, and the model inherited from the session unless
  the caller names a Tau model/provider. Because the worker is Tau too, the
  ground-truth guard stays live inside it — a sub-agent is not a way around it.
  The driver still runs `pursuit close`; this tool only does the work and
  returns the report.
- **ground-truth guard** — the one invariant a hook can enforce: `.beagle/
  pursuit.toml` is the user's, and criteria the agent can edit are criteria the
  agent can meet by editing them. The founding write is allowed (the file does
  not exist yet); editing it after founding is blocked. This fails open: a hook
  that raised on its own error would block the very tool call it inspects.
- **orientation** — when the project is a pursuit, its goal and criteria are
  added to the system prompt at load, so the driver re-reads the goal every
  session without anything triggering a turn. It is a frame, not an order.

Everything degrades quietly: with no `beagle`, no pursuit, or no `tau` on PATH,
the extension loads and simply does less.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import re
import subprocess
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tau_agent.messages import TextContent
from tau_agent.tools import (
    AgentTool,
    AgentToolResult,
    ToolCancellationToken,
    ToolUpdateCallback,
)
from tau_coding.extensions import (
    ExtensionAPI,
    ExtensionContext,
    ToolCallHookResult,
)

#: The beagle checkout. `BEAGLE_ROOT` overrides the default `~/beagle`.
BEAGLE = Path(os.environ.get("BEAGLE_ROOT") or Path.home() / "beagle").expanduser()
BEAGLE_BIN = os.environ.get("BEAGLE_BIN", "beagle")
TAU_BIN = os.environ.get("TAU_BIN", "tau")
PLUGINS = BEAGLE / "plugins"

#: Skills linked into the merged root, per plugin; None means all of them. The
#: pursuit skills live in the deprecated campaign plugin, so only they are
#: taken from it — `containment` because a worker's brief names its
#: `run_contained.sh` for every heavy command.
SKILL_SOURCES: Mapping[str, tuple[str, ...] | None] = {
    "beagle-dev": None,
    "beagle-reference": None,
    "beagle-campaign": ("pursuit-dispatch", "offload", "containment"),
}
#: Non-skill trees a driver or skill reaches through `${CLAUDE_PLUGIN_ROOT}`.
PLUGIN_ROOT_LINKS = {
    "commands": PLUGINS / "beagle-campaign" / "commands",
    "agents": PLUGINS / "beagle-dev" / "agents",
}
#: The merged plugin root, under the Tau home (so `TAU_HOME` profiles each
#: get their own).
MERGED_ROOT_NAME = "beagle-plugin"

STEP_EXECUTOR = PLUGINS / "beagle-dev" / "agents" / "step-executor.md"
PURSUIT_COMMAND = PLUGINS / "beagle-campaign" / "commands" / "pursuit.md"
PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"
GOAL_BASENAME = "pursuit.toml"

DEFAULT_DISPATCH_TIMEOUT = 900.0

#: Pin the worker's model/provider for every dispatch without editing code.
#: Left unset, the worker inherits the session's configured provider/model —
#: correct here, where the only reachable model is local (beagle's Claude tier
#: names like `sonnet` are not Tau catalog ids and would fail validation).
WORKER_MODEL_ENV = "BEAGLE_TAU_DISPATCH_MODEL"
WORKER_PROVIDER_ENV = "BEAGLE_TAU_DISPATCH_PROVIDER"

#: Escape hatch: `BEAGLE_TAU_ALLOW_PURSUIT_EDIT=1` disables the ground-truth guard.
GUARD_DISABLE_ENV = "BEAGLE_TAU_ALLOW_PURSUIT_EDIT"

#: Last session cwd the extension saw, so the dispatch tool (which gets no
#: context) can default to the project it is working in.
_SEEN_CWD: Path | None = None
#: The merged plugin root once built, for spelling out driver text.
_PLUGIN_ROOT: Path | None = None


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def _find_goal(start: Path | None) -> Path | None:
    """The active `.beagle/pursuit.toml`, walking up from `start`; else None.

    Keyed on the file, never on a `state.json`: a pursuit founded through the
    campaign interview keeps one beside it, and reading that first would call
    the project a campaign. Same tie-break Beagle's `state.mode` makes.
    """
    if start is None:
        return None
    try:
        here = Path(start).expanduser().resolve()
    except (OSError, ValueError):
        return None
    for candidate in (here, *here.parents):
        goal = candidate / ".beagle" / GOAL_BASENAME
        try:
            if goal.is_file():
                return goal
        except OSError:
            continue
    return None


def _driver_text(path: Path) -> str:
    """A command file as a turn: frontmatter off, the plugin root spelled out.

    The text reaches the model, not a shell, so a `${CLAUDE_PLUGIN_ROOT}` left
    in it would be read literally — or resolved by a model guessing.
    """
    text = _strip_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    if _PLUGIN_ROOT is not None:
        text = text.replace(PLUGIN_ROOT_VAR, str(_PLUGIN_ROOT))
    return text


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


def _run(cmd: list[str], cwd: Path | None, timeout: float) -> tuple[int, str]:
    """Run a short capture command, failing soft (rc!=0 with the reason inline)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return 127, f"{cmd[0]}: not found on PATH"
    except subprocess.TimeoutExpired:
        return 124, f"{cmd[0]}: timed out after {timeout:.0f}s"
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return proc.returncode, out.strip()


# --------------------------------------------------------------------------- #
# ground-truth guard
# --------------------------------------------------------------------------- #

_WRITE_TOKEN = re.compile(r"(>>|>|tee\b|\bsed\b|\btruncate\b|\bdd\b|\binstall\b)")


def _bash_touches_goal(command: str) -> bool:
    """True if a bash command plausibly writes the pursuit goal, not reads it.

    Conservative in the safe direction: it only fires when the command names
    `pursuit.toml` AND carries a write token (`>`, `tee`, `sed`, ...). `cat
    pursuit.toml` or `git commit -m 'tighten pursuit.toml'` pass through; a
    redirect, in-place `sed`, or `cp/mv/tee` naming the goal does not. This is a
    backstop for the write/edit path, which is the exact mistake, not a parser.
    """
    if GOAL_BASENAME not in command:
        return False
    return bool(_WRITE_TOKEN.search(command))


def _goal_path_from_args(args: Mapping[str, Any], cwd: Path) -> Path | None:
    raw = args.get("path")
    if not isinstance(raw, str) or not raw.strip():
        return None
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = cwd / candidate
    try:
        return candidate.resolve()
    except (OSError, ValueError):
        return None


def make_guard() -> Any:
    """Build the `tool_call` guard handler (closed over nothing it can't fail open on)."""

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        global _SEEN_CWD
        # Record cwd for the dispatch tool, which receives no context.
        with contextlib.suppress(Exception):  # a stale/retired generation, ignore
            _SEEN_CWD = context.cwd

        # Fail open on EVERYTHING: a tool_call handler that raises blocks the
        # tool it was only inspecting, turning a guard bug into a hard wedge.
        if os.environ.get(GUARD_DISABLE_ENV):
            return None
        try:
            cwd = context.cwd
            goal = _find_goal(cwd)
            if goal is None:
                return None  # not a pursuit; nothing here is the ground truth
            goal_r = goal.resolve()
            tool = event.tool_name
            args = event.arguments or {}

            if tool in ("write", "edit"):
                target = _goal_path_from_args(args, cwd)
                if target is None or target != goal_r:
                    return None
                exists = goal_r.exists()
                if tool == "edit" or (tool == "write" and exists):
                    return ToolCallHookResult(
                        block=True,
                        reason=(
                            "refusing to edit .beagle/pursuit.toml after founding — its "
                            "criteria are the user's acceptance criteria, and criteria the "
                            "agent can edit are criteria the agent can meet by editing them. "
                            "If the criteria are genuinely wrong, that is a conversation with "
                            f"the user, who edits {goal}. Nothing else here writes it. "
                            f"(Escape hatch, if the user directs it: set {GUARD_DISABLE_ENV}=1.)"
                        ),
                    )
                return None  # founding write: the file does not exist yet

            if (
                tool == "bash"
                and goal_r.exists()
                and _bash_touches_goal(str(args.get("command", "")))
            ):
                return ToolCallHookResult(
                    block=True,
                    reason=(
                        f"refusing a shell write to {goal} — the pursuit goal is the user's. "
                        "Reading it (`cat`, `grep`) is fine; this command looks like a write. "
                        f"(Escape hatch, if the user directs it: set {GUARD_DISABLE_ENV}=1.)"
                    ),
                )
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return None

    return guard


# --------------------------------------------------------------------------- #
# dispatch tool: the headless step-executor
# --------------------------------------------------------------------------- #


def _worker_model(explicit: str | None) -> str:
    """Model id for the worker: explicit arg, else env, else inherit ('')."""
    if explicit and explicit.strip():
        return explicit.strip()
    return os.environ.get(WORKER_MODEL_ENV, "").strip()


def _worker_provider(explicit: str | None) -> str:
    """Provider name for the worker: explicit arg, else env, else inherit ('')."""
    if explicit and explicit.strip():
        return explicit.strip()
    return os.environ.get(WORKER_PROVIDER_ENV, "").strip()


def _make_dispatch_result(text: str) -> AgentToolResult:
    return AgentToolResult(content=[TextContent(text=text)])


def make_dispatch() -> Any:
    """Build the `pursuit_dispatch` tool executor."""

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id, on_update
        brief = arguments.get("brief")
        if not isinstance(brief, str) or not brief.strip():
            return _make_dispatch_result(
                "pursuit_dispatch: 'brief' is required. For an open task, pass: run "
                "`beagle pursuit brief <task>` and do what it says."
            )

        cwd_raw = arguments.get("cwd")
        cwd = (
            Path(cwd_raw).expanduser()
            if isinstance(cwd_raw, str) and cwd_raw
            else _SEEN_CWD or Path.cwd()
        )

        if not STEP_EXECUTOR.is_file():
            return _make_dispatch_result(
                f"pursuit_dispatch: step-executor persona not found at {STEP_EXECUTOR}."
            )

        model = _worker_model(arguments.get("model"))
        provider = _worker_provider(arguments.get("provider"))
        try:
            timeout = float(arguments.get("timeout") or DEFAULT_DISPATCH_TIMEOUT)
        except (TypeError, ValueError):
            timeout = DEFAULT_DISPATCH_TIMEOUT

        # The brief rides on stdin (tau prepends it to the prompt); the persona
        # is appended to tau's base system prompt, not swapped for it, so the
        # worker keeps the built-in tool guidance and only gains the persona.
        cmd = [
            TAU_BIN,
            "-p",
            "--cwd",
            str(cwd),
            "--append-system-prompt",
            str(STEP_EXECUTOR),
        ]
        if provider:
            cmd += ["--provider", provider]
        if model:
            cmd += ["--model", model]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(cwd),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            return _make_dispatch_result(
                f"pursuit_dispatch: {TAU_BIN!r} not found on PATH; cannot delegate. "
                "Do the work inline, or set TAU_BIN."
            )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(brief.encode("utf-8")), timeout=timeout
            )
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                proc.kill()
            await proc.wait()
            return _make_dispatch_result(
                f"pursuit_dispatch: step-executor exceeded its wall-clock budget of "
                f"{timeout:.0f}s and was killed. Budget the worker in wall-clock, not "
                "tokens; raise 'timeout' or split the task."
            )

        out = (stdout or b"").decode("utf-8", "replace").strip()
        err = (stderr or b"").decode("utf-8", "replace").strip()
        header = (
            f"[pursuit_dispatch] step-executor "
            f"(model={model or 'inherit'} provider={provider or 'inherit'}) "
            f"cwd={cwd} rc={proc.returncode}\n\n"
        )
        body = out or (f"(no stdout)\nstderr:\n{err}" if err else "(no output)")
        footer = (
            "\n\n— YOU run the close, not the worker: `beagle pursuit close <task> "
            "--outcome done --spent <n>`, after running its --done-when yourself."
        )
        return _make_dispatch_result(header + body + footer)

    return execute


DISPATCH_PARAMETERS = {
    "type": "object",
    "properties": {
        "brief": {
            "type": "string",
            "description": (
                "The worker's brief. For an open task: 'run `beagle pursuit brief <task>` "
                "and do what it says' — the record holds the intent, scope and check. "
                "The worker has no memory of this conversation."
            ),
        },
        "cwd": {
            "type": "string",
            "description": "Project root for the worker. Defaults to the session cwd.",
        },
        "model": {
            "type": "string",
            "description": (
                "Tau model id for the worker (a configured provider's id, not a Claude "
                f"tier). Omit to inherit the session's model. Env default: {WORKER_MODEL_ENV}."
            ),
        },
        "provider": {
            "type": "string",
            "description": (
                "Tau provider name for the worker. Omit to inherit. "
                f"Env default: {WORKER_PROVIDER_ENV}."
            ),
        },
        "timeout": {
            "type": "number",
            "description": (
                "Wall-clock seconds before the worker is killed. "
                f"Default: {DEFAULT_DISPATCH_TIMEOUT:.0f}."
            ),
        },
    },
    "required": ["brief"],
}


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #


def _command_pursuit(args: str, context: Any) -> str:
    """Load Beagle's `/pursuit` driver as this turn."""
    if not PURSUIT_COMMAND.is_file():
        return f"/pursuit: driver not found at {PURSUIT_COMMAND}"
    driver = _driver_text(PURSUIT_COMMAND)
    note = f"User input to /pursuit:\n{args}\n\n" if args.strip() else ""
    context.api.send_user_message(f"{note}{driver}")
    return "/pursuit: loaded the pursuit driver as this turn."


def _command_pursuit_view(args: str, context: Any) -> str:
    """Print the pursuit's current state without spending a model on it."""
    cwd = _SEEN_CWD or Path.cwd()
    rc, out = _run([BEAGLE_BIN, "status", "--root", str(cwd)], cwd, timeout=15.0)
    if rc == 127:
        return "/pursuit-view: beagle not found on PATH."
    return out or f"(beagle status exited {rc})"


# --------------------------------------------------------------------------- #
# orientation (frame, not a turn)
# --------------------------------------------------------------------------- #


def _goal_section(goal_file: Path) -> str | None:
    """A compact orientation block from `pursuit.toml`, or None if unreadable.

    Read straight from the goal file rather than shelling out to `beagle`, so
    loading never depends on `beagle` being on PATH or paying a subprocess at
    setup. The counts and ready set live behind `/pursuit-view` and
    `beagle pursuit next`; this only pins the goal and its criteria — the part
    the driver must not lose — and points at the tools.
    """
    try:
        data = tomllib.loads(goal_file.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, ValueError):
        return None
    goal = data.get("goal")
    if not isinstance(goal, dict):
        return None
    statement = goal.get("statement")
    if not isinstance(statement, str) or not statement.strip():
        return None
    criteria = goal.get("criteria")
    lines = [f"This project is a **pursuit**: {statement.strip()}", ""]
    if isinstance(criteria, list) and criteria:
        lines.append("Acceptance criteria (the user's; do not edit them to fit the work):")
        lines += [f"  - {str(c).strip()}" for c in criteria if str(c).strip()]
    lines += [
        "",
        "The loop is `beagle pursuit next` / `open` / `close` — the `done_when` bound at "
        "`open`, before the work, stands in for a verifier. Delegate a chunky step to the "
        "`pursuit_dispatch` tool (a headless step-executor sub-agent) instead of "
        "grinding it here; YOU run the close, not the worker. `/pursuit` loads the full "
        "driver; `/pursuit-view` shows counts and the ready set without a model.",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# skill wiring
# --------------------------------------------------------------------------- #


def _wanted_skills() -> dict[str, Path]:
    """Skill name -> its directory in the checkout, for every skill to load."""
    wanted: dict[str, Path] = {}
    for plugin, names in SKILL_SOURCES.items():
        skills = PLUGINS / plugin / "skills"
        if names is None:
            try:
                names = tuple(sorted(child.name for child in skills.iterdir()))
            except OSError:
                continue
        for name in names:
            src = skills / name
            if (src / "SKILL.md").is_file():
                wanted.setdefault(name, src)
    return wanted


def _sync_link(link: Path, target: Path) -> None:
    """Point `link` at `target`, replacing only a symlink this module could own."""
    try:
        if link.is_symlink():
            if Path(os.readlink(link)) == target:
                return
            link.unlink()
        elif link.exists():
            return  # a real file or dir the user manages; leave it alone
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        return


def build_plugin_root(root: Path) -> Path | None:
    """Link the loaded skills and plugin trees under `root`; its skills dir, or None.

    Idempotent, and it only ever creates or removes symlinks: a link whose
    skill left the checkout (or the load set) is dropped so the loader never
    trips on a dangling entry, and anything that is not a symlink is left as
    the user made it.
    """
    skills_dir = root / "skills"
    try:
        skills_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    wanted = _wanted_skills()
    try:
        existing = list(skills_dir.iterdir())
    except OSError:
        existing = []
    for entry in existing:
        if entry.is_symlink() and entry.name not in wanted:
            with contextlib.suppress(OSError):
                entry.unlink()
    for name, src in wanted.items():
        _sync_link(skills_dir / name, src)
    for name, target in PLUGIN_ROOT_LINKS.items():
        if target.is_dir():
            _sync_link(root / name, target)
    return skills_dir


# --------------------------------------------------------------------------- #
# setup
# --------------------------------------------------------------------------- #


def setup(tau: ExtensionAPI) -> None:
    global _SEEN_CWD, _PLUGIN_ROOT
    # 1-2. Load the engineering-practice and pursuit skills from one merged
    #      plugin root. Skills run scripts from ${CLAUDE_PLUGIN_ROOT}/skills/...;
    #      the bash tool's subprocesses inherit this process env, so exporting
    #      the merged root makes every such path resolve, whichever plugin
    #      shipped the skill. Overwritten rather than defaulted: one inherited
    #      from a Claude Code shell names a single plugin and resolves half.
    if PLUGINS.is_dir():
        root = tau.context.paths.home / MERGED_ROOT_NAME
        skills_dir = build_plugin_root(root)
        if skills_dir is not None:
            tau.register_skill_dir(skills_dir)
            _PLUGIN_ROOT = root
            os.environ["CLAUDE_PLUGIN_ROOT"] = str(root)

    # 3. The driver command, and a no-model state read.
    tau.register_command(
        "pursuit",
        _command_pursuit,
        description="Found or run a beagle pursuit — one goal, a task tree, no denominator.",
    )
    tau.register_command(
        "pursuit-view",
        _command_pursuit_view,
        description="Show the current pursuit's goal, counts and ready set (no model).",
    )

    # 4. The headless step-executor, since Tau has no Task tool.
    tau.register_tool(
        AgentTool(
            name="pursuit_dispatch",
            label="pursuit_dispatch",
            description=(
                "Delegate one well-specified pursuit task to a headless step-executor (a nested "
                "`tau -p`, inheriting this session's model unless a Tau model id is given). Pass "
                "the brief ('run `beagle pursuit brief <task>` and do what it says'). Returns "
                "the executor's report; the caller still runs `beagle pursuit close`. Use for "
                "roughly ten tool calls or more of mechanical work, not one-line edits or "
                "open-ended exploration."
            ),
            parameters=DISPATCH_PARAMETERS,
            execute_fn=make_dispatch(),
            prompt_snippet="Delegate one pursuit task to a headless step-executor sub-agent.",
            prompt_guidelines=(
                "Hand pursuit_dispatch a self-contained brief; the worker sees no conversation.",
                "The worker does the work; YOU run `beagle pursuit close` after its --done-when.",
            ),
        )
    )

    # 5. Enforce the pursuit ground truth on every tool call.
    tau.on("tool_call", make_guard())

    # 6. If this project is a pursuit, pin its goal into the prompt at load —
    #    the frame arrives, but nothing here triggers a turn. A pursuit founded
    #    mid-session (outside a load) simply misses the section until the next
    #    reload, which is the right trade against auto-starting work.
    try:
        cwd = tau.context.cwd
        _SEEN_CWD = cwd
    except Exception:  # noqa: BLE001 - context may not be bound yet
        cwd = None
    if cwd is not None:
        goal = _find_goal(cwd)
        if goal is not None:
            section = _goal_section(goal)
            if section:
                tau.add_prompt_section("Beagle pursuit", section)
