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
  driver file. The `pursuit_driver` tool returns the same text for `/pursuit`
  or `/pursuit-run`, since Tau shows commands to no model and a user who asks
  for the loop in prose otherwise gets a model that cannot reach it.
- **`beagle` on PATH** — the pursuit plugin's `bin/` is linked into the merged
  root and put first on PATH, so the CLI is the checkout's own release, never
  a stale one a plugin cache left in `~/.local/bin`.
- **`pursuit_dispatch`** — a headless `step-executor`. Tau has no Task tool, so
  delegation is a nested `tau -p` run: the step-executor persona appended, the
  target dir set with `--cwd`, and the model inherited from the session unless
  the caller names a Tau model/provider. Because the worker is Tau too, the
  ground-truth guard stays live inside it — a sub-agent is not a way around it.
  The driver still runs `pursuit close`; this tool only does the work and
  returns the report.
- **steering** — `pursuit_found`, `pursuit_plan` and `pursuit_step` carry a
  session through the pursuit without the driver text, which runs to tens of
  thousands of tokens a small model cannot hold: found the goal (the user's
  words, confirmed) and split it into milestones; split a milestone into
  steps; and work one task — `next`, `open` with the criteria and check the
  model writes, a step-executor run on `beagle pursuit brief`, the check run
  before the close (a done close the check refuses blocks the task for
  good), then `close` with the worker's measured spend. While a pursuit is
  founded, the session the host started may edit only `.beagle/`; the work
  is the sub-agents' (`BEAGLE_TAU_DRIVER_EDITS=1` lifts that).
- **history guard** — in a founded pursuit no session runs the `git` verbs
  that discard the tree or rewrite commits (`reset --hard`, `clean -f`,
  `checkout .`, `stash`, `rebase`, `commit --amend`, `push --force`): the
  claims and checks stand on both, so a mistake is fixed forward.
- **ground-truth guard** — the one invariant a hook can enforce: `.beagle/
  pursuit.toml` is the user's, and criteria the agent can edit are criteria the
  agent can meet by editing them. The founding write is allowed (the file does
  not exist yet); editing it after founding is blocked. This fails open: a hook
  that raised on its own error would block the very tool call it inspects.
- **scope guard** — while `/pursuit-run` waits on a background worker
  (`beagle loop tick --awaiting`, inside its lease), the driver session's
  edit, write and writing-bash calls into an open task's declared `scope`
  are refused: two writers on one tree lose one's work. Only the recorded
  driver session is held; a subagent's calls carry its own session id. A
  cancelled worker sends no notice to end that wait, so a `stop_subagent`
  result while one stands says to clear it with a bare `beagle loop tick`.
- **ended drivers** — workers and the wakeup end with the Tau session that
  started them, so a run whose driver session has ended is stopped at the
  next session start (`beagle loop stop`), and the next `/pursuit-run` is
  told where the cancelled worker's partial work is. Each session records
  its pid under the Tau home, since beagle trusts no Tau pid.
- **orientation** — when the project is a pursuit, its goal and criteria are
  added to the system prompt at load, so the driver re-reads the goal every
  session without anything triggering a turn. It is a frame, not an order.
  Beagle's `loop-report` SessionStart hook output rides along with it. A
  project with no pursuit yet gets a few lines instead: the CLI is already on
  PATH, and founding one goes through `pursuit_found`.
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

import ast
import asyncio
import contextlib
import fnmatch
import functools
import html.parser
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import tomllib
import urllib.parse
import urllib.request
import uuid
from collections.abc import Callable, Mapping
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
    ToolResultHookResult,
)
from tau_coding.paths import TauPaths
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
#: The CLI shim. Its plugin's `bin/` is linked into the merged root and put
#: first on PATH, so the CLI always matches the skills loaded beside it.
BIN_REL = Path("bin") / "beagle"
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

#: Turns a worker gets before it is told to stop and report (`tau --max-turns`).
#: R01's 9B workers ran 43 and 51 turns into the kill and handed back nothing;
#: a turn cap ends the run with a report instead.
WORKER_MAX_TURNS_ENV = "BEAGLE_TAU_WORKER_MAX_TURNS"
DEFAULT_WORKER_MAX_TURNS = 30

#: The worker's thinking level; unset runs it with thinking off, since most of
#: R01's worker time went to reasoning spirals.
WORKER_THINKING_ENV = "BEAGLE_TAU_DISPATCH_THINKING"

#: Escape hatch: `BEAGLE_TAU_ALLOW_PURSUIT_EDIT=1` disables the ground-truth guard.
GUARD_DISABLE_ENV = "BEAGLE_TAU_ALLOW_PURSUIT_EDIT"

#: Set in a `pursuit_dispatch` worker's environment. A worker acts for its
#: parent: it keeps the parent's session id and runs no loop of its own.
WORKER_ENV = "BEAGLE_TAU_WORKER"
#: The task a `pursuit_step` worker was sent on, which keeps it from beagle and
#: `.beagle/`, and the task's scope, newline-joined: unset when the task has
#: none, and then the worker's writes are not held to one. A worker sent with
#: no task (`pursuit_dispatch`, an audit) may read the pursuit.
WORKER_TASK_ENV = "BEAGLE_TAU_WORKER_TASK"
WORKER_SCOPE_ENV = "BEAGLE_TAU_WORKER_SCOPE"

#: The memory cap a worker and a pre-close check run under, as a systemd size
#: (`4G`, `512M`); `off` runs them uncapped. Applied through a systemd user
#: scope with swap shut off, so a runaway is killed rather than left to drag
#: the machine into swap; without systemd the cap is skipped.
MEMORY_MAX_ENV = "BEAGLE_TAU_MEMORY_MAX"
DEFAULT_MEMORY_MAX = "4G"

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
#: Where each Tau session that may drive a pursuit records its process, one
#: `<session id>.json` per session, under the Tau home.
DRIVERS_REL = Path("state") / "beagle-drivers"
#: How long an ended or dead driver's record is kept before it is pruned.
DRIVER_RECORD_DAYS = 7

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
#: Whether the last run ended on its own, rather than aborted, errored or cut
#: off at the output limit.
_LAST_RUN_CLEAN = True
# The last prompt the user typed, and whether this session has already been
# told to found before it does the work: see `make_found_first_steer`.
_LAST_PROMPT = ""
_FOUND_FIRST_SENT = False
_SETUP_CALLS = 0
#: The driver records' directory, once the Tau home is known.
_DRIVERS_DIR: Path | None = None
#: The session this process last registered as a possible driver.
_DRIVER_SESSION: str | None = None
#: The session whose `session_start` this extension saw: the host's, never an
#: in-process subagent's.
_STARTED_SESSION: str | None = None
#: What the next `/pursuit-run` turn is told about a run stopped because its
#: Tau driver had ended, until one is sent.
_ENDED_RUN_NOTE: str | None = None


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

    @property
    def bin_dir(self) -> Path | None:
        """The `bin/` holding the `beagle` CLI shim this checkout ships."""
        found = self.first(BIN_REL)
        return found.parent if found is not None else None

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
    if name == "touch":
        return _positional(args, frozenset({"-d", "--date", "-r", "--reference", "-t"}))
    if name == "mkdir":
        return _positional(args, frozenset({"-m", "--mode", "--context"}))
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


def _live_wait(root: Path, session_id: str) -> str | None:
    """What this session's run declares it is awaiting, while the lease holds.

    None unless a run is in flight, this session is its recorded driver (a
    subagent's own session never is), and the declared wait is in its lease.
    """
    record = _json_out(["loop", "read", "--json"], root)
    if not isinstance(record, dict) or not record.get("awaiting"):
        return None
    if not session_id or record.get("driver_session") != session_id:
        return None
    return str(record["awaiting"]) if _lease_live(record) else None


def _read_awaited_scope(root: Path, session_id: str) -> _AwaitedScope | None:
    """The scope this session's run is waiting on a worker in, or None.

    None without a live wait (`_live_wait`). The scope is every open task's:
    `awaiting` is free text, so which open task the worker holds cannot be
    read off it reliably.
    """
    awaiting = _live_wait(root, session_id)
    if awaiting is None:
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
    return _AwaitedScope(awaiting, tuple(tasks), tuple(scope))


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


#: Appended to a `stop_subagent` result while this session's run declares a wait.
STOPPED_WORKER_NOTE = """

beagle: this session's pursuit run still declares it is awaiting \
"{awaiting}". If that was the worker just stopped, nothing will arrive to \
clear it: run a bare `beagle loop tick` now, then take the task back or \
dispatch it again."""


def make_stopped_worker_note() -> Any:
    """Build the `tool_result` hook that remembers a stopped worker's wait.

    A cancelled tau-subagents run sends no `<task-notification>`, so a
    `--awaiting` declared for it would stand until its lease ran out, holding
    the scope guard and silencing the Stop hooks. When the driver stops a
    worker itself, the result says so. It does not tick for the driver:
    `awaiting` is free text naming a worker type and a task, not a run id,
    so which of several parallel workers it meant cannot be told from here.
    """

    async def note(event: Any, context: ExtensionContext) -> ToolResultHookResult | None:
        try:
            if event.tool_name != "stop_subagent":
                return None
            goal = _find_goal(Path(context.cwd))
            if goal is None:
                return None
            root, session = goal.parent.parent, context.session_id or ""
            awaiting = await asyncio.to_thread(_live_wait, root, session)
            if awaiting is None:
                return None
            text = event.result.text + STOPPED_WORKER_NOTE.format(awaiting=awaiting)
        except Exception:  # noqa: BLE001 - fail open; a note must not break the tool
            return None
        return ToolResultHookResult(content=text)

    return note


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


def _worker_max_turns() -> int:
    """The worker's turn cap: env, else DEFAULT_WORKER_MAX_TURNS."""
    raw = os.environ.get(WORKER_MAX_TURNS_ENV, "").strip()
    try:
        return max(1, int(raw)) if raw else DEFAULT_WORKER_MAX_TURNS
    except ValueError:
        return DEFAULT_WORKER_MAX_TURNS


def _worker_timeout(raw: Any) -> tuple[float, str]:
    """A model-supplied worker timeout, clamped to DEFAULT_DISPATCH_TIMEOUT.

    Returns the timeout and a note for the tool result, empty unless clamped.
    A longer wall clock bought R01 only a longer spiral; the turn cap is what
    ends a worker with a report.
    """
    try:
        asked = float(raw or DEFAULT_DISPATCH_TIMEOUT)
    except (TypeError, ValueError):
        return DEFAULT_DISPATCH_TIMEOUT, ""
    if asked <= 0:
        return DEFAULT_DISPATCH_TIMEOUT, ""
    if asked > DEFAULT_DISPATCH_TIMEOUT:
        return DEFAULT_DISPATCH_TIMEOUT, (
            f"(timeout {asked:.0f}s was clamped to {DEFAULT_DISPATCH_TIMEOUT:.0f}s, the most a "
            "worker gets; split a task that needs longer.)"
        )
    return asked, ""


def _with_note(result: AgentToolResult, note: str) -> AgentToolResult:
    if not note:
        return result
    return AgentToolResult(content=[TextContent(text=f"{note}\n\n"), *result.content])


def _make_dispatch_result(text: str) -> AgentToolResult:
    return AgentToolResult(content=[TextContent(text=text)])


@dataclass(frozen=True)
class _WorkerRun:
    """What one headless step-executor run came back with."""

    returncode: int | None = None
    report: str = ""
    #: The worker's peak context: its largest request's tokens, from its JSON events.
    spent: int | None = None
    #: Why no report came back (no persona, no `tau`, timeout, cancelled).
    problem: str | None = None
    #: The worker's session file, for reading what it did beyond its report.
    transcript: Path | None = None

    @property
    def shown_report(self) -> str:
        """The report as the driver reads it, with the transcript's path."""
        if self.transcript is None:
            return self.report
        return f"{self.report}\n\n(Worker transcript: {self.transcript})"


#: How the stub a worker that wrote no report gets in its place begins.
NO_REPORT = "(The worker wrote no report"
#: How often a running worker is checked for the caller's cancellation.
_WORKER_POLL_SECONDS = 0.5


#: The worker's stdout is read in chunks this size...
_READ_CHUNK = 1 << 16
#: ...and a line longer than this is dropped unparsed. Only `message_end` lines
#: are kept, and one message is far smaller; the long lines are the
#: `message_update` events, which repeat the whole partial message every time.
_MAX_EVENT_LINE = 16 << 20
#: How much of a worker's stderr, and of its last thinking, a report quotes.
_WORKER_TAIL_CHARS = 2000


@dataclass
class _WorkerEvents:
    """What a `--mode json` run's `message_end` events say, read as they stream."""

    #: The last non-empty assistant text.
    report: str = ""
    #: The largest request's tokens: the run's peak context.
    spent: int | None = None
    #: How the last assistant message ended, and its thinking.
    stop_reason: str | None = None
    thinking: str = ""
    error: str | None = None

    def feed(self, line: bytes) -> None:
        if b'"message_end"' not in line[:64]:
            return
        try:
            event = json.loads(line)
        except ValueError:
            return
        if not isinstance(event, dict) or event.get("type") != "message_end":
            return
        message = event.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            return
        usage = message.get("usage")
        total = usage.get("totalTokens") if isinstance(usage, dict) else None
        if isinstance(total, int):
            # Each request re-sends the conversation, so a sum counts the start
            # of the run once per turn. The largest request is what the run
            # held at its peak, which is how Claude Code reports a subagent.
            self.spent = max(self.spent or 0, total)
        content = message.get("content")
        blocks = (
            [block for block in content if isinstance(block, dict)]
            if isinstance(content, list)
            else []
        )
        text = "\n".join(
            str(block.get("text", "")) for block in blocks if block.get("type") == "text"
        ).strip()
        if text:
            self.report = text
        self.thinking = "\n".join(
            str(block.get("thinking", "")) for block in blocks if block.get("type") == "thinking"
        ).strip()
        stop = message.get("stopReason")
        self.stop_reason = stop if isinstance(stop, str) else None
        error = message.get("errorMessage")
        self.error = str(error) if stop == "error" and error else None

    def final_report(self, stderr: str) -> str:
        """The report for the driver: always short, never the raw event stream."""
        report = self.report
        if self.error:
            report = f"{report}\n\n(worker error: {self.error})".strip()
        if not report:
            ended = (
                f"ended on stopReason={self.stop_reason}"
                if self.stop_reason
                else "produced no assistant message"
            )
            report = f"{NO_REPORT}: it {ended}.)"
            if self.stop_reason == "length" and self.thinking:
                report += (
                    "\nIt spent its output on reasoning. The reasoning ended:\n"
                    f"{self.thinking[-_WORKER_TAIL_CHARS:]}"
                )
            if stderr:
                report += f"\nstderr ended:\n{stderr[-_WORKER_TAIL_CHARS:]}"
        return report


async def _read_worker_events(stream: asyncio.StreamReader, events: _WorkerEvents) -> None:
    """Feed `events` each stdout line, holding at most one line in memory."""
    line = bytearray()
    skipping = False
    while chunk := await stream.read(_READ_CHUNK):
        start = 0
        while (end := chunk.find(b"\n", start)) != -1:
            if not skipping:
                line += chunk[start:end]
                events.feed(bytes(line))
            line.clear()
            skipping = False
            start = end + 1
        if not skipping:
            line += chunk[start:]
            if len(line) > _MAX_EVENT_LINE:
                line.clear()
                skipping = True
    if line and not skipping:
        events.feed(bytes(line))


async def _read_tail(stream: asyncio.StreamReader, keep: int) -> str:
    tail = b""
    while chunk := await stream.read(_READ_CHUNK):
        tail = (tail + chunk)[-keep:]
    return tail.decode("utf-8", "replace").strip()


async def _talk(proc: asyncio.subprocess.Process, brief: str, events: _WorkerEvents) -> str:
    """Send the brief, read the events, wait for exit; return stderr's tail."""
    stdin, stdout, stderr = proc.stdin, proc.stdout, proc.stderr
    assert stdin is not None and stdout is not None and stderr is not None

    async def send() -> None:
        with contextlib.suppress(BrokenPipeError, ConnectionResetError):
            stdin.write(brief.encode("utf-8"))
            await stdin.drain()
        stdin.close()

    _, _, err = await asyncio.gather(
        send(),
        _read_worker_events(stdout, events),
        _read_tail(stderr, _WORKER_TAIL_CHARS * 2),
    )
    await proc.wait()
    return err


#: A tool call written out as text, which a turn-capped worker can end on.
_TOOL_CALL_MARKUP = re.compile(r"<tool_call>|<function=")


def _unreported_changes(cwd: Path, scope: list[str]) -> str:
    """The report for a worker that ended on a raw tool call: what git sees it change.

    Run R02's turn-capped workers ended on `<tool_call><function=bash>…` text,
    which the driver was handed as the report.
    """
    stub = f"{NO_REPORT}: the sub-agent ended without a report, on a raw tool call.)"
    rc, stat = _run(["git", "diff", "--stat", "--", *scope], cwd, timeout=30.0)
    changed = [rel for rel in _changed_files(cwd) if _in_scope(rel, scope)]
    lines = [stub]
    if rc == 0 and stat.strip():
        lines.append(f"git diff --stat:\n{stat.strip()}")
    if changed:
        lines.append("Changed or new in its scope: " + ", ".join(changed))
    elif rc == 0 and not stat.strip():
        lines.append("git diff --stat: no change.")
    return "\n".join(lines)


async def _run_worker(
    brief: str,
    cwd: Path,
    model: str,
    provider: str,
    timeout: float,
    signal: ToolCancellationToken | None = None,
    task: str = "",
    scope: list[str] | None = None,
) -> _WorkerRun:
    """Run one step-executor as a nested `tau -p --mode json` and read its report.

    A task's scope rides in the worker's environment, where its scope guard
    holds the worker's writes to it.

    The brief rides on stdin (tau prepends it to the prompt); the persona is
    appended to tau's base system prompt, not swapped for it, so the worker
    keeps the built-in tool guidance and only gains the persona. JSON mode is
    for the usage figures: `pursuit close --spent` wants what the work cost,
    and beagle cannot see it from a subprocess.
    """
    step_executor = _LAYOUT.step_executor
    if step_executor is None:
        return _WorkerRun(
            problem=f"no beagle plugin ships {STEP_EXECUTOR_REL} "
            f"(looked in {_LAYOUT.found_by or BEAGLE})."
        )
    session_id = uuid.uuid4().hex
    transcript = TauPaths().project_session_dir(cwd) / f"{session_id}.jsonl"
    cmd = [
        TAU_BIN,
        "-p",
        "--mode",
        "json",
        "--session-id",
        session_id,
        "--cwd",
        str(cwd),
        "--append-system-prompt",
        str(step_executor),
    ]
    if provider:
        cmd += ["--provider", provider]
    if model:
        cmd += ["--model", model]
    cmd += ["--max-turns", str(_worker_max_turns())]
    cmd += ["--thinking", os.environ.get(WORKER_THINKING_ENV, "").strip() or "off"]

    limit = _memory_max()
    env = {**os.environ, WORKER_ENV: "1"}
    env.pop(WORKER_TASK_ENV, None)
    env.pop(WORKER_SCOPE_ENV, None)
    if task:
        env[WORKER_TASK_ENV] = task
    if scope:
        env[WORKER_SCOPE_ENV] = "\n".join(scope)
    try:
        proc = await asyncio.create_subprocess_exec(
            *_capped(cmd, limit),
            cwd=str(cwd),
            env=env,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError:
        return _WorkerRun(
            problem=f"{TAU_BIN!r} not found on PATH; cannot delegate. "
            "Do the work inline, or set TAU_BIN."
        )

    events = _WorkerEvents()
    talk = asyncio.ensure_future(_talk(proc, brief, events))
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    problem: str | None = None
    while not talk.done():
        if signal is not None and signal.is_cancelled():
            problem = "cancelled; the worker was killed and its partial work is in the tree."
            break
        remaining = deadline - loop.time()
        if remaining <= 0:
            problem = (
                f"the step-executor exceeded its wall-clock budget of {timeout:.0f}s and "
                "was killed. Split the task, or lower its turn cap "
                f"({WORKER_MAX_TURNS_ENV})."
            )
            break
        await asyncio.wait({talk}, timeout=min(_WORKER_POLL_SECONDS, remaining))
    if problem is not None:
        with contextlib.suppress(ProcessLookupError):
            proc.kill()
        with contextlib.suppress(Exception):
            await talk
        return _WorkerRun(returncode=proc.returncode, problem=problem, transcript=transcript)

    stderr = talk.result()
    note = _killed_note(proc.returncode, limit)
    if _TOOL_CALL_MARKUP.search(events.report):
        report = _unreported_changes(cwd, scope or [])
    else:
        report = events.final_report(f"{stderr}\n{note}".strip() if note else stderr)
    return _WorkerRun(
        returncode=proc.returncode,
        report=report,
        spent=events.spent,
        transcript=transcript,
    )


def _founded_dispatch_refusal(cwd: Path) -> str | None:
    """Why the driver of a founded pursuit may not dispatch, or None.

    R01's 9B driver founded its pursuit and then called pursuit_dispatch
    twice, not pursuit_step: a dispatch opens and closes no task, so 45 of
    58 minutes left nothing in the tree. A worker never has the tool.
    """
    if _is_worker():
        return None
    goal = _find_goal(cwd)
    if goal is None:
        return None
    task = ""
    with contextlib.suppress(Exception):  # the refusal stands without a task id
        rc, ready, _raw = _next_ready(goal.parent.parent)
        if rc in (0, 3) and isinstance(ready, dict):
            task = (_ids(ready.get("open")) + _ids(ready.get("ready")) or [""])[0]
    then = (
        f"Call pursuit_step with task={task}: it opens {task}, has a sub-agent do it, runs "
        "its check and closes it."
        if task
        else "Call pursuit_step with no arguments: it shows the next ready task."
    )
    return (
        "pursuit_dispatch: refused, nothing was spawned. This pursuit is founded, and its "
        "work goes through pursuit_step; a dispatch opens and closes no task, so nothing "
        f"it does is recorded. {then}"
    )


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
        refusal = _founded_dispatch_refusal(cwd)
        if refusal is not None:
            return _make_dispatch_result(refusal)

        model = _worker_model(arguments.get("model"))
        provider = _worker_provider(arguments.get("provider"))
        timeout, clamped = _worker_timeout(arguments.get("timeout"))

        run = await _run_worker(brief, cwd, model, provider, timeout, signal)
        if run.problem is not None:
            return _with_note(_make_dispatch_result(f"pursuit_dispatch: {run.problem}"), clamped)
        header = (
            f"[pursuit_dispatch] step-executor "
            f"(model={model or 'inherit'} provider={provider or 'inherit'}) "
            f"cwd={cwd} rc={run.returncode}\n\n"
        )
        footer = (
            "\n\n— YOU run the close, not the worker: `beagle pursuit close <task> "
            "--outcome done --spent <n>`, after running its --done-when yourself."
        )
        return _with_note(_make_dispatch_result(header + run.shown_report + footer), clamped)

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
                f"Default and maximum: {DEFAULT_DISPATCH_TIMEOUT:.0f}."
            ),
        },
    },
    "required": ["brief"],
}


# --------------------------------------------------------------------------- #
# steering: found, plan and step a pursuit through tools, not the driver text
# --------------------------------------------------------------------------- #

#: Opts the driver session back into editing project files itself.
DRIVER_EDITS_ENV = "BEAGLE_TAU_DRIVER_EDITS"
#: Default budget written at founding: roughly one focused task's worth.
FOUNDING_BUDGET_TOKENS = 100_000
#: Worker attempts `pursuit_step` makes before handing a failing check back.
DEFAULT_STEP_ATTEMPTS = 2
#: Cap on a done close's `--body`, which beagle refuses past 4000 characters.
CLOSE_BODY_CHARS = 3_900
#: How much of a failing check's output goes back to the next attempt.
CHECK_TAIL_CHARS = 1_500
#: Fallback for a check with no recorded timeout.
DEFAULT_CHECK_TIMEOUT = 600.0

_TASK_ID = re.compile(r"\bT\d{4,}\b")


def _step_result(text: str) -> AgentToolResult:
    return AgentToolResult(content=[TextContent(text=text)])


def _project_root() -> tuple[Path, Path | None]:
    """The project root and its goal file (None when nothing is founded)."""
    cwd = _SEEN_CWD or Path.cwd()
    goal = _find_goal(cwd)
    return (goal.parent.parent if goal is not None else cwd), goal


#: beagle refuses a task title longer than this.
MAX_TASK_TITLE = 200


def _task_title(statement: str) -> str:
    """The root task's title: the statement's first line, cut at a word to fit."""
    line = statement.strip().splitlines()[0].strip()
    if len(line) <= MAX_TASK_TITLE:
        return line
    cut = line[: MAX_TASK_TITLE - 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    return f"{cut}…"


def _ensure_git_repo(root: Path) -> bool:
    """`git init` a project that is in no repository; True if it ran.

    The history guard, `commit-claims` and every step's diff stand on git; a
    model founding a pursuit in a bare directory never thinks to make one.
    """
    rc, _ = _run(["git", "rev-parse", "--git-dir"], root, timeout=10.0)
    if rc == 0:
        return False
    rc, _ = _run(["git", "init", "--quiet"], root, timeout=10.0)
    return rc == 0


def _ignore_caches(root: Path) -> None:
    """Add the tool caches a project has no `.gitignore` line for to its `.gitignore`.

    Run 11d's one commit carried `__pycache__`; a worker's `git add .` and
    the step's own commit both read the ignore file.
    """
    _ignore(root, sorted(_CACHE_DIRS))


def _ignore(root: Path, names: list[str]) -> None:
    """Add a `<name>/` line to the project's `.gitignore` for each name it lacks."""
    ignore = root / ".gitignore"
    try:
        have = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    except OSError:
        return
    lines = {line.strip().strip("/") for line in have.splitlines()}
    missing = [name for name in names if name not in lines]
    if not missing:
        return
    sep = "" if not have or have.endswith("\n") else "\n"
    with contextlib.suppress(OSError):
        ignore.write_text(have + sep + "".join(f"{name}/\n" for name in missing), encoding="utf-8")


#: Where founding puts the references the user's prompt links to, as text.
REFERENCES_DIR = "references"
#: What founding recorded there: the request, and each URL's file or failure.
REFERENCES_INDEX = "index.json"
REFERENCE_FETCH_TIMEOUT = 30.0
REFERENCE_MAX_BYTES = 5 * 1024 * 1024
_PROMPT_URL = re.compile(r"https?://[^\s<>\"'`]+")


def _prompt_urls(text: str) -> list[str]:
    """The http(s) URLs in `text`, in order, each once, trailing punctuation off."""
    urls: list[str] = []
    for match in _PROMPT_URL.finditer(text):
        url = match.group(0).rstrip(".,;:!?")
        while url.endswith((")", "]", "}")) and url.count(url[-1]) > url.count(
            {")": "(", "]": "[", "}": "{"}[url[-1]]
        ):
            url = url[:-1].rstrip(".,;:!?")
        if url not in urls:
            urls.append(url)
    return urls


def _reference_name(url: str, taken: set[str]) -> str:
    """`references/<name>.txt`'s name for `url`: its last path segment, extension off."""
    parsed = urllib.parse.urlsplit(url)
    segments = [s for s in urllib.parse.unquote(parsed.path).split("/") if s]
    stem = segments[-1] if segments else parsed.hostname or "reference"
    stem = re.sub(r"\.(pdf|html?|php|aspx?|txt|md)$", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.") or "reference"
    name, n = f"{stem}.txt", 1
    while name in taken or name == REFERENCES_INDEX:
        n += 1
        name = f"{stem}-{n}.txt"
    taken.add(name)
    return name


class _HtmlText(html.parser.HTMLParser):
    """An HTML page's text, script and style left out, block elements on their own lines."""

    _SKIP = frozenset({"script", "style", "noscript", "template", "svg", "head"})
    _BLOCK = frozenset(
        {
            "p",
            "div",
            "br",
            "li",
            "tr",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "pre",
            "section",
            "article",
            "blockquote",
            "table",
            "ul",
            "ol",
            "dt",
            "dd",
            "hr",
            "figure",
        }
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skipping = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag in self._SKIP:
            self._skipping += 1
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP:
            self._skipping = max(0, self._skipping - 1)
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skipping:
            self.parts.append(data)

    def text(self) -> str:
        lines = (
            re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in "".join(self.parts).splitlines()
        )
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def _pdf_text(body: bytes) -> str:
    if shutil.which("pdftotext") is None:
        raise OSError("it is a PDF and pdftotext is not installed")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "reference.pdf"
        pdf.write_bytes(body)
        proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf), "-"],
            capture_output=True,
            timeout=120,
            check=False,
        )
    if proc.returncode != 0:
        why = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        raise OSError(f"pdftotext failed (exit {proc.returncode}): {why[-1] if why else ''}")
    return proc.stdout.decode("utf-8", "replace")


def _fetch_reference(url: str) -> str:
    """`url`'s content as text: a PDF through `pdftotext -layout`, HTML stripped.

    Raises OSError (urllib's errors are its subclasses) or ValueError on failure.
    """
    request = urllib.request.Request(url, headers={"User-Agent": "tau-beagle/1"})
    with urllib.request.urlopen(request, timeout=REFERENCE_FETCH_TIMEOUT) as response:
        body = response.read(REFERENCE_MAX_BYTES + 1)
        kind = response.headers.get_content_type() if response.headers else ""
        charset = (response.headers.get_content_charset() if response.headers else None) or "utf-8"
    if len(body) > REFERENCE_MAX_BYTES:
        raise ValueError(f"larger than {REFERENCE_MAX_BYTES // (1024 * 1024)} MB")
    if kind == "application/pdf" or body.startswith(b"%PDF"):
        text = _pdf_text(body)
    else:
        try:
            text = body.decode(charset, "replace")
        except LookupError:
            text = body.decode("utf-8", "replace")
        if kind in ("text/html", "application/xhtml+xml") or re.match(
            r"\s*(<!doctype html|<html)", text[:512], re.IGNORECASE
        ):
            parser = _HtmlText()
            parser.feed(text)
            parser.close()
            text = parser.text()
    if not text.strip():
        raise ValueError("it held no text")
    return text


def _fetch_references(root: Path, prompt: str) -> dict[str, Any]:
    """Fetch each URL in the user's `prompt` once into `references/`, as text.

    R02's workers never saw the paper: the driver, barred from the
    reference, wrote the domain into its step notes from the name alone.
    The request itself, and each URL's file or why it could not be fetched,
    go in `references/index.json`, which every worker brief is built from.
    A failed fetch is recorded, never fatal.
    """
    urls = _prompt_urls(prompt)
    if not prompt.strip():
        return {}
    folder = root / REFERENCES_DIR
    index: dict[str, Any] = {"request": prompt, "fetched": {}, "failed": {}}
    taken: set[str] = set()
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {**index, "failed": {url: f"cannot make {folder}: {exc}" for url in urls}}
    for url in urls:
        name = _reference_name(url, taken)
        try:
            (folder / name).write_text(_fetch_reference(url), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001 - one bad URL must not stop founding
            index["failed"][url] = str(exc).strip() or type(exc).__name__
            continue
        index["fetched"][name] = url
    with contextlib.suppress(OSError):
        (folder / REFERENCES_INDEX).write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    _ignore(root, [REFERENCES_DIR])
    return index


def _references_for(root: Path, prompt: str) -> dict[str, Any]:
    """`references/index.json` if it already holds `prompt`'s fetch, else a fresh fetch.

    The found-first steer fetches before founding so the driver sees the
    references while it writes the criteria; founding then reuses that.
    """
    folder = root / REFERENCES_DIR
    try:
        index = json.loads((folder / REFERENCES_INDEX).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        index = None
    if (
        isinstance(index, dict)
        and prompt.strip()
        and index.get("request") == prompt
        and all((folder / name).is_file() for name in index.get("fetched") or {})
    ):
        _ignore(root, [REFERENCES_DIR])
        return index
    return _fetch_references(root, prompt)


#: About how much of each reference the found-first steer shows the driver.
REFERENCE_EXTRACT_CHARS = 1500
_ABSTRACT = re.compile(r"(?im)^\s*abstract\b[\s.:\-\u2014]*")


def _reference_extract(text: str) -> str:
    """A reference's title and opening (its abstract when it has one), cut at a word.

    The title is the `<title>` when the text still has one, else its first
    non-empty line. The whole is about REFERENCE_EXTRACT_CHARS long.
    """
    found = re.search(r"(?is)<title[^>]*>(.*?)</title>", text)
    lines = text.splitlines()
    if found and found.group(1).strip():
        title = " ".join(found.group(1).split())
        body = text[found.end() :]
    else:
        first = next((i for i, line in enumerate(lines) if line.strip()), None)
        if first is None:
            return ""
        title = " ".join(lines[first].split())
        body = "\n".join(lines[first + 1 :])
    abstract = _ABSTRACT.search(body, 0, 4 * REFERENCE_EXTRACT_CHARS)
    if abstract:
        body = body[abstract.end() :]
    body = " ".join(re.sub(r"<[^>]+>", " ", body).split())
    if len(title) > REFERENCE_EXTRACT_CHARS // 4:
        title = title[: REFERENCE_EXTRACT_CHARS // 4].rsplit(" ", 1)[0] + "\u2026"
    room = REFERENCE_EXTRACT_CHARS - len(title) - 2
    if len(body) > room:
        cut = body[: room + 1]
        body = (cut.rsplit(" ", 1)[0] if " " in cut else cut[:room]).rstrip(" ,;:") + "\u2026"
    return f"{title}\n\n{body}" if body else title


def _references_note(index: Mapping[str, Any], root: Path) -> str:
    """The found-first steer's part on the request's references: an extract each."""
    fetched, failed = index.get("fetched") or {}, index.get("failed") or {}
    if not fetched and not failed:
        return ""
    parts = []
    for name, url in fetched.items():
        try:
            text = (root / REFERENCES_DIR / name).read_text(encoding="utf-8")
        except OSError as exc:
            parts.append(f"Could not read {REFERENCES_DIR}/{name} (from {url}): {exc}")
            continue
        parts.append(
            f"From {url} ({REFERENCES_DIR}/{name}), its opening:\n<<<\n"
            f"{_reference_extract(text)}\n>>>"
        )
    parts += [f"Could not fetch {url}: {why}" for url, why in failed.items()]
    return (
        "The references in the request, fetched for you:\n\n"
        + "\n\n".join(parts)
        + "\n\nThe statement and criteria you give pursuit_found must describe this in "
        "the reference's own terms, not from the name alone: a name can mean more than "
        "one thing, and the reference says which."
    )


def _references_brief(root: Path) -> str:
    """The worker brief's part from `references/index.json`: request and references."""
    try:
        index = json.loads((root / REFERENCES_DIR / REFERENCES_INDEX).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    if not isinstance(index, dict):
        return ""
    parts = []
    fetched = index.get("fetched") or {}
    failed = index.get("failed") or {}
    if fetched or failed:
        lines = [f"- {REFERENCES_DIR}/{name} (from {url})" for name, url in fetched.items()]
        lines += [f"- could not fetch {url}: {why}" for url, why in failed.items()]
        parts.append(
            "References: read first; outranks the driver's notes. Where the driver's "
            "notes or the task disagree with the reference, the reference is right:\n"
            + "\n".join(lines)
        )
    request = str(index.get("request") or "").strip()
    if request:
        parts.append(f"The user's original request, verbatim:\n<<<\n{request}\n>>>")
    return "\n\n".join(parts)


def _git_identity(root: Path) -> bool:
    """Whether a commit in `root` would know who made it (config, env or host)."""
    return all(
        _run(["git", "var", ident], root, timeout=10.0)[0] == 0
        for ident in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT")
    )


@functools.cache
def _scopes_work() -> bool:
    """Whether `systemd-run --user --scope` can start a process here."""
    if shutil.which("systemd-run") is None:
        return False
    try:
        probe = subprocess.run(
            ["systemd-run", "--user", "--scope", "-q", "true"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return probe.returncode == 0


def _memory_max() -> str | None:
    """The memory cap to run a worker or check under, or None for none."""
    limit = os.environ.get(MEMORY_MAX_ENV, DEFAULT_MEMORY_MAX).strip()
    if limit.lower() in {"", "off", "0", "infinity"} or not _scopes_work():
        return None
    return limit


def _capped(argv: list[str], limit: str | None) -> list[str]:
    """`argv` run in its own systemd scope under `limit`, or as is for no limit.

    A scope execs the command in place, so the pid is the command's own and
    killing it kills the command; an over-cap kill shows as SIGKILL.
    """
    if limit is None:
        return argv
    return [
        "systemd-run",
        "--user",
        "--scope",
        "-q",
        "-p",
        f"MemoryMax={limit}",
        "-p",
        "MemorySwapMax=0",
        "--",
        *argv,
    ]


def _killed_note(returncode: int | None, limit: str | None) -> str:
    """Why a capped process may have died, for a SIGKILL nobody here sent."""
    if limit is None or returncode != -9:
        return ""
    return (
        f"(It was killed with SIGKILL, most likely for going over its {limit} memory cap; "
        f"{MEMORY_MAX_ENV} sets the cap.)"
    )


def _pursuit(args: list[str], root: Path, timeout: float = 60.0) -> tuple[int, str]:
    return _run([BEAGLE_BIN, "pursuit", *args], root, timeout=timeout)


def _json_reply(out: str) -> Any:
    """The JSON object in a beagle reply, which may carry a stderr line after it."""
    start = out.find("{")
    if start < 0:
        return None
    try:
        return json.JSONDecoder().raw_decode(out[start:])[0]
    except ValueError:
        return None


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _toml_string(text: str) -> str:
    # A JSON string is a valid TOML basic string: same quotes, same escapes.
    return json.dumps(text)


def _tree(root: Path) -> str:
    rc, out = _pursuit(["tree"], root)
    return out if rc == 0 else ""


FOUND_PARAMETERS: dict[str, Any] = {
    "type": "object",
    "properties": {
        "statement": {
            "type": "string",
            "description": "One sentence, in the user's words: what this pursuit is for.",
        },
        "criteria": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Two to six acceptance criteria, the user's: each about the product, "
                "checkable by someone else (a command that exits 0, a file that exists)."
            ),
        },
        "milestones": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "The parts of the goal you can already name, in order, each "
                "'<title>::<what it is for>'. Three to seven is typical."
            ),
        },
        "ordered": {
            "type": "boolean",
            "description": "Each milestone waits on the one before. Default true.",
        },
        "user_confirmed": {
            "type": "boolean",
            "description": (
                "True only when the user gave or approved this statement and these "
                "criteria, word for word, in this conversation."
            ),
        },
        "user_delegated": {
            "type": "boolean",
            "description": (
                "True when the user told you to decide the details yourself ('use your "
                "judgement', 'without further discussion'): the criteria are then your "
                "draft from their request, and you found without asking."
            ),
        },
    },
    "required": ["statement", "criteria", "milestones", "user_confirmed"],
}


def _add_children(task: str, parts: list[str], root: Path) -> tuple[int, str]:
    """Add each `title::intent` part under `task`; stops at the first refusal.

    `add --parent` reads no `title::intent`, so the intent goes in its own
    flag. It takes a child under a container or the root task, but refuses a
    pending leaf, which only `split` decomposes.
    """
    rc, lines = 0, []
    for part in parts:
        title, _, intent = part.partition("::")
        argv = ["add", title.strip(), "--parent", task]
        if intent.strip():
            argv += ["--intent", intent.strip()]
        rc, added = _pursuit(argv, root)
        lines.append(added)
        if rc != 0:
            break
    return rc, "\n".join(lines)


def _children(task: str, root: Path) -> dict[str, str]:
    """`task`'s children by lower-cased title, each its id; ended-undone ones left out."""
    rc, out = _pursuit(["tree", "--json"], root)
    tree = _json_reply(out) if rc == 0 else None
    nodes = tree.get("nodes") if isinstance(tree, dict) else None
    if not isinstance(nodes, list):
        return {}
    return {
        str(node.get("title") or "").strip().lower(): str(node["id"])
        for node in nodes
        if isinstance(node, dict)
        and node.get("parent") == task
        and node.get("id")
        and node.get("status") not in ("abandoned", "superseded")
    }


def _release_waiters(task: str, why: str, root: Path) -> list[str]:
    """Drop every edge that waits on `task`, now abandoned; the tasks released.

    beagle counts an abandoned task as never done, so a task waiting on one
    waits for ever: run 10's driver abandoned T0005 and found nothing ready.
    """
    rc, out = _pursuit(["tree", "--json"], root)
    tree = _json_reply(out) if rc == 0 else None
    nodes = tree.get("nodes") if isinstance(tree, dict) else None
    released = []
    for node in nodes if isinstance(nodes, list) else []:
        if isinstance(node, dict) and task in (node.get("waiting_on") or []):
            waiter = str(node.get("id"))
            reason = f"{task} abandoned: {why}"[:500]
            if _pursuit(["depend", waiter, task, "--drop", "--reason", reason], root)[0] == 0:
                released.append(waiter)
    return released


def _part_title(part: str) -> str:
    return part.partition("::")[0].strip()


def _tree_nodes(root: Path) -> list[dict[str, Any]]:
    """The pursuit's `tree --json` nodes; empty when beagle cannot say."""
    rc, out = _pursuit(["tree", "--json"], root)
    tree = _json_reply(out) if rc == 0 else None
    nodes = tree.get("nodes") if isinstance(tree, dict) else None
    return [n for n in nodes if isinstance(n, dict)] if isinstance(nodes, list) else []


def _duplicate_of(why: str, task: str, nodes: list[dict[str, Any]]) -> str | None:
    """The done or open task that `why` names as the one `task` repeats, or None."""
    status = {str(n.get("id")): n.get("status") for n in nodes}
    for named in _TASK_ID.findall(why):
        if named != task and status.get(named) in ("done", "open"):
            return str(named)
    return None


#: A hard wait: the task that waits, the task its edge names, and the task it
#: waits on now, which differs when the named one was superseded.
_Wait = tuple[str, str, str]


def _heir(task: str, nodes: list[dict[str, Any]]) -> str:
    """The task now holding `task`'s work: `task` itself, unless it was superseded,
    then the last successor (`sibling_of`) in its chain, as beagle's scheduler does."""
    by_id = {str(n.get("id")): n for n in nodes}
    heir = {str(n.get("sibling_of")): str(n.get("id")) for n in nodes if n.get("sibling_of")}
    seen = {task}
    while by_id.get(task, {}).get("status") == "superseded" and heir.get(task, task) not in seen:
        task = heir[task]
        seen.add(task)
    return task


def _hard_waits(nodes: list[dict[str, Any]]) -> dict[str, list[_Wait]]:
    """Each unfinished task's unmet hard waits, by task.

    A superseded task is followed to its heir (`sibling_of`), as beagle's
    scheduler does, and a task waits on whatever its containers wait on.
    """
    by_id = {str(n.get("id")): n for n in nodes}
    own: dict[str, list[_Wait]] = {}
    for task, node in by_id.items():
        for named in node.get("waiting_on") or []:
            now = _heir(str(named), nodes)
            if by_id.get(now, {}).get("status") != "done":
                own.setdefault(task, []).append((task, str(named), now))
    waits: dict[str, list[_Wait]] = {}
    for task, node in by_id.items():
        if node.get("status") in ("done", "abandoned", "superseded"):
            continue
        found: list[_Wait] = []
        up, seen = task, set()
        while up and up not in seen:
            seen.add(up)
            found += own.get(up, [])
            up = str(by_id.get(up, {}).get("parent") or "")
        if found:
            waits[task] = found
    return waits


def _wait_text(wait: _Wait, nodes: list[dict[str, Any]]) -> str:
    """One hard wait in words: `waits on T0002 (superseded, handed to T0008: pending)`."""
    _, named, now = wait
    status = {str(n.get("id")): n.get("status") for n in nodes}
    if named != now:
        return f"waits on {named} (superseded, handed to {now}: {status.get(now)})"
    return f"waits on {named} ({status.get(named)})"


def _wait_cycle(nodes: list[dict[str, Any]]) -> list[_Wait] | None:
    """The hard waits that form one cycle among unfinished tasks, in order, or None.

    A container waits on its parts and a part on what its container waits
    on, so a cycle through either is found. Run R06's driver closed
    T0003 -> T0002 (superseded by T0008) -> T0008 -> T0003 with a bash
    `depend`, and every step after it said only that nothing was ready.
    """
    status = {str(n.get("id")): n.get("status") for n in nodes}
    edges: dict[str, list[tuple[str, _Wait | None]]] = {}
    for task, found in _hard_waits(nodes).items():
        edges[task] = [(wait[2], wait) for wait in found]
    for node in nodes:
        parent, task = str(node.get("parent") or ""), str(node.get("id"))
        if parent and status.get(task) not in ("done", "abandoned", "superseded"):
            edges.setdefault(parent, []).append((task, None))
    state: dict[str, int] = {}  # 1 on the path, 2 finished

    def visit(path: list[str], via: list[_Wait | None]) -> list[_Wait] | None:
        task = path[-1]
        state[task] = 1
        for nxt, wait in edges.get(task, []):
            if state.get(nxt) == 1:
                cycle = [w for w in [*via[path.index(nxt) :], wait] if w is not None]
                if cycle:
                    return cycle
            elif nxt not in state and (found := visit([*path, nxt], [*via, wait])):
                return found
        state[task] = 2
        return None

    for origin in list(edges):
        if origin not in state and (found := visit([origin], [])):
            return found
    return None


def _cycle_break(cycle: list[_Wait], nodes: list[dict[str, Any]]) -> str:
    """What to tell the driver about a cycle of hard waits: the cycle and the drop.

    The edge dropped is the one most likely added by hand: one a successor
    holds, then one that names its task directly. An edge that names a
    superseded task is the plan's order, handed on to the heir.
    """
    succeeds = {str(n.get("id")) for n in nodes if n.get("sibling_of")}
    waiter, named, _ = min(
        cycle, key=lambda w: (w[1] != w[2], w[0] not in succeeds, cycle.index(w))
    )
    ring = " -> ".join([cycle[0][0], *(w[2] for w in cycle)])
    reason = f"breaks the cycle {ring}"
    return (
        f"These hard waits form a cycle, so none of these tasks can ever start "
        f"({ring}):\n"
        + "\n".join(f"- {w[0]} {_wait_text(w, nodes)}" for w in cycle)
        + f"\n\nBreak it by dropping the wait of {waiter} on {named}. Run in bash, "
        f'exactly:\n\n    beagle pursuit depend {waiter} {named} --drop --reason "{reason}"\n\n'
        "then call pursuit_step with no arguments. Splitting a task or abandoning one "
        "does not break the cycle: the parts keep the waits."
    )


def _unfinished(nodes: list[dict[str, Any]]) -> list[str] | None:
    """What keeps the pursuit from done, one line a task; None when it is done.

    None too when the tree has no root, so a tree beagle cannot show is not
    called unfinished. A leaf that ended undone counts unless another task
    took its work on (`sibling_of`) or it was dropped as a duplicate of a
    done task: run R02's driver abandoned four of five milestones as
    "already done", and the root, stalled, read as finished to it.
    """
    roots = [n for n in nodes if not n.get("parent")]
    if not roots:
        return None
    if roots[0].get("status") == "done":
        return None
    by_id = {str(n.get("id")): n for n in nodes}
    heirs = {str(n.get("sibling_of")) for n in nodes if n.get("sibling_of")}
    waits = _hard_waits(nodes)
    left = []
    for node in nodes:
        task, status = str(node.get("id")), node.get("status")
        if node.get("container") or status == "done" or task in heirs:
            continue
        if status == "abandoned":
            named = _TASK_ID.findall(str(node.get("reason") or ""))
            if any(by_id.get(n, {}).get("status") == "done" for n in named if n != task):
                continue
        reason = str(node.get("reason") or "").strip()
        left.append(
            f"- {task} — {node.get('title', '')} ({status}"
            + (f": {reason[:120]}" if reason and status != "pending" else "")
            + ")"
            + "".join(
                f"; {_wait_text(w, nodes)}" + (f" through {w[0]}" if w[0] != task else "")
                for w in waits.get(task, [])
            )
        )
    if not left and roots[0].get("container"):
        return None
    return left or [f"- {roots[0].get('id')} — {roots[0].get('title', '')} (not closed)"]


def _abandon_problem(task: str, why: str, nodes: list[dict[str, Any]]) -> str | None:
    """Why the driver may not abandon `task` for `why`, or None.

    Run R02's driver abandoned four of five milestones in 0.3 min, each as
    "already exists / passes", right after tau's own hint offered abandoning
    work "already done". A task is dropped only as a duplicate of one that
    holds its work; a milestone is the goal's and is never dropped here.
    """
    parent = {str(n.get("id")): str(n.get("parent") or "") for n in nodes}
    roots = [t for t, p in parent.items() if not p]
    if task in roots:
        # Run R04 abandoned the root as "duplicate of T0002"; beagle refused it.
        return (
            f"pursuit_step: {task} not abandoned — it is the root, the goal itself, and "
            "the goal is the user's. Work its open tasks with pursuit_step, or add what "
            "is missing with pursuit_plan."
        )
    by_id = {str(n.get("id")): n for n in nodes}
    predecessor = str(by_id.get(task, {}).get("sibling_of") or "")
    if (
        roots
        and parent.get(predecessor) == roots[0]
        and by_id.get(predecessor, {}).get("status") == "superseded"
        and why
    ):
        # A successor of a superseded milestone: run R06's T0008 was refused
        # as "a milestone" four times, with no other way to drop it.
        return None
    if roots and parent.get(task) == roots[0]:
        return (
            f"pursuit_step: {task} not abandoned — it is a milestone, and a milestone is "
            "the goal's. Split it with pursuit_plan, or give it a new route with "
            f'pursuit_step task="{task}", new_route=true and notes.'
        )
    if _duplicate_of(why, task, nodes) is not None:
        return None
    return (
        f"pursuit_step: {task} not abandoned — a task is dropped only as a duplicate of "
        "a done or open task, named as abandon='duplicate of Tnnnn'. Work that seems "
        "already done is not a reason: if its check already passes, bind the goal "
        "criterion's test as done_when (one that imports and runs the code), so the "
        "check shows the work is there."
    )


#: What the driver is told to do with a task that should not be worked.
ABANDON_HINT = (
    "To drop a task that repeats another, call pursuit_step with its task and "
    "abandon='duplicate of Tnnnn', naming the done or open task that holds its work."
)


#: Set when founding refused an unconfirmed goal in a session with no user to
#: ask; the stop gate holds a turn that ends on it, once.
_FOUND_AWAITS_USER = False
#: How much of the user's prompt a print-mode refusal quotes back.
PROMPT_QUOTE = 400


def _unconfirmed_refusal(statement: str, criteria: list[str], *, interactive: bool) -> str:
    """What `pursuit_found` says to a goal nobody confirmed.

    Run R05's mimo, told "ask the user to confirm … If the user already told
    you to decide, call again with user_delegated=true", asked — in `tau -p`,
    where no one answers — and the run ended after 18 s. With no UI, the
    branch that can apply comes first, beside the prompt that decides it.
    """
    listed = "\n".join(f"  - {c}" for c in criteria)
    drafted = f"Goal: {statement}\nCriteria:\n{listed}"
    if interactive:
        return (
            "pursuit_found: nothing written. The goal and its criteria are the user's: "
            "read them back word for word and ask the user to confirm or correct them:\n\n"
            f"{drafted}\n\n"
            "Then call pursuit_found again with what they approved and "
            "user_confirmed=true. If the user already told you to decide this "
            "yourself, call it again with user_delegated=true instead."
        )
    said = " ".join(_LAST_PROMPT.split())
    if len(said) > PROMPT_QUOTE:
        said = said[:PROMPT_QUOTE].rsplit(" ", 1)[0] + " …"
    return (
        "pursuit_found: nothing written yet. This session runs in print mode: no user "
        "can answer a question, and the prompt that started it is all they will say. "
        f'It said: "{said}"\n\n'
        "If that tells you to set up, decide or go ahead without discussion, call "
        "pursuit_found again now, with the goal and criteria below and "
        "user_delegated=true. Do not ask the user to confirm: nobody will reply. Only "
        "if the prompt gives you nothing to decide from, stop and say what you need.\n\n"
        f"{drafted}"
    )


def make_found_tool(
    on_founded: Callable[[Path], None] | None = None,
    interactive: Callable[[], bool] = lambda: True,
) -> Any:
    """Build `pursuit_found`: write the goal, root the tree, split it into milestones.

    The driver text spends pages on founding; a small model loses the thread
    long before the file is written. The judgement it guards — the goal and
    the criteria are the user's — stays, as `user_confirmed`; the mechanics
    (the TOML shape, the root task, the split) are done here. `on_founded`
    gets the goal file once the root task exists.
    """

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id, signal, on_update
        root, goal = _project_root()
        if goal is not None:
            return _step_result(
                f"pursuit_found: {goal} already exists, so the pursuit is founded. Add "
                "work with pursuit_plan, and work it with pursuit_step."
            )
        statement = str(arguments.get("statement") or "").strip()
        criteria = _strings(arguments.get("criteria"))
        milestones = _strings(arguments.get("milestones"))
        if not statement or not criteria:
            return _step_result("pursuit_found: 'statement' and 'criteria' are both required.")
        if not milestones:
            return _step_result(
                "pursuit_found: name the milestones: the parts of the goal you can "
                "already see, each '<title>::<what it is for>'."
            )
        # Run R03's driver, refused for a setup first milestone, sent the same
        # call fourteen times: what founding can repair itself, it repairs.
        milestones, repairs = _repair_milestones(milestones)
        if not milestones:
            return _step_result(f"pursuit_found: nothing written — {repairs[0]}")
        repaired = "".join(f"{note}\n\n" for note in repairs)
        delegated = arguments.get("user_delegated") is True
        if arguments.get("user_confirmed") is not True and not delegated:
            global _FOUND_AWAITS_USER
            alone = not interactive()
            _FOUND_AWAITS_USER = alone
            refusal = _unconfirmed_refusal(statement, criteria, interactive=not alone)
            return _step_result(f"{repaired}{refusal}")
        initialized = _ensure_git_repo(root)

        goal = root / ".beagle" / GOAL_BASENAME
        goal.parent.mkdir(parents=True, exist_ok=True)
        goal.write_text(
            "[goal]\n"
            f"statement = {_toml_string(statement)}\n"
            f"criteria = [{', '.join(_toml_string(c) for c in criteria)}]\n"
            f"default_budget_tokens = {FOUNDING_BUDGET_TOKENS}\n"
            # pursuit_step opens, works and closes in one call, so nothing
            # else stands where `prove` goes; beagle holds every done close
            # to a witnessed check only when told to.
            '\n[close]\nrequire = "witness"\n',
            encoding="utf-8",
        )
        _ignore_caches(root)
        title = _task_title(statement)
        rc, out = _pursuit(["add", title, "--root-task", "--intent", statement], root)
        found = _TASK_ID.search(out) if rc == 0 else None
        if found is None:
            # Unwritten, so a corrected call founds afresh.
            goal.unlink(missing_ok=True)
            return _step_result(
                f"pursuit_found: nothing founded; `beagle pursuit add --root-task` "
                f"failed (exit {rc}):\n{out}"
            )
        root_task = found.group(0)
        references = await asyncio.to_thread(_references_for, root, _LAST_PROMPT)
        if on_founded is not None:
            on_founded(goal)
        if len(milestones) == 1:
            # beagle refuses a one-part split as a rename; one milestone is
            # one child of the root, which `add --parent` takes.
            rc, out = _add_children(root_task, milestones, root)
        else:
            split = ["split", root_task, *milestones]
            if arguments.get("ordered", True) is not False:
                split.append("--ordered")
            rc, out = _pursuit(split, root)
        if rc != 0:
            return _step_result(
                f"pursuit_found: founded {goal} with root task {root_task}, but the "
                f"milestone split failed (exit {rc}):\n{out}\n\nAdd them with pursuit_plan."
            )
        notes = []
        if initialized:
            notes.append(f"{root} was not a git repository; ran `git init` there.")
        if not _git_identity(root):
            notes.append(
                "git has no user.name or user.email here, so commits will fail. Tell the "
                "user now; do not set one yourself."
            )
        fetched, failed = references.get("fetched") or {}, references.get("failed") or {}
        if fetched or failed:
            got = ", ".join(f"{REFERENCES_DIR}/{name}" for name in fetched) or "none"
            missed = "".join(f"; could not fetch {url}: {why}" for url, why in failed.items())
            notes.append(
                f"References from the user's request, fetched for the workers: {got}{missed}. "
                "Every pursuit_step brief carries them and the request; leave reading them "
                "to the workers."
            )
        if delegated:
            notes.append(
                "The user delegated the details: in your reply, tell them the criteria "
                "you chose, so they can correct them."
            )
        noted = "".join(f"{note}\n\n" for note in [*repairs, *notes])
        return _step_result(
            f"Founded the pursuit in {goal}, root task {root_task}.\n\n{_tree(root)}\n\n"
            f"{noted}{DRIVER_STEERS_NOTE}\n\n{CASES_FIRST_NOTE}\n\n"
            "Next: call pursuit_step with no arguments to see the first ready task. A "
            "milestone too big for one sub-agent's sitting: split it into steps with "
            "pursuit_plan first. The goal file is now the user's; never edit it."
        )

    return execute


PLAN_PARAMETERS: dict[str, Any] = {
    "type": "object",
    "properties": {
        "task": {
            "type": "string",
            "description": "The task to break down (T0002), or the root task to add to.",
        },
        "parts": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Its steps, each '<title>::<what it is for>'.",
        },
        "ordered": {
            "type": "boolean",
            "description": "Each step waits on the one before. Default true.",
        },
    },
    "required": ["task", "parts"],
}


def make_plan_tool() -> Any:
    """Build `pursuit_plan`: split a task into steps, or add steps to a container."""

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id, signal, on_update
        root, goal = _project_root()
        if goal is None:
            return _step_result("pursuit_plan: no pursuit here yet; call pursuit_found first.")
        task = str(arguments.get("task") or "").strip()
        parts = _strings(arguments.get("parts"))
        if not task or not parts:
            return _step_result("pursuit_plan: 'task' and 'parts' are both required.")
        setup = _setup_milestone(parts)
        if setup is not None:
            return _step_result(f"pursuit_plan: nothing added — {setup}")
        # A small model re-sends the plan it already made; beagle adds every
        # part again, and the copies are then worked twice.
        existing = _children(task, root)
        repeated = [
            f"{_part_title(part)} ({existing[_part_title(part).lower()]})"
            for part in parts
            if _part_title(part).lower() in existing
        ]
        parts = [part for part in parts if _part_title(part).lower() not in existing]
        if not parts:
            return _step_result(
                f"pursuit_plan: nothing added — {task} already has {', '.join(repeated)}. "
                "Work them with pursuit_step; call it with no arguments for the next ready one."
            )
        if len(parts) == 1:
            # beagle refuses a one-part split as a rename. A container or the
            # root still takes one more child; a leaf with one part is
            # already a single step, which is the model's to work, not split.
            rc, out = _add_children(task, parts, root)
            # beagle says "a pending leaf" or, for one being worked, "a open
            # leaf": run R06's plan of one part on open T0002 came back raw.
            if rc != 0 and "leaf with work of its own" in out:
                return _step_result(
                    f"pursuit_plan: nothing added — {task} is already one step, so one "
                    "part does not break it down: a plan needs two or more parts, which "
                    f"split {task} into smaller tasks. Give two or more parts, or work it "
                    f"with pursuit_step task={task}."
                )
        else:
            ordered = arguments.get("ordered", True) is not False
            rc, out = _pursuit(["split", task, *parts, *(["--ordered"] if ordered else [])], root)
            if rc != 0 and "already has children" in out:
                rc, out = _add_children(task, parts, root)
        if rc != 0:
            return _step_result(f"pursuit_plan: beagle refused (exit {rc}):\n{out}")
        _forget_task(root, task)
        notes = ""
        if repeated:
            notes += f"Not added again, {task} already has: {', '.join(repeated)}.\n\n"
        if "--outcome abandoned" in out:
            notes += f"{ABANDON_HINT}\n\n"
        return _step_result(f"{out}\n\n{_tree(root)}\n\n{notes}Next: pursuit_step.")

    return execute


STEP_PARAMETERS: dict[str, Any] = {
    "type": "object",
    "properties": {
        "task": {
            "type": "string",
            "description": "The task to work. Omit to be shown the next ready one.",
        },
        "criteria": {
            "type": "string",
            "description": "What will be true when this task is done, in one or two sentences.",
        },
        "done_when": {
            "type": "string",
            "description": (
                "ONE command that exits 0 only when the task is done: a targeted test or a "
                "check, e.g. `python3 -m pytest -q tests/test_x.py`. It is split into words "
                "and run without a shell, so no prose and no &&, |, > or $(...); for more, "
                "write a script and run that. It must fail now, before the work. On an open "
                "task, a new done_when replaces a check that cannot judge the work."
            ),
        },
        "scope": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The paths the work will touch.",
        },
        "locks": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Files this task writes that no later task may change, such as the "
                "known-answer cases from the reference. Locked when the task closes done; "
                "after that a sub-agent's change to them is undone before every check."
            ),
        },
        "notes": {
            "type": "string",
            "description": (
                "What the sub-agent should know that the task record does not: where to "
                "start, what to leave alone, what a previous attempt got wrong."
            ),
        },
        "abandon": {
            "type": "string",
            "description": (
                "Drop this task as a duplicate of a done or open task: 'duplicate of "
                "T0014'. Refused for a milestone and for any other reason. No sub-agent runs."
            ),
        },
        "new_route": {
            "type": "boolean",
            "description": (
                "The task's route resisted: replace it with a new attempt at the same "
                "criteria, done the way notes says (required). A new done_when may come "
                "with it. A blocked task with no new_route is reworked on its own check."
            ),
        },
        "budget": {
            "type": "string",
            "description": "Token budget, as 40k or 100000. Default: the goal's.",
        },
        "attempts": {
            "type": "integer",
            "description": (
                f"Sub-agent runs before a failing check comes back to you. "
                f"Default {DEFAULT_STEP_ATTEMPTS}."
            ),
        },
        "timeout": {
            "type": "number",
            "description": (
                "Wall-clock seconds per sub-agent run. Default and maximum "
                f"{DEFAULT_DISPATCH_TIMEOUT:.0f}."
            ),
        },
    },
}


#: Bare words that mark a `done_when` as a sentence about a check, not a check.
_PROSE_WORDS = frozenset(
    {"exits", "exit", "and", "or", "passes", "succeeds", "should", "must", "covers", "asserts"}
)


#: Programs that exit 0 whatever the work did.
_ALWAYS_PASSES = frozenset({"true", ":", "echo", "printf", "yes"})
#: Programs that pass once a file is there, whatever is in it.
_SHOWS_A_FILE = frozenset({"cat", "ls", "head", "tail", "wc", "stat", "file"})
#: `test` and `[`, and the operators with which they only ask whether a file is there.
_TESTS = frozenset({"test", "["})
_FILE_TESTS = frozenset({"-f", "-e", "-s"})


def _check_problem(command: str) -> str | None:
    """Why `command` cannot be a task's check, or None.

    beagle splits a `done_when` into words and runs it with no shell, so the
    checks a small model writes go wrong in a few known ways:

    - a sentence: `python3 -m pytest -q exits 0 and a test asserts ...` is
      bound and then fails whatever the work does. Words inside quotes are
      data, so only bare ones past the program name count;
    - beagle itself, even inside `bash -c '...'`: `beagle pursuit close T0002`
      as T0002's own check, or `beagle doctor`, which hung a run for good;
    - beagle's own store: `grep -q X .beagle/tree/T0008.md` reads what was
      recorded about the task, and passes once the notes say so;
    - a bare `&&`, `|` or `>`, which reaches the program as an argument;
    - a check that cannot fail: `true`, which run 9 bound to "abandon" a
      duplicate, or one that only shows a file is there (`cat docs/x.md`,
      `python3 -m json.tool cases.json`) and passes whatever it says.
    """
    try:
        words = shlex.split(command)
    except ValueError:
        return None  # beagle says why it will not split
    if not words:
        return None
    one_command = (
        "It must be ONE command over the project that exits 0 exactly when the task is "
        "done, such as `python3 -m pytest -q tests/test_greet.py`"
    )
    if _bash_find(command, lambda argv: "beagle" if _named(argv, "beagle") else None):
        # The close runs the check, so a check that runs beagle can only ever
        # answer how it was called, never whether the work is done.
        return (
            f"done_when runs beagle itself, which cannot say whether the work is done. "
            f"{one_command}; pursuit_step does the close. Call pursuit_step again with that."
        )
    if any(".beagle" in word for word in words):
        return (
            "done_when reads .beagle/, beagle's record of the pursuit, which says what was "
            "written about the work, not what was built: a grep of a task's notes passes "
            f"as soon as the notes say so. {one_command}. A file the task writes goes in the "
            "project, not in .beagle/: a note or summary in docs/, checked with `grep -q "
            "'<a phrase it must contain>' docs/<name>.md`. Call pursuit_step again with that."
        )
    operators = _bare_operators(command)
    if operators:
        return (
            f"done_when has a bare {operators[0]!r}, but it runs without a shell, so "
            f"{operators[0]!r} reaches {words[0]!r} as an argument. {one_command}; for "
            "more than one thing, write a test that checks them all and run that. Call "
            "pursuit_step again with it."
        )
    program = Path(words[0]).name
    if program in _ALWAYS_PASSES:
        return (
            f"done_when `{command}` exits 0 whatever the work does, so it cannot judge it. "
            f"{one_command}. {ABANDON_HINT}"
        )
    if program in _TESTS and _FILE_TESTS & set(words[1:]):
        # Run R02 closed its reference task on `test -f src/design.md`; the
        # design's content was never judged.
        return (
            f"done_when `{command}` only tests that a file exists, so it passes whatever "
            f"the file says. {one_command}; for a document, `grep -q '<a term the "
            "reference uses>' <doc>`, so the check reads what it must hold. Call "
            "pursuit_step again with that."
        )
    if program in _SHOWS_A_FILE or (program.startswith("python") and "json.tool" in words[1:3]):
        return (
            f"done_when `{command}` passes as soon as the file is there, whatever it says. "
            f"{one_command}, testing what the file must hold; for a document, `grep -q "
            "'<a phrase it must contain>' <path>`. Call pursuit_step again with that."
        )
    if program.startswith("python") and _only_imports(words[1:]):
        # Run R04 bound `python3 -c "from tests.test_case_data import
        # validate_fork_seed; print('OK')"`, which passes once the name exists.
        return (
            f"done_when `{command}` only imports and prints, so it passes as soon as the "
            f"file is there, whatever it says. {one_command}, testing what the code must "
            "do. Call pursuit_step again with that."
        )
    found = [w for w in words[1:] if w.lower() in _PROSE_WORDS]
    if not found:
        return None
    return (
        f"done_when reads as a sentence (bare {', '.join(repr(w) for w in found[:3])}), not "
        "a command. It is split into words and run as-is, so it must be ONE command "
        "that exits 0 exactly when the task is done, such as `python3 -m pytest -q "
        "tests/test_greet.py`. Put what the test must assert in criteria and notes, "
        "and call pursuit_step again."
    )


def _only_imports(args: list[str]) -> bool:
    """Whether a python argv's `-c` code only imports, prints and passes."""
    if "-c" not in args or args.index("-c") + 1 >= len(args):
        return False
    try:
        body = ast.parse(args[args.index("-c") + 1]).body
    except SyntaxError:
        return False

    def inert(node: ast.stmt) -> bool:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Pass)):
            return True
        if not isinstance(node, ast.Expr):
            return False
        value = node.value
        if isinstance(value, ast.Constant):
            return True
        return (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "print"
            and all(isinstance(a, ast.Constant) for a in value.args)
        )

    return bool(body) and all(inert(node) for node in body)


def _bare_operators(command: str) -> list[str]:
    """The unquoted shell operators in `command`, in order."""
    lexer = shlex.shlex(command, posix=False, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return [token for token in lexer if _is_operator(token)]
    except ValueError:
        return []


def _scope_problem(scope: list[str]) -> str | None:
    """Why a task's scope is wrong, or None: it names beagle's own store."""
    store = [path for path in scope if Path(path).parts[:1] == (".beagle",)]
    if not store:
        return None
    return (
        f"scope names {store[0]}, beagle's own record of the pursuit. pursuit_found "
        "already set the pursuit up, and the tools keep its record; a task's work and "
        "scope are in the project. Name the project paths the task will touch."
    )


#: Words a milestone about setting the pursuit up is made of, and nothing else.
_SETUP_WORDS = frozenset(
    {
        "setup",
        "set",
        "up",
        "init",
        "initial",
        "initialize",
        "initialise",
        "configure",
        "config",
        "configuration",
        "install",
        "bootstrap",
        "project",
        "pursuit",
        "beagle",
        "the",
        "for",
        "and",
    }
)


def _setup_milestone(parts: list[str]) -> str | None:
    """Why one of `parts` is not work toward the goal, or None.

    Asked to "set this project up for beagle pursuit, and then implement X",
    a small model made `setup` its first milestone: a task with no work in the
    project, a check over `.beagle/`, and every later milestone ordered behind
    it. Founding is the setup.
    """
    for part in parts:
        # `title::purpose` is asked for, but `title: purpose` is what came.
        title = part.split(":", 1)[0]
        words = re.findall(r"[a-z]+", title.lower())
        if (words and set(words) <= _SETUP_WORDS) or ".beagle" in part:
            return (
                f"{title.strip()!r} is not part of the goal's work: pursuit_found is what "
                "sets the pursuit up, and it is done once it is founded. Leave it out. If "
                "the project itself needs scaffolding, name what, e.g. 'package layout::"
                "pyproject.toml, src/ and tests/ so the later parts have a home'."
            )
    return None


def _repair_milestones(milestones: list[str]) -> tuple[list[str], list[str]]:
    """`milestones` with what founding can fix fixed, and a note for each fix.

    A setup milestone is dropped and an over-long title is cut at a word, its
    whole text moved after '::'. With every milestone dropped, nothing is
    left: the list comes back empty and the one note says why.
    """
    kept: list[str] = []
    dropped: list[str] = []
    for part in milestones:
        if _setup_milestone([part]) is not None:
            dropped.append(part)
        else:
            kept.append(part)
    if not kept:
        return [], [_setup_milestone(dropped) or "every milestone sets the pursuit up."]
    notes = []
    if dropped:
        named = ", ".join(repr(part.split(":", 1)[0].strip()) for part in dropped)
        notes.append(
            f"Dropped the setup milestone {named}: founding is the setup, so it is not "
            "part of the goal's work. The milestones are the rest."
        )
    repaired: list[str] = []
    for index, part in enumerate(kept, 1):
        title, sep, intent = part.partition("::")
        title = title.strip()
        if len(title) <= MAX_TASK_TITLE:
            repaired.append(part)
            continue
        short = _task_title(title)
        detail = f"{title} — {intent.strip()}" if sep and intent.strip() else title
        repaired.append(f"{short}::{detail}")
        notes.append(
            f"Milestone {index} had a {len(title)}-character title; beagle takes at most "
            f"{MAX_TASK_TITLE}, so it is now {short!r}, with the whole text after '::'."
        )
    return repaired, notes


def _check_argv(command: str, root: Path) -> list[str]:
    """The argv beagle's close runs a `done_when` as: split into words, no shell.

    A launcher declared under `[run] contain` in the goal file goes in front,
    as beagle's `contained()` puts it. Raises ValueError for a command that
    will not split.
    """
    prefix = ""
    with contextlib.suppress(Exception):
        goal = tomllib.loads((root / ".beagle" / GOAL_BASENAME).read_text(encoding="utf-8"))
        contain = goal.get("run", {}).get("contain")
        prefix = contain.strip() if isinstance(contain, str) else ""
    return shlex.split(f"{prefix} {command}" if prefix else command)


async def _run_check(command: str, root: Path, timeout: float) -> tuple[int, str]:
    """Run a task's `done_when` the way its close will, before the close does.

    A done close that the check refuses blocks the task for good, so the step
    learns the verdict first and keeps a failing task open for another try.
    Beagle runs the check as words, not through a shell, and so does this: a
    check that only passes under `bash -c` would pass here and block there.
    """
    try:
        argv = _check_argv(command, root)
    except ValueError as exc:
        return 2, f"the check will not split into arguments ({exc})"
    if not argv:
        return 2, "the check is empty"
    limit = _memory_max()
    try:
        proc = await asyncio.create_subprocess_exec(
            *_capped(argv, limit),
            cwd=str(root),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
    except OSError as exc:
        return 127, f"the check could not start: {exc}"
    try:
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError:
        with contextlib.suppress(ProcessLookupError):
            proc.kill()
        await proc.wait()
        return 124, f"the check timed out after {timeout:.0f}s"
    out = (stdout or b"").decode("utf-8", "replace").strip()
    note = _killed_note(proc.returncode, limit)
    return proc.returncode or 0, f"{out}\n{note}".strip() if note else out


#: What a worker is asked to end its report with: one defect `prove` can put back.
WITNESS_NOTE = (
    "When the check passes, end your report with the WITNESS block below. It names one "
    "small defect the check must catch, in the code you wrote — or, if this task only "
    "adds tests, in the code they test — never in a test file: "
    "`prove` puts it back, and if the check still passes, the task is not done. The "
    "NEEDLE is text copied exactly from the file that occurs there only once; the "
    "REPLACEMENT is the same text made wrong (a flipped condition, a wrong constant, a "
    "dropped step).\n\n"
    "WITNESS: <path of the source file>\n"
    "NEEDLE:\n<exact text from the file>\n"
    "REPLACEMENT:\n<that text with the defect>\n"
    "END WITNESS"
)
_WITNESS = re.compile(
    r"^WITNESS:[ \t]*(?P<path>\S+)[ \t]*\n"
    r"NEEDLE:[ \t]*\n(?P<needle>.*?)\n"
    r"REPLACEMENT:[ \t]*\n(?P<replacement>.*?)\n?"
    r"^END WITNESS",
    re.MULTILINE | re.DOTALL,
)
#: How `prove` gives its verdict: exit 0 for PROVEN, 9 for NOT PROVEN.
_PROVE_VERDICT = re.compile(r"^(T\d+): (PROVEN|NOT PROVEN) —", re.MULTILINE)
#: Why a witness may sit in code the task did not write.
PREDATES_BECAUSE = (
    "this task's check tests code an earlier task wrote; the defect is put back there "
    "to show the check this task added catches it"
)
#: How much of a `prove` reply the driver and the next worker see.
PROVE_TAIL_CHARS = 1_500


def _witness(report: str) -> tuple[str, str, str] | None:
    """The last WITNESS block in a worker's report: (path, needle, replacement)."""
    found = list(_WITNESS.finditer(report))
    if not found:
        return None
    last = found[-1]
    needle = last.group("needle").strip("\n")
    if not needle.strip():
        return None
    path = last.group("path").strip("`'\"")
    return path, needle, last.group("replacement").strip("\n")


def _is_test_path(rel: str) -> bool:
    parts = Path(rel).parts
    name = parts[-1] if parts else rel
    return (
        bool({"test", "tests"} & set(parts[:-1]))
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
    )


def _only_data_and_tests(paths: list[str]) -> bool:
    """Whether `paths` are tests and data files (not .py), at least one a test.

    Without a test it is not known answers: a docs-only task's design.md is
    neither proved by its absence nor locked.
    """

    def test(rel: str) -> bool:
        path = Path(rel.rstrip("/"))
        return path.name in {"test", "tests"} or _is_test_path(str(path))

    def data(rel: str) -> bool:
        suffix = Path(rel.rstrip("/")).suffix
        return bool(suffix) and suffix != ".py"

    return any(test(rel) for rel in paths) and all(test(rel) or data(rel) for rel in paths)


def _is_fixture(decorator: ast.expr) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute):
        return target.attr == "fixture"
    return isinstance(target, ast.Name) and target.id == "fixture"


#: A top-level function in a test file longer than this is implementation, not a helper.
_HELPER_MAX_LINES = 15


def _implementation_in_tests(root: Path, changed: list[str]) -> list[str]:
    """`<file>: <definition>` for each top-level class, or non-test function over
    `_HELPER_MAX_LINES` lines, in a changed test.

    Run R04: a cases-first worker wrote an `IntervalTreeClock` class into
    tests/test_cases.py, and twenty more workers debugged it there. Run R06: a
    passing cases-first task stayed open over a three-line `load_cases()`, so a
    small function is let through as a helper.
    """
    found: list[str] = []
    for rel in changed:
        if not (_is_test_path(rel) and rel.endswith(".py")) or rel.endswith("conftest.py"):
            continue
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"), filename=rel)
        except (OSError, SyntaxError, ValueError):
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith("Test"):  # pytest's test grouping
                    found.append(f"{rel}: class {node.name}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith(("test_", "_", "pytest_")):
                    continue
                if any(_is_fixture(d) for d in node.decorator_list):
                    continue
                if (node.end_lineno or node.lineno) - node.lineno + 1 <= _HELPER_MAX_LINES:
                    continue
                found.append(f"{rel}: def {node.name}")
    return found


def _changed_files(root: Path) -> list[str]:
    """Paths git sees changed or new, beagle's record and caches left out."""
    rc, out = _run(["git", "status", "--porcelain", "--untracked-files=all"], root, timeout=30.0)
    if rc != 0:
        return []
    paths = []
    for line in out.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:].split(" -> ")[-1].strip().strip('"')
        parts = Path(rel).parts
        if not parts or parts[0] == ".beagle" or _CACHE_DIRS & set(parts):
            continue
        paths.append(rel)
    return paths


def _in_scope(rel: str, scope: list[str]) -> bool:
    if not scope:
        return True
    return any(rel == s.rstrip("/") or rel.startswith(s.rstrip("/") + "/") for s in scope)


@dataclass(frozen=True)
class _Proof:
    """What `prove` said of a passing check, or why it could not be asked."""

    proven: bool
    text: str
    #: A defect was put back and the check still passed: the check, not the
    #: work, is what falls short.
    weak: bool = False


async def _prove(
    task: str, report: str, scope: list[str], root: Path, timeout: float
) -> _Proof | None:
    """Ask `beagle pursuit prove` whether the passing check can refuse at all.

    A check that passes over a defect put back into the work is not about the
    work: run 11d closed two tasks on import-only checks. The worker names the
    defect (`WITNESS_NOTE`); a missing or misshapen one falls back to taking
    away the source files the task changed, or with none, its data files. None
    when neither can be tried —
    no witness and no changed file — and the close decides.
    """
    attempts: list[list[str]] = []
    refused: list[str] = []
    witness = _witness(report)
    if witness is not None and _is_test_path(witness[0]):
        # Run R04: W24's witness was in tests/test_case_data.py, and beagle
        # answered about the needle's count, not the check.
        refused.append(
            f"{witness[0]}: the WITNESS is in a test file; name a defect in the code the "
            "test runs, and leave the test as it is."
        )
    elif witness is not None:
        path, needle, replacement = witness
        attempts.append(["--mutate", path, "--needle", needle, "--replacement", replacement])
    sources = [
        rel
        for rel in _changed_files(root)
        if _in_scope(rel, scope) and not _is_test_path(rel) and (root / rel).is_file()
    ]
    if not sources:
        # A known-answers task changes only data and tests: taking its data
        # file away is the defect (beagle proves it when the task wrote it).
        sources = [
            rel
            for rel in _changed_files(root)
            if _in_scope(rel, scope) and not rel.endswith(".py") and (root / rel).is_file()
        ]
    if sources:
        attempts.append([arg for rel in sources for arg in ("--absent", rel)])
    for how in attempts:
        argv = [BEAGLE_BIN, "pursuit", "prove", task, *how, "--check-timeout", f"{timeout:.0f}"]
        rc, out = await asyncio.to_thread(
            _run, _capped(argv, _memory_max()), root, 2 * timeout + 120
        )
        if rc != 0 and "--predates-because" in out and "--mutate" in how:
            # A task that adds tests for code an earlier task wrote: its
            # witness is a defect in that code, which beagle takes when said.
            argv += ["--predates-because", PREDATES_BECAUSE]
            rc, out = await asyncio.to_thread(
                _run, _capped(argv, _memory_max()), root, 2 * timeout + 120
            )
        tail = out[-PROVE_TAIL_CHARS:]
        verdicts = {m.group(1): m.group(2) for m in _PROVE_VERDICT.finditer(out)}
        if rc == 0 and verdicts.get(task) == "PROVEN":
            return _Proof(proven=True, text=tail)
        if verdicts.get(task) == "NOT PROVEN" and "STILL PASSES" in out:
            # The check passed over the defect: a real answer, not one a
            # different witness should be asked to overturn.
            return _Proof(proven=False, text=tail, weak=True)
        refused.append(tail)
    if not attempts and not refused:
        if not _requires_witness(root):
            return None
        return _Proof(
            proven=False,
            text="The worker gave no WITNESS block, and changed no source file in the "
            "task's scope that could be taken away instead.",
        )
    return _Proof(proven=False, text="\n\n".join(refused))


def _requires_witness(root: Path) -> bool:
    """Whether the pursuit's `[close] require` holds a done close to a witnessed check."""
    try:
        goal = tomllib.loads((root / ".beagle" / GOAL_BASENAME).read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return False
    close = goal.get("close")
    require = close.get("require") if isinstance(close, dict) else None
    # beagle reads any value but "none" as "witness".
    return require is not None and require != "none"


def _commit(task: str, title: str, scope: list[str], root: Path) -> str:
    """Commit what a proven task changed with `pursuit commit`; a line saying what happened.

    Run 11d left six of seven tasks' work uncommitted. Claims are the worker's
    to record; with none, the commit says so rather than not landing at all.
    """
    paths = [rel for rel in _changed_files(root) if _in_scope(rel, scope)]
    if not paths:
        return "Nothing to commit: the task changed no file in its scope."
    if not _git_identity(root):
        return (
            "Not committed: git has no user.name or user.email here. That is the user's "
            "to set; tell them, and do not set one yourself."
        )
    subject = f"{task}: {title}"
    if len(subject) > 72:
        subject = subject[:71].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    argv = ["commit", task, *paths, "--subject", subject]
    rc, out = _pursuit(argv, root)
    if rc != 0 and "--no-claims" in out:
        rc, out = _pursuit([*argv, "--no-claims"], root)
    if rc != 0:
        # beagle puts the index back itself when it refuses after staging.
        return f"Not committed (`pursuit commit` exit {rc}):\n{out[-PROVE_TAIL_CHARS:]}"
    return out.splitlines()[0] if out else f"Committed {len(paths)} file(s)."


def _next_ready(root: Path) -> tuple[int, Any, str]:
    rc, out = _pursuit(["next", "--json"], root)
    return rc, _json_reply(out), out


def _ids(entries: Any) -> list[str]:
    ids = []
    for entry in entries if isinstance(entries, list) else []:
        task = entry.get("id") if isinstance(entry, dict) else entry
        if isinstance(task, str):
            ids.append(task)
    return ids


#: Under `.beagle/`: the known copy of each locked file, and the locks a task
#: asked for, held until it closes done.
LOCKED_DIR = "locked"
PENDING_LOCKS = "locks-pending.json"


def _locked(goal: Path) -> list[str]:
    """The project paths locked so far, as their known copies name them."""
    store = goal.parent / LOCKED_DIR
    try:
        return sorted(str(f.relative_to(store)) for f in store.rglob("*") if f.is_file())
    except OSError:
        return []


def _project_file(root: Path, entry: str) -> Path | None:
    """`entry` as a file under the project and outside `.beagle/`, else None."""
    try:
        target = (root / entry).resolve()
        base = root.resolve()
    except (OSError, ValueError):
        return None
    if base not in target.parents or (base / ".beagle") in (target, *target.parents):
        return None
    return target


def _lock(goal: Path, root: Path, entries: list[str]) -> tuple[list[str], list[str]]:
    """Copy each named file to the locked store; (locked, why the rest were not)."""
    store = goal.parent / LOCKED_DIR
    held = set(_locked(goal))
    locked: list[str] = []
    skipped: list[str] = []
    for entry in entries:
        target = _project_file(root, entry)
        if target is None or not target.is_file():
            skipped.append(f"{entry}: not a file in the project")
            continue
        rel = str(target.relative_to(root.resolve()))
        if rel in held:
            skipped.append(f"{rel}: already locked")
            continue
        copy = store / rel
        try:
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(target.read_bytes())
        except OSError as exc:
            skipped.append(f"{rel}: {exc}")
            continue
        locked.append(rel)
    return locked, skipped


def _restore_locked(goal: Path, root: Path) -> list[str]:
    """Put back every locked file a worker changed or removed; the ones it did."""
    store = goal.parent / LOCKED_DIR
    restored = []
    for rel in _locked(goal):
        target = root / rel
        try:
            known = (store / rel).read_bytes()
            if target.is_file() and target.read_bytes() == known:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(known)
        except OSError:
            continue
        restored.append(rel)
    return restored


def _pending_locks(goal: Path, task: str, add: list[str] | None = None) -> list[str]:
    """The locks `task` asked for, adding `add`; kept until the task closes done."""
    path = goal.parent / PENDING_LOCKS
    try:
        pending = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pending = {}
    if not isinstance(pending, dict):
        pending = {}
    entries = [e for e in pending.get(task) or [] if isinstance(e, str)]
    if add:
        entries += [e for e in add if e not in entries]
        pending[task] = entries
        with contextlib.suppress(OSError):
            path.write_text(json.dumps(pending, indent=1), encoding="utf-8")
    return entries


def _drop_pending_locks(goal: Path, task: str) -> None:
    path = goal.parent / PENDING_LOCKS
    with contextlib.suppress(OSError, ValueError, AttributeError):
        pending = json.loads(path.read_text(encoding="utf-8"))
        if pending.pop(task, None) is not None:
            path.write_text(json.dumps(pending, indent=1), encoding="utf-8")


#: Retries beagle allows a task its own check blocked.
MAX_RETRIES = 3


def _blocked_tasks(root: Path) -> dict[str, dict[str, Any]]:
    """The pursuit's blocked tasks by id, each its `tree --json` node."""
    rc, out = _pursuit(["tree", "--json"], root)
    tree = _json_reply(out) if rc == 0 else None
    nodes = tree.get("nodes") if isinstance(tree, dict) else None
    if not isinstance(nodes, list):
        return {}
    return {
        str(node["id"]): node
        for node in nodes
        if isinstance(node, dict) and node.get("status") == "blocked" and node.get("id")
    }


def _blocked_routes(blocked: Mapping[str, Mapping[str, Any]]) -> str:
    """What the driver can do about each blocked task, for when nothing is ready."""
    listed = "\n".join(f"- {task} — {node.get('title', '')}" for task, node in blocked.items())
    return (
        f"Blocked, and holding up what comes after:\n{listed}\n\n"
        "For each, call pursuit_step with its task and:\n"
        "- notes saying what to fix, to rework it on the same route and check; or\n"
        "- new_route=true and notes saying what to do differently, for a route that "
        "resisted. A done_when that could not judge the work goes with it: the new route "
        "is checked by that instead."
    )


def _retryable(record: Mapping[str, Any], done_when: str, arguments: Mapping[str, Any]) -> bool:
    """Whether a blocked task is reworked under its own check, not spawned anew.

    beagle retries only a block the task's own check made, three times; a new
    check is a new route, since the one bound at open cannot change.
    """
    bound = str(record.get("done_when") or "").strip()
    return (
        arguments.get("new_route") is not True
        and bool(record.get("check_refused"))
        and int(record.get("retries") or 0) < MAX_RETRIES
        and (not done_when or done_when == bound)
        and _check_problem(bound) is None
    )


def _spawn(
    task: str, record: Mapping[str, Any], notes: str, done_when: str, root: Path
) -> tuple[str | None, str]:
    """Spawn a successor to `task`: its id, or None, and what beagle said."""
    bound = str(record.get("done_when") or "").strip()
    reason = str(record.get("reason") or "").strip() or "the route did not get the check to pass"
    argv = ["spawn", task, "--approach-delta", notes[:500], "--reason", reason[:500]]
    if len(notes) > 500:
        argv += ["--body", notes]
    if record.get("title"):
        argv += ["--title", str(record["title"])[:200]]
    if done_when and done_when != bound:
        argv.append("--check-defect")
    rc, out = _pursuit(argv, root)
    found = re.search(rf"{re.escape(task)} superseded by ({_TASK_ID.pattern})", out)
    if rc != 0 or found is None:
        return None, out
    return found.group(1), out


#: Where beagle's brief starts and ends the steps that commit the work.
_COMMIT_STEPS_START = "Before you report back, commit"
_COMMIT_STEPS_END = "name only the files you changed."
#: What a worker is told in their place.
NO_COMMIT_NOTE = "Do not commit or claim; pursuit_step commits on close."


def _without_commit_steps(brief: str) -> str:
    """beagle's brief with its commit and claim steps swapped for `NO_COMMIT_NOTE`.

    pursuit_step commits a task's work itself before the close, and the worker
    guard refuses `beagle pursuit commit` and `claim`: in run R02 the steps
    drew about 20 refusals, then raw `git add`/`git commit`, and a sub-agent
    spawned to record claims.
    """
    start = brief.find(_COMMIT_STEPS_START)
    if start == -1:
        return brief
    end = brief.find(_COMMIT_STEPS_END, start)
    rest = "" if end == -1 else brief[end + len(_COMMIT_STEPS_END) :]
    return f"{brief[:start]}{NO_COMMIT_NOTE}{rest}"


#: The log a worker's test run is redirected to when beagle's habit names none.
_DEFAULT_TEST_LOG = "/tmp/tau-worker-test.log"
_HABIT_LOG = re.compile(r">\s*(\S+\.log)\b")
_SHOW_ASIDE = re.compile(r"[;,]?\s*`beagle pursuit show[^`]*` has the whole record")


def _without_beagle_habits(brief: str) -> str:
    """beagle's brief without the lines that tell a worker to run `beagle`.

    The worker guard refuses every `beagle` command. Run R06: W2 and W4 ran the
    "Working habits" line's `RUN_CONTAINED_FOREGROUND=1 beagle contain run heavy
    -- …` and were refused. That line is said again with a plain capped,
    redirected command; the standing-checks line (`beagle pursuit recheck`) is
    dropped, and the `beagle pursuit show` aside is cut.
    """
    lines: list[str] = []
    for line in brief.splitlines(keepends=True):
        if "beagle contain run" in line:
            match = _HABIT_LOG.search(line)
            log = match.group(1) if match else _DEFAULT_TEST_LOG
            bullet = "- " if line.lstrip().startswith("- ") else ""
            ending = "\n" if line.endswith("\n") else ""
            lines.append(
                f"{bullet}Run every test, build and check capped and redirected, as a plain "
                f'command: `timeout 540 <cmd> > {log} 2>&1; echo "exit $?"` (e.g. '
                f"`timeout 540 python3 -m pytest -q tests/ > {log} 2>&1; "
                f'echo "exit $?"`), then read the tail of {log}.{ending}'
            )
        elif "beagle pursuit recheck" in line:
            continue
        else:
            lines.append(_SHOW_ASIDE.sub("", line))
    return "".join(lines)


def _blocked_brief(task: str, record: Mapping[str, Any]) -> str:
    """A worker's brief for a blocked task, which `beagle pursuit brief` refuses."""
    lines = [f"Task {task}: {record.get('title', '')}"]
    for label, key in (("Why", "intent"), ("Done means", "criteria")):
        value = str(record.get(key) or "").strip()
        if value:
            lines.append(f"{label}: {value}")
    lines.append(f"Check (must exit 0): `{record.get('done_when', '')}`")
    scope = _strings(record.get("scope"))
    if scope:
        lines.append(f"Scope: {', '.join(scope)}")
    reason = str(record.get("reason") or record.get("check_refused") or "").strip()
    lines.append(
        f"\nAn earlier attempt was closed as done, but the check refused it ({reason}). "
        "Find what is still missing and finish the work so the check passes."
    )
    return "\n".join(lines)


#: What the auditing sub-agent is told beyond beagle's audit brief.
AUDIT_NOTE = (
    "\n\nRead the work and the checks; change nothing. Do not run `beagle pursuit "
    "audit`: the session that sent you records what you report. End your report with "
    "one line: SOUND, or DEFECTS and how many."
)
#: Most of the auditor's report beagle keeps with the audit.
AUDIT_NOTE_CHARS = 2_000


async def _audit(
    root: Path, signal: ToolCancellationToken | None, on_update: ToolUpdateCallback | None
) -> str:
    """Run a due audit by a sub-agent and record its verdict; what the driver is told.

    While one is due beagle opens nothing, and its refusal names bash verbs: in
    run 9 the driver recorded a verdict by hand without reading anything, then
    lost the thread. The auditor is a fresh sub-agent, which closed none of
    the tasks it reads.
    """
    rc, brief = _pursuit(["audit"], root)
    if rc != 0:
        return (
            f"pursuit_step: an audit is due, but `beagle pursuit audit` failed (exit {rc}):"
            f"\n{brief}"
        )
    brief = brief.split("\nFor the driver:")[0].rstrip()
    if on_update is not None:
        with contextlib.suppress(Exception):
            on_update(_step_result("An audit is due: a sub-agent is reading the closes."))
    run = await _run_worker(
        brief + AUDIT_NOTE,
        root,
        _worker_model(None),
        _worker_provider(None),
        DEFAULT_DISPATCH_TIMEOUT,
        signal,
    )
    if run.problem is not None or run.report.startswith(NO_REPORT):
        why = run.problem or "it wrote no report"
        return (
            f"pursuit_step: an audit is due, and nothing opens until one is kept, but its "
            f"sub-agent did not finish — {why}\n\nCall pursuit_step again to send it again."
        )
    lines = [line for line in run.report.splitlines() if line.strip()]
    last = lines[-1].upper() if lines else ""
    sound = "SOUND" in last and "DEFECT" not in last
    verdict = "defects" if not sound and re.search(r"\b(DEFECTS?|SHORT)\b", run.report) else "sound"
    rc, kept = _pursuit(
        ["audit", "--record", "--verdict", verdict, "--note", run.report[:AUDIT_NOTE_CHARS]],
        root,
    )
    if rc != 0:
        return (
            f"pursuit_step: an audit is due; its sub-agent reported, but `beagle pursuit "
            f"audit --record` refused (exit {rc}):\n{kept}\n\nReport:\n{run.shown_report}"
        )
    then = (
        "Each defect becomes work before more is opened: for each task the report finds "
        "SHORT, add what is missing with pursuit_plan, or rework the task with "
        "pursuit_step and notes saying what to fix. Then call pursuit_step with no "
        "arguments."
        if verdict == "defects"
        else "Next: call pursuit_step with no arguments for the next task."
    )
    return (
        f"An audit came due, and a sub-agent read the closes since the last one: "
        f"{verdict}.\n\n{kept}\n\nAuditor's report:\n{run.shown_report}\n\n{then}"
    )


def _abandon(task: str, why: str, root: Path, goal: Path) -> str:
    """Close `task` as abandoned and release what waited on it; what happened."""
    argv = ["close", task, "--outcome", "abandoned", "--reason", why[:500]]
    rc, out = _pursuit(argv, root)
    if rc != 0:
        return (
            f"pursuit_step: `beagle pursuit close {task} --outcome abandoned` refused "
            f"(exit {rc}):\n{out}"
        )
    _drop_pending_locks(goal, task)
    _forget_task(root, task)
    released = _release_waiters(task, why, root)
    freed = f"\nNo longer waiting on it: {', '.join(released)}." if released else ""
    return (
        f"{out.splitlines()[0] if out else task + ' abandoned'}{freed}\n\n"
        f"{_tree(root)}\n\nNext: call pursuit_step with no arguments for the next task."
    )


#: Open tasks whose passing check `prove` could not show to refuse, by (project
#: root, task). A further step on the task runs no worker, whatever check or
#: scope it is sent with: run R04's driver got past a (check, scope) key by
#: changing the scope. A new route or a plan of the task clears it.
_UNPROVEN: set[tuple[str, str]] = set()

#: Step results that left a task not done (stays open or blocked, not run,
#: unproven), by (project root, task), and the scope it was worked in. Run
#: R04 sent 14 such steps at one task, none of which offered another way.
_NOT_DONE: dict[tuple[str, str], int] = {}
_NOT_DONE_SCOPE: dict[tuple[str, str], tuple[str, ...]] = {}

#: Not-done results after which a further step on the task dispatches no worker.
ESCALATE_AFTER = 3

#: Not-done results after which the driver may not read the task's files.
DRIVER_READS_UNTIL = 2


def _carried_criteria(predecessor: str, root: Path) -> str:
    """The criteria of the task a successor follows, which its own must keep."""
    rc, out = _pursuit(["show", predecessor], root)
    record = _json_reply(out) if rc == 0 else None
    return str(record.get("criteria") or "").strip() if isinstance(record, dict) else ""


def _already_passes(check: str) -> str:
    """Why a check that passes before any work is not bound."""
    return (
        f"`{check}` already passes, before any work, so it cannot tell this task's work "
        "from none. Bind a check that fails now: name a new test file for what this task "
        "adds, e.g. `python3 -m pytest -q tests/test_<this task>.py`, put it in scope, and "
        "say in the notes what it should test. It fails until the sub-agent writes it; do "
        "not write it yourself. If the work is there already, bind the goal criterion's "
        "test, which imports and runs the code. " + ABANDON_HINT
    )


def _escalation(task: str, count: int) -> str:
    """The fixed refusal of a step on a task `count` steps have left not done."""
    return (
        f"pursuit_step: {task} not run: {count} steps on it have left it not done, and "
        "another sub-agent on the same task, however its scope or notes are put, is "
        "how run R04 spent 14 steps on one. Choose one:\n"
        f'- pursuit_plan task="{task}" with two or more parts, to split it into smaller '
        "tasks (a plan of one part is refused: the task is already one step);\n"
        f'- pursuit_step task="{task}", new_route=true, with a rewritten done_when and '
        "notes saying what the new route does differently (the criteria stay);\n"
        "- stop, and tell the user what blocks it."
    )


def _forget_task(root: Path, task: str) -> None:
    """Drop what the step tool remembers of `task`: closed, re-routed or planned."""
    key = (str(root), task)
    _UNPROVEN.discard(key)
    _NOT_DONE.pop(key, None)
    _NOT_DONE_SCOPE.pop(key, None)


def _not_done(root: Path, task: str, scope: list[str], text: str) -> AgentToolResult:
    """Count a result that left `task` not done, and return it."""
    key = (str(root), task)
    count = _NOT_DONE[key] = _NOT_DONE.get(key, 0) + 1
    if scope:
        _NOT_DONE_SCOPE[key] = tuple(scope)
    if count >= ESCALATE_AFTER:
        text += "\n\n" + _escalation(task, count).replace(
            f"pursuit_step: {task} not run: ", "The next step on it runs no sub-agent: ", 1
        )
    elif count >= DRIVER_READS_UNTIL and scope:
        text += (
            f"\n\nThe files in {task}'s scope are the sub-agent's while it is open: "
            "reading them yourself is refused. Say what to fix in the step's notes, "
            f'or give it a new route (pursuit_step task="{task}", new_route=true).'
        )
    return _step_result(text)


def _held_scope(target: Path, root: Path) -> tuple[str, str, int] | None:
    """The open task, its scope entry and not-done count, holding `target` from the driver."""
    root = _resolved(root)
    for (where, task), count in _NOT_DONE.items():
        if count < DRIVER_READS_UNTIL or _resolved(Path(where)) != root:
            continue
        for entry in _NOT_DONE_SCOPE.get((where, task), ()):
            text = entry.strip().rstrip("/")
            if not text or text == ".":
                continue
            if _GLOB_CHARS & set(text):
                if fnmatch.fnmatch(str(target), str(root / text)):
                    return task, entry, count
                continue
            path = _resolved(root / text)
            if target == path or path in target.parents:
                return task, entry, count
    return None


#: Commands that print a file's text, and the options of each that take a value.
_FILE_READERS: dict[str, frozenset[str]] = {
    "cat": frozenset(),
    "head": frozenset({"-n", "-c"}),
    "tail": frozenset({"-n", "-c"}),
    "sed": frozenset({"-e", "-f"}),
    "grep": frozenset({"-e", "-f", "-m", "-A", "-B", "-C", "--include", "--exclude"}),
}


def _bash_read_targets(command: str, cwd: Path) -> list[Path]:
    """The files a `cat`, `head`, `tail`, `sed -n` or `grep` in `command` reads."""
    tokens = _shell_tokens(command) or []
    targets: list[Path] = []
    argv: list[str] = []
    for token in [*tokens, ";"]:
        if not _is_operator(token):
            argv.append(token)
            continue
        while argv and argv[0] in _WRAPPERS:
            argv = argv[1:]
        name = Path(argv[0]).name if argv else ""
        if name in _FILE_READERS and (name != "sed" or "-n" in argv[1:]):
            args = argv[1:]
            files = _positional(args, _FILE_READERS[name])
            if name in ("sed", "grep") and not any(a in ("-e", "-f") for a in args):
                files = files[1:]  # the script or the pattern
            targets += [_resolved(cwd / Path(f).expanduser()) for f in files]
        argv = []
    return targets


def make_step_tool() -> Any:
    """Build `pursuit_step`: one task, opened, done by a sub-agent, checked and closed.

    A pursuit task is `next`, `open`, a dispatch, then `close`, with rules at
    every step that the driver text explains at length. Here the model brings
    only the judgement — the criteria and the check, written before the work
    — and the rest is mechanical: the brief comes from beagle, a nested `tau
    -p` step-executor does the work, the check runs before the close (a done
    close the check refuses would block the task for good), and the close
    carries the worker's measured spend.
    """

    async def _execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id
        root, goal = _project_root()
        if goal is None:
            return _step_result("pursuit_step: no pursuit here yet; call pursuit_found first.")
        rc, ready, raw = _next_ready(root)
        if rc == 4 or rc not in (0, 3) or not isinstance(ready, dict):
            return _step_result(
                f"pursuit_step: beagle cannot hand out work now (exit {rc}):\n{raw}\n\n"
                "Stop here and tell the user what it said."
            )
        open_ids = _ids(ready.get("open"))
        ready_ids = _ids(ready.get("ready"))
        blocked = _blocked_tasks(root)
        nodes = _tree_nodes(root)
        left = _unfinished(nodes)
        cycle = _wait_cycle(nodes)
        if cycle:
            after = _cycle_break(cycle, nodes)
        elif blocked:
            after = _blocked_routes(blocked)
        elif left:
            # Run R02's driver was offered "tell the user the pursuit is done"
            # here with the root stalled and four milestones abandoned.
            after = (
                "The pursuit is NOT done: these tasks are not done, and nothing took "
                "their work on:\n" + "\n".join(left) + "\n\nDo not tell the user it is "
                "done. A task that waits on another starts once that one is done. Add "
                "missing work with pursuit_plan, or give a task a new route with "
                'pursuit_step task="<id>", new_route=true and notes.'
            )
        else:
            after = (
                "If every criterion of the goal now holds, tell the user the pursuit "
                "is done. If work remains, add it with pursuit_plan."
            )
        nothing_ready = f"Nothing is ready to work.\n\n{_tree(root)}\n\n{after}"
        task = str(arguments.get("task") or "").strip()
        abandon = str(arguments.get("abandon") or "").strip()
        if abandon:
            if not task:
                return _step_result("pursuit_step: abandon names the task to drop; pass task too.")
            refused = _abandon_problem(task, abandon, nodes)
            if refused is not None:
                return _step_result(refused)
            return _step_result(_abandon(task, abandon, root, goal))
        if ready.get("audit_due"):
            return _step_result(await _audit(root, signal, on_update))
        if not task:
            task = (open_ids or ready_ids or [""])[0]
            if not task:
                return _step_result(nothing_ready)
        elif task not in open_ids and task not in ready_ids and task not in blocked:
            # A container (done when its parts are) or a task still waiting on
            # one: opening it is refused, and offering to is where a model
            # that finished the leaves goes next.
            heir = _heir(task, nodes)
            if heir != task:
                # Run R06 told its driver a superseded T0002 was "a container".
                if heir in open_ids or heir in ready_ids:
                    return _step_result(
                        f"{task} was superseded by {heir}, which took its work on: work "
                        f'{heir} instead, with pursuit_step task="{heir}".'
                    )
                return _step_result(
                    f"{task} was superseded by {heir}, which took its work on, and {heir} "
                    f"is not ready either. {nothing_ready}"
                )
            if open_ids or ready_ids:
                workable = ", ".join(open_ids + ready_ids)
                return _step_result(
                    f"{task} is not a task to work now: it is a container, done when its "
                    f"parts are, or it waits on another task. Workable now: {workable}. "
                    "Call pursuit_step with no arguments."
                )
            return _step_result(f"{task} is not a task to work now. {nothing_ready}")

        rc, out = _pursuit(["show", task], root)
        record = _json_reply(out) if rc == 0 else None
        if not isinstance(record, dict):
            return _step_result(f"pursuit_step: cannot read {task} (exit {rc}):\n{out}")
        title = str(record.get("title") or "")
        if record.get("status") != "open" and _setup_milestone([title]) is not None:
            # Founding set the pursuit up, so a set-up task has no work in the
            # project and no check that can pass: run 11's driver spent its
            # first turns writing checks over .beagle/ for one. It is dropped
            # here, since a hint to abandon it is one a small model ignores.
            return _step_result(
                f"{task} ({title}) is setting the pursuit up, which pursuit_found already "
                f"did, so it is not worked.\n"
                + _abandon(task, "founding set the pursuit up", root, goal)
            )
        criteria = str(arguments.get("criteria") or "").strip()
        done_when = str(arguments.get("done_when") or "").strip()
        scope = _strings(arguments.get("scope"))
        notes = str(arguments.get("notes") or "").strip()
        opened = route = ""
        retrying = False
        status = record.get("status")
        if status == "blocked" or arguments.get("new_route") is True:
            if status == "blocked" and _retryable(record, done_when, arguments):
                retrying = True
            else:
                # A route that resisted, or a check that could not judge the
                # work: a successor, with the same end and a new way there.
                if not notes:
                    return _step_result(
                        f"pursuit_step: a new route for {task} needs notes saying how it "
                        "differs from the one that failed: what the sub-agent will do "
                        "differently, specifically. Call pursuit_step again with them."
                    )
                old_check = str(record.get("done_when") or "").strip()
                problem = _check_problem(done_when or old_check)
                if problem is not None:
                    if not done_when:
                        problem = f"its check `{old_check}` cannot judge the work: {problem}"
                    return _step_result(f"pursuit_step: no new route for {task} — {problem}")
                old_criteria = str(record.get("criteria") or "").strip()
                if criteria and old_criteria and criteria != old_criteria:
                    return _step_result(
                        f"pursuit_step: no new route for {task} — a new route changes how "
                        f"the work is done or checked, not what it is for, so it keeps the "
                        f"criteria: {old_criteria!r}. If the end itself is wrong, that is "
                        "the user's to change: ask them. Call pursuit_step again without "
                        "criteria."
                    )
                # Checked before the spawn, which supersedes the task for good:
                # run R06 spawned T0008, then refused to open it on a check that
                # already passed, and left a successor with no criteria.
                scoped = _scope_problem(scope or _strings(record.get("scope")))
                if scoped is not None:
                    return _step_result(f"pursuit_step: no new route for {task} — {scoped}")
                new_check = done_when or old_check
                if (await _run_check(new_check, root, DEFAULT_CHECK_TIMEOUT))[0] == 0:
                    return _step_result(
                        f"pursuit_step: no new route for {task}, which stays as it is — "
                        + _already_passes(new_check)
                    )
                successor, spawned = _spawn(task, record, notes, done_when, root)
                if successor is None:
                    return _step_result(
                        f"pursuit_step: `beagle pursuit spawn {task}` refused:\n{spawned}\n\n"
                        "Say more specifically in notes how this route differs."
                    )
                route = f"{spawned}\n\n"
                _forget_task(root, task)
                task = successor
                criteria = old_criteria or criteria
                done_when = done_when or old_check
                scope = scope or _strings(record.get("scope"))
                rc, out = _pursuit(["show", task], root)
                record = _json_reply(out) if rc == 0 else None
                if not isinstance(record, dict):
                    return _step_result(f"pursuit_step: cannot read {task} (exit {rc}):\n{out}")
        tried = _NOT_DONE.get((str(root), task), 0)
        if not route and tried >= ESCALATE_AFTER:
            return _step_result(_escalation(task, tried))
        if not retrying and task not in open_ids and record.get("status") != "open":
            predecessor = str(record.get("sibling_of") or "").strip()
            carried = _carried_criteria(predecessor, root) if predecessor and not route else ""
            if carried:
                # beagle refuses a successor whose criteria drift from its
                # predecessor's: run R06's driver wrote new ones three times.
                if criteria and criteria != carried:
                    route += (
                        f"Criteria kept from {predecessor}, which {task} succeeds; a new "
                        f"route does not change what the work is for: {carried!r}\n\n"
                    )
                criteria = carried
            if not criteria or not done_when:
                why = str(record.get("intent") or "").strip()
                return _step_result(
                    f"Next task: {task} — {title}\n"
                    + (f"Why: {why}\n" if why else "")
                    + "\nCall pursuit_step again with:\n"
                    f'  task: "{task}"\n'
                    + (
                        f"  (no criteria: they are carried over from {predecessor}, the "
                        f"task it succeeds: {carried!r})\n"
                        if carried
                        else "  criteria: what will be true when it is done\n"
                    )
                    + "  done_when: ONE command that exits 0 only then, e.g. `python3 -m "
                    "pytest -q tests/test_x.py`. It is split into words and run without a "
                    "shell: no prose, no &&, |, > or $(...). It should fail now.\n"
                    "  scope: the paths it will touch\n"
                    "  notes: where to start, what to leave alone\n"
                    "A sub-agent does the work and the check decides. If you cannot write "
                    "the criteria yet, the task is too big: split it with pursuit_plan."
                )
            prose = _check_problem(done_when)
            if prose is not None:
                return _step_result(f"pursuit_step: {task} not opened — {prose}")
            scoped = _scope_problem(scope)
            if scoped is not None:
                return _step_result(f"pursuit_step: {task} not opened — {scoped}")
            # A check bound once it already passes closes the task on no work:
            # run 9 bound `cat docs/design.md` and a test an earlier task had
            # made pass.
            if (await _run_check(done_when, root, DEFAULT_CHECK_TIMEOUT))[0] == 0:
                return _step_result(
                    f"pursuit_step: {task} not opened — " + _already_passes(done_when)
                )
            argv = ["open", task, "--criteria", criteria, "--done-when", done_when]
            if scope:
                argv += ["--scope", *scope]
            budget = str(arguments.get("budget") or "").strip()
            if budget:
                argv += ["--budget", budget]
            rc, opened = _pursuit(argv, root)
            if rc != 0:
                return _step_result(
                    f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{opened}"
                )
            rc, out = _pursuit(["show", task], root)
            record = _json_reply(out) if rc == 0 else record
        elif done_when and done_when != str(record.get("done_when") or "").strip():
            # Open already, with a check the model now writes differently: the
            # bound one could not judge the work (prose, a usage error), and
            # repeating the old one forever is the loop this breaks.
            prose = _check_problem(done_when)
            if prose is not None:
                return _step_result(f"pursuit_step: {task}'s check not changed — {prose}")
            argv = ["amend", task, "--done-when", done_when]
            if criteria and criteria != str(record.get("criteria") or "").strip():
                argv += ["--criteria", criteria]
            argv += ["--reason", "the bound check could not judge the work; rewritten"]
            rc, amended = _pursuit(argv, root)
            if rc != 0:
                return _step_result(
                    f"pursuit_step: `beagle pursuit amend` refused the new check (exit {rc}):"
                    f"\n{amended}"
                )
            opened = amended
            record = {**record, "done_when": done_when}
        check = str(record.get("done_when") or done_when).strip()
        prose = _check_problem(check) if check else None
        if prose is not None:
            # Bound before this guard, or by hand: no worker can make it pass.
            return _step_result(
                f"pursuit_step: {task} is open, but its bound check `{check}` cannot pass "
                f"whatever the work does — {prose} Pass the corrected done_when with "
                f'task="{task}"; it is amended.'
            )

        if retrying:
            # beagle briefs only an open task; a blocked one is briefed from its record.
            brief = _blocked_brief(task, record)
        else:
            rc, brief = _pursuit(["brief", task], root)
            if rc != 0:
                return _step_result(f"pursuit_step: `beagle pursuit brief {task}` failed:\n{brief}")
            brief = _without_beagle_habits(_without_commit_steps(brief))
        references = _references_brief(root)
        if references:
            brief = f"{brief}\n\n{references}"
        if notes:
            brief = f"{brief}\n\nFrom the driver (who has not read the reference):\n{notes}"
        brief += "\n\n" + NO_BEAGLE_NOTE
        locks = _pending_locks(goal, task, _strings(arguments.get("locks")))
        locked = _locked(goal)
        if locked:
            brief += (
                "\n\nLocked files: known-answer cases an earlier task wrote from the "
                "reference. Read them; do not edit them. Any change is undone before the "
                "check runs, so make the code pass them as they are:\n"
                + "\n".join(f"- {rel}" for rel in locked)
            )
        try:
            attempts = max(1, int(arguments.get("attempts") or DEFAULT_STEP_ATTEMPTS))
        except (TypeError, ValueError):
            attempts = DEFAULT_STEP_ATTEMPTS
        timeout = _worker_timeout(arguments.get("timeout"))[0]
        check_timeout = float(record.get("check_timeout") or DEFAULT_CHECK_TIMEOUT)

        spent: int | None = None
        report = shown = ""
        verdict: tuple[int, str] = (1, "")
        model = _worker_model(None)
        provider = _worker_provider(None)
        retry_note = ""
        restored: set[str] = set()
        attempt = 0
        proof: _Proof | None = None
        scope = scope or _strings(record.get("scope"))
        unproven_key = (str(root), task)
        tests_only = _only_data_and_tests(scope)
        if unproven_key in _UNPROVEN:
            return _not_done(
                root,
                task,
                scope,
                f"pursuit_step: {task} not run: this check already passes and cannot be "
                f"shown to refuse, since no defect could be put back into a file in its "
                f"scope ({', '.join(scope) or 'none'}). Another sub-agent would change "
                "nothing, whatever check or scope this task is sent with. "
                + (
                    TESTS_ONLY_PROOF_NOTE
                    + " Give it a new route whose done_when runs that file's test and "
                    "whose scope names the data file"
                    if tests_only
                    else "Give it a new route whose done_when imports the code this task "
                    "tests and runs it (e.g. `python3 -m pytest -q "
                    "tests/test_<this task>.py`, a test that imports the module), with "
                    "that code's source file in scope"
                )
                + f': pursuit_step task="{task}", new_route=true, the new done_when and '
                "notes; or split it with pursuit_plan.",
            )
        brief += "\n\n" + WITNESS_NOTE
        if retrying:
            # The work may have been done since, under another task.
            verdict = await _run_check(check, root, check_timeout)
            if verdict[0] == 0:
                proof = await _prove(task, "", scope, root, check_timeout)
        for attempt in range(1, attempts + 1):
            if verdict[0] == 0 and (proof is None or proof.proven):
                break
            if on_update is not None:
                with contextlib.suppress(Exception):
                    on_update(_step_result(f"{task}: sub-agent attempt {attempt} of {attempts}"))
            run = await _run_worker(
                brief + retry_note, root, model, provider, timeout, signal, task, scope
            )
            undone = _restore_locked(goal, root)
            restored.update(undone)
            if run.spent is not None:
                spent = (spent or 0) + run.spent
            if run.problem is not None:
                return _not_done(
                    root,
                    task,
                    scope,
                    f"pursuit_step: {task} stays open — {run.problem}\n\n"
                    f'Call pursuit_step with task="{task}" to send it again.',
                )
            report, shown = run.report, run.shown_report
            if not check:
                verdict = (0, "")
                break
            verdict = await _run_check(check, root, check_timeout)
            if verdict[0] == 0:
                proof = await _prove(task, report, scope, root, check_timeout)
                if proof is None or proof.proven:
                    break
                if not proof.weak:
                    # No defect could be put back: run R02 sent a second worker
                    # after every such verdict, and six identical steps more.
                    _UNPROVEN.add(unproven_key)
                    break
                retry_note = (
                    "\n\nAn earlier attempt reported back and the check passes, but `prove` "
                    "could not show the check catches a defect in the work:\n"
                    f"{proof.text}\n"
                    + (
                        "The check passed with the defect put back, so it does not test "
                        "what this task built. Make the task's tests catch such a defect "
                        "(in the test file, not by changing the check), then give a new "
                        "WITNESS block."
                        if proof.weak
                        else "Give a WITNESS block whose NEEDLE occurs exactly once in a "
                        "source file you changed (not a test)."
                    )
                )
                continue
            retry_note = (
                f"\n\nAn earlier attempt reported back, but the check still fails (exit "
                f"{verdict[0]}). Its output ends:\n{verdict[1][-CHECK_TAIL_CHARS:]}\n"
                "Fix the work, not the check."
            )
            if undone:
                retry_note += (
                    f" It also changed locked files ({', '.join(undone)}); they were put "
                    "back. Make the code pass them as they are."
                )
        undid = (
            f"The sub-agent changed locked files ({', '.join(sorted(restored))}); they "
            "were put back before the check.\n\n"
            if restored
            else ""
        )

        if check and verdict[0] != 0:
            state = "stays blocked" if retrying else "stays open"
            fix_check = (
                "pass a corrected done_when with notes saying what this route does "
                "differently; a new route is spawned with it."
                if retrying
                else "pass a corrected done_when too; it is amended."
            )
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check still fails after {attempts} "
                f"sub-agent run(s), so the task {state}.\n\n`{check}` exit {verdict[0]}:\n"
                f"{verdict[1][-CHECK_TAIL_CHARS:]}\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying what to fix. If '
                "the check itself is wrong — it says how it was called (a usage error, a "
                "file it treats as an argument) rather than what is missing — "
                f"{fix_check} If this route is wrong, pursuit_step with "
                f'task="{task}", new_route=true and notes saying what to do instead.',
            )
        if proof is not None and not proof.proven:
            state = "stays blocked" if retrying else "stays open"
            why = (
                "the check passes even with a defect put back into the work, so it does "
                "not test what this task built"
                if proof.weak
                else "no defect could be put back to show the check can fail"
            )
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but {why}; the task "
                f"{state}, since a done close needs a check shown to refuse.\n\n"
                f"`prove` said:\n{proof.text}\n\nLast report:\n{shown}\n\n"
                + (
                    f'Next: pursuit_step with task="{task}" and notes saying what to '
                    f"fix. {TESTS_ONLY_PROOF_NOTE}"
                    if tests_only and proof.weak
                    else f'Next: pursuit_step with task="{task}" and a done_when that runs '
                    "a test of the behaviour itself, e.g. `python3 -m pytest -q "
                    "tests/test_<this task>.py`, with notes saying what that test must "
                    "check. A bare import or file-exists check cannot be shown to refuse."
                    if proof.weak
                    else f'Next: a new route, pursuit_step with task="{task}", '
                    "new_route=true, notes and "
                    + (
                        f"a done_when that runs that file's test. {TESTS_ONLY_PROOF_NOTE}"
                        if tests_only
                        else "a done_when that runs a test of the behaviour itself, e.g. "
                        "`python3 -m pytest -q tests/test_<this task>.py`. The test must "
                        "import the code this task tests, and that code's source file "
                        "must be in scope."
                    )
                    + " Another step on this task without a new route runs no sub-agent."
                ),
            )
        changed = [
            rel for rel in _changed_files(root) if _in_scope(rel, scope) and (root / rel).is_file()
        ]
        misplaced = _implementation_in_tests(root, changed)
        if misplaced:
            state = "stays blocked" if retrying else "stays open"
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but the task {state}: "
                "implementation belongs in the module the test imports, not the test "
                "file. A test file holds `test_` functions, `_` helpers and pytest "
                "fixtures; it defines:\n"
                + "\n".join(f"- {where}" for where in misplaced)
                + f"\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying to move these '
                "out of the test file (into the module the test imports, under a task "
                "whose scope holds it) or delete them.",
            )
        if not locks and _only_data_and_tests(changed):
            # Run R04: the driver passed no locks for its known-answers task.
            locks = changed
        # Committed while the task is still open, as beagle has a worker do:
        # the close's sweep then finds the work in history, not in the tree.
        committed = _commit(task, title, scope, root)
        if retrying:
            because = (
                f"a sub-agent reworked it ({attempt} run(s)) and the check now passes"
                if attempt
                else "the check passes now, on work done since it refused"
            )
            argv = ["retry", task, "--because", because]
        else:
            body = report[:CLOSE_BODY_CHARS] or "-"
            argv = ["close", task, "--outcome", "done", "--body", body]
        if spent is not None:
            argv += ["--spent", str(spent)]
        elif retrying:
            argv += ["--spent", "0", "--spent-because", "no sub-agent ran: " + because]
        rc, closed = _pursuit(argv, root, timeout=check_timeout + 60)
        if rc != 0 and spent is not None and "--spent-because" in closed:
            # An overrun of the task's budget: allowed, but beagle wants it said.
            because = (
                f"measured, not estimated: the peak context of each of the "
                f"{attempt} sub-agent run(s) it took, summed"
            )
            rc, closed = _pursuit(
                [*argv, "--spent-because", because], root, timeout=check_timeout + 60
            )
        verb = "retry" if retrying else "close"
        state = "closed done" if rc == 0 else f"{verb} exited {rc}"
        if rc == 0:
            _forget_task(root, task)
        lock_note = ""
        if rc == 0 and locks:
            now, skipped = _lock(goal, root, locks)
            _drop_pending_locks(goal, task)
            if now:
                lock_note += (
                    f"Locked: {', '.join(now)}. No later sub-agent can change them; make "
                    "the later tasks' done_when run them.\n\n"
                )
            if skipped:
                lock_note += f"Not locked: {'; '.join(skipped)}.\n\n"
        return _step_result(
            f"{route}{task} — {title}: {state}.\n\n{committed}\n\n{closed}\n\n"
            f"{undid}{lock_note}"
            f"Sub-agent report:\n{shown}\n\n"
            "Next: call pursuit_step with no arguments for the next task."
        )

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        result = await _execute(tool_call_id, arguments, signal, on_update)
        return _with_note(result, _worker_timeout(arguments.get("timeout"))[1])

    return execute


#: Caches a tool run leaves in the project; clearing one changes no work.
_CACHE_DIRS = frozenset({"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"})
#: `git` subcommands that change what the project's history holds.
_GIT_CHANGES = frozenset(
    {"add", "commit", "mv", "rm", "apply", "am", "cherry-pick", "merge", "revert", "stage"}
)
#: Formatters that rewrite files, and the flag that makes a linter one.
_FORMATTERS = frozenset({"black", "isort", "autopep8", "yapf", "prettier"})
#: Interpreters a driver writes files through with an inline script.
_INTERPRETERS = ("python", "node", "perl", "ruby")
#: What an inline script that writes a file says.
_SCRIPT_WRITE = re.compile(
    r"""open\([^)]*['"][wax]b?\+?['"]|\.write_(?:text|bytes)\(|shutil\.(?:copy|move|rmtree)"""
    r"""|os\.(?:remove|rename|replace|unlink)\(|\.unlink\(|writeFileSync"""
)


def _driver_change(argv: list[str]) -> str | None:
    """What one simple command changes in the project that a write target misses."""
    if argv[:2] == ["uv", "run"]:
        argv = argv[2:]
        while argv and argv[0].startswith("-"):
            argv = argv[1:]
    if not argv:
        return None
    name = Path(argv[0]).name
    if name.startswith("python") and argv[1:2] == ["-m"] and len(argv) > 2:
        name, argv = argv[2], argv[2:]
    if name == "git":
        args = _git_args(argv)
        return f"git {args[0]}" if args and args[0] in _GIT_CHANGES else None
    if name == "ruff" and "--fix" in argv and "format" not in argv:
        # Run R02 quoted `ruff check src --fix` as `ruff check src`, beside
        # "`ruff check` is fine": the flag that makes it a write must be named.
        return " ".join(argv)
    if name in _FORMATTERS or (name == "ruff" and "format" in argv):
        return " ".join(argv[:3])
    if name.startswith(_INTERPRETERS):
        return name
    return None


def _driver_bash_change(command: str, cwd: Path, root: Path, store: Path) -> str | None:
    """What a driver's bash command would do to the project, as "change X" or
    "run `Y`", or None.

    The write targets `_bash_write_targets` sees (beagle's store and caches
    aside, and anything outside the project), then what it does not: `git
    add`/`commit`, a formatter, and an inline script that writes a file.
    """
    for target in _bash_write_targets(command, cwd) or []:
        path = _resolved(target)
        inside = path == root or root in path.parents
        stored = path == store or store in path.parents
        if inside and not stored and not _CACHE_DIRS & set(path.parts):
            return f"change {path.relative_to(root) if path != root else target}"
    found = _bash_find(command, _driver_change)
    if found is None:
        return None
    if found.startswith(_INTERPRETERS):
        return f"run a {found} script that writes files" if _SCRIPT_WRITE.search(command) else None
    if found.startswith("ruff") and "--fix" in found.split():
        return f"run `{found}`, whose `--fix` flag rewrites files (without `--fix` it only reads)"
    return f"run `{found}`"


def make_driver_edit_guard() -> Any:
    """Build the `tool_call` guard that keeps the driver session's hands off the work.

    In a founded pursuit the driving session plans, opens, dispatches and
    closes; the work is a sub-agent's. A driver that edits project files
    itself writes code no brief described and no check was bound for, and
    spends the context the loop needs to keep going. In run 9, with the
    write and edit tools refused, the driver did it through bash instead:
    `sed -i`, `cat > justfile`, Python heredocs, `ruff --fix`, `git add`.
    In run 10, with those refused, it had the `agent` tool's sub-agent write
    the file: that sub-agent's session is its own, so only refusing the
    spawn keeps it out. Its `.beagle/` store is left to `make_record_guard`.
    `BEAGLE_TAU_DRIVER_EDITS=1` lets it edit.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        if os.environ.get(DRIVER_EDITS_ENV):
            return None
        try:
            # Only the session the host started: an in-process subagent loads
            # this extension into a runtime of its own that never sees a
            # `session_start`, and its edits are the work.
            tool = event.tool_name
            if tool not in ("write", "edit", "bash", "agent") or _STARTED_SESSION is None:
                return None
            if context.session_id != _STARTED_SESSION:
                return None
            cwd = Path(context.cwd)
            goal = _find_goal(cwd)
            if goal is None:
                return None
            store = _resolved(goal.parent)
            args = event.arguments or {}
            if tool == "bash":
                command = str(args.get("command", ""))
                what = _driver_bash_change(command, cwd, store.parent, store)
                if what is None:
                    return None
            elif tool == "agent":
                what = "spawn a sub-agent with the agent tool"
            else:
                target = _goal_path_from_args(args, cwd)
                if target is None or target == store or store in target.parents:
                    return None
                what = f"{tool} {target}"
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to {what} from the driving session: in a pursuit the work, and "
                "its commits, are done by sub-agents. Call pursuit_step, with what you "
                "meant to change in its notes; a sub-agent does it and the task's check "
                "decides. For work no task covers (a failing gate, a lint fix), add a task "
                "with pursuit_plan. Reading and running (tests, `ruff check` without "
                "`--fix`, `git status`) is fine. (If the user wants this session to edit, they set "
                f"{DRIVER_EDITS_ENV}=1.)"
            ),
        )

    return guard


#: `git` options that take a value before the subcommand (`git -C dir reset`).
_GIT_VALUE_OPTIONS = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace"})
#: Subcommands of `git stash` and `git rebase` that keep or finish work.
_STASH_KEEPS = frozenset({"list", "show", "pop", "apply", "branch"})
_REBASE_ENDS = frozenset({"--abort", "--continue", "--skip", "--quit"})


def _git_args(argv: list[str]) -> list[str]:
    """A `git` argv from its subcommand on, past the options before it."""
    args = argv[1:]
    while args and args[0].startswith("-"):
        args = args[2:] if args[0] in _GIT_VALUE_OPTIONS else args[1:]
    return args


def _git_discard(argv: list[str]) -> str | None:
    """What a `git` argv throws away or rewrites, or None when it does neither."""
    args = _git_args(argv)
    if not args:
        return None
    sub, rest = args[0], args[1:]
    flags = [a for a in rest if a.startswith("-") and a != "--"]
    short = "".join(a[1:] for a in flags if not a.startswith("--"))
    if sub == "reset" and {"--hard", "--merge", "--keep"} & set(flags):
        return "reset --hard"
    if sub == "clean" and ("f" in short or "--force" in flags):
        return "clean"
    if sub in ("checkout", "restore") and "." in rest:
        return f"{sub} ."
    if sub == "checkout" and ("f" in short or "--force" in flags):
        return "checkout --force"
    if sub == "stash" and not (rest and rest[0] in _STASH_KEEPS):
        return "stash"
    if sub == "rebase" and not _REBASE_ENDS & set(flags):
        return "rebase"
    if sub == "commit" and "--amend" in flags:
        return "commit --amend"
    if sub == "push" and ("f" in short or any(f.startswith("--force") for f in flags)):
        return "push --force"
    if sub in ("filter-branch", "filter-repo"):
        return sub
    return None


def _bash_find(command: str, match: Callable[[list[str]], str | None]) -> str | None:
    """The first simple command in a bash command that `match` names, or None.

    Read like `_bash_write_targets`: per simple command, wrappers skipped,
    `bash -c '...'` one level down. A command too broken to parse is None.
    """
    tokens = _shell_tokens(command)
    if tokens is None:
        return None
    segment: list[str] = []
    for token in [*tokens, ";"]:
        if not _is_operator(token):
            segment.append(token)
            continue
        argv = segment
        segment = []
        while argv and ("=" in argv[0] and not argv[0].startswith("=") or argv[0] in _WRAPPERS):
            argv = argv[1:]
        if not argv:
            continue
        if Path(argv[0]).name in _SHELLS and "-c" in argv[1:]:
            script_at = argv.index("-c") + 1
            found = _bash_find(argv[script_at], match) if script_at < len(argv) else None
        else:
            found = match(argv)
        if found is not None:
            return found
    return None


def _bash_git_discard(command: str) -> str | None:
    """The first work-discarding `git` call in a bash command, or None."""
    return _bash_find(command, lambda argv: _git_discard(argv) if _named(argv, "git") else None)


def _named(argv: list[str], program: str) -> bool:
    return Path(argv[0]).name == program


#: The `beagle pursuit` verbs that only read the pursuit. A worker sent with no
#: task may run these; every other verb changes the tree or the log.
_PURSUIT_READ_VERBS = frozenset(
    {"next", "brief", "show", "status", "view", "tree", "findings", "rules", "review-check"}
)


def _pursuit_verb(argv: list[str]) -> str | None:
    """The verb of a `beagle pursuit <verb>` argv, or None for any other command."""
    if not _named(argv, "beagle"):
        return None
    words: list[str] = []
    args = iter(argv[1:])
    for arg in args:
        if arg == "--root":  # the one option before the verb that takes a value
            next(args, None)
        elif not arg.startswith("-"):
            words.append(arg)
    if len(words) < 2 or words[0] != "pursuit":
        return None
    return words[1]


def _pursuit_write_verb(argv: list[str]) -> str | None:
    """The verb of a `beagle pursuit <verb>` argv that changes the pursuit, or None."""
    verb = _pursuit_verb(argv)
    return None if verb in _PURSUIT_READ_VERBS else verb


def make_history_guard() -> Any:
    """Build the `tool_call` guard that keeps a pursuit's history and tree.

    A pursuit's ground truth is this repository: commits carry the claims a
    close is judged by, and the work tree is what a check runs on. A model
    that tidies up a mistake with `git reset --hard <old commit>` throws away
    every task's work since, the store with it — a 9B worker did exactly that
    after committing a stray `__pycache__`. In a founded pursuit every
    session, driver and worker, fixes forward instead. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        try:
            if event.tool_name != "bash":
                return None
            found = _bash_git_discard(str((event.arguments or {}).get("command", "")))
            if found is None or _find_goal(Path(context.cwd)) is None:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing `git {found}` in a pursuit: it throws away work or rewrites "
                "commits, and the pursuit's claims and checks stand on both. Fix forward: "
                "`git rm --cached <path>` for a file committed by mistake, an ignore rule, "
                "`git restore <path>` for one file, or a new commit that undoes the last. "
                "If the tree is wrong beyond that, say so in your report and stop."
            ),
        )

    return guard


#: `git` subcommands that stage or commit, which a worker leaves to pursuit_step.
_WORKER_GIT_REFUSED = frozenset({"add", "commit", "stage"})


def _worker_git_commit(argv: list[str]) -> str | None:
    if not _named(argv, "git"):
        return None
    args = _git_args(argv)
    return args[0] if args and args[0] in _WORKER_GIT_REFUSED else None


#: Why a worker is kept from beagle and its store.
NO_BEAGLE_REASON = (
    "the brief has everything; do the task. A worker does not inspect .beagle/ or run "
    "beagle: the session that sent you does that."
)
#: What a worker is told in its brief, to the same end.
NO_BEAGLE_NOTE = "Do not inspect .beagle/ or run beagle."
#: Programs that only show what a path holds: a worker reading `.beagle/` with one
#: is orienting, not working. A check script under it (`bash .beagle/checks/...`)
#: is run, not read, and passes.
_READERS = frozenset(
    {"cat", "ls", "head", "tail", "less", "more", "find", "tree", "grep", "rg", "wc", "stat"}
)
#: The path an inline script opens or writes, as its source says it.
_SCRIPT_PATH = re.compile(
    r"""open\(\s*['"](?P<open>[^'"]+)['"]\s*,\s*['"][wax]"""
    r"""|Path\(\s*['"](?P<path>[^'"]+)['"]\s*\)\s*\.write_(?:text|bytes)\("""
    r"""|writeFileSync\(\s*['"](?P<node>[^'"]+)['"]"""
)


def _in_store(word: str) -> bool:
    return any(part == ".beagle" for part in Path(word).parts)


def _worker_orientation(tool: str, args: Mapping[str, Any], cwd: Path) -> str | None:
    """What a worker's call does to orient itself on beagle, or None.

    Run R04: 20 of 25 workers capped at 30 turns, W1 spending about ten on
    `.beagle/`, `beagle doctor`, the tree and `pursuit open` before writing a
    line. Its own test runs, and a check script under `.beagle/checks/`, pass.
    """
    if tool == "read":
        target = _goal_path_from_args(args, cwd)
        raw = str(args.get("path") or "")
        if _in_store(raw) or (target is not None and ".beagle" in target.parts):
            return f"read {raw}"
        return None
    if tool != "bash":
        return None
    command = str(args.get("command", ""))

    def match(argv: list[str]) -> str | None:
        if _named(argv, "beagle"):
            return f"run `{' '.join(argv[:3])}`"
        if Path(argv[0]).name in _READERS and any(_in_store(a) for a in argv[1:]):
            return f"run `{' '.join(argv)}`"
        return None

    return _bash_find(command, match)


def _script_write_targets(command: str, cwd: Path) -> list[Path]:
    """The paths an inline script in `command` writes, as its source names them.

    Run R04: W9, refused a write to src/__init__.py, wrote it with
    `python3 -c "open('src/__init__.py','w').write(...)"`. A path the script
    does not spell out is not guessed at: the guard fails open on it.
    """
    found = [next(g for g in m.groups() if g is not None) for m in _SCRIPT_PATH.finditer(command)]
    return [_resolved(Path(p) if Path(p).is_absolute() else cwd / p) for p in found]


def _worker_scope() -> tuple[str, tuple[str, ...]] | None:
    """The task and scope this worker was sent with, or None when it has no scope."""
    scope = tuple(
        line.strip() for line in os.environ.get(WORKER_SCOPE_ENV, "").splitlines() if line.strip()
    )
    if not scope:
        return None
    return os.environ.get(WORKER_TASK_ENV, "").strip() or "this task", scope


def make_worker_scope_guard() -> Any:
    """Build the `tool_call` guard that keeps a worker's writes inside its task's scope.

    The scope was recorded and not enforced: in run R02 a worker wrote
    `tests/` over .gitignore with two turns left, and the next three steps went
    to repairing it. A worker sent with a scope (`BEAGLE_TAU_WORKER_SCOPE`) may
    write in it, outside the project (/tmp), in beagle's store (the record guard
    has that) and `.git/beagle/` (the task's log). A worker with no scope is
    not held. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        try:
            cwd = Path(context.cwd)
            arguments = event.arguments or {}
            sent_on_task = bool(os.environ.get(WORKER_TASK_ENV, "").strip())
            orientation = (
                _worker_orientation(event.tool_name, arguments, cwd) if sent_on_task else None
            )
            if orientation is not None:
                return ToolCallHookResult(
                    block=True,
                    reason=f"refusing to {orientation}: {NO_BEAGLE_REASON}",
                )
            sent = _worker_scope()
            if sent is None:
                return None
            task, scope = sent
            command = str(arguments.get("command", "")) if event.tool_name == "bash" else ""
            script = _bash_find(command, _driver_change) if command else None
            scripted = (
                script is not None
                and script.startswith(_INTERPRETERS)
                and _SCRIPT_WRITE.search(command) is not None
            )
            targets = _write_targets(event.tool_name, arguments, cwd)
            if scripted:
                targets += _script_write_targets(command, cwd)
            goal = _find_goal(cwd) if targets else None
            if goal is None:
                return None
            root = _resolved(goal.parent.parent)
            allowed = [_resolved(goal.parent), root / ".git" / "beagle"]
            for target in targets:
                target = _resolved(target)
                if target != root and root not in target.parents:
                    continue  # outside the project: /tmp, /dev/null
                if any(target == a or a in target.parents for a in allowed):
                    continue
                if _CACHE_DIRS & set(target.parts):
                    continue
                if _scope_hit(target, root, scope) is None:
                    break
            else:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        rel = target.relative_to(root) if target != root else target
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to write {rel}: it is outside {task}'s scope "
                f"({', '.join(scope)}); name it in your report as follow-up. Scratch "
                "files go in /tmp."
            ),
        )

    return guard


def make_worker_pursuit_guard() -> Any:
    """Build the `tool_call` guard that keeps a worker out of the pursuit's books.

    A worker is one step of its parent's pursuit: the parent opens the task,
    runs its check and closes it. A worker that opens, closes or dispatches
    tasks itself runs a pursuit nobody is driving — in run 7 a worker opened
    the next task and sent a nested worker at it, which ate its whole budget.
    Reading the pursuit (`brief`, `show`, `status` …) passes here; a worker
    sent on a task is kept from that by `make_worker_scope_guard`.

    Committing is the parent's too: pursuit_step commits a task's scope before
    its close. In run R02 workers ran `git add` and `git commit` around the
    refused `beagle pursuit commit`, and one spawned an `agent` sub-agent to
    record claims, which ran 39 turns into a provider error. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        del context
        try:
            if event.tool_name == "agent":
                what = "spawn a sub-agent with the agent tool"
            elif event.tool_name == "bash":
                command = str((event.arguments or {}).get("command", ""))
                verb = _bash_find(command, _pursuit_write_verb)
                git = _bash_find(command, _worker_git_commit)
                if verb is not None:
                    what = f"run `beagle pursuit {verb}`"
                elif git is not None:
                    what = f"run `git {git}`"
                else:
                    return None
            else:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to {what} in a sub-agent: the session that sent you opens, "
                "checks, commits and closes the pursuit's tasks. Do not commit or claim; "
                "do the work in your brief yourself, then end with a report of what you "
                "changed and what is left."
            ),
        )

    return guard


#: The `beagle pursuit` verbs the driver's tools run, and the tool for each.
_STEERED_VERBS = {
    "open": "pursuit_step (with criteria and done_when)",
    "close": (
        "pursuit_step, which closes a task on its check; to drop one, pursuit_step with "
        "its task and abandon='<why>'"
    ),
    "retry": "pursuit_step on the blocked task, with notes saying what to fix",
    "spawn": "pursuit_step with new_route=true and notes saying what to do instead",
    "amend": "pursuit_step on the open task, with the new done_when",
    "bind": "pursuit_step (with criteria and done_when)",
    "spend": "pursuit_step, which records each sub-agent's measured spend",
    "audit": "pursuit_step, which has a sub-agent do a due audit and records it",
    "split": "pursuit_plan",
    "add": "pursuit_plan",
    "depend": (
        "pursuit_step with no arguments, which hands out the next ready task, and "
        "pursuit_plan for work that is missing. A wait added by hand can close a "
        "cycle that nothing then starts; only withdrawing one, `beagle pursuit depend "
        "<task> <after> --drop --reason '<why>'`, runs from bash"
    ),
    "commit": (
        "nothing: pursuit_step commits the files a task changed in its scope before it "
        "closes the task"
    ),
}


def _steered_verb(argv: list[str]) -> str | None:
    """The steered `beagle pursuit` verb of one argv, or None.

    A `depend` that withdraws an edge passes; one that adds an edge does not.
    Run R06's driver added `depend T0008 --hard T0003` to "skip" T0008, and
    the wait closed a cycle through the task T0008 had superseded.
    """
    verb = _pursuit_verb(argv)
    if verb == "depend" and "--drop" in argv:
        return None
    return verb if verb in _STEERED_VERBS else None


def make_driver_pursuit_guard() -> Any:
    """Build the `tool_call` guard that steers the driver's pursuit verbs to its tools.

    pursuit_found, pursuit_plan and pursuit_step run beagle's verbs with the
    rules around them: a check screened before it is bound and run before a
    close, a spend measured, a blocked task retried or spawned anew. A driver
    that runs `beagle pursuit close` from bash skips all of it — in run 8 it
    closed, spawned, opened and re-split one task over and over by hand. The
    verbs no tool runs (`retire`, `rebudget` …) and a `depend --drop` stay
    allowed, and so does reading. Only the host-started session, and only in a founded
    pursuit. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        if os.environ.get(DRIVER_EDITS_ENV):
            return None
        try:
            if event.tool_name != "bash" or _STARTED_SESSION is None:
                return None
            if context.session_id != _STARTED_SESSION:
                return None
            verb = _bash_find(str((event.arguments or {}).get("command", "")), _steered_verb)
            if verb is None or _find_goal(Path(context.cwd)) is None:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing `beagle pursuit {verb}` from bash: use {_STEERED_VERBS[verb]}. "
                "The tool runs it with the checks around it that the bare verb skips. "
                f"(If the user wants this session to run it by hand, they set "
                f"{DRIVER_EDITS_ENV}=1.)"
            ),
        )

    return guard


#: Programs that fetch a URL, and the Python modules a script fetches one with.
_URL_FETCHERS = frozenset({"curl", "wget", "lynx", "w3m", "links", "elinks", "aria2c", "http"})
_URL = re.compile(r"https?://")
_SCRIPT_FETCH = re.compile(r"\b(?:urllib|requests|httpx|aiohttp|urlopen)\b")


def _url_fetch(argv: list[str]) -> str | None:
    """The program in one simple command that fetches an http(s) URL, or None."""
    name = Path(argv[0]).name
    if name in _URL_FETCHERS and any(_URL.search(arg) for arg in argv[1:]):
        return name
    if name.startswith("python"):
        script = " ".join(argv[1:])
        if _SCRIPT_FETCH.search(script) and _URL.search(script):
            return f"a {name} script"
    return None


def _bash_url_fetch(command: str) -> str | None:
    """What in a bash command fetches an http(s) URL, or None."""
    found = _bash_find(command, _url_fetch)
    if found is not None:
        return found
    # A heredoc script's body is not in the shell words `_bash_find` reads.
    python = _bash_find(command, lambda a: a[0] if Path(a[0]).name.startswith("python") else None)
    if python is not None and _SCRIPT_FETCH.search(command) and _URL.search(command):
        return f"a {Path(python).name} script"
    return None


def _web_tool(name: str) -> bool:
    lowered = name.lower()
    return "fetch" in lowered or lowered.startswith(("web", "browse"))


def _driver_readable_dirs() -> list[Path]:
    """Outside the project, where the driver still reads: Tau's and beagle's own files."""
    tau_home = os.environ.get("TAU_HOME")
    dirs = [
        Path(tau_home).expanduser() if tau_home else Path.home() / ".tau",
        Path.home() / ".agents",
        AGENTS_DIR,
        Path(tempfile.gettempdir()) / "tau-buffers",
        BEAGLE,
    ]
    dirs += [d for d in (_PLUGIN_ROOT, _DRIVERS_DIR) if d is not None]
    return [_resolved(d) for d in dirs]


def _held_read(tool: str, args: Mapping[str, Any], cwd: Path) -> ToolCallHookResult | None:
    """Refuse the driver a read of a file in the scope of a task steps left open.

    Run R04: with T0002 open after a run of stays-open results, the driver
    spent about 60 bash and read calls on the workers' test files itself,
    and four compactions followed. Debugging the work is the sub-agent's;
    the driver's lever is the step's notes, or a new route.
    """
    if _is_worker() or not _NOT_DONE:
        return None
    if tool == "read":
        target = _goal_path_from_args(args, cwd)
        targets = [target] if target is not None else []
    elif tool == "bash":
        targets = _bash_read_targets(str(args.get("command", "")), cwd)
    else:
        return None
    goal = _find_goal(cwd) if targets else None
    if goal is None:
        return None
    for target in targets:
        held = _held_scope(target, goal.parent.parent)
        if held is not None:
            task, entry, count = held
            return ToolCallHookResult(
                block=True,
                reason=(
                    f"refusing to read {target} from the driving session: it is in the "
                    f"scope of {task} ({entry}), which {count} steps have left not done, "
                    "and debugging its work is the sub-agent's. Say what to fix in "
                    f'pursuit_step\'s notes (task="{task}"), or give it a new route: '
                    f'pursuit_step task="{task}", new_route=true, with a rewritten '
                    "done_when and notes saying what to do differently."
                ),
            )
    return None


def make_driver_reference_guard() -> Any:
    """Build the `tool_call` guard that leaves references to the workers.

    The found-first gate keeps a driver from reading references before it
    founds; R01's 9B driver founded and then fetched and read the ITC paper
    itself, and what it read fed the spirals that followed. Once founded,
    the host-started session may not fetch a URL (curl, wget, a Python
    urllib or requests script, a web tool) or `read` a file outside the
    project, Tau's and beagle's own files aside, or one founding fetched into
    `references/`. A worker reads what its task needs. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        if os.environ.get(DRIVER_EDITS_ENV):
            return None
        try:
            tool = event.tool_name
            if _STARTED_SESSION is None or context.session_id != _STARTED_SESSION:
                return None
            args = event.arguments or {}
            cwd = Path(context.cwd)
            held = _held_read(tool, args, cwd)
            if held is not None:
                return held
            if tool == "bash":
                found = _bash_url_fetch(str(args.get("command", "")))
                what = f"fetch a URL with {found}" if found is not None else None
            elif tool == "read":
                target = _goal_path_from_args(args, cwd)
                what = f"read {target}" if target is not None else None
            elif _web_tool(tool):
                what = f"use {tool}"
            else:
                return None
            if what is None:
                return None
            goal = _find_goal(cwd)
            if goal is None:
                return None
            if tool == "read":
                root = _resolved(goal.parent.parent)
                fetched = root / REFERENCES_DIR
                allowed = [root, *_driver_readable_dirs()]
                if fetched not in target.parents and any(
                    target == d or d in target.parents for d in allowed
                ):
                    return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to {what} from the driving session: references are read by the "
                "worker that a pursuit_step dispatches. Call pursuit_step, naming in its "
                "notes the reference the task needs (its URL or path); the sub-agent reads "
                f"it. Files inside the project, {REFERENCES_DIR}/ aside, are yours to read. "
                f"(If the user wants this session to read it, they set {DRIVER_EDITS_ENV}=1.)"
            ),
        )

    return guard


#: What beagle keeps under `.beagle/` as its record of the pursuit, and the
#: cases this extension locks. Only beagle and this extension write them;
#: the `*.toml` beside them is configuration, and editable.
_STORE_RECORDS = frozenset(
    {
        "tree",
        "log",
        "findings",
        "state.json",
        "LOG.md",
        "STATUS.md",
        "cadence-runs.json",
        "hook-trace.json",
        ".lock",
        ".gate.lock",
        LOCKED_DIR,
        PENDING_LOCKS,
    }
)


def _store_record(path: Path, store: Path) -> str | None:
    """`path` relative to `store` if it is one of beagle's records, else None."""
    try:
        rel = _resolved(path).relative_to(store)
    except ValueError:
        return None
    return str(rel) if rel.parts and rel.parts[0] in _STORE_RECORDS else None


def make_record_guard() -> Any:
    """Build the `tool_call` guard that keeps every session's hands off beagle's records.

    A task's file, the log and the state are beagle's account of what was
    opened, checked and closed; a check that greps them, or a model that
    edits them, makes that account say whatever it was told. In run 8 the
    driver `sed -i`'d a check into a task file and two log notes. Write and
    edit tools and the bash writes `_bash_write_targets` sees are refused;
    `BEAGLE_TAU_DRIVER_EDITS=1` lets them through. Fails open.
    """

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        if os.environ.get(DRIVER_EDITS_ENV):
            return None
        try:
            cwd = Path(context.cwd)
            args = event.arguments or {}
            if event.tool_name in ("write", "edit"):
                target = _goal_path_from_args(args, cwd)
                targets = [target] if target is not None else []
            elif event.tool_name == "bash":
                targets = _bash_write_targets(str(args.get("command", "")), cwd) or []
            else:
                return None
            goal = _find_goal(cwd) if targets else None
            if goal is None:
                return None
            store = _resolved(goal.parent)
            record = next((rel for rel in (_store_record(t, store) for t in targets) if rel), None)
            if record is None:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to change .beagle/{record}: it is beagle's record of the "
                "pursuit, and only beagle writes it. What a sub-agent should know goes in "
                "pursuit_step's notes; a check that cannot judge the work is replaced by "
                "pursuit_step with a new done_when."
            ),
        )

    return guard


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
    global _SEEN_CWD, _STARTED_SESSION
    del event
    _SEEN_CWD = context.cwd
    _STARTED_SESSION = context.session_id
    _adopt_session(context)


async def _on_driver_session_start(event: Any, context: ExtensionContext) -> None:
    """Retire a run whose Tau driver has ended, then record this session.

    Load already did this for the process's cwd; this covers `/new`,
    `/resume` and branches in the same process, whose outgoing session was
    marked ended at shutdown. Retiring comes first: a resumed session is the
    run's recorded driver, but not the process that ran its workers.
    """
    global _ENDED_RUN_NOTE
    del event
    goal = _find_goal(context.cwd)
    if goal is not None:
        note = await asyncio.to_thread(_retire_gone_driver, goal.parent.parent)
        if note is not None:
            _ENDED_RUN_NOTE = note
            context.ui.notify(RETIRED_NOTICE, "warning")
    _register_driver(context.session_id)


def _notify_retired_once() -> Any:
    """A `session_start` handler saying, once, that load retired a run."""
    shown: list[bool] = []

    def notify(event: Any, context: ExtensionContext) -> None:
        del event
        if not shown:
            shown.append(True)
            context.ui.notify(RETIRED_NOTICE, "warning")

    return notify


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


def _note_run_start(event: Any, context: ExtensionContext) -> None:
    """Count a run as unclean until its `agent_end` says otherwise.

    An aborted run can settle without ever emitting `agent_end`, and the flag
    left over from the run before would then let the Stop hooks object to it.
    """
    global _LAST_RUN_CLEAN
    del event, context
    _LAST_RUN_CLEAN = False


def _note_run_end(event: Any, context: ExtensionContext) -> None:
    """Remember whether the run ended by itself, for the Stop hooks."""
    global _LAST_RUN_CLEAN
    del context
    stops = [getattr(m, "stop_reason", None) for m in getattr(event, "messages", ())]
    stops = [stop for stop in stops if stop is not None]
    # `length` is the model running out of room, not choosing to stop. The
    # session already nudges a turn cut off at the output limit; a run that
    # still ends there needs a person, not another objection.
    _LAST_RUN_CLEAN = not stops or stops[-1] not in ("aborted", "error", "length")


#: Tool calls a steered driver may spend on setup before it must found.
FOUND_FIRST_SETUP_CALLS = 6

FOUND_FIRST_NOTE = (
    "Beagle: this project is not a pursuit yet. Found it before anything else: "
    "`beagle init` if `.beagle/` is missing, then `pursuit_found`. Do not read "
    "references or design the solution first; reading the reference and choosing "
    "a design are milestones, which `pursuit_step` sub-agents do. Name the "
    f"reference (URL) in the milestones. After {FOUND_FIRST_SETUP_CALLS} setup "
    "tool calls, every tool but the pursuit tools is refused until it is founded."
)


def _note_prompt(event: Any, context: ExtensionContext) -> None:
    """Keep the user's prompt for the `agent_start` that follows it."""
    global _LAST_PROMPT
    del context
    if getattr(event, "source", "interactive") == "interactive":
        _LAST_PROMPT = str(getattr(event, "text", "") or "")


def make_found_first_steer(tau: ExtensionAPI) -> Any:
    """Steer a request to set beagle up toward `pursuit_found`, once.

    The prompt section says to found first, and a 9B model still reads the
    reference and spends whole turns designing the solution in the driver.
    A note right after the user's request, before the first model call, is
    the part of the context such a model follows. It carries an extract of
    each reference the request links, which founding then reuses.
    """

    async def steer(event: Any, context: ExtensionContext) -> None:
        global _FOUND_FIRST_SENT
        del event, context
        if _FOUND_FIRST_SENT or not re.search(r"(?i)\b(beagle|pursuit)", _LAST_PROMPT):
            return
        root, goal = _project_root()
        if goal is not None:
            return
        _FOUND_FIRST_SENT = True
        note = FOUND_FIRST_NOTE
        if _prompt_urls(_LAST_PROMPT):
            # R02 and R03 wrote criteria for interval trees when the request
            # was interval tree clocks: nothing of the reference had reached
            # the driver before it founded.
            prompt = _LAST_PROMPT
            index = await asyncio.to_thread(_fetch_references, root, prompt)
            extracts = _references_note(index, root)
            if extracts:
                note = f"{note}\n\n{extracts}"
        tau.send_custom_message(note, custom_type="beagle", deliver_as="steer")

    return steer


def _pin_founded(tau: ExtensionAPI) -> Callable[[Path], None]:
    """Swap the not-yet-founded orientation for the pursuit's own, once founded.

    The prompt sections are set at load, so a pursuit founded mid-session
    kept "nothing founded yet" for the rest of it. Every tool result that
    said how to work the pursuit was compacted away in time, and run 10's
    driver was left with only a summary's account of the loop.
    """

    def pin(goal: Path) -> None:
        section = _goal_section(goal)
        if section:
            tau.set_prompt_section("Beagle pursuit", section)
            tau.set_prompt_section("Beagle", None)

    return pin


#: Focus for the summarizer when this session drives a pursuit. Run 10's
#: summaries listed the driver's own commands as done tasks (T0015-T0022,
#: none of them beagle's), dropped the task that was ready, and carried a
#: search the driver had repeated 78 times forward as the next step.
PURSUIT_COMPACTION_FOCUS = (
    "If this session drives a beagle pursuit: task ids (T0001, ...) and their status come "
    "only from beagle's own output: pursuit_found, pursuit_plan, pursuit_step, and "
    "`beagle pursuit tree` or `next`. Never record this session's own commands, checks "
    "or investigations as tasks or as finished work. Keep, by id, the tasks beagle "
    "still shows open or ready. The next step is pursuit_step: do not carry a side "
    "investigation (a gate, a lint run, a search) forward as a next step, and leave out "
    "how many times a command was run."
)


def make_state_after_compaction(tau: ExtensionAPI) -> Any:
    """After a compaction, tell the driver where the pursuit stands, from beagle.

    A summary is a model's account of the record, and a small model's account
    drifts: run 10's said nothing was ready while a task was. The ledger is
    one command away, so the driver gets it, not the summary's version.
    """

    def note(event: Any, context: ExtensionContext) -> None:
        del context
        if getattr(event, "aborted", False):
            return
        root, goal = _project_root()
        if goal is None:
            return
        rc, ready, _raw = _next_ready(root)
        ready_ids = _ids(ready.get("ready")) if isinstance(ready, dict) else []
        open_ids = _ids(ready.get("open")) if isinstance(ready, dict) else []
        if ready_ids:
            now = f"Ready now: {', '.join(ready_ids)}."
        elif open_ids:
            now = f"Open now: {', '.join(open_ids)}."
        else:
            now = "Nothing is ready now."
        tree = _tree(root)
        tau.send_custom_message(
            "The conversation was just compacted. Where the pursuit stands, from beagle "
            f"itself (trust this over the summary):\n\n{tree}\n\n{now} Next: call "
            "pursuit_step with no arguments. Work no task covers goes in with "
            "pursuit_plan; this session does not do it itself.",
            custom_type="beagle",
            deliver_as="steer",
        )

    return note


def make_found_first_gate() -> Any:
    """Build the `tool_call` gate behind the found-first steer.

    The steer alone was not enough: a 9B driver acknowledged nothing, fetched
    the reference, thought itself out of output room and then began building
    the project in the driver. Once steered, the driver gets a few calls for
    setup; after them only the pursuit tools run until the goal exists.
    """

    async def gate(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        global _SETUP_CALLS
        try:
            if not _FOUND_FIRST_SENT or event.tool_name.startswith("pursuit_"):
                return None
            if _STARTED_SESSION is None or context.session_id != _STARTED_SESSION:
                return None
            if _find_goal(Path(context.cwd)) is not None:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        _SETUP_CALLS += 1
        if _SETUP_CALLS <= FOUND_FIRST_SETUP_CALLS:
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing {event.tool_name}: setup is done and the pursuit is not founded. "
                "Call pursuit_found now with the user's goal, criteria and milestones "
                "(user_delegated=true if they told you to decide). Reading references, "
                "designing and building are milestones for pursuit_step's sub-agents."
            ),
        )

    return gate


#: Follow-ups the stop gate queues in one run before it lets the driver stop.
MAX_STOP_GATE_FOLLOWUPS = 2
_STOP_GATE_SENT = 0


def _reset_stop_gate(event: Any, context: ExtensionContext) -> None:
    global _STOP_GATE_SENT
    del event, context
    _STOP_GATE_SENT = 0


def make_stop_gate(tau: ExtensionAPI) -> Any:
    """Build the driver's `turn_end` gate: no stop while the pursuit is unfinished.

    Run R02's driver ended a `tau -p` run with "complete" while the root was
    stalled, and nothing objected: the Stop hooks do not run in print mode. A
    turn that ends with no tool call is the run's last unless something is
    queued, so this queues a follow-up naming what is not done, as the
    session's output-limit nudge does; the loop sends it in print mode too.
    At most `MAX_STOP_GATE_FOLLOWUPS` a run, then the stop is let through.
    """

    async def gate(event: Any, context: ExtensionContext) -> None:
        global _STOP_GATE_SENT, _FOUND_AWAITS_USER
        message = getattr(event, "message", None)
        if (
            getattr(message, "role", None) != "assistant"
            or getattr(message, "tool_calls", None)
            or getattr(message, "stop_reason", None) in ("error", "aborted", "length")
            or _STOP_GATE_SENT >= MAX_STOP_GATE_FOLLOWUPS
        ):
            return
        goal = _find_goal(Path(context.cwd))
        if goal is None:
            # Run R05 ended here, asking an absent user to confirm the goal.
            if _FOUND_AWAITS_USER and not context.has_ui:
                _FOUND_AWAITS_USER = False
                _STOP_GATE_SENT += 1
                tau.send_user_message(
                    "[beagle] Nothing is founded, and this is print mode: no user will "
                    "answer, and their prompt is all they said. If it tells you to set up "
                    "or decide without discussion, call pursuit_found again now with your "
                    "goal and criteria and user_delegated=true. Stop only if the prompt "
                    "gives you nothing to decide from."
                )
            return
        nodes = await asyncio.to_thread(_tree_nodes, goal.parent.parent)
        left = _unfinished(nodes)
        if not left:
            return
        _STOP_GATE_SENT += 1
        tau.send_user_message(
            "[beagle] The pursuit is not done, so this is not the place to stop. Not "
            "done, and nothing took their work on:\n" + "\n".join(left) + "\n\nCall "
            "pursuit_step with no arguments for the next task; if nothing is ready, add "
            "the missing work with pursuit_plan, or give a task a new route with "
            'pursuit_step task="<id>", new_route=true and notes. Stop only when the '
            "pursuit is done or a step says to stop and tell the user."
        )

    return gate


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


ENDED_RUN_NOTE = """\
beagle (Tau): the pursuit run driven by Tau session {session} was stopped \
with `beagle loop stop`, because that session ended ({why}). A Tau session's \
workers and wakeup end with it, so nothing was going to come back for that \
run. {awaiting}Start a new run as the driver below says. A task that run left \
open may hold a cancelled worker's partial work: before redoing it, read \
`git status` and `git diff` in its scope (or the worker's `tau-agent-*` \
branch, if it ran in a worktree) and the worker's transcript under \
`~/.tau/subagents/*/{session}/tasks/`, then finish the task or close it \
abandoned."""


RETIRED_NOTICE = (
    "Beagle: stopped the pursuit run left by an ended Tau session; /pursuit-run starts a new one."
)


def _process_start(pid: int) -> str | None:
    """`pid`'s start time in clock ticks (Linux `/proc`), to tell a reused pid apart."""
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
    except OSError:
        return None
    fields = stat.rpartition(")")[2].split()  # the name may hold spaces
    return fields[19] if len(fields) > 19 else None  # field 22, `starttime`


def _pid_alive(pid: int, start: str | None) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        pass  # someone else's process: alive, and not ours
    now = _process_start(pid)
    return start is None or now is None or now == start


def _driver_record(session_id: str | None) -> Path | None:
    if _DRIVERS_DIR is None or not session_id or "/" in session_id:
        return None
    return _DRIVERS_DIR / f"{session_id}.json"


def _register_driver(session_id: str | None) -> None:
    """Record this process as the one `session_id` runs in; prune stale records.

    beagle records a run's driver session but, under Tau, no pid it believes
    (see `_adopt_session`), so it cannot tell a gone driver from a live one and
    tells every other session to stand down until the wait's lease runs out.
    This record is what lets the next session tell instead.
    """
    global _DRIVER_SESSION
    path = _driver_record(session_id)
    if path is None:
        return
    _DRIVER_SESSION = session_id
    pid = os.getpid()
    record = {"pid": pid, "start": _process_start(pid), "ended": False}
    with contextlib.suppress(OSError):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(record), encoding="utf-8")
        tmp.replace(path)
        cutoff = datetime.now(UTC).timestamp() - DRIVER_RECORD_DAYS * 86400
        for old in path.parent.glob("*.json"):
            if old != path and old.stat().st_mtime < cutoff and _driver_gone(old.stem):
                old.unlink(missing_ok=True)


def _end_driver() -> None:
    """Mark this process's driver session ended: its workers and wakeup go with it."""
    path = _driver_record(_DRIVER_SESSION)
    if path is None:
        return
    with contextlib.suppress(OSError, ValueError):
        record = json.loads(path.read_text(encoding="utf-8"))
        record["ended"] = True
        path.write_text(json.dumps(record), encoding="utf-8")


def _driver_gone(session_id: str) -> str | None:
    """Why the Tau session `session_id` can no longer drive a run, or None.

    None too for a session with no record here — a Claude Code session, or
    one from before this record existed — which is left to beagle's own rules.
    """
    path = _driver_record(session_id)
    try:
        record = json.loads(path.read_text(encoding="utf-8")) if path else None
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    if record.get("ended"):
        return "the session was closed, replaced or reloaded"
    pid = record.get("pid")
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        return None
    start = record.get("start")
    if not _pid_alive(pid, start if isinstance(start, str) else None):
        return f"its Tau process {pid} exited"
    return None


def _retire_gone_driver(root: Path) -> str | None:
    """Stop the run whose Tau driver has ended; the note for the next driver.

    Workers do not outlive the Tau session that spawned them, so a run whose
    driver session ended has nothing left that will come back: no worker to
    report, no wakeup to fire. Left in place, beagle would tell a new session
    to stand down, and a resumed one that its dead worker still holds the
    task. Stopping it lets the next `/pursuit-run` start clean and pick the
    open task up as one a previous session left.
    """
    if not (root / LOOP_REL).is_file():
        return None
    record = _json_out(["loop", "read", "--json"], root)
    if not isinstance(record, dict):
        return None
    session = str(record.get("driver_session") or "")
    why = _driver_gone(session)
    if why is None:
        return None
    awaiting = str(record.get("awaiting") or "")
    reason = f"Tau driver session {session} ended ({why}); its workers ended with it"
    if awaiting:
        reason += f"; it was awaiting: {awaiting}"
    rc, _ = _run(
        [BEAGLE_BIN, "loop", "stop", "--reason", reason, "--root", str(root)], root, HOOK_TIMEOUT
    )
    if rc != 0:
        return None
    return ENDED_RUN_NOTE.format(
        session=session,
        why=why,
        awaiting=f'It was awaiting "{awaiting}". ' if awaiting else "",
    )


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
`<task-notification>` message that starts your next turn, an errored run's \
too; clear the wait with a bare `beagle loop tick` whatever its status, \
read the full report with `get_subagent_result` if the notification is \
truncated, and run the close. Claude Code's `SendMessage` \
to a running worker is `steer_subagent`; `get_subagent_result` with `wait: \
true` blocks on one. Parallel independent tasks may each get a background \
agent.
- Spawning a worker: leave `provider` and `model` unset, so it runs on this \
session's own provider and model; Claude Code's `sonnet`-style picks name \
nothing Tau serves. Set `max_turns` from the task's budget (`budget_tokens` in \
`beagle pursuit show <task>`), so a worker past it is told to wrap up. After a \
background spawn, end the turn; do not poll `get_subagent_result`, since the \
notification comes to you.
- Prose in a shell command (briefs, intents, close notes, commit messages) \
goes in a quoted heredoc (`<<'EOF'`), a file, or single quotes, never double \
quotes, which expand `$` and backticks.
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
    """The `/pursuit-run` driver as a turn, or None when it is not installed.

    A note about a run stopped because its Tau driver ended leads the first
    one sent after the stop.
    """
    global _ENDED_RUN_NOTE
    preamble = TAU_HOST_NOTE
    if _ENDED_RUN_NOTE is not None:
        preamble = f"{_ENDED_RUN_NOTE}\n\n{preamble}"
    text = _driver_turn(PURSUIT_RUN_COMMAND, args, preamble=preamble)
    if text is not None:
        _ENDED_RUN_NOTE = None
    return text


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


DRIVER_PARAMETERS: dict[str, Any] = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "enum": ["pursuit", "pursuit-run"],
            "description": (
                "`pursuit` to found a pursuit or work its tree in this session; "
                "`pursuit-run` to run it task after task across turns."
            ),
        },
        "args": {
            "type": "string",
            "description": "What the user asked for, passed to the driver as its arguments.",
        },
    },
    "required": ["command"],
}


def make_driver_tool() -> Any:
    """Build the `pursuit_driver` tool: `/pursuit` and `/pursuit-run`, model-callable.

    The commands are the user's to type; under Claude Code the model reaches
    the same text as a skill. Tau lists commands to no model, so without this a
    user who asks in prose for the pursuit loop gets a model that cannot find
    it. The driver comes back as the result, in the block the command sends.
    """

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id, signal, on_update
        command = arguments.get("command")
        args = arguments.get("args")
        args = args if isinstance(args, str) else ""
        if command == "pursuit-run" and _is_worker():
            return _make_dispatch_result(
                "pursuit_driver: a worker runs one step of its parent's loop, never its own."
            )
        if command == "pursuit":
            text, name = _pursuit_turn(args), PURSUIT_COMMAND
        elif command == "pursuit-run":
            text, name = _pursuit_run_turn(args), PURSUIT_RUN_COMMAND
        else:
            return _make_dispatch_result(
                "pursuit_driver: 'command' must be 'pursuit' or 'pursuit-run'."
            )
        if text is None:
            return _make_dispatch_result(f"pursuit_driver: {_driver_missing(name)}")
        return _make_dispatch_result(text)

    return execute


def _command_pursuit_view(args: str, context: Any) -> str:
    """Print the pursuit's current state without spending a model on it."""
    cwd = _SEEN_CWD or Path.cwd()
    rc, out = _run([BEAGLE_BIN, "pursuit", "status", "--root", str(cwd)], cwd, timeout=15.0)
    if rc == 127:
        return "/pursuit-view: beagle not found on PATH."
    return out or f"(beagle pursuit status exited {rc})"


# --------------------------------------------------------------------------- #
# orientation (frame, not a turn)
# --------------------------------------------------------------------------- #


#: How the driving session spends its turns. A small model that reads the
#: reference or works out the design here thinks itself past its output limit
#: (30K characters of reasoning, then nothing, in every ITC trial); a worker
#: that does it burns only its own step's budget.
DRIVER_STEERS_NOTE = (
    "You steer; sub-agents think. Do not fetch or read the reference, and do not "
    "work out the design or the algorithm in this session: a question you would "
    "have to think hard about is a task. Send it as a step, with the reference (its "
    "URL) and the one question in the step's notes, or split it with pursuit_plan. "
    "Keep your turns short: pick the next task, write its check, dispatch it, read "
    "the verdict."
)

#: Where a worker's tests come from. A small model that writes the code and its
#: tests in one sitting makes them agree with each other, not with the reference
#: (the ITC trial with qwen: wrong fork, join and event, and every test passed).
#: How a tests-only (known-answers) task is shown to refuse; said instead of
#: "import the code", which such a task has no code to do. It names only the data
#: test: run R06's text also described the cases test's import of unwritten code,
#: and a worker put that import into the check's test.
TESTS_ONLY_PROOF_NOTE = (
    "This scope holds only tests and data, so the data file's absence is the proof: "
    "the check must run a test that reads the data file this task writes, so that "
    "taking the file away makes it fail (e.g. tests/test_case_data.py must fail when "
    "tests/cases.json is removed). That test reads only the data file."
)

CASES_FIRST_NOTE = (
    "Cases first. Make the first milestone after the reference the known answers: a "
    "sub-agent reads the reference and writes, without any implementation, (a) a data "
    "file of small inputs and the exact results the reference gives for them, each "
    "citing where in the reference it comes from (e.g. `tests/cases.json`), and (b) "
    "a test that runs every case against the code (e.g. `tests/test_cases.py`). That "
    "test imports the module later tasks will write, by name (e.g. `from <package> "
    "import …`), and defines no class or helper of its own: it fails with ImportError "
    "until the code exists. Its done_when checks only the data, with a small "
    "test of the file itself (e.g. `python3 -m pytest -q tests/test_case_data.py`: "
    "every case has its inputs, its result and its citation, and there are enough "
    "of them); not `python3 -m json.tool`, which passes once the file parses and is "
    "refused as a check. It passes `locks` with the data file and both tests. Once it "
    "closes they are locked, and every later task's done_when runs the cases test."
)

#: Commits need an identity; a model that meets "Please tell me who you are"
#: makes one up (the qwen trial set "Developer <dev@example.com>").
GIT_IDENTITY_NOTE = (
    "Never set a git identity (`git config user.name` / `user.email`, in the repo or "
    "globally). If a commit fails for want of one, stop and tell the user."
)

#: How a worker takes on a hard part. Its reasoning is lost when a reply runs
#: out of room, so a thought only survives once it is written to a file.
PIECE_BY_PIECE_NOTE = (
    "Hard parts, one piece per turn. When the task needs real working out (an "
    "algorithm, an encoding, an invariant), do not try to solve it whole in one "
    "reply: that runs out of room and loses all of it. Instead:\n"
    "1. Write the concrete cases first: the smallest inputs and their exact "
    "expected results, as test cases or a table in a file, simplest first.\n"
    "2. In a new turn, read them back and find the rule that produces them; write "
    "the rule down, as code or a comment.\n"
    "3. Run the cases against it, and fix the rule from the first failure.\n"
    "If you find yourself going round the same question, stop: write down what you "
    "know and the one open question, and answer only that in your next turn.\n"
    "Stay inside your task: build what its brief asks, not the rest of the goal."
)


def _goal_section(goal_file: Path, *, worker: bool = False) -> str | None:
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
    if worker:
        lines += ["", "You are a sub-agent doing one task of it; your brief says which.", ""]
        return "\n".join([*lines, PIECE_BY_PIECE_NOTE, GIT_IDENTITY_NOTE])
    lines += [
        "",
        "How to work it — this session steers, sub-agents do the work:",
        "1. `pursuit_step` with no arguments shows the next ready task.",
        "2. `pursuit_step` again with that task, its `criteria`, a `done_when` (one "
        "command, no shell operators, that exits 0 only when the task is done, such as "
        "`python3 -m pytest -q tests/test_x.py`), and its `scope`: a sub-agent does the "
        "work, the check runs, and the task closes when it passes.",
        "3. Repeat until nothing is ready. A task too big for one sub-agent: split it "
        "into steps with `pursuit_plan` first.",
        "Do not edit project files in this session; put what you want changed in the "
        "step's `notes`.",
        DRIVER_STEERS_NOTE,
        CASES_FIRST_NOTE,
        GIT_IDENTITY_NOTE,
        "",
        # No slash commands here: run 11c's driver read `/pursuit-run` in this
        # line as something to run, and ran it through bash.
        "For the rarer moves — spawning another route, binding a container's check, "
        "gates — call the `pursuit_driver` tool.",
    ]
    return "\n".join(lines)


def _unfounded_section(root: Path) -> str | None:
    """Orientation for a project with no pursuit yet, or None with no driver.

    Without it a model asked to set beagle up gets no frame at all until the
    goal file exists — and the setup skill, written for Claude Code, has it
    hunt for a CLI shim and look for a `/pursuit` it cannot type.
    """
    if _driver_file(PURSUIT_COMMAND) is None:
        return None
    lines = ["This project is not a beagle pursuit yet."]
    if (root / BIN_REL).exists():
        lines.append(
            f"- `beagle` on PATH is already this checkout's CLI ({root / BIN_REL}); skip "
            "the setup skill's step that links it. Never link or run a `beagle` from "
            "`~/.claude/plugins/cache/...`: that is another release, with other commands."
        )
    lines += [
        "- Found it first. Asked to set beagle up and build something, call "
        "`pursuit_found` as your first move, before you read any reference or design "
        "anything: reading the reference and choosing a design are themselves "
        "milestones, which sub-agents do. Your part is to steer, a few steps at a time.",
        "- Pass `pursuit_found` the user's goal, their acceptance criteria and the "
        "milestones you can already name. The goal and the criteria are the user's: use "
        "their words. If they gave none, ask, unless they told you to decide yourself "
        "('use your judgement', 'without further discussion'). Then draft the criteria "
        "from their request and set `user_delegated`.",
        "- It runs `git init` if the project is not a repository yet.",
        "- Then work it with `pursuit_step`, which runs each task in a sub-agent. A "
        "reference the work needs (a URL, a paper) goes in the step's notes, or is "
        "saved inside the project; a sub-agent cannot see your context.",
        f"- {DRIVER_STEERS_NOTE}",
        f"- {CASES_FIRST_NOTE}",
        f"- {GIT_IDENTITY_NOTE}",
        "- The `pursuit_driver` tool loads the full written procedure, for what these "
        "tools do not cover.",
        "- `beagle init` places templates; read one when you need it, not all of them.",
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


def _prepend_path(directory: Path) -> None:
    """Put `directory` first on PATH, once, for this process and its children."""
    entries = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p and p != str(directory)]
    os.environ["PATH"] = os.pathsep.join([str(directory), *entries])


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
    trees = (
        ("commands", _LAYOUT.commands_dir),
        ("agents", _LAYOUT.agents_dir),
        ("bin", _LAYOUT.bin_dir),
    )
    for name, target in trees:
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
    global _SEEN_CWD, _PLUGIN_ROOT, _LAYOUT, _DRIVERS_DIR, _ENDED_RUN_NOTE
    # Every beagle this process starts, hooks and the bash tool's alike,
    # inherits this, so beagle can tell it is not under Claude Code.
    os.environ[HOST_ENV] = "tau"
    _LAYOUT = resolve_layout(BEAGLE)
    _DRIVERS_DIR = tau.context.paths.home / DRIVERS_REL
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
            # The checkout's own CLI goes first on PATH, ahead of any `beagle`
            # a stale plugin cache left linked in ~/.local/bin, so the skills
            # and the CLI they name are always the same release — and no
            # model has to find and link a shim before its first command.
            if (root / BIN_REL).exists():
                _prepend_path(root / "bin")
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
    if _driver_file(PURSUIT_COMMAND) is not None and not _is_worker():
        tau.register_tool(
            AgentTool(
                name="pursuit_driver",
                label="pursuit_driver",
                description=(
                    "Load beagle's pursuit driver — what the user's `/pursuit` or `/pursuit-run` "
                    "command sends — and follow it. Call this when the user asks in prose to "
                    "found a pursuit, work one, or use the pursuit or pursuit-run loop. Slash "
                    "commands are not shell commands: never run `/pursuit` through bash."
                ),
                parameters=DRIVER_PARAMETERS,
                execute_fn=make_driver_tool(),
                prompt_snippet="Load the /pursuit or /pursuit-run driver when asked for a pursuit.",
                prompt_guidelines=(
                    "Founding a pursuit is pursuit_driver with command 'pursuit'; its goal and "
                    "criteria are the user's, read back to them before .beagle/pursuit.toml is "
                    "written.",
                ),
            )
        )
    tau.register_command(
        "pursuit-view",
        _command_pursuit_view,
        description="Show the current pursuit's goal, counts and ready set (no model).",
    )

    # 4. The headless step-executor: the blocking fallback for when the
    #    tau-subagents extension (background `agent` tool) is not loaded. A
    #    worker is never given it: one step does not start another.
    if not _is_worker():
        tau.register_tool(
            AgentTool(
                name="pursuit_dispatch",
                label="pursuit_dispatch",
                description=(
                    "Delegate one well-specified pursuit task to a headless step-executor (a "
                    "nested `tau -p`, inheriting this session's model unless a Tau model id is "
                    "given). Pass the brief ('run `beagle pursuit brief <task>` and do what it "
                    "says'). Returns the executor's report; the caller still runs `beagle "
                    "pursuit close`. Use for roughly ten tool calls or more of mechanical work, "
                    "not one-line edits or open-ended exploration."
                ),
                parameters=DISPATCH_PARAMETERS,
                execute_fn=make_dispatch(),
                prompt_snippet="Delegate one pursuit task to a headless step-executor sub-agent.",
                prompt_guidelines=(
                    "Hand pursuit_dispatch a self-contained brief; the worker sees no "
                    "conversation.",
                    "The worker does the work; YOU run `beagle pursuit close` after its "
                    "--done-when.",
                ),
            )
        )

    # 4b. The steering tools: found, plan and step a pursuit without reading
    #     the driver text, each step's work done by a step-executor. The
    #     driver session keeps its hands off the work; a worker is the work.
    if not _is_worker():
        tau.register_tool(
            AgentTool(
                name="pursuit_found",
                label="pursuit_found",
                description=(
                    "Found a beagle pursuit: write the user's goal and acceptance criteria, "
                    "and split the goal into milestone tasks. Call it once, when the user asks "
                    "for a pursuit or for beagle to run their project."
                ),
                parameters=FOUND_PARAMETERS,
                execute_fn=make_found_tool(
                    on_founded=_pin_founded(tau), interactive=lambda: tau.context.has_ui
                ),
                prompt_snippet="Found a pursuit: goal, criteria, milestones.",
                prompt_guidelines=(
                    "The pursuit's goal and criteria are the user's: use their words, and set "
                    "user_confirmed only when they gave or approved them. When they told you "
                    "to decide the details yourself, draft the criteria from their request "
                    "and set user_delegated instead of asking.",
                ),
            )
        )
        tau.register_tool(
            AgentTool(
                name="pursuit_plan",
                label="pursuit_plan",
                description=(
                    "Break a pursuit task into steps (each '<title>::<why>'), or add steps "
                    "under a milestone. Use it when a task is too big for one sub-agent."
                ),
                parameters=PLAN_PARAMETERS,
                execute_fn=make_plan_tool(),
                prompt_snippet="Split a pursuit task into steps.",
            )
        )
        tau.register_tool(
            AgentTool(
                name="pursuit_step",
                label="pursuit_step",
                description=(
                    "Work the pursuit one task at a time. With no arguments: shows the next "
                    "ready task. With task, criteria, done_when and scope: opens it, has a "
                    "sub-agent do the work, runs the check, and closes the task when the check "
                    "passes. Call it again until nothing is ready."
                ),
                parameters=STEP_PARAMETERS,
                execute_fn=make_step_tool(),
                prompt_snippet="Run the next pursuit task in a sub-agent; close it on its check.",
                prompt_guidelines=(
                    "In a pursuit, project work goes through pursuit_step; this session plans "
                    "and checks, sub-agents edit.",
                ),
            )
        )
        tau.on("tool_call", make_driver_edit_guard())
        tau.on("tool_call", make_driver_pursuit_guard())
        tau.on("tool_call", make_driver_reference_guard())

    # 5. Enforce the pursuit ground truth on every tool call, and bridge
    #    beagle's Bash PreToolUse hooks onto the same seam.
    tau.on("tool_call", make_guard())
    tau.on("tool_call", make_record_guard())
    tau.on("tool_call", make_bash_hooks())
    if _is_worker():
        tau.on("tool_call", make_worker_pursuit_guard())
        tau.on("tool_call", make_worker_scope_guard())
    else:
        tau.on("tool_call", make_scope_guard())
        tau.on("tool_result", make_stopped_worker_note())
    # After the scope guard: a reset in a worker's scope is a race first.
    tau.on("tool_call", make_history_guard())

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
        tau.on("input", _note_prompt)
        tau.on("agent_start", make_found_first_steer(tau))
        tau.on("compaction_end", make_state_after_compaction(tau))
        tau.add_compaction_instructions(PURSUIT_COMPACTION_FOCUS)
        tau.on("tool_call", make_found_first_gate())
        tau.on("agent_start", _note_run_start)
        tau.on("agent_end", _note_run_end)
        tau.on("agent_settled", make_stop_hooks(tau))
        tau.on("agent_start", _reset_stop_gate)
        tau.on("turn_end", make_stop_gate(tau))
        tau.on("agent_settled", make_wakeup_delivery(tau))
        tau.on("session_shutdown", lambda event, context: _void_wakeup())
        # Workers do not outlive their session, so a run this session drives
        # ends with it; the next session to start sees that and retires it.
        tau.on("session_start", _on_driver_session_start)
        tau.on("session_shutdown", lambda event, context: _end_driver())

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
        section = _goal_section(goal, worker=_is_worker())
        # loop-report is the SessionStart hook: what a run left in flight, and
        # the driver's core while one is. The system prompt outlives
        # compaction, so this also covers what the hook re-prints after one.
        report = ""
        if not _is_worker():
            # Before loop-report, so it does not tell this session to stand
            # down for a driver that has ended.
            _ENDED_RUN_NOTE = _retire_gone_driver(goal.parent.parent)
            if _ENDED_RUN_NOTE is not None:
                tau.on("session_start", _notify_retired_once())
            report = _session_start_report("loop-report", goal.parent.parent)
        if section and report:
            section = f"{section}\n\nAt session start, `beagle hook loop-report` said:\n\n{report}"
        if section:
            tau.add_prompt_section("Beagle pursuit", section)
    elif _PLUGIN_ROOT is not None and not _is_worker():
        section = _unfounded_section(_PLUGIN_ROOT)
        if section:
            tau.add_prompt_section("Beagle", section)
