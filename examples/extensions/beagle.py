"""Beagle's engineering-practice skills and pursuit-mode support for Tau.

Beagle ships as a Claude Code plugin, but Tau does not run Claude Code's
`.claude/settings.json` hooks — its hooks are this Python extension API. This
module is therefore the port point: it loads Beagle's skills and re-implements,
on Tau's own seams, the small set of behaviours pursuit mode needs.

Campaign mode is on its way out, so nothing here reintroduces it: no slots, no
counted loop. A pursuit is a goal, a task tree grown by doing the work, and a
`done_when` command bound before the work it judges. The pieces below exist
because a specific part of that model has no Tau equivalent:

- **Skills** — a pursuit's own guidance arrives only if it is loaded. Which
  plugins the checkout ships, and where, is read from beagle's marketplace
  manifest (`.claude-plugin/marketplace.json`; a checkout without one is
  scanned for `plugins/*/.claude-plugin/plugin.json`), never assumed: the
  pursuit plugin is whichever holds the driver commands, the worker's is
  whichever holds `agents/step-executor.md`. Every skill of every plugin is
  loaded — no curated subset to go stale — and a name two plugins share is
  taken from the first in manifest order and reported. Skills run scripts
  from `${CLAUDE_PLUGIN_ROOT}/skills/<name>/...`. Claude Code sets that
  variable per plugin; a shell has one. So the extension links every skill
  into one merged plugin root under the Tau home, points `CLAUDE_PLUGIN_ROOT`
  at it, and registers its `skills/` — every script path then resolves,
  whichever plugin shipped it. A listed plugin that is missing, a manifest
  that does not parse, or a missing driver is said at session start (a
  warning, and a prompt section), not degraded quietly.
- **`/pursuit`** — the driver. Injects the command's own text as the turn, in
  the `<skill>` block `/skill:<name>` sends, with `${CLAUDE_PLUGIN_ROOT}`
  spelled out as the merged root. Registered only when the checkout has the
  driver file.
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
- **scope guard** — while `/pursuit-run` waits on a background worker
  (`beagle loop tick --awaiting`, inside its lease), the driver session's
  edit, write and writing-bash calls into an open task's declared `scope`
  are refused: two writers on one tree lose one's work. Only the recorded
  driver session is held; a subagent's calls carry its own session id.
- **orientation** — when the project is a pursuit, its goal and criteria are
  added to the system prompt at load, so the driver re-reads the goal every
  session without anything triggering a turn. It is a frame, not an order.
  Beagle's `loop-report` SessionStart hook output rides along with it.
- **`/pursuit-run`** — the uncounted loop around `/pursuit`, which needs three
  things Claude Code gives it: a session id beagle records as the run's driver
  (exported as `CLAUDE_CODE_SESSION_ID`), a way to arm the next turn
  (`pursuit_wakeup`, standing in for `ScheduleWakeup`), and the hooks (next
  bullet). The driver text is prefixed with a short note mapping its Claude
  Code names onto these. A dispatched worker runs none of the loop: it is one step of its
  parent's, and keeps the parent's session id.
- **hooks** — Tau never reads `.claude/settings.json`, so beagle's hooks run
  here, on Tau's seams: Stop hooks on `agent_settled` (objections joined into
  one more turn, and `stop_hook_active` set on the settle it produces),
  SessionStart hooks at load into the system prompt, and Bash PreToolUse hooks
  on the bash `tool_call`. `loop-guard`, `loop-report` and `commit-claims` run
  in any pursuit; `close-out`, `cadence`, `cadence-report` and
  `commit-trailer` run when `beagle hooks install` put them in the project's
  settings, under their installed timeouts — installing is how to switch them
  on under Tau as well. `tilth-load` (a Claude Code ToolSearch reminder) and
  `transcript-guard` (which needs a transcript path Tau does not expose) are
  not bridged; if installed, a one-time note at session start says so.
- **`BEAGLE_HOST=tau`** — set for every subprocess, so beagle can tell a Tau
  host from Claude Code, whose `CLAUDE_*` variables this extension borrows.
- **agent types** — background dispatch, completion notices and messaging a
  running worker come from the separate tau-subagents extension. This module
  only feeds it: each agent a beagle plugin ships is written as an agent type
  `~/.tau/agents/<plugin>:<agent>.md`, its Claude tool grants mapped onto
  Tau's, so the driver's `beagle-dev:step-executor` resolves by name. Without
  tau-subagents the files are unused and `pursuit_dispatch` stands in.

Everything degrades quietly: with no `beagle`, no pursuit, or no `tau` on PATH,
the extension loads and simply does less.
"""

from __future__ import annotations

import asyncio
import contextlib
import fnmatch
import json
import math
import os
import re
import shlex
import subprocess
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
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
from tau_coding.resources import parse_markdown_resource
from tau_coding.skills import Skill, format_skill_invocation

#: The beagle checkout. `BEAGLE_ROOT` overrides the default `~/beagle`.
BEAGLE = Path(os.environ.get("BEAGLE_ROOT") or Path.home() / "beagle").expanduser()
BEAGLE_BIN = os.environ.get("BEAGLE_BIN", "beagle")
TAU_BIN = os.environ.get("TAU_BIN", "tau")
#: Beagle's marketplace manifest: which plugins the checkout ships, in order,
#: and where each lives. The layout is read from it, never assumed.
MARKETPLACE = Path(".claude-plugin") / "marketplace.json"
#: A plugin's own manifest, for a checkout with no marketplace file.
PLUGIN_MANIFEST = Path(".claude-plugin") / "plugin.json"
#: What makes a plugin the pursuit plugin, and which one ships the worker.
DRIVER_DIR = Path("commands")
STEP_EXECUTOR_REL = Path("agents") / "step-executor.md"
#: The merged plugin root, under the Tau home (so `TAU_HOME` profiles each
#: get their own).
MERGED_ROOT_NAME = "beagle-plugin"
#: Where tau-subagents reads user agent types (it uses `~`, not `TAU_HOME`).
AGENTS_DIR = Path(
    os.environ.get("BEAGLE_TAU_AGENTS_DIR") or Path.home() / ".tau" / "agents"
).expanduser()
#: Frontmatter key marking an agent file this module wrote and may replace.
GENERATED_KEY = "generated_by"
GENERATED_BY = "beagle-tau-extension"
#: Claude Code tool names -> Tau's coding tools. Grep and Glob run through bash;
#: anything unmapped (MCP tools, Task, ...) has no Tau equivalent and is dropped.
AGENT_TOOL_MAP = {
    "Read": "read",
    "Write": "write",
    "Edit": "edit",
    "Bash": "bash",
    "Grep": "bash",
    "Glob": "bash",
}

PURSUIT_COMMAND = "pursuit.md"
PURSUIT_RUN_COMMAND = "pursuit-run.md"
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

#: Set in a `pursuit_dispatch` worker's environment. A worker acts for its
#: parent: it keeps the parent's session id and runs no loop of its own.
WORKER_ENV = "BEAGLE_TAU_WORKER"

#: Wall-clock cap on one bridged-by-default `beagle hook` call; a hook that
#: hangs fails open. An installed hook gets its own entry's timeout instead.
HOOK_TIMEOUT = 30.0
#: Where Claude Code reads a project's hooks, the key beagle marks its own
#: entries with, and the timeout `beagle hooks install` writes by default.
SETTINGS_REL = Path(".claude") / "settings.json"
HOOK_MARKER = "beagle"
DEFAULT_HOOK_TIMEOUT = 900.0
#: Installed Stop hooks bridged on `agent_settled`, in the order they run.
STOP_HOOKS = ("cadence", "close-out")
#: Every hook this extension runs, installed or not.
BRIDGED_HOOKS = frozenset(
    {"loop-guard", "loop-report", "commit-claims", *STOP_HOOKS, "cadence-report", "commit-trailer"}
)
#: Installed hooks deliberately not bridged, and why; said once at session start.
UNBRIDGED_HOOKS = {
    "tilth-load": "it prints a call to Claude Code's ToolSearch, which Tau does not have",
    "transcript-guard": "it needs the session transcript path, which Tau does not give extensions",
}
#: Set for every beagle subprocess (and the bash tool's), so beagle can tell a
#: Tau host from Claude Code, whose `CLAUDE_*` variables this extension borrows.
HOST_ENV = "BEAGLE_HOST"
#: The wakeup delay's bounds, in minutes (Claude Code clamps to 1..60 too).
WAKEUP_MIN_MINUTES = 1
WAKEUP_MAX_MINUTES = 60
#: `beagle loop read`'s exit status when no run is in flight.
LOOP_IDLE_EXIT = 3
#: beagle's loop record (`beagle loop --file`'s default), watched only for
#: change; what it says is read through `beagle loop read --json`.
LOOP_REL = Path(".beagle") / "loop.json"
#: How long beagle believes an `awaiting` with no `--for`, in minutes.
AWAITING_TTL_MINUTES = 45

#: Last session cwd the extension saw, so the dispatch tool (which gets no
#: context) can default to the project it is working in.
_SEEN_CWD: Path | None = None
#: The merged plugin root once built, for spelling out driver text.
_PLUGIN_ROOT: Path | None = None
#: The armed or fired-but-undelivered `pursuit_wakeup`, if any. One at a time,
#: like `ScheduleWakeup`.
_WAKEUP: _Wakeup | None = None
#: Whether the run now settling was started by a Stop-hook objection — the
#: hooks' `stop_hook_active`, which lets the next stop through.
_STOP_BLOCKED = False
#: Whether the last run ended on its own, rather than aborted or errored.
_LAST_RUN_CLEAN = True


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


@dataclass(frozen=True)
class Layout:
    """The beagle checkout's plugins, as its own manifests describe them.

    `plugins` is (name, directory) in manifest order, which is also the order
    ties break in: a skill, driver or agents tree is taken from the first
    plugin that has it. `problems` are what a user should hear at session
    start — a listed plugin that is missing, a manifest that does not parse,
    a skill two plugins both ship.
    """

    plugins: tuple[tuple[str, Path], ...] = ()
    found_by: str = ""
    problems: tuple[str, ...] = ()

    def first(self, rel: Path) -> Path | None:
        """`<plugin>/rel` from the first plugin where it exists."""
        for _, directory in self.plugins:
            if (directory / rel).exists():
                return directory / rel
        return None

    @property
    def commands_dir(self) -> Path | None:
        """The pursuit plugin's `commands/`: the one holding a driver."""
        for name in (PURSUIT_RUN_COMMAND, PURSUIT_COMMAND):
            found = self.first(DRIVER_DIR / name)
            if found is not None:
                return found.parent
        return None

    @property
    def step_executor(self) -> Path | None:
        return self.first(STEP_EXECUTOR_REL)

    @property
    def agents_dir(self) -> Path | None:
        """The `agents/` holding the step-executor, else the first there is."""
        found = self.step_executor
        return found.parent if found is not None else self.first(Path("agents"))

    def skills(self) -> tuple[dict[str, Path], list[str]]:
        """Every plugin's skills, name -> directory; and the clashes, described.

        All of them, not a curated list: a pursuit's driver and briefs name
        skills beyond the three it opens with (`state-stores`, `repo-hygiene`,
        ...), and a curated list goes stale the day beagle adds one.
        """
        wanted: dict[str, Path] = {}
        owner: dict[str, str] = {}
        clashes: list[str] = []
        for plugin, directory in self.plugins:
            try:
                children = sorted((directory / "skills").iterdir())
            except OSError:
                continue
            for src in children:
                if not (src / "SKILL.md").is_file():
                    continue
                if src.name in wanted:
                    clashes.append(
                        f"skill {src.name!r} ships in both {owner[src.name]} and {plugin}; "
                        f"{owner[src.name]}'s is loaded."
                    )
                    continue
                wanted[src.name] = src
                owner[src.name] = plugin
        return wanted, clashes


#: The checkout's plugins, resolved at setup.
_LAYOUT = Layout()


def _plugin_name(directory: Path) -> str:
    try:
        data = json.loads((directory / PLUGIN_MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return directory.name
    name = data.get("name") if isinstance(data, dict) else None
    return name if isinstance(name, str) and name else directory.name


def resolve_layout(beagle: Path) -> Layout:
    """Read which plugins `beagle` ships, and where, from its manifests.

    The marketplace manifest first — it names each plugin and its `source`
    directory, so a rename or a move is followed rather than broken. A
    checkout without one is scanned: `plugins/*` directories that carry a
    `plugin.json`, else every `plugins/*` directory. No beagle at all is an
    empty layout with no problems: the extension then does less, quietly.
    """
    problems: list[str] = []
    manifest = beagle / MARKETPLACE
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            entries = data.get("plugins") if isinstance(data, dict) else None
            if not isinstance(entries, list):
                raise ValueError("no `plugins` list")
        except (OSError, ValueError) as exc:
            problems.append(f"{manifest} could not be read ({exc}); scanned the checkout instead.")
        else:
            plugins: list[tuple[str, Path]] = []
            for entry in entries:
                name = entry.get("name") if isinstance(entry, dict) else None
                source = entry.get("source") if isinstance(entry, dict) else None
                if not isinstance(name, str) or not isinstance(source, str):
                    continue  # a remote source: nothing in this checkout to load
                directory = Path(os.path.normpath(beagle / source))
                if directory.is_dir():
                    plugins.append((name, directory))
                else:
                    problems.append(f"{manifest} lists {name} at {source}, which is missing.")
            if plugins:
                return Layout(tuple(plugins), str(manifest), tuple(problems))
    scanned = beagle / "plugins"
    try:
        dirs = sorted(d for d in scanned.iterdir() if d.is_dir())
    except OSError:
        return Layout(problems=tuple(problems))
    chosen = [d for d in dirs if (d / PLUGIN_MANIFEST).is_file()] or dirs
    plugins = tuple((_plugin_name(d), d) for d in chosen)
    return Layout(plugins, f"a scan of {scanned}", tuple(problems))


def _driver_file(name: str) -> Path | None:
    """The pursuit plugin's command file `name`, from the first plugin that has it."""
    return _LAYOUT.first(DRIVER_DIR / name)


def _driver_missing(name: str) -> str:
    """Why a driver command cannot run: where it was looked for."""
    plugins = ", ".join(f"{n} ({d})" for n, d in _LAYOUT.plugins) or "none found"
    return (
        f"beagle's {name} driver was not found in the commands/ of any plugin "
        f"({plugins}; from {_LAYOUT.found_by or BEAGLE}). The beagle checkout at "
        f"{BEAGLE} may predate or postdate this extension."
    )


def _driver_text(path: Path) -> str:
    """A command file's body: frontmatter off, the plugin root spelled out.

    The text reaches the model, not a shell, so a `${CLAUDE_PLUGIN_ROOT}` left
    in it would be read literally — or resolved by a model guessing.
    """
    text = _strip_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    if _PLUGIN_ROOT is not None:
        text = text.replace(PLUGIN_ROOT_VAR, str(_PLUGIN_ROOT))
    return text


def _driver_turn(name: str, args: str, preamble: str = "") -> str | None:
    """Driver command file `name` as a Tau skill invocation; None when absent.

    The same `<skill>` block `/skill:<name>` sends, so the TUI shows "Using
    skill" rather than the whole driver as a user message, and the user's
    input follows the block as `/skill:` arguments do. Located under the merged
    root, where `${CLAUDE_PLUGIN_ROOT}` in its body now points. A Tau-only
    preamble goes inside the block, ahead of the driver it qualifies.
    """
    path = _driver_file(name)
    if path is None:
        return None
    location = _PLUGIN_ROOT / "commands" / name if _PLUGIN_ROOT is not None else path
    if preamble and _PLUGIN_ROOT is not None:
        preamble = preamble.replace(PLUGIN_ROOT_VAR, str(_PLUGIN_ROOT))
    body = f"{preamble}\n{_driver_text(path)}" if preamble else _driver_text(path)
    skill = Skill(name=Path(name).stem, path=location, content=body)
    return format_skill_invocation(skill, args)


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


def _run(cmd: list[str], cwd: Path | None, timeout: float, stdin: str = "") -> tuple[int, str]:
    """Run a short capture command, failing soft (rc!=0 with the reason inline).

    stdin is always fed, never inherited: under the TUI it is the terminal, and
    a beagle hook reads its payload from it.
    """
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            input=stdin,
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
_HEREDOC = re.compile(r"(?<!<)<<(-?)\s*(['\"]?)([A-Za-z_][\w.-]*)\2")
#: Words that run the command after them: skipped to find the real one.
_WRAPPERS = frozenset({"sudo", "env", "command", "nice", "nohup", "time", "exec", "builtin"})
_SHELLS = frozenset({"sh", "bash", "zsh", "dash"})
_GLOB_CHARS = frozenset("*?[")


def _strip_heredocs(command: str) -> str:
    """`command` with every here-document body removed, keeping the `<<` lines.

    A body is data fed to a command, not shell: `cat <<EOF > notes.md` followed
    by a paragraph that mentions `> pursuit.toml` writes only notes.md.
    """
    kept: list[str] = []
    pending: list[tuple[str, bool]] = []
    for line in command.split("\n"):
        if pending:
            delimiter, dash = pending[0]
            if (line.lstrip("\t") if dash else line).strip() == delimiter:
                pending.pop(0)
            continue
        kept.append(line)
        pending += [(m.group(3), bool(m.group(1))) for m in _HEREDOC.finditer(line)]
    return "\n".join(kept)


def _shell_tokens(command: str) -> list[str] | None:
    """Shell words and operators, heredoc bodies dropped; None if unparseable."""
    text = _strip_heredocs(command).replace("\\\n", " ").replace("\n", " ; ")
    lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:  # an unclosed quote: not a command this can read
        return None


def _is_operator(token: str) -> bool:
    return bool(token) and all(c in "();<>|&" for c in token)


def _positional(args: list[str], takes_value: frozenset[str] = frozenset()) -> list[str]:
    """`args` without options, and without the values of options in `takes_value`."""
    out: list[str] = []
    skip = ended = False
    for arg in args:
        if skip:
            skip = False
        elif ended:
            out.append(arg)
        elif arg == "--":
            ended = True
        elif arg.startswith("-") and arg != "-":
            skip = arg in takes_value
        else:
            out.append(arg)
    return out


def _sed_in_place_files(args: list[str]) -> list[str]:
    """The files `sed -i` rewrites; [] when it is not in-place."""
    in_place = False
    has_script = False
    rest: list[str] = []
    it = iter(args)
    for arg in it:
        if arg.startswith("--in-place"):
            in_place = True
        elif arg in ("--expression", "--file"):
            has_script = True
            next(it, None)
        elif arg.startswith(("--expression=", "--file=")):
            has_script = True
        elif arg.startswith("-") and not arg.startswith("--") and arg != "-":
            for i, flag in enumerate(arg[1:]):
                if flag == "i":
                    in_place = True
                    break  # the rest is a backup suffix
                if flag in "ef":
                    has_script = True
                    if i == len(arg) - 2:
                        next(it, None)
                    break
        elif not arg.startswith("--"):
            rest.append(arg)
    if not in_place:
        return []
    return rest if has_script else rest[1:]


def _copy_targets(args: list[str], cwd: Path, moves: bool) -> list[str]:
    """What `cp`/`mv`/`install`/`ln` writes: the destination (per source when it
    is a directory), and for `mv` the sources it removes."""
    target_dir: str | None = None
    rest: list[str] = []
    it = iter(args)
    for arg in it:
        if arg in ("-t", "--target-directory"):
            target_dir = next(it, None)
        elif arg.startswith("--target-directory="):
            target_dir = arg.split("=", 1)[1]
        elif arg in ("-m", "--mode", "-o", "--owner", "-g", "--group", "-S", "--suffix"):
            next(it, None)
        elif not arg.startswith("-") or arg == "-":
            rest.append(arg)
    if target_dir is not None:
        sources, dest = rest, target_dir
    elif len(rest) >= 2:
        sources, dest = rest[:-1], rest[-1]
    else:
        return []
    dest_path = Path(dest).expanduser()
    is_dir = dest.endswith("/") or (cwd / dest_path).is_dir()
    targets = [str(dest_path / Path(s).name) for s in sources] if is_dir else [dest]
    return targets + (sources if moves else [])


def _command_targets(argv: list[str], cwd: Path) -> list[str] | None:
    """The paths one simple command (argv, redirects removed) writes."""
    while argv and ("=" in argv[0] and not argv[0].startswith("=") or argv[0] in _WRAPPERS):
        argv = argv[1:]
        while argv and argv[0].startswith("-"):  # a wrapper's own options
            argv = argv[1:]
    if not argv:
        return []
    name, args = Path(argv[0]).name, argv[1:]
    if name == "tee":
        return _positional(args)
    if name == "sed":
        return _sed_in_place_files(args)
    if name in ("cp", "mv", "install", "ln"):
        return _copy_targets(args, cwd, moves=name == "mv")
    if name in ("rm", "truncate", "shred", "unlink"):
        return _positional(args, frozenset({"-s", "--size", "-r", "--reference", "-n"}))
    if name == "dd":
        return [a[3:] for a in args if a.startswith("of=")]
    if name == "git" and args:
        sub, sub_args = args[0], args[1:]
        if sub == "checkout" and "--" in sub_args:
            return sub_args[sub_args.index("--") + 1 :]
        if sub == "restore":
            return _positional(sub_args, frozenset({"-s", "--source"}))
        if sub in ("stash", "clean") or (sub == "reset" and "--hard" in sub_args):
            return ["."]  # the whole work tree
    return []


def _bash_write_targets(command: str, cwd: Path) -> list[Path] | None:
    """Every path a bash command would write, resolved; None if unparseable.

    Deliberately narrow: a redirect target, a `tee` argument, a `sed -i` file,
    a `cp`/`mv`/`install`/`ln` destination (and what `mv` removes), `dd of=`,
    `rm`/`truncate`, and the `git` verbs that rewrite tracked files (`stash`,
    `clean` and `reset --hard` stand for the whole tree as `.`). A path that is
    only read — `cat pursuit.toml > /tmp/x`, `git check-ignore -v pursuit.toml`
    — is not a target. `cd` is followed along a chain, and `bash -c '...'` is
    read one level down. Anything else (a Python one-liner, `find -delete`) is
    not seen: this backs up the write/edit guard, it does not replace it.
    """
    tokens = _shell_tokens(command)
    if tokens is None:
        return None
    here = cwd
    found: list[Path] = []

    def add(raw: str, base: Path) -> None:
        path = Path(raw).expanduser()
        found.append(Path(os.path.normpath(base / path)))

    segment: list[str] = []
    tokens.append(";")
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if _is_operator(token) and ("<" in token or ">" in token):
            target = tokens[i + 1] if i + 1 < len(tokens) else ""
            if segment and segment[-1].isdigit():
                segment.pop()  # the fd number of `2>`, not an argument
            fd_dup = token.endswith("&") and (target.isdigit() or target == "-")
            if ">" in token and target and not _is_operator(target) and not fd_dup:
                add(target, here)
            i += 2 if target and not _is_operator(target) else 1
            continue
        if not _is_operator(token):
            segment.append(token)
            i += 1
            continue
        # A separator: the simple command before it is complete.
        if segment and segment[0] == "cd":
            dest = next((a for a in segment[1:] if not a.startswith("-")), "~")
            here = Path(os.path.normpath(here / Path(dest).expanduser()))
        elif segment and Path(segment[0]).name in _SHELLS and "-c" in segment[1:]:
            script_at = segment.index("-c") + 1
            if script_at < len(segment):
                nested = _bash_write_targets(segment[script_at], here)
                if nested is None:
                    return None
                found += nested
        else:
            for raw in _command_targets(segment, here):
                add(raw, here)
        segment = []
        i += 1
    return found


def _names_path(targets: list[Path], path: Path) -> bool:
    """Whether one of `targets` is `path`, literally or as a glob matching it."""
    for target in targets:
        text = str(target)
        if target == path or (_GLOB_CHARS & set(text) and fnmatch.fnmatch(str(path), text)):
            return True
    return False


def _bash_writes_goal(command: str, cwd: Path, goal: Path) -> bool:
    """True if a bash command writes the pursuit goal, not merely reads it.

    Blocks only when `pursuit.toml` is an actual write target (see
    `_bash_write_targets`): `git check-ignore -v .beagle/pursuit.toml` beside
    an unrelated `> /tmp/out` passes, `sed -i ... .beagle/pursuit.toml` does
    not. A command too broken to parse falls back to the old test — it names
    the goal and carries a write token — so doubt still lands on the safe side.
    """
    if GOAL_BASENAME not in command:
        return False
    targets = _bash_write_targets(command, cwd)
    if targets is None:
        return bool(_WRITE_TOKEN.search(command))
    return _names_path([_resolved(t) for t in targets], goal)


def _resolved(path: Path) -> Path:
    try:
        return path.resolve()
    except (OSError, ValueError):
        return path


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
                and _bash_writes_goal(str(args.get("command", "")), Path(cwd), goal_r)
            ):
                return ToolCallHookResult(
                    block=True,
                    reason=(
                        f"refusing a shell write to {goal} — the pursuit goal is the user's. "
                        "Reading it (`cat`, `grep`) is fine; this command writes it. "
                        f"(Escape hatch, if the user directs it: set {GUARD_DISABLE_ENV}=1.)"
                    ),
                )
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return None

    return guard


# --------------------------------------------------------------------------- #
# driver/worker isolation: the driver keeps out of an awaited worker's scope
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class _AwaitedScope:
    """What the driver session is waiting on, and the open tasks' scope."""

    awaiting: str
    tasks: tuple[str, ...]
    scope: tuple[str, ...]


#: Root -> (loop file stat, session, scope), so beagle is asked once per change.
_SCOPE_CACHE: dict[Path, tuple[tuple[int, int, str], _AwaitedScope | None]] = {}


def _lease_live(record: Mapping[str, Any]) -> bool:
    """Whether a declared `awaiting` is inside its lease, as beagle judges it.

    An undatable or future-dated wait is not believed — beagle's own rule,
    since a suppression nobody can date is one nobody can end.
    """
    try:
        at = datetime.fromisoformat(str(record.get("awaiting_at") or ""))
    except ValueError:
        return False
    if at.tzinfo is None:
        at = at.replace(tzinfo=UTC)
    minutes = record.get("awaiting_minutes") or AWAITING_TTL_MINUTES
    elapsed = (datetime.now(UTC) - at).total_seconds()
    return isinstance(minutes, int | float) and 0 <= elapsed <= minutes * 60


def _json_out(argv: list[str], root: Path) -> Any:
    rc, out = _run([BEAGLE_BIN, *argv, "--root", str(root)], root, HOOK_TIMEOUT)
    return json.loads(out) if rc == 0 else None


def _read_awaited_scope(root: Path, session_id: str) -> _AwaitedScope | None:
    """The scope this session's run is waiting on a worker in, or None.

    None unless a run is in flight, this session is its recorded driver (a
    subagent's own session never is), and a declared wait is inside its
    lease. The scope is every open task's: `awaiting` is free text, so which
    open task the worker holds cannot be read off it reliably.
    """
    record = _json_out(["loop", "read", "--json"], root)
    if not isinstance(record, dict) or not record.get("awaiting"):
        return None
    if not session_id or record.get("driver_session") != session_id:
        return None
    if not _lease_live(record):
        return None
    listing = _json_out(["pursuit", "tree", "--json", "--status", "open"], root)
    tasks = [row["id"] for row in listing or () if isinstance(row, dict) and row.get("id")]
    scope: list[str] = []
    for task in tasks:
        node = _json_out(["pursuit", "show", str(task)], root)
        entries = node.get("scope") if isinstance(node, dict) else None
        scope += [e for e in entries or () if isinstance(e, str) and e.strip()]
    if not scope:
        return None
    return _AwaitedScope(str(record["awaiting"]), tuple(tasks), tuple(scope))


async def _awaited_scope(root: Path, session_id: str) -> _AwaitedScope | None:
    """`_read_awaited_scope`, cached until beagle's loop record changes."""
    try:
        stat = (root / LOOP_REL).stat()
    except OSError:
        return None  # no record: no run in flight
    key = (stat.st_mtime_ns, stat.st_size, session_id)
    cached = _SCOPE_CACHE.get(root)
    if cached is None or cached[0] != key:
        found = await asyncio.to_thread(_read_awaited_scope, root, session_id)
        _SCOPE_CACHE[root] = cached = (key, found)
    return cached[1]


def _scope_hit(target: Path, root: Path, scope: tuple[str, ...]) -> str | None:
    """The scope entry `target` writes into, or contains, or None.

    A scope entry is a path under the project root — a file, a directory, or a
    glob. A write lands in it when the target is the entry, sits under it, or
    matches its glob; a target that CONTAINS an entry (`rm -r src`, or the
    whole tree for `git reset --hard`) lands in it too.
    """
    for entry in scope:
        text = entry.strip().rstrip("/") or "."
        if _GLOB_CHARS & set(text):
            pattern = str(root / text)
            static = Path(pattern.split("*")[0].split("?")[0].split("[")[0])
            if fnmatch.fnmatch(str(target), pattern) or target in (static, *static.parents):
                return entry
            continue
        path = _resolved(root / text)
        if target == path or path in target.parents or target in path.parents:
            return entry
    return None


def _write_targets(tool: str, args: Mapping[str, Any], cwd: Path) -> list[Path]:
    """The paths an edit, write or bash call writes; [] for anything else."""
    if tool in ("write", "edit"):
        target = _goal_path_from_args(args, cwd)
        return [target] if target is not None else []
    if tool == "bash":
        return [_resolved(t) for t in _bash_write_targets(str(args.get("command", "")), cwd) or ()]
    return []


def make_scope_guard() -> Any:
    """Build the `tool_call` guard that keeps the driver out of a worker's scope.

    While `/pursuit-run` waits on a background worker (`beagle loop tick
    --awaiting`), the worker owns the open task's declared scope; a driver
    that edits it too races the worker and one side's work is lost. Only the
    driver session is held back: a subagent's tool calls carry its own
    session id and pass. A command too broken to parse passes too — this
    guards a race, not the ground truth, and fails open like everything here.
    """

    async def scope_guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        try:
            cwd = Path(context.cwd)
            targets = _write_targets(event.tool_name, event.arguments or {}, cwd)
            goal = _find_goal(cwd) if targets else None
            if goal is None:
                return None
            root = _resolved(goal.parent.parent)
            waiting = await _awaited_scope(root, context.session_id or "")
            if waiting is None:
                return None
            for target in targets:
                entry = _scope_hit(target, root, waiting.scope)
                if entry is not None:
                    break
            else:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        tasks = ", ".join(waiting.tasks)
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to write {target}: it is in open task {tasks}'s scope "
                f"(`{entry}`), and this session is waiting on a worker for it "
                f"({waiting.awaiting}). Two writers on one tree lose one's work. Wait "
                "for its completion notice, steer it with `steer_subagent`, or stop it "
                "and take the task back; if the worker is gone, clear the wait with a "
                "bare `beagle loop tick` first."
            ),
        )

    return scope_guard


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

        step_executor = _LAYOUT.step_executor
        if step_executor is None:
            return _make_dispatch_result(
                "pursuit_dispatch: no beagle plugin ships "
                f"{STEP_EXECUTOR_REL} (looked in {_LAYOUT.found_by or BEAGLE})."
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
            str(step_executor),
        ]
        if provider:
            cmd += ["--provider", provider]
        if model:
            cmd += ["--model", model]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(cwd),
                env={**os.environ, WORKER_ENV: "1"},
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
# host bridge: what Claude Code gives /pursuit-run that Tau does not
# --------------------------------------------------------------------------- #


def _is_worker() -> bool:
    return bool(os.environ.get(WORKER_ENV))


def _adopt_session(context: ExtensionContext) -> None:
    """Name this Tau session to beagle the way Claude Code names its own.

    `beagle loop start` records `CLAUDE_CODE_SESSION_ID` as the run's driver,
    and `loop-guard` and `loop show` compare against it to tell this session's
    run from another's. `CLAUDE_PID` is dropped rather than set: beagle only
    believes a pid whose process is named claude or node, so Tau's would read
    as dead — and one inherited from a Claude Code shell would name the wrong
    driver. Without it, beagle judges liveness by the run's own promises.
    A worker keeps its parent's id: it acts on the parent's run.
    """
    if _is_worker():
        return
    os.environ.pop("CLAUDE_PID", None)
    session_id = context.session_id
    if session_id:
        os.environ["CLAUDE_CODE_SESSION_ID"] = session_id
    else:
        os.environ.pop("CLAUDE_CODE_SESSION_ID", None)


def _on_session_start(event: Any, context: ExtensionContext) -> None:
    global _SEEN_CWD
    del event
    _SEEN_CWD = context.cwd
    _adopt_session(context)


def _block_reason(stdout: str) -> str | None:
    """The reason from a hook's `{"decision": "block"}` line, or None (allow)."""
    for line in reversed(stdout.strip().splitlines()):
        try:
            data = json.loads(line)
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("decision") == "block":
            return str(data.get("reason") or "blocked by beagle")
    return None


async def _run_hook(
    name: str, root: Path, payload: Mapping[str, Any], timeout: float = HOOK_TIMEOUT
) -> str | None:
    """Run `beagle hook NAME` as Claude Code would; its stdout, or None on failure.

    The bare `hook NAME` argv is beagle's fast path, which reads the root from
    the cwd rather than `--root`, so the hook runs in the project root. Every
    failure — beagle missing, a hang, a crash — fails open, as beagle's own
    hooks do: a bridge bug must not wedge the agent.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            BEAGLE_BIN,
            "hook",
            name,
            cwd=str(root),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
    except OSError:
        return None
    try:
        stdout, _ = await asyncio.wait_for(
            proc.communicate(json.dumps(payload).encode("utf-8")), timeout=timeout
        )
    except TimeoutError:
        with contextlib.suppress(ProcessLookupError):
            proc.kill()
        await proc.wait()
        return None
    return (stdout or b"").decode("utf-8", "replace")


def _hook_root(cwd: Path) -> tuple[Path, dict[str, float]] | None:
    """The project whose `.claude/settings.json` installs beagle hooks, and them.

    Claude Code reads a project's hooks from `<root>/.claude/settings.json`;
    beagle marks the entries it wrote with a `"beagle": "<name>"` key, which is
    how `beagle hooks installed` finds them and how this finds them. Each name
    maps to the entry's own timeout (beagle writes 900s). The nearest ancestor
    of `cwd` with such a file wins; None when there is none or it is unreadable.
    """
    for directory in (cwd, *cwd.parents):
        settings = directory / SETTINGS_REL
        if not settings.is_file():
            continue
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        hooks: dict[str, float] = {}
        groups = data.get("hooks") if isinstance(data, dict) else None
        for entries in (groups or {}).values() if isinstance(groups, dict) else ():
            for group in entries if isinstance(entries, list) else ():
                inner = group.get("hooks") if isinstance(group, dict) else None
                for hook in inner if isinstance(inner, list) else ():
                    name = hook.get(HOOK_MARKER) if isinstance(hook, dict) else None
                    if isinstance(name, str) and name:
                        timeout = hook.get("timeout")
                        ok = isinstance(timeout, int | float) and timeout > 0
                        hooks[name] = float(timeout) if ok else DEFAULT_HOOK_TIMEOUT
        if hooks:
            return directory, hooks
    return None


def _session_start_report(name: str, root: Path) -> str:
    """A SessionStart hook's text (`loop-report`, `cadence-report`); "" when silent."""
    payload = json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": str(root)})
    rc, out = _run([BEAGLE_BIN, "hook", name], root, HOOK_TIMEOUT, stdin=payload)
    if rc != 0 or _block_reason(out) is not None:
        return ""
    return out.strip()


def _unbridged_notice(cwd: Path) -> str | None:
    """A one-line note naming installed hooks Tau deliberately does not run."""
    found = _hook_root(cwd)
    if found is None:
        return None
    skipped = [name for name in sorted(found[1]) if name not in BRIDGED_HOOKS]
    if not skipped:
        return None
    why = "; ".join(
        f"{name} ({UNBRIDGED_HOOKS.get(name, 'no Tau equivalent')})" for name in skipped
    )
    return f"Beagle: installed hooks not run under Tau: {why}."


def make_bash_hooks() -> Any:
    """Build the `tool_call` bridge for beagle's Bash PreToolUse hooks.

    `commit-claims` runs whenever the project is a pursuit, as it always has
    here; `commit-trailer` runs when `beagle hooks install` put it in the
    project's settings. Both only judge `git commit`, so both are skipped for a
    command that does not say "commit" — beagle's own fast path leaves there too.
    """

    async def bash_hooks(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        try:
            if event.tool_name != "bash":
                return None
            command = str((event.arguments or {}).get("command", ""))
            if "commit" not in command:
                return None
            cwd = Path(context.cwd)
            runs: list[tuple[str, Path, float]] = []
            goal = _find_goal(cwd)
            if goal is not None:
                runs.append(("commit-claims", goal.parent.parent, HOOK_TIMEOUT))
            installed = _hook_root(cwd)
            if installed is not None and "commit-trailer" in installed[1]:
                runs.append(("commit-trailer", installed[0], installed[1]["commit-trailer"]))
            payload = {
                "hook_event_name": "PreToolUse",
                "session_id": context.session_id or "",
                "cwd": str(cwd),
                "tool_name": "Bash",
                "tool_input": {"command": command},
            }
            reasons: list[str] = []
            for name, root, timeout in runs:
                out = await _run_hook(name, root, payload, timeout)
                reason = _block_reason(out) if out else None
                if reason is not None:
                    reasons.append(f"beagle {name}: {reason}")
        except Exception:  # noqa: BLE001 - fail open, never block on a bridge bug
            return None
        if not reasons:
            return None
        return ToolCallHookResult(block=True, reason="\n\n".join(reasons))

    return bash_hooks


def _note_run_end(event: Any, context: ExtensionContext) -> None:
    """Remember whether the run ended by itself, for the Stop hooks."""
    global _LAST_RUN_CLEAN
    del context
    stops = [getattr(m, "stop_reason", None) for m in getattr(event, "messages", ())]
    stops = [stop for stop in stops if stop is not None]
    _LAST_RUN_CLEAN = not stops or stops[-1] not in ("aborted", "error")


def make_stop_hooks(tau: ExtensionAPI) -> Any:
    """Build the `agent_settled` bridge for beagle's Stop hooks.

    `loop-guard` runs whenever the project is a pursuit; `cadence` and
    `close-out` run when `beagle hooks install` put them in the project's
    settings, each under its installed timeout. Claude Code runs Stop hooks
    when the agent finishes a turn — not when the user interrupts it — and a
    block becomes the model's next input with `stop_hook_active` set on the
    stop after it. Here every objection on one settle joins one more turn
    through `send_user_message`, and the settle that turn produces passes
    `stop_hook_active` to all of them, so each objects at most once per stop,
    as under Claude Code. Beagle does not order its Stop hooks, and neither
    does this: each is run in turn, and none sees another's verdict.
    """

    async def stop_hooks(event: Any, context: ExtensionContext) -> None:
        global _STOP_BLOCKED
        del event
        active, _STOP_BLOCKED = _STOP_BLOCKED, False
        try:
            # Print mode ends with the turn whatever a hook says, and an
            # interrupted or failed run is not a turn the agent chose to end.
            if not context.has_ui or not _LAST_RUN_CLEAN:
                return
            cwd = Path(context.cwd)
            runs: list[tuple[str, Path, float]] = []
            goal = _find_goal(cwd)
            if goal is not None:
                runs.append(("loop-guard", goal.parent.parent, HOOK_TIMEOUT))
            installed = _hook_root(cwd)
            if installed is not None:
                root, hooks = installed
                runs += [(name, root, hooks[name]) for name in STOP_HOOKS if name in hooks]
            payload = {
                "hook_event_name": "Stop",
                "session_id": context.session_id or "",
                "cwd": str(cwd),
                "stop_hook_active": active,
            }
            reasons: list[str] = []
            for name, root, timeout in runs:
                out = await _run_hook(name, root, payload, timeout)
                reason = _block_reason(out) if out else None
                if reason is not None:
                    reasons.append(f"[beagle {name}]\n\n{reason}")
            if reasons:
                _STOP_BLOCKED = True
                tau.send_user_message("\n\n".join(reasons))
        except Exception:  # noqa: BLE001 - fail open; a hook must not wedge the session
            return

    return stop_hooks


@dataclass(eq=False)
class _Wakeup:
    """One armed `pursuit_wakeup`: the token delivery checks it still holds.

    Stop, a re-arm and shutdown void it by replacing `_WAKEUP`; a delivery
    whose token is no longer `_WAKEUP` sends nothing. `run` is the loop run in
    flight when it was armed (its `started_at`), so a wakeup that outlives the
    run it was armed for is dropped rather than starting the loop again.
    """

    prompt: str
    root: Path | None
    run: str | None
    handle: asyncio.TimerHandle | None = None
    fired: bool = False
    task: asyncio.Task[None] | None = None


async def _loop_run(root: Path) -> str | None:
    """The in-flight loop run's start time; "" when idle; None when unknown.

    `beagle loop read` prints the start time and exits 3 with no run in
    flight. Anything else — beagle missing, a crash, a hang — is unknown,
    which the caller treats as "do not second-guess the wakeup".
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            BEAGLE_BIN,
            "loop",
            "read",
            "--root",
            str(root),
            cwd=str(root),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
    except OSError:
        return None
    try:
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=HOOK_TIMEOUT)
    except TimeoutError:
        with contextlib.suppress(ProcessLookupError):
            proc.kill()
        await proc.wait()
        return None
    if proc.returncode == LOOP_IDLE_EXIT:
        return ""
    if proc.returncode != 0:
        return None
    return (stdout or b"").decode("utf-8", "replace").strip() or None


def _void_wakeup() -> _Wakeup | None:
    """Void the current wakeup, armed or fired-and-pending; the one voided."""
    global _WAKEUP
    wakeup, _WAKEUP = _WAKEUP, None
    if wakeup is not None and wakeup.handle is not None:
        wakeup.handle.cancel()
    return wakeup


def _fire_wakeup(tau: ExtensionAPI, wakeup: _Wakeup) -> None:
    """The timer ran out: deliver now if the session is idle, else at its settle."""
    if _WAKEUP is not wakeup:
        return
    wakeup.fired = True
    with contextlib.suppress(Exception):  # a reloaded or closed session: the settle decides
        if tau.context.is_running:
            return  # a turn is on; `_deliver_pending_wakeup` sends it when it ends
    wakeup.task = asyncio.get_running_loop().create_task(_deliver_wakeup(tau, wakeup, False))


async def _deliver_wakeup(tau: ExtensionAPI, wakeup: _Wakeup, settling: bool) -> None:
    """Send a fired wakeup's prompt, unless something since has voided it.

    Checked at the last moment, because a message once queued cannot be
    recalled: the token must still be current (no stop, no newer arm), and a
    loop run the wakeup was armed for must still be in flight. Outside a
    settle, a turn that started meanwhile keeps it pending for that turn's
    settle, where it is sent after the Stop hooks have had their say.
    """
    if _WAKEUP is not wakeup:
        return
    if wakeup.run and wakeup.root is not None:
        now = await _loop_run(wakeup.root)
        if _WAKEUP is not wakeup:
            return
        if now is not None and now != wakeup.run:
            _void_wakeup()
            with contextlib.suppress(Exception):
                tau.context.ui.notify(
                    f"pursuit_wakeup: dropped {wakeup.prompt!r} — the loop run it was "
                    "armed for is no longer in flight (`beagle loop stop` ran, or a new "
                    "run started).",
                    "info",
                )
            return
    with contextlib.suppress(Exception):
        if not settling and tau.context.is_running:
            return  # still pending; the settle delivers it
    _void_wakeup()
    with contextlib.suppress(Exception):  # a reloaded or closed session: nothing to wake
        tau.send_user_message(_wakeup_turn(tau, wakeup.prompt))


def _in_context(tau: ExtensionAPI, text: str) -> bool:
    """Whether a user message in the live context still carries `text` verbatim.

    Read from the transcript rather than remembered, so a compaction (which
    folds old turns into a summary), a resume or a branch all count as the
    driver being gone, and so does a driver file that changed since.
    """
    try:
        transcript = tau.context.transcript
    except Exception:  # noqa: BLE001 - unknown means "send it in full"
        return False
    return any(
        getattr(message, "role", None) == "user" and text in message.text for message in transcript
    )


def _wakeup_turn(tau: ExtensionAPI, prompt: str) -> str:
    """What a wakeup sends: its prompt, with a driver command expanded.

    An extension's message reaches the model as text, not through the slash
    command parser, so a driver command is expanded here — in full the first
    time, and as a short resume stub while the full driver is still in the
    context, since a loop's every wakeup re-sending several pages of an
    unchanged skill is most of what it would spend.
    """
    name, _, args = prompt.strip().partition(" ")
    expand = _DRIVER_TURNS.get(name)
    block = expand("") if expand is not None else None
    if expand is None or block is None:
        return prompt
    if _in_context(tau, block):
        return RESUME_STUB.format(prompt=prompt.strip(), name=name)
    return expand(args) or prompt


def make_wakeup_delivery(tau: ExtensionAPI) -> Any:
    """Build the `agent_settled` handler that sends a wakeup that fired mid-turn.

    Registered after the Stop-hook bridge, so it sees whether a hook objected
    on this settle; an objection already starts the next turn, and the wakeup
    waits for the settle after it rather than queueing behind it.
    """

    async def deliver(event: Any, context: ExtensionContext) -> None:
        del event, context
        wakeup = _WAKEUP
        if wakeup is None or not wakeup.fired or _STOP_BLOCKED:
            return
        try:
            await _deliver_wakeup(tau, wakeup, True)
        except Exception:  # noqa: BLE001 - a delivery bug must not wedge the session
            return

    return deliver


def make_wakeup(tau: ExtensionAPI) -> Any:
    """Build the `pursuit_wakeup` tool: Tau's `ScheduleWakeup`."""

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        global _WAKEUP
        del tool_call_id, signal, on_update
        if arguments.get("stop"):
            voided = _void_wakeup()
            if voided is None:
                return _make_dispatch_result(
                    "pursuit_wakeup: nothing was armed, and no fired wakeup is waiting "
                    "to be delivered."
                )
            if voided.fired:
                return _make_dispatch_result(
                    f"pursuit_wakeup: the wakeup had already fired, during a turn, and "
                    f"its {voided.prompt!r} was waiting for that turn to end. That "
                    "pending delivery is now voided; it will not arrive."
                )
            return _make_dispatch_result("pursuit_wakeup: disarmed before it fired.")
        if not tau.context.has_ui:
            return _make_dispatch_result(
                "pursuit_wakeup: REFUSED — this Tau session has no interactive frontend "
                "(print mode ends with the turn), so nothing would come back. A refused "
                "arm is a stopping condition: do not record a resumption."
            )
        try:
            minutes = math.ceil(float(arguments.get("delay_minutes") or WAKEUP_MIN_MINUTES))
        except (TypeError, ValueError):
            minutes = WAKEUP_MIN_MINUTES
        minutes = max(WAKEUP_MIN_MINUTES, min(WAKEUP_MAX_MINUTES, minutes))
        raw_prompt = arguments.get("prompt")
        prompt = raw_prompt.strip() if isinstance(raw_prompt, str) and raw_prompt.strip() else ""
        prompt = prompt or "/pursuit-run"
        goal = _find_goal(tau.context.cwd)
        root = goal.parent.parent if goal is not None else None
        run = await _loop_run(root) if root is not None else None
        replaced = _void_wakeup()
        wakeup = _Wakeup(prompt=prompt, root=root, run=run or None)
        _WAKEUP = wakeup
        wakeup.handle = asyncio.get_running_loop().call_later(
            minutes * 60, _fire_wakeup, tau, wakeup
        )
        return _make_dispatch_result(
            f"pursuit_wakeup: armed — {prompt!r} in {minutes} minute(s)"
            + (", replacing the previous wakeup" if replaced is not None else "")
            + f". Record it: `beagle loop tick --resuming-in {minutes}`."
        )

    return execute


WAKEUP_PARAMETERS = {
    "type": "object",
    "properties": {
        "delay_minutes": {
            "type": "number",
            "description": (
                f"Minutes until the wakeup ({WAKEUP_MIN_MINUTES}-{WAKEUP_MAX_MINUTES}, "
                "rounded up). The shortest is right when the next task is ready."
            ),
        },
        "prompt": {
            "type": "string",
            "description": "What the wakeup delivers. Default: /pursuit-run.",
        },
        "stop": {
            "type": "boolean",
            "description": "Disarm the pending wakeup instead of arming one.",
        },
    },
}

#: A repeat wakeup's turn while the driver it names is still in the context.
RESUME_STUB = """\
{prompt}

(A `pursuit_wakeup`. The `{name}` driver and its Tau host mapping are already \
in this conversation, unchanged since they were loaded; do not reload them. \
Continue the loop from its next step.)"""

#: Read before `pursuit-run.md`, which names Claude Code's tools and hooks.
TAU_HOST_NOTE = """\
Host mapping — this driver was written for Claude Code. Under Tau, read it as:

- `ScheduleWakeup` is the `pursuit_wakeup` tool: `delay_minutes`, \
`prompt: "/pursuit-run"`, and `stop: true` to disarm. It refuses when Tau \
cannot come back (print mode); that is the refused arm the driver treats as a \
stopping condition.
- Dispatching `beagle-dev:step-executor`: when the `agent` tool is available \
(the tau-subagents extension), call it with `subagent_type: \
"beagle-dev:step-executor"`, the brief as `prompt`, and `run_in_background: \
true`, then end the turn exactly as the driver says for a dispatched worker — \
arm `pursuit_wakeup` with a long delay and record `beagle loop tick --awaiting \
"<worker> on <task>" --for N --resuming-in N`, `--for` the driver's believed \
wait. The worker's completion arrives as a \
`<task-notification>` message that starts your next turn; clear the wait with \
a bare `beagle loop tick`, read the full report with `get_subagent_result` if \
the notification is truncated, and run the close. Claude Code's `SendMessage` \
to a running worker is `steer_subagent`; `get_subagent_result` with `wait: \
true` blocks on one. Parallel independent tasks may each get a background \
agent.
- While a background worker is awaited, its open task's declared scope is \
the worker's: this extension refuses this session's writes there. For a \
worker that must not share your tree, pass `isolation: "worktree"`; it works \
in a detached copy and its changes come back on a `tau-agent-<id>` branch for \
you to merge. `isolated: true` is not that: it only spawns the worker without \
extensions, so without beagle's skills and guards.
- Without the `agent` tool, dispatch is the `pursuit_dispatch` tool. It \
returns the worker's report within the same turn, so skip the `--awaiting` \
tick and the bare tick that clears it; run the close straight after.
- Skill scripts live under `${CLAUDE_PLUGIN_ROOT}`; the containment launcher \
is `${CLAUDE_PLUGIN_ROOT}/skills/containment/scripts/run_contained.sh`. Use \
that path, in briefs too, never a `~/.claude/plugins/cache/...` one, even if \
beagle prints it: a Tau-only host has no such cache, and an upgrade moves it.
- Beagle's hooks run inside this Tau extension, never from \
`.claude/settings.json`: `loop-guard`, `loop-report` and `commit-claims` \
always, and `close-out`, `cadence`, `cadence-report` and `commit-trailer` when \
`beagle hooks install` has put them in the project's settings — so installing \
them is how to switch them on here too. `tilth-load` and `transcript-guard` \
have no Tau equivalent and are skipped.
"""


def _pursuit_turn(args: str) -> str | None:
    """The `/pursuit` driver as a turn, or None when it is not installed."""
    return _driver_turn(PURSUIT_COMMAND, args)


def _pursuit_run_turn(args: str) -> str | None:
    """The `/pursuit-run` driver as a turn, or None when it is not installed."""
    return _driver_turn(PURSUIT_RUN_COMMAND, args, preamble=TAU_HOST_NOTE)


#: Driver commands a wakeup's prompt may name, expanded as their command would.
_DRIVER_TURNS = {"/pursuit": _pursuit_turn, "/pursuit-run": _pursuit_run_turn}


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #


def _command_pursuit(args: str, context: Any) -> str:
    """Load Beagle's `/pursuit` driver as this turn."""
    text = _pursuit_turn(args)
    if text is None:
        return f"/pursuit: {_driver_missing(PURSUIT_COMMAND)}"
    context.api.send_user_message(text)
    return "/pursuit: loaded the pursuit driver as this turn."


def _command_pursuit_run(args: str, context: Any) -> str:
    """Load Beagle's `/pursuit-run` loop driver as this turn."""
    text = _pursuit_run_turn(args)
    if text is None:
        return f"/pursuit-run: {_driver_missing(PURSUIT_RUN_COMMAND)}"
    context.api.send_user_message(text)
    return "/pursuit-run: loaded the pursuit loop driver as this turn."


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
        "driver, `/pursuit-run` runs it task after task (arming turns with "
        "`pursuit_wakeup`), and `/pursuit-view` shows counts and the ready set without "
        "a model.",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# skill wiring
# --------------------------------------------------------------------------- #


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
    wanted, _ = _LAYOUT.skills()
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
    for name, target in (("commands", _LAYOUT.commands_dir), ("agents", _LAYOUT.agents_dir)):
        if target is not None:
            _sync_link(root / name, target)
        elif (root / name).is_symlink():
            # Its tree left the checkout: a dangling link would read as present.
            with contextlib.suppress(OSError):
                (root / name).unlink()
    return skills_dir


AGENT_HOST_NOTE = """\
You run as a Tau sub-agent, translated from a Claude Code agent definition. \
Your tools are Tau's: `read`, `write`, `edit` and `bash`. Where the text below \
names `Grep` or `Glob`, use `rg` or `find` through `bash`; MCP tools it names \
(`mcp__...`) are not available. Beagle's skill scripts live under \
`${CLAUDE_PLUGIN_ROOT}/skills/`; run the containment launcher as \
`${CLAUDE_PLUGIN_ROOT}/skills/containment/scripts/run_contained.sh`, not from \
any `~/.claude/plugins/cache/...` path a brief or beagle names.
"""


def _agent_type_text(src: Path) -> str | None:
    """A tau-subagents agent-type file translated from a beagle agent, or None."""
    try:
        metadata, body = parse_markdown_resource(src.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return None
    tools: list[str] = []
    for name in (metadata.get("tools") or "").split(","):
        mapped = AGENT_TOOL_MAP.get(name.strip())
        if mapped is not None and mapped not in tools:
            tools.append(mapped)
    description = " ".join((metadata.get("description") or "").split())
    lines = ["---", f"description: {description}"]
    if tools:
        lines.append(f"tools: {', '.join(tools)}")
    # No `model:` — Claude's aliases name nothing a Tau provider serves, so the
    # sub-agent inherits the parent session's model.
    lines += [f"{GENERATED_KEY}: {GENERATED_BY}", "---", ""]
    text = AGENT_HOST_NOTE + "\n" + body.lstrip("\n")
    text = text.replace(PLUGIN_ROOT_VAR, str(_PLUGIN_ROOT)) if _PLUGIN_ROOT else text
    return "\n".join(lines) + text


def _is_generated(path: Path) -> bool:
    try:
        metadata, _ = parse_markdown_resource(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return False
    return metadata.get(GENERATED_KEY) == GENERATED_BY


def sync_agent_types(agents_dir: Path) -> list[str]:
    """Write beagle's agents into `agents_dir` as tau-subagents types; their names.

    Idempotent. Only files carrying the generated marker are ever replaced or
    removed, so an agent type the user wrote under the same name wins, and a
    type whose beagle agent is gone is pruned rather than left to go stale.
    """
    wanted: dict[str, str] = {}
    for plugin, directory in _LAYOUT.plugins:
        try:
            sources = sorted((directory / "agents").glob("*.md"))
        except OSError:
            continue
        for src in sources:
            text = _agent_type_text(src)
            if text is not None:
                wanted[f"{plugin}:{src.stem}"] = text
    try:
        agents_dir.mkdir(parents=True, exist_ok=True)
        existing = list(agents_dir.glob("*.md"))
    except OSError:
        return []
    for path in existing:
        if path.stem not in wanted and _is_generated(path):
            with contextlib.suppress(OSError):
                path.unlink()
    written: list[str] = []
    for name, text in wanted.items():
        path = agents_dir / f"{name}.md"
        try:
            if path.exists():
                if not _is_generated(path):
                    continue
                if path.read_text(encoding="utf-8") == text:
                    written.append(name)
                    continue
            path.write_text(text, encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        written.append(name)
    return written


# --------------------------------------------------------------------------- #
# setup
# --------------------------------------------------------------------------- #


def _bridge_session_start_hooks(tau: ExtensionAPI, cwd: Path) -> None:
    """Run an installed `cadence-report` into the prompt; note unbridged hooks.

    SessionStart stdout joins the session's context under Claude Code; here it
    is a prompt section, which also outlives compaction. The note about hooks
    left unbridged is shown once per load, not on every session switch.
    """
    installed = _hook_root(cwd)
    if installed is not None and "cadence-report" in installed[1]:
        report = _session_start_report("cadence-report", installed[0])
        if report:
            tau.add_prompt_section(
                "Beagle cadences",
                f"At session start, `beagle hook cadence-report` said:\n\n{report}",
            )
    notice = _unbridged_notice(cwd)
    if notice is None:
        return
    shown: list[bool] = []

    def notify(event: Any, context: ExtensionContext) -> None:
        del event
        if not shown:
            shown.append(True)
            context.ui.notify(notice, "info")

    tau.on("session_start", notify)


def setup(tau: ExtensionAPI) -> None:
    global _SEEN_CWD, _PLUGIN_ROOT, _LAYOUT
    # Every beagle this process starts, hooks and the bash tool's alike,
    # inherits this, so beagle can tell it is not under Claude Code.
    os.environ[HOST_ENV] = "tau"
    _LAYOUT = resolve_layout(BEAGLE)
    problems: list[str] = list(_LAYOUT.problems)
    # 1-2. Load the engineering-practice and pursuit skills from one merged
    #      plugin root. Skills run scripts from ${CLAUDE_PLUGIN_ROOT}/skills/...;
    #      the bash tool's subprocesses inherit this process env, so exporting
    #      the merged root makes every such path resolve, whichever plugin
    #      shipped the skill. Overwritten rather than defaulted: one inherited
    #      from a Claude Code shell names a single plugin and resolves half.
    if _LAYOUT.plugins:
        problems += _LAYOUT.skills()[1]
        root = tau.context.paths.home / MERGED_ROOT_NAME
        skills_dir = build_plugin_root(root)
        if skills_dir is not None:
            tau.register_skill_dir(skills_dir)
            _PLUGIN_ROOT = root
            os.environ["CLAUDE_PLUGIN_ROOT"] = str(root)
        # Beagle's agents as tau-subagents agent types, for background
        # dispatch. Harmless without that extension: nothing reads the dir.
        sync_agent_types(AGENTS_DIR)

    # 3. The driver command, and a no-model state read. A driver command is
    #    registered only when its file is there: one that exists but cannot run
    #    reads, to a model listing its commands, as a loop it can offer. A
    #    checkout that is present but lacks a driver is a layout mismatch, not
    #    an absent install, so it is said aloud rather than degraded quietly.
    if _driver_file(PURSUIT_COMMAND) is not None:
        tau.register_command(
            "pursuit",
            _command_pursuit,
            description="Found or run a beagle pursuit — one goal, a task tree, no denominator.",
        )
    elif _LAYOUT.plugins:
        problems.append(f"/pursuit is not registered: {_driver_missing(PURSUIT_COMMAND)}")
    tau.register_command(
        "pursuit-view",
        _command_pursuit_view,
        description="Show the current pursuit's goal, counts and ready set (no model).",
    )

    # 4. The headless step-executor: the blocking fallback for when the
    #    tau-subagents extension (background `agent` tool) is not loaded.
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

    # 5. Enforce the pursuit ground truth on every tool call, and bridge
    #    beagle's Bash PreToolUse hooks onto the same seam.
    tau.on("tool_call", make_guard())
    tau.on("tool_call", make_bash_hooks())
    if not _is_worker():
        tau.on("tool_call", make_scope_guard())

    # 6. What /pursuit-run needs from its host: a session id beagle can record
    #    as the driver, a wakeup, and the Stop hook. A worker runs none of the
    #    loop — it is one step of its parent's.
    with contextlib.suppress(Exception):  # context may not be bound yet
        _adopt_session(tau.context)
    tau.on("session_start", _on_session_start)
    if not _is_worker():
        if _driver_file(PURSUIT_RUN_COMMAND) is not None:
            tau.register_command(
                "pursuit-run",
                _command_pursuit_run,
                description="Run a beagle pursuit task after task until it cannot move.",
            )
        elif _LAYOUT.plugins:
            problems.append(
                f"/pursuit-run is not registered: {_driver_missing(PURSUIT_RUN_COMMAND)}"
            )
        tau.register_tool(
            AgentTool(
                name="pursuit_wakeup",
                label="pursuit_wakeup",
                description=(
                    "Arm this session's next turn (Claude Code's ScheduleWakeup): after "
                    "delay_minutes, deliver prompt (default /pursuit-run). One wakeup at a "
                    "time; arming again replaces it, stop=true disarms it. Refused in print "
                    "mode, where the session ends with the turn."
                ),
                parameters=WAKEUP_PARAMETERS,
                execute_fn=make_wakeup(tau),
                prompt_snippet="Arm the pursuit loop's next turn (ScheduleWakeup).",
                prompt_guidelines=(
                    "Arm pursuit_wakeup before `beagle loop tick --resuming-in`, never after, "
                    "and treat a refused arm as a stopping condition.",
                ),
            )
        )
        tau.on("agent_end", _note_run_end)
        tau.on("agent_settled", make_stop_hooks(tau))
        tau.on("agent_settled", make_wakeup_delivery(tau))
        tau.on("session_shutdown", lambda event, context: _void_wakeup())

    if problems:
        notice = "Beagle extension: " + " ".join(problems)
        tau.on("session_start", lambda event, context: context.ui.notify(notice, "warning"))
        tau.add_prompt_section(
            "Beagle extension problems",
            "\n".join(f"- {p}" for p in problems)
            + "\n\nDo not offer a command listed here as not registered, or say the "
            "pursuit loop is available when it is not; tell the user the extension and the "
            "beagle checkout disagree.",
        )

    # 7. If this project is a pursuit, pin its goal into the prompt at load —
    #    the frame arrives, but nothing here triggers a turn. A pursuit founded
    #    mid-session (outside a load) simply misses the section until the next
    #    reload, which is the right trade against auto-starting work.
    #    Extensions load before the session binds, so the session cwd is not
    #    readable yet; the process cwd is where `tau` (or a worker) was started.
    try:
        cwd = tau.context.cwd
    except Exception:  # noqa: BLE001 - not bound yet at load
        cwd = Path.cwd()
    _SEEN_CWD = cwd
    if not _is_worker():
        _bridge_session_start_hooks(tau, cwd)
    goal = _find_goal(cwd)
    if goal is not None:
        section = _goal_section(goal)
        # loop-report is the SessionStart hook: what a run left in flight, and
        # the driver's core while one is. The system prompt outlives
        # compaction, so this also covers what the hook re-prints after one.
        report = "" if _is_worker() else _session_start_report("loop-report", goal.parent.parent)
        if section and report:
            section = f"{section}\n\nAt session start, `beagle hook loop-report` said:\n\n{report}"
        if section:
            tau.add_prompt_section("Beagle pursuit", section)
