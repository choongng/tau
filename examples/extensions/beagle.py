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
  Before a pursuit is founded the driver still runs `pursuit close`; once it
  is, the tool is refused and pursuit_step closes. It only does the work and
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
import bisect
import builtins
import contextlib
import fnmatch
import functools
import hashlib
import html.parser
import importlib.util
import itertools
import json
import math
import os
import re
import shlex
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Callable, Collection, Mapping
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
from tau_coding.tool_buffers import WINDOW_LINES

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

#: The worker's output limit in tokens, which sizes the parts a call cut off at
#: it is told to write in. Runs R15 and R33 were cut off at 8192.
WORKER_OUTPUT_TOKENS_ENV = "BEAGLE_TAU_WORKER_OUTPUT_TOKENS"
DEFAULT_WORKER_OUTPUT_TOKENS = 8192

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
#: The tail of the last `pursuit_step` result per task, for the note after a
#: compaction: run R10's summary paraphrased a refusal and the driver never
#: called pursuit_step again.
_LAST_STEP_RESULT: dict[str, str] = {}
LAST_STEP_RESULT_CHARS = 2000
#: The driver's non-`pursuit_` tool calls in a row since the goal existed.
_OFF_PURSUIT_CALLS = 0
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


def _run(
    cmd: list[str], cwd: Path | None, timeout: float, stdin: str = "", limit: str | None = None
) -> tuple[int, str]:
    """Run a short capture command, failing soft (rc!=0 with the reason inline).

    stdin is always fed, never inherited: under the TUI it is the terminal, and
    a beagle hook reads its payload from it. The command leads its own process
    group, under `limit` when one is given, and a timeout kills the group.
    """
    if limit is not None and shutil.which(cmd[0]) is None:
        return 127, f"{cmd[0]}: not found on PATH"
    try:
        proc = subprocess.Popen(
            _capped(cmd, limit),
            cwd=str(cwd) if cwd else None,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
    except FileNotFoundError:
        return 127, f"{cmd[0]}: not found on PATH"
    try:
        stdout, stderr = proc.communicate(stdin, timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_group(proc, limit)
        return 124, f"{cmd[0]}: timed out after {timeout:.0f}s"
    out = (stdout or "") + (("\n" + stderr) if stderr else "")
    note = _killed_note(proc.returncode, limit)
    out = f"{out.strip()}\n{note}" if note else out
    return proc.returncode, out.strip()


def _kill_group(proc: subprocess.Popen[str], limit: str | None) -> None:
    """Kill `proc`'s process group, and its memory scope's leftovers, then reap it.

    A check beagle rehearses runs in a session of its own, outside the group;
    under a cap it is still in the scope's cgroup, which `cgroup.kill` empties.
    """
    scope = _own_scope(proc.pid) if limit is not None else None
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(proc.pid, signal.SIGKILL)
    if scope is not None:
        with contextlib.suppress(OSError):
            (scope / "cgroup.kill").write_text("1")
    with contextlib.suppress(subprocess.TimeoutExpired):
        proc.wait(timeout=10)
    for stream in (proc.stdin, proc.stdout, proc.stderr):
        if stream is not None:
            with contextlib.suppress(OSError):
                stream.close()


def _own_scope(pid: int) -> Path | None:
    """The cgroup directory of the transient scope `pid` runs in, or None.

    Only a `run-*.scope` that is not this process's own cgroup qualifies, so
    the kill can never reach tau itself.
    """

    def cgroup(of: str) -> str:
        try:
            text = Path(f"/proc/{of}/cgroup").read_text()
        except OSError:
            return ""
        return next((line[3:] for line in text.splitlines() if line.startswith("0::")), "")

    path = cgroup(str(pid))
    name = path.rsplit("/", 1)[-1]
    if not (name.startswith("run-") and name.endswith(".scope")) or path == cgroup("self"):
        return None
    return Path("/sys/fs/cgroup") / path.lstrip("/")


# --------------------------------------------------------------------------- #
# ground-truth guard
# --------------------------------------------------------------------------- #

_WRITE_TOKEN = re.compile(r"(>>|>|tee\b|\bsed\b|\btruncate\b|\bdd\b|\binstall\b)")
_HEREDOC = re.compile(r"(?<!<)<<(-?)\s*(['\"]?)([A-Za-z_][\w.-]*)\2")
#: Words that run the command after them: skipped to find the real one.
_WRAPPERS = frozenset(
    {"sudo", "env", "command", "nice", "nohup", "time", "exec", "builtin", "timeout"}
)
#: Wrapper options that take the next word as their value.
_WRAPPER_VALUE_OPTIONS = frozenset(
    {"-n", "--adjustment", "-u", "--unset", "-C", "--chdir", "-s", "--signal", "-k"}
    | {"--kill-after", "-g", "--group", "-U", "--user"}
)
_SHELLS = frozenset({"sh", "bash", "zsh", "dash"})
_GLOB_CHARS = frozenset("*?[")


def _strip_heredocs(command: str) -> str:
    """`command` with every here-document body removed, keeping the `<<` lines.

    A body is data fed to a command, not shell: `cat <<EOF > notes.md` followed
    by a paragraph that mentions `> pursuit.toml` writes only notes.md.
    """
    return _split_heredocs(command)[0]


def _split_heredocs(command: str) -> tuple[str, list[tuple[str, str]]]:
    """`command` without its here-document bodies, and each body with the line
    that opened it."""
    kept: list[str] = []
    bodies: list[tuple[str, str]] = []
    pending: list[tuple[str, bool, str, list[str]]] = []
    for line in command.split("\n"):
        if pending:
            delimiter, dash, opener, body = pending[0]
            if (line.lstrip("\t") if dash else line).strip() == delimiter:
                pending.pop(0)
                bodies.append((opener, "\n".join(body)))
            else:
                body.append(line)
            continue
        kept.append(line)
        pending += [(m.group(3), bool(m.group(1)), line, []) for m in _HEREDOC.finditer(line)]
    return "\n".join(kept), bodies


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


#: `uv init`/`uv add` options that take a value, so it is not read as a directory.
_UV_VALUE_OPTIONS = frozenset(
    {
        *("--name", "--python", "-p", "--build-backend", "--vcs", "--author-from"),
        *("--description", "--group", "--optional", "--extra", "--index", "--index-url"),
        *("--default-index", "--extra-index-url", "-r", "--requirements", "--rev", "--tag"),
        *("--branch", "--package", "--script", "--cache-dir", "--config-file", "--color"),
        *("--marker", "-m", "--bounds"),
    }
)


def _unwrapped(argv: list[str]) -> list[str]:
    """`argv` without its leading `NAME=value` words and `_WRAPPERS`.

    A wrapper's own options go with it, and `timeout` its duration, so
    `X=1 env -u Y timeout 5 bash -c '...'` is read from `bash`.
    """
    while argv and ("=" in argv[0] and not argv[0].startswith("=") or argv[0] in _WRAPPERS):
        wrapper, argv = argv[0], argv[1:]
        while argv and argv[0].startswith("-") and argv[0] != "-":
            option, argv = argv[0], argv[1:]
            if option in _WRAPPER_VALUE_OPTIONS and argv:
                argv = argv[1:]
        if wrapper == "timeout" and argv:
            argv = argv[1:]
    return argv


def _command_targets(argv: list[str], cwd: Path) -> list[str] | None:
    """The paths one simple command (argv, redirects removed) writes."""
    argv = _unwrapped(argv)
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
    if name == "uv" and args and args[0] in ("init", "add"):
        # Run R15: W1's `uv init itc_clocks` made itc_clocks/ outside its scope, unseen.
        rest = _positional(args[1:], _UV_VALUE_OPTIONS)
        if args[0] == "init" and rest:
            return [rest[0]]
        return ["pyproject.toml"]
    if name == "git" and args:
        sub, sub_args = args[0], args[1:]
        if sub == "checkout" and "--" in sub_args:
            return sub_args[sub_args.index("--") + 1 :]
        if sub == "restore":
            return _positional(sub_args, frozenset({"-s", "--source"}))
        if sub in ("stash", "clean") or (sub == "reset" and "--hard" in sub_args):
            return ["."]  # the whole work tree
    return []


def _cd_into(segment: list[str], here: Path) -> Path:
    """The directory a simple `cd` command, as tokens, moves to from `here`."""
    dest = next((a for a in segment[1:] if not a.startswith("-")), "~")
    return Path(os.path.normpath(here / Path(dest).expanduser()))


def _cwd_after_cd(command: str, cwd: Path) -> Path:
    """The directory the leading chain of `cd` commands in `command` leaves.

    Run R21: W2's `cd /tmp/itc && python3 - <<PY open('explore.py','w')` was
    refused as if explore.py were a project file.
    """
    tokens = _shell_tokens(command)
    if tokens is None:
        return cwd
    here = cwd
    segment: list[str] = []
    redirect = False
    for token in [*tokens, ";"]:
        if redirect and not _is_operator(token):
            redirect = False  # a redirect's target, not an argument
            continue
        redirect = False
        if not _is_operator(token):
            segment.append(token)
            continue
        if "<" in token or ">" in token:
            if segment and segment[-1].isdigit():
                segment.pop()
            redirect = True
            continue
        if not segment or segment[0] != "cd":
            break
        here = _cd_into(segment, here)
        segment = []
    return here


def _bash_write_targets(command: str, cwd: Path) -> list[Path] | None:
    """Every path a bash command would write, resolved; None if unparseable.

    Deliberately narrow: a redirect target, a `tee` argument, a `sed -i` file,
    a `cp`/`mv`/`install`/`ln` destination (and what `mv` removes), `dd of=`,
    `rm`/`truncate`, the directory `uv init <dir>` creates (pyproject.toml for
    `uv add` or a bare `uv init`), and the `git` verbs that rewrite tracked files (`stash`,
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
        # Run R22: `BEAGLE_TAU_DRIVER_EDITS=1 bash -c '...'` hid its script.
        segment = _unwrapped(segment)
        if segment and segment[0] == "cd":
            here = _cd_into(segment, here)
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
        # A link in the project is its own path, and also where it points.
        for path in {_resolved(root / text), _own_path(root / text, root)}:
            if target == path or path in target.parents or target in path.parents:
                return entry
    return None


def _write_targets(
    tool: str, args: Mapping[str, Any], cwd: Path, *, resolve: bool = True
) -> list[Path]:
    """The paths an edit, write or bash call writes; [] for anything else.

    With `resolve=False` they are absolute and normalized but links are not
    followed, so a symlink names itself rather than what it points at.
    """
    if tool in ("write", "edit"):
        raw = args.get("path")
        if not resolve and isinstance(raw, str) and raw.strip():
            return [Path(os.path.normpath(cwd / Path(raw).expanduser()))]
        target = _goal_path_from_args(args, cwd)
        return [target] if target is not None else []
    if tool == "bash":
        found = _bash_write_targets(str(args.get("command", "")), cwd) or []
        return [_resolved(t) for t in found] if resolve else found
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


def _worker_output_tokens() -> int:
    """The worker's output limit in tokens: env, else DEFAULT_WORKER_OUTPUT_TOKENS."""
    raw = os.environ.get(WORKER_OUTPUT_TOKENS_ENV, "").strip()
    try:
        return max(1, int(raw)) if raw else DEFAULT_WORKER_OUTPUT_TOKENS
    except ValueError:
        return DEFAULT_WORKER_OUTPUT_TOKENS


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
    #: How its last assistant message ended, and that message's text or an earlier one's.
    stop_reason: str | None = None
    last_words: str = ""
    #: The memory cap the run was killed at, when SIGKILL ended it under one.
    killed_at: str | None = None
    #: The command of the tool call its last assistant message made, if any.
    pending_command: str = ""

    @property
    def unreported(self) -> bool:
        """Whether it ended without a report: a problem, a stub, or mid-call (R27 W7)."""
        return (
            self.problem is not None
            or self.report.startswith(NO_REPORT)
            or self.stop_reason == "toolUse"
        )

    @property
    def shown_report(self) -> str:
        """The report as the driver reads it, with the transcript's path."""
        if self.transcript is None:
            return self.report
        return f"{self.report}\n\n(Worker transcript: {self.transcript})"


def _capped_report(run: _WorkerRun) -> str:
    """`run.shown_report` cut to its first and last lines, for a step result.

    The cut names the worker transcript, which holds the whole report. The
    stub of a worker that wrote no report is short already, and kept whole.
    """
    if run.report.startswith(NO_REPORT):
        return run.shown_report
    lines = run.report.strip("\n").splitlines()
    head_lines = lines[:STEP_REPORT_HEAD_LINES]
    tail_lines = lines[STEP_REPORT_HEAD_LINES:][-STEP_REPORT_TAIL_LINES:]
    head = "\n".join(head_lines)[:STEP_REPORT_END_CHARS]
    tail = "\n".join(tail_lines)[-STEP_REPORT_END_CHARS:]
    if len(head) + len(tail) + (1 if tail_lines else 0) >= len("\n".join(lines)):
        return run.shown_report
    where = (
        f"the whole report is in the worker transcript, {run.transcript}"
        if run.transcript is not None
        else "the worker left no transcript"
    )
    return f"{head}\n[... {len(lines)}-line report cut; {where}]\n{tail}"


#: A project-relative file path in prose: at least one directory and a
#: suffix that starts with a letter, not inside an absolute path or a URL.
_REPORT_PATH = re.compile(
    r"(?<![\w./~$*:-])((?:[\w][\w.-]*/)+[\w][\w-]*(?:\.[\w-]+)*\.[A-Za-z][A-Za-z0-9]{0,7})"
    r"(?![\w/-])"
)
#: A file name with or without a directory, for telling a preamble from notes.
_REPORT_FILE_NAME = re.compile(r"(?<![\w.])[\w][\w./-]*\.[A-Za-z][A-Za-z0-9]{0,7}(?![\w/-])")
#: A report shorter than this that names no file is a preamble
#: (R17 W3: "I'll start by reading the reference materials.").
PREAMBLE_REPORT_CHARS = 300


def _report_paths(report: str, root: Path) -> list[str]:
    """The project-relative file paths a report names, in order, once each."""
    seen: list[str] = []
    for match in _REPORT_PATH.finditer(report):
        rel = match.group(1)
        if rel in seen or rel.split("/", 1)[0] in (".beagle", ".git", "tmp"):
            continue
        if not (root / rel).resolve().is_relative_to(root.resolve()):
            continue
        seen.append(rel)
    return seen


def _report_missing_paths(report: str, root: Path) -> str:
    """One line per project path the report names that is not on disk (R17 W4/W9/W11)."""
    if report.startswith(NO_REPORT):
        return ""
    return "".join(
        f"The report names {rel}, which is not on disk.\n"
        for rel in _report_paths(report, root)
        if not (root / rel).exists()
    )


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


#: How tau's repeat breaker words a refused call's tool result, and the stop.
_REFUSED = "Not run: "
_BREAKER_STOP = "Not run, and the run is stopped"
#: How the refusal of a call cut off at the output limit begins (`_truncated_call`).
CUT_OFF_REFUSAL = "This call's arguments were cut off"
#: The turns over a run cut off at the output limit that end the worker.
WORKER_CUT_OFFS = 2
CUT_OFF_TWICE = "cut off twice at the output limit"
#: How tau words the tool result of a call an extension blocked.
_BLOCKED = "Tool call blocked: "
#: The countdown sentence tau appends to each refusal's problem.
_REFUSAL_COUNTDOWN = re.compile(r"\s*\d+ more refused calls? in a row stop the run\.\s*$")


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
    #: The command (or tool name) of the last assistant message's last tool call.
    pending_command: str = ""
    error: str | None = None
    #: The problem in the last tool result tau refused a call with, if any.
    refusal: str | None = None
    #: Whether tau's breaker stopped the run after refused calls in a row.
    stopped: bool = False
    #: How many assistant turns in a row, up to the last, ended at the output-token
    #: limit. Audit 7: a count over the whole run blamed the limit for a wall a
    #: worker hit long after its last cut-off turn. Run R27: a turn whose call was
    #: refused as cut off counts too, since the provider reported it as "toolUse".
    length_stops: int = 0
    #: How many turns over the whole run ended at the output limit, in a row or
    #: not. Run R33: W2 was cut off three times, each followed by a normal turn.
    cut_offs: int = 0
    #: The count before the last turn, and whether that turn was counted as cut off.
    _before_turn: int = 0
    _turn_cut: bool = False

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
        if isinstance(message, dict) and message.get("role") == "toolResult":
            self._note_refusal(message.get("content"))
            return
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
        calls = [block for block in blocks if block.get("type") == "toolCall"]
        arguments = calls[-1].get("arguments") if calls else None
        command = arguments.get("command") if isinstance(arguments, dict) else None
        self.pending_command = (
            command if isinstance(command, str) else str(calls[-1].get("name", "")) if calls else ""
        )
        self.thinking = "\n".join(
            str(block.get("thinking", "")) for block in blocks if block.get("type") == "thinking"
        ).strip()
        stop = message.get("stopReason")
        self.stop_reason = stop if isinstance(stop, str) else None
        self._before_turn = self.length_stops
        self._turn_cut = stop == "length"
        self.length_stops = self._before_turn + 1 if self._turn_cut else 0
        self.cut_offs += self._turn_cut
        error = message.get("errorMessage")
        self.error = str(error) if stop == "error" and error else None

    def _note_refusal(self, content: object) -> None:
        """Track tau's refusals: the last one's problem, the breaker's stop, cut-off calls."""
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = "".join(
                str(block.get("text", ""))
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            )
        else:
            return
        text = text.strip()
        if text.removeprefix(_BLOCKED).startswith(CUT_OFF_REFUSAL) and not self._turn_cut:
            self._turn_cut = True
            self.length_stops = self._before_turn + 1
            self.cut_offs += 1
        if text.startswith(_BREAKER_STOP):
            self.stopped = True
        elif text.startswith(_REFUSED):
            problem = text.removeprefix(_REFUSED)
            self.refusal = _REFUSAL_COUNTDOWN.sub("", problem).strip()

    def final_report(self, stderr: str) -> str:
        """The report for the driver: always short, never the raw event stream."""
        report = self.report
        if self.stopped:
            last = f"; the last refusal: {self.refusal}" if self.refusal else ""
            stopped = f"(the sub-agent was stopped by tau after repeated refused calls{last})"
            report = f"{report}\n\n{stopped}".strip()
        elif self.error:
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
    return "\n".join([stub, *_scope_changes(cwd, scope)])


def _report_before_markup(report: str, cwd: Path, scope: list[str]) -> str:
    """A report that ends in raw tool-call markup: the text before it, or the stub.

    Run R15's W2 wrote a whole report and then `<tool_call><function=bash>…`;
    replacing all of it told the driver the worker wrote nothing. Audit 7: a
    short text is kept too; the changed-files lines after it say what was done.
    """
    match = _TOOL_CALL_MARKUP.search(report)
    before = report[: match.start()].strip() if match else report.strip()
    if not before:
        return _unreported_changes(cwd, scope)
    return "\n".join(
        [before, "\n(The report ended on a raw tool call, cut here.)", *_scope_changes(cwd, scope)]
    )


def _helpers_left_in_scope(root: Path, scope: list[str], check: str) -> str:
    """A line naming each untracked .py in `scope` that no test imports and the
    check does not name, or "".

    Run R31: W2 saved a generator script beside the data it wrote, and the driver
    first heard of it from 51 refusals that counted it as the code under test.
    """
    if not scope:
        return ""
    rc, out = _run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--", *scope],
        root,
        timeout=30.0,
    )
    new = {rel for rel in out.split("\0") if rel.endswith(".py")} if rc == 0 else set()
    if not new:
        return ""
    _, helpers = _judged_sources(_scope_entries(scope, root), root, check)
    left = [rel for rel in helpers if rel in new]
    if not left:
        return ""
    return (
        f"Helper left in scope: {', '.join(left)}: new, untracked, no test imports it "
        "and the check does not name it; delete it or leave it out of scope.\n"
    )


def _scope_changes(cwd: Path, scope: list[str]) -> list[str]:
    """What git sees changed in `scope`: the diff stat and the changed or new files."""
    rc, stat = _run(["git", "diff", "--stat", "--", *scope], cwd, timeout=30.0)
    changed = [rel for rel in _changed_files(cwd) if _in_scope(rel, scope, cwd)]
    lines: list[str] = []
    if rc == 0 and stat.strip():
        lines.append(f"git diff --stat:\n{stat.strip()}")
    if changed:
        lines.append("Changed or new in its scope: " + ", ".join(changed))
    elif rc == 0 and not stat.strip():
        lines.append("git diff --stat: no change.")
    return lines


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
        if events.cut_offs >= WORKER_CUT_OFFS:
            # Run R33: W2 was cut off three times, not in a row, and ran to the wall.
            with contextlib.suppress(ProcessLookupError):
                proc.kill()
            with contextlib.suppress(Exception):
                await talk
            ended = (
                f"(the sub-agent was ended: {CUT_OFF_TWICE}. Split the task or have the "
                "notes say to write in parts.)"
            )
            return _WorkerRun(
                returncode=proc.returncode,
                report=f"{events.report}\n\n{ended}".strip(),
                spent=events.spent,
                transcript=transcript,
                stop_reason="length",
                last_words=events.report,
            )
        if signal is not None and signal.is_cancelled():
            problem = "cancelled; the worker was killed and its partial work is in the tree."
            break
        remaining = deadline - loop.time()
        if remaining <= 0:
            problem = f"the step-executor exceeded its wall-clock budget of {timeout:.0f}s and " + (
                f"was killed: its last {events.length_stops} turn(s) ended at the output limit, "
                "writing more than one reply holds. Split the task, or say in the notes "
                "to write files in smaller pieces."
                if events.length_stops
                else f"was killed. Split the task, or lower its turn cap ({WORKER_MAX_TURNS_ENV})."
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
    if note and events.stop_reason == "toolUse" and events.pending_command:
        note += f" It was killed while its own command `{events.pending_command}` was running."
    if _TOOL_CALL_MARKUP.search(events.report):
        report = _report_before_markup(events.report, cwd, scope or [])
    else:
        report = events.final_report(f"{stderr}\n{note}".strip() if note else stderr)
    if note and note not in report:
        report = f"{report}\n\n{note}".strip()
    return _WorkerRun(
        returncode=proc.returncode,
        report=report,
        spent=events.spent,
        transcript=transcript,
        stop_reason=events.stop_reason,
        last_words=events.report,
        killed_at=limit if note else None,
        pending_command=events.pending_command,
    )


#: How much of an unreported worker's last text a step result quotes.
UNREPORTED_WORDS_CHARS = 300


def _unreported_runs(runs: list[tuple[int, _WorkerRun, list[str]]], total: int) -> str:
    """One paragraph per run before the last that ended without a report.

    Run R27: W7 ended on a bash call with no report, having changed both test
    files and found, in text, a contradiction in the criteria; the step result
    after W8 showed only W8's report. Run R30: W4-W7 were killed at the memory
    cap while their own test command ran, and the result said only
    "stopReason=toolUse"; such a run names the kill and the command.
    """
    lines = []
    for number, run, changes in runs:
        if number >= total:
            continue
        why = run.problem or (
            f"stopReason={run.stop_reason}" if run.stop_reason else "no assistant message"
        )
        changed = "; ".join(changes) or "nothing git sees"
        words = " ".join(run.last_words.split())
        cut = words[:UNREPORTED_WORDS_CHARS] + ("…" if len(words) > UNREPORTED_WORDS_CHARS else "")
        ended = (
            f"was killed at its {run.killed_at} memory cap while its own command "
            f"`{run.pending_command}` was running"
            if run.killed_at and run.stop_reason == "toolUse" and run.pending_command
            else f"ended without a report ({why})"
        )
        lines.append(
            f"Run {number} of {total} {ended}; it changed: {changed}; "
            f"its last words: {cut or '(none)'}\n\n"
        )
    return "".join(lines)


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


def _dispatch_footer(session_cwd: Path) -> str:
    """The line after a worker's report: who closes the task, and with what.

    Once the session's pursuit is founded the driver guard refuses a bash
    `beagle pursuit close`, so the line names pursuit_step instead (T0209's
    report: the footer still sent the driver to the refused bash verb).
    """
    if _find_goal(session_cwd) is not None:
        return (
            "\n\n— The worker closes nothing, and this dispatch recorded nothing. In a "
            "founded pursuit pursuit_step does the task: it has a sub-agent do it, runs its "
            "check and closes it."
        )
    return (
        "\n\n— YOU run the close, not the worker: `beagle pursuit close <task> "
        "--outcome done --spent <n>`, after running its --done-when yourself."
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
        footer = _dispatch_footer(_SEEN_CWD or Path.cwd())
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
#: How much of the previous attempt's report a retry brief carries.
RETRY_REPORT_CHARS = 4_000
#: Lines of the last worker report a step result keeps from its start and its end.
#: Run R16 E16: a 350-line report pushed the lead and the check output out of the
#: 60 lines tau shows of a tool result.
STEP_REPORT_HEAD_LINES = 8
STEP_REPORT_TAIL_LINES = 8
#: Characters of the last worker report a step result keeps from each end.
STEP_REPORT_END_CHARS = 750
#: Fallback for a check with no recorded timeout.
DEFAULT_CHECK_TIMEOUT = 600.0

_TASK_ID = re.compile(r"\bT\d{4,}\b")


def _step_result(text: str) -> AgentToolResult:
    return AgentToolResult(content=[TextContent(text=text)])


# Narrow on purpose: bare "error" and "fail" match ordinary prose.
_REPORTED_FAILURE = re.compile(
    r"\b[1-9]\d* failed\b|\bexit (code )?[1-9]|(?i:\bunfixed\b|remaining failures)|\bFAILED\b"
    r"|\b\w*Error:"
)
_SUPERSEDED_REPORT_NOTE = (
    "The check passed at close: failures this report names are from before the "
    "worker's last edit, and are fixed.\n"
)


def _report_claims_failure(text: str) -> bool:
    """Whether a worker report says something still fails (R09: a stale claim)."""
    return _REPORTED_FAILURE.search(text) is not None


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


_BARE_LABEL = re.compile(r"[A-Za-z]{0,3}[0-9]+")


def _split_part(part: str) -> tuple[str, str]:
    """A `title::intent` part as (title, intent), both stripped.

    Run R09 titled its milestones 'M1'..'M4' and its parts 'P1'..'P5', which
    carry no meaning in the tree or a commit: a bare label like that gives way
    to a title taken from the intent.

    Run R15 planned a 216-character part, which beagle refuses as a title: one
    over MAX_TASK_TITLE keeps the text before ' — ' (else a cut at a word) as
    its title, and the whole part becomes its intent.
    """
    title, _, intent = part.partition("::")
    title, intent = title.strip(), intent.strip()
    if intent and _BARE_LABEL.fullmatch(title):
        title = _task_title(intent)
    if len(title) > MAX_TASK_TITLE:
        intent = f"{title} — {intent}" if intent else title
        title = _task_title(title.split(" — ", 1)[0])
    return title, intent


def _fit_part(part: str) -> str:
    """`part` as `title::intent` when its title is over beagle's cap, else unchanged."""
    if len(part.partition("::")[0].strip()) <= MAX_TASK_TITLE:
        return part
    title, intent = _split_part(part)
    return f"{title}::{intent}"


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
#: A fetch that timed out is tried once more with this: R09's itc2008.pdf
#: timed out at 30 s and every worker re-downloaded it to /tmp.
REFERENCE_FETCH_RETRY_TIMEOUT = 90.0
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
    """An HTML page's text: script, style and page chrome left out, blocks and table rows on
    their own lines, cells in a row kept apart by " | "."""

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

    # Page chrome: always left out, or (header, footer) only outside the article or main body,
    # where a header can hold the article's own title.
    _CHROME = frozenset({"nav", "aside"})
    _PAGE_CHROME = frozenset({"header", "footer"})
    _CONTENT = frozenset({"article", "main"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skipping = 0
        self._chrome_tag = ""
        self._chrome_depth = 0
        self._in_content = 0
        self._row_has_cell = False

    def _is_chrome(self, tag: str, attrs: Any) -> bool:
        if tag in self._CHROME:
            return True
        if tag in self._PAGE_CHROME and not self._in_content:
            return True
        return any(k == "role" and (v or "").strip().lower() == "navigation" for k, v in attrs)

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if self._chrome_depth:
            if tag == self._chrome_tag:
                self._chrome_depth += 1
            return
        if tag in self._SKIP:
            self._skipping += 1
        elif self._is_chrome(tag, attrs):
            self._chrome_tag, self._chrome_depth = tag, 1
            self.parts.append("\n")
        else:
            if tag in self._CONTENT:
                self._in_content += 1
            if tag == "tr":
                self._row_has_cell = False
            elif tag in ("td", "th"):
                if self._row_has_cell and not self._skipping:
                    self.parts.append(" | ")
                self._row_has_cell = True
            if tag in self._BLOCK:
                self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._chrome_depth:
            if tag == self._chrome_tag:
                self._chrome_depth -= 1
            return
        if tag in self._SKIP:
            self._skipping = max(0, self._skipping - 1)
        else:
            if tag in self._CONTENT:
                self._in_content = max(0, self._in_content - 1)
            if tag in self._BLOCK:
                self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skipping and not self._chrome_depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = (
            re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in "".join(self.parts).splitlines()
        )
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


_NON_NEWLINE_BREAKS = str.maketrans(dict.fromkeys("\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029", " "))


def _newline_only(text: str) -> str:
    """`text` with no line break `splitlines()` sees but newline: CRLF to LF, the rest to spaces.

    R25: a PDF's form feeds and \\x1c/\\x1d made `splitlines()` count 718 lines
    where the read tool, splitting on newlines, counted 671, so workers checking
    a citation in Python "fixed" correct line numbers into wrong ones.
    """
    return text.replace("\r\n", "\n").translate(_NON_NEWLINE_BREAKS)


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
    return _newline_only(proc.stdout.decode("utf-8", "replace"))


def _is_timeout(exc: BaseException) -> bool:
    """Whether `exc` is a timeout, bare or wrapped in urllib's URLError."""
    if isinstance(exc, urllib.error.URLError) and not isinstance(exc, urllib.error.HTTPError):
        return isinstance(exc.reason, (TimeoutError, socket.timeout))
    return isinstance(exc, (TimeoutError, socket.timeout))


def _fetch_reference(url: str, timeout: float = REFERENCE_FETCH_TIMEOUT) -> str:
    """`url`'s content as text: a PDF through `pdftotext -layout`, HTML stripped.

    Raises OSError (urllib's errors are its subclasses) or ValueError on failure.
    """
    request = urllib.request.Request(url, headers={"User-Agent": "tau-beagle/1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
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
    return _newline_only(text)


def _failure_reason(exc: BaseException) -> str:
    return str(exc).strip() or type(exc).__name__


def _fetch_references(root: Path, prompt: str) -> dict[str, Any]:
    """Fetch each URL in the user's `prompt` once into `references/`, as text.

    R02's workers never saw the paper: the driver, barred from the
    reference, wrote the domain into its step notes from the name alone.
    The request itself, and each URL's file or why it could not be fetched,
    go in `references/index.json`, which every worker brief is built from.
    A failed fetch is recorded, never fatal; one that timed out is tried
    once more with REFERENCE_FETCH_RETRY_TIMEOUT before it is.
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
            try:
                text = _fetch_reference(url)
            except Exception as exc:  # noqa: BLE001 - only a timeout is retried
                if not _is_timeout(exc):
                    raise
                first = _failure_reason(exc)
                try:
                    text = _fetch_reference(url, timeout=REFERENCE_FETCH_RETRY_TIMEOUT)
                except Exception as again:  # noqa: BLE001 - recorded with both reasons
                    raise OSError(
                        f"{first}; retried with {REFERENCE_FETCH_RETRY_TIMEOUT:g} s: "
                        f"{_failure_reason(again)}"
                    ) from again
            (folder / name).write_text(text, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001 - one bad URL must not stop founding
            index["failed"][url] = _failure_reason(exc)
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


#: Asked of a known-answers task with references/ fetched. Runs R12 and R14:
#: cases cited bare URLs, nothing, or a file:line that held a page number.
QUOTED_SOURCE_NOTE = (
    "Known answers: give each case a `source` that quotes, verbatim, the line of "
    f"{REFERENCES_DIR}/*.txt it comes from, at least four words copied as written. "
    "A bare file:line (such as `paper.txt:221`), a page number or a URL is not a "
    "source: at close, a cases file most of whose sources quote nothing found in "
    f"{REFERENCES_DIR}/*.txt keeps the task open."
)


def _references_brief(root: Path, context_only: bool = False) -> str:
    """The worker brief's part from `references/index.json`: request and references.

    `context_only` is for a data task: run R09's T0002 brief ended on the
    request verbatim, and its worker set out to implement the library.
    """
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
        lines = [
            f"- {REFERENCES_DIR}/{name} (from {url}){_reference_size(root / REFERENCES_DIR / name)}"
            for name, url in fetched.items()
        ]
        lines += [f"- could not fetch {url}: {why}" for url, why in failed.items()]
        parts.append(
            "References: read first; outranks the driver's notes. Where the driver's "
            "notes or the task disagree with the reference, the reference is right:\n"
            + "\n".join(lines)
        )
    request = str(index.get("request") or "").strip()
    if request:
        lead = (
            "The user's original request, as context only; your task is the one above, "
            "not this request"
            if context_only
            else "The user's original request, verbatim"
        )
        parts.append(f"{lead}:\n<<<\n{request}\n>>>")
    if context_only and fetched:
        parts.append(QUOTED_SOURCE_NOTE)
        parts.append(
            "A case needs only the lines it cites: read those by line range "
            "(offset and limit), not the whole file."
        )
    return "\n\n".join(parts)


def _reference_size(path: Path) -> str:
    """` — N lines, R reads`: a whole read shows WINDOW_LINES lines at a time (R25)."""
    try:
        count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return ""
    reads = max(1, -(-count // WINDOW_LINES))
    noun = "read" if reads == 1 else "reads"
    return f" — {count} lines, {reads} {noun} at {WINDOW_LINES} lines per read"


def _turn_cap_note() -> str:
    """The worker's tool-call cap, as pursuit_step's brief states it (R21-R25)."""
    cap = _worker_max_turns()
    return (
        f"You have {cap} tool calls in all. Write the files by about call {cap // 2}, "
        "then use the rest to run the check and fix them."
    )


def _git_identity(root: Path) -> bool:
    """Whether a commit in `root` would know who made it (config, env or host)."""
    return all(
        _run(["git", "var", ident], root, timeout=10.0)[0] == 0
        for ident in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT")
    )


def _commit_setup(root: Path) -> str | None:
    """Commit beagle's setup (.beagle/ and .gitignore) alone; None, or why not.

    R08: `beagle init`'s files stayed untracked, so the workspace-clean gate
    was red from the first task. A pathspec commit leaves whatever else the
    user has staged or changed exactly as it was; a failed commit unstages
    only what this call staged.
    """
    pathspec = ["--", ".beagle", ".gitignore"]
    rc, out = _run(["git", "diff", "--cached", "--name-only", *pathspec], root, timeout=30.0)
    if rc != 0:
        return f"`git diff --cached` failed: {out}"
    before = set(out.splitlines())
    rc, out = _run(["git", "add", "-A", *pathspec], root, timeout=30.0)
    if rc != 0:
        return f"`git add` failed: {out}"
    rc, out = _run(
        ["git", "diff", "--cached", "--name-only", *pathspec], root, timeout=30.0
    )
    if rc != 0:
        return f"`git diff --cached` failed: {out}"
    staged = out.splitlines()
    specs = [
        spec
        for spec in (".beagle", ".gitignore")
        if any(path == spec or path.startswith(f"{spec}/") for path in staged)
    ]
    if not specs:
        return None
    rc, out = _run(
        ["git", "commit", "-q", "-m", "pursuit: found — beagle setup", "--", *specs],
        root,
        timeout=60.0,
    )
    if rc != 0:
        added = [path for path in staged if path not in before]
        if added:
            _run(["git", "reset", "-q", "--", *added], root, timeout=30.0)
        return f"`git commit` failed: {out}"
    return None


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


#: The longest a worker's own command runs, and its share of the worker's wall clock.
COMMAND_TIMEOUT = 540
COMMAND_TIMEOUT_SHARE = 0.6
_MEMORY_SIZE = re.compile(r"(\d+(?:\.\d+)?)\s*([KMGT]?)B?", re.IGNORECASE)


def _half_memory(limit: str | None) -> str | None:
    """Half of a systemd MemoryMax value, or None when it is unset or unreadable."""
    if limit is None:
        return None
    text = limit.strip()
    if text.endswith("%"):
        try:
            return f"{float(text[:-1]) / 2:g}%"
        except ValueError:
            return None
    match = _MEMORY_SIZE.fullmatch(text)
    if match is None:
        return None
    power = "KMGT".find(match.group(2).upper()) + 1 if match.group(2) else 0
    mebibytes = int(float(match.group(1)) * 1024**power / 2 / 1024**2)
    return f"{mebibytes}M" if mebibytes > 0 else None


def _command_bound(limit: str | None, timeout: float) -> str:
    """The prefix a worker's own command runs under: half its memory cap, under its wall.

    Run R30: W4-W7 ran `timeout 540 python3 -m pytest …` inside their own capped
    scope; the runaway test took the worker down with it, and no report came
    back. A `systemd-run --user --scope` started by the worker is a scope of its
    own, so the command's memory is not the worker's and an over-cap command
    dies alone, exit 137, with the worker left to report it.
    """
    seconds = max(1, int(min(COMMAND_TIMEOUT, timeout * COMMAND_TIMEOUT_SHARE)))
    return " ".join(_capped(["timeout", str(seconds)], _half_memory(limit)))


def _killed_note(returncode: int | None, limit: str | None) -> str:
    """Why a capped process may have died, for a SIGKILL nobody here sent."""
    if limit is None or returncode != -9:
        return ""
    return (
        f"(It was killed with SIGKILL, most likely for going over its {limit} memory cap; "
        f"{MEMORY_MAX_ENV} sets the cap.)"
    )


def _pursuit(args: list[str], root: Path, timeout: float = 60.0) -> tuple[int, str]:
    """`beagle pursuit <args>`, under the worker memory cap with every check it runs."""
    return _run([BEAGLE_BIN, "pursuit", *args], root, timeout=timeout, limit=_memory_max())


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
        title, intent = _split_part(part)
        argv = ["add", title, "--parent", task]
        if intent:
            argv += ["--intent", intent]
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
    A wait on a superseded task whose heir is `task` is dropped too: run R08's
    T0007 waited on T0006, handed to T0011, and abandoning T0011 left it.
    """
    nodes = _tree_nodes(root)
    released = []
    for node in nodes:
        heirs = node.get("waiting_heirs")
        heirs = heirs if isinstance(heirs, dict) else {}
        for named in node.get("waiting_on") or []:
            named = str(named)
            if task not in (named, str(heirs.get(named) or ""), _heir(named, nodes)):
                continue
            waiter = str(node.get("id"))
            reason = f"{task} abandoned: {why}"[:500]
            if _pursuit(["depend", waiter, named, "--drop", "--reason", reason], root)[0] == 0:
                released.append(waiter)
    return released


def _part_title(part: str) -> str:
    return _split_part(part)[0]


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


def _state(task: str, nodes: list[dict[str, Any]]) -> str | None:
    """`task`'s status, or "stalled" for a container whose subtree beagle calls stalled."""
    for node in nodes:
        if str(node.get("id")) == task:
            if node.get("container") and node.get("subtree") == "stalled":
                return "stalled"
            return node.get("status")
    return None


def _wait_text(wait: _Wait, nodes: list[dict[str, Any]]) -> str:
    """One hard wait in words: `waits on T0002 (superseded, handed to T0008: pending)`."""
    _, named, now = wait
    if named != now:
        return f"waits on {named} (superseded, handed to {now}: {_state(now, nodes)})"
    return f"waits on {named} ({_state(named, nodes)})"


def _dead_waits(nodes: list[dict[str, Any]]) -> list[_Wait]:
    """The hard waits of unfinished tasks that can never be met, in tree order.

    A wait is dead when the task it names, or that task's heir, is abandoned or
    a stalled container. Run R08's T0007 waited on T0006, handed to stalled
    T0011, and nothing was ready for the last 6.7 minutes.
    """
    dead: list[_Wait] = []
    for node in nodes:
        if node.get("status") in ("done", "abandoned", "superseded"):
            continue
        task = str(node.get("id"))
        heirs = node.get("waiting_heirs")
        heirs = heirs if isinstance(heirs, dict) else {}
        for named in node.get("waiting_on") or []:
            named = str(named)
            now = str(heirs.get(named) or "") or _heir(named, nodes)
            if any(_state(t, nodes) in ("abandoned", "stalled") for t in (named, now)):
                dead.append((task, named, now))
    return dead


def _dead_wait_drops(dead: list[_Wait], nodes: list[dict[str, Any]]) -> str:
    """What to tell the driver about waits that can never be met: each one's drop."""

    def reason(named: str, now: str) -> str:
        handed = f" was handed to {now}, which" if now != named else ""
        return f"{named}{handed} is {_state(now, nodes)} and will never be done"

    drops = "\n".join(
        f'    beagle pursuit depend {waiter} {named} --drop --reason "{reason(named, now)}"'
        for waiter, named, now in dead
    )
    return (
        "These hard waits can never be met, so the tasks that hold them can never start:\n"
        + "\n".join(f"- {w[0]} {_wait_text(w, nodes)}" for w in dead)
        + f"\n\nDrop each one. Run in bash, exactly:\n\n{drops}\n\n"
        "then call pursuit_step with no arguments."
    )


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


def _setup_abandonable(task: str, nodes: list[dict[str, Any]]) -> bool:
    """Whether `task` is a setup milestone (by `_setup_milestone`) never opened.

    Run R10 founded with "Setup beagle pursuit infrastructure - ..." as T0002,
    ordered every later milestone behind it, and had no way to drop it: each
    step named `.beagle/` and was refused, and so was abandoning a milestone.
    Never opened: it is pending and none of its children left pending.
    """
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    if node is None or node.get("status") != "pending":
        return False
    if _setup_milestone([str(node.get("title") or "")]) is None:
        return False
    return all(n.get("status") == "pending" for n in nodes if str(n.get("parent") or "") == task)


def _setup_abandon_route(task: str) -> str:
    """The abandon call that drops `task`, a never-opened setup milestone."""
    return (
        f" If this task only sets beagle up, founding did that: pursuit_step "
        f'task="{task}", abandon="setup: founding did it".'
    )


#: An abandon reason that says founding did a setup task's work.
_DONE_BY_FOUNDING = re.compile(r"(?i)\bdone\s+by\s+found")


def _founding_did(task: str, why: str, nodes: list[dict[str, Any]]) -> bool:
    """Whether `why` abandons `task`, a setup milestone not done, as done by founding.

    Run R19's T0002, "Found the pursuit: ...", was refused five times for a
    done_when over .beagle/; the refusal now says to abandon it so, which holds
    for an opened one too: founding did its work, so no done task holds it.
    """
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    return (
        node is not None
        and node.get("status") in ("pending", "open")
        and _setup_milestone([str(node.get("title") or "")]) is not None
        and _DONE_BY_FOUNDING.search(why) is not None
    )


def _setup_lead(task: str) -> str:
    """What leads a refusal of a step on `task`, a setup milestone."""
    return (
        f"{task} is the setup, and pursuit_found already did it: it has no work in the "
        f"project. Abandon it: pursuit_step task {task} abandon 'done by founding'. The "
        "tasks waiting on it then become ready.\n\n"
    )


def _stale_known_answers_duplicate(
    task: str, why: str, by_id: dict[str, dict[str, Any]]
) -> str | None:
    """The task `why` names, when `task` writes the known answers and that one is not live.

    Run R18 #50 abandoned T0005, the known-answers successor, as "duplicate of
    T0002", which was superseded: no task held the known answers after that.
    """
    node = by_id.get(task)
    if node is None or not _names_known_answers(str(node.get("title") or "")):
        return None
    for named in _TASK_ID.findall(why):
        if named != task and named in by_id:
            if by_id[named].get("status") in ("done", "open"):
                return None
            return str(named)
    return None


def _task_number(task: str) -> int | None:
    digits = task.lstrip("T")
    return int(digits) if digits.isdigit() else None


def _founding_milestones(nodes: list[dict[str, Any]]) -> set[str]:
    """The root's children that `pursuit_found` made, as the tree shows them.

    Founding adds the root and then splits it, so its milestones are the root's
    children numbered straight after it, with no other task between. A child
    of the root numbered after any other task was added later, by a plan.
    """
    roots = [n for n in nodes if not n.get("parent")]
    if len(roots) != 1:
        return set()
    root = str(roots[0].get("id"))
    number = _task_number(root)
    if number is None:
        return set()
    by_number = {_task_number(str(n.get("id"))): n for n in nodes}
    found: set[str] = set()
    while True:
        node = by_number.get(number + len(found) + 1)
        if node is None or str(node.get("parent") or "") != root:
            return found
        found.add(str(node.get("id")))


def _live_duplicate_of(why: str, task: str, nodes: list[dict[str, Any]]) -> str | None:
    """The task `why` names as the one `task` duplicates, when it still holds that work.

    It is pending, open or done, and neither the root nor under `task`.
    """
    if not why.strip().lower().startswith("duplicate of"):
        return None
    by_id = {str(n.get("id")): n for n in nodes}
    for named in _TASK_ID.findall(why):
        node = by_id.get(named)
        if named == task or node is None or not node.get("parent"):
            continue
        up, seen = named, set()
        while up and up not in seen and up != task:
            seen.add(up)
            up = str(by_id.get(up, {}).get("parent") or "")
        if up != task and node.get("status") in ("pending", "open", "done"):
            return str(named)
    return None


def _abandon_problem(task: str, why: str, nodes: list[dict[str, Any]]) -> str | None:
    """Why the driver may not abandon `task` for `why`, or None.

    Run R02's driver abandoned four of five milestones in 0.3 min, each as
    "already exists / passes", right after tau's own hint offered abandoning
    work "already done". A task is dropped only as a duplicate of one that
    holds its work; a milestone from founding is the goal's and is never dropped
    here. One a plan added later may go as a duplicate of a task that holds its
    work: run R22's driver planned five such on the root, and none could go.
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
    stale = _stale_known_answers_duplicate(task, why, by_id)
    if stale is not None:
        heir = _heir(stale, nodes)
        work = (
            f"{task} is its live successor: work {task}"
            if heir == task
            else f"its live successor is {heir} ({_state(heir, nodes)}): work {heir}"
        )
        return (
            f"pursuit_step: {task} not abandoned — it writes the known answers, and "
            f"{stale}, the task named as holding its work, is not live "
            f"({by_id[stale].get('status')}), so dropping {task} would drop the known "
            f'answers. {work} with pursuit_step task="{heir}" instead.'
        )
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
        if _setup_abandonable(task, nodes) or _founding_did(task, why, nodes):
            return None
        later = task not in _founding_milestones(nodes)
        if later and _live_duplicate_of(why, task, nodes) is not None:
            return None
        duplicate = (
            " It was added after founding, so if a pending, open or done task holds its "
            f'work, pursuit_step task="{task}", abandon="duplicate of Tnnnn" drops it.'
            if later
            else ""
        )
        if by_id.get(task, {}).get("status") == "pending":
            # Run R14: beagle refuses a new route for a task never opened.
            return (
                f"pursuit_step: {task} not abandoned — it is a milestone, and a milestone "
                "is the goal's. Split it with pursuit_plan, or, if a done task's commit "
                f'already did its work, call pursuit_step task="{task}", abandon="done by '
                'Tnnnn" and done_when, naming that task; it closes done on that commit '
                f"if the check passes now.{duplicate}"
            )
        return (
            f"pursuit_step: {task} not abandoned — it is a milestone, and a milestone is "
            "the goal's. Split it with pursuit_plan, or give it a new route with "
            f'pursuit_step task="{task}", new_route=true and notes.{duplicate}'
        )
    if _duplicate_of(why, task, nodes) is not None:
        container = parent.get(task, "")
        if container and container not in roots:
            # Run R08: beagle keeps an abandoned leaf with no successor as
            # accountable, so its container can never be all-done and stalls.
            return (
                f"pursuit_step: {task} not abandoned — {container} would stall for good "
                f'with a part abandoned. Work it with pursuit_step task="{task}" and a '
                "done_when that runs the code and fails now. If a done task's commit "
                f'already did its work, call pursuit_step task="{task}", abandon="done by '
                'Tnnnn" and done_when, naming that task; it closes done on that commit '
                "if the check passes now."
            )
        return None
    return (
        f"pursuit_step: {task} not abandoned — a task is dropped only as a duplicate of "
        "a done or open task, named as abandon='duplicate of Tnnnn'. Work that seems "
        "already done is not a reason. If a done task's commit did it, call "
        f'pursuit_step task="{task}", abandon="done by Tnnnn" and done_when, naming '
        "that task; it closes done on that commit if the check passes now. Otherwise "
        "work it with a done_when that imports and runs the code and fails now."
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
#: The statement a print-mode `pursuit_found` refused as unconfirmed, folded;
#: sending it again is the delegation the refusal asked for.
_FOUND_REFUSED_STATEMENT: str | None = None
#: Wording in a prompt that hands the founding decisions to the model.
DELEGATING_WORDS = re.compile(
    r"(?i)\b(?:use (?:your|ur) (?:own |best )?judge?ment"
    r"|without (?:any |further |more )?(?:discussion|asking|confirmation)"
    r"|(?:up to you|your call|at your discretion)"
    r"|(?:you|yourself) (?:can |should )?decide|decide (?:for )?yourself"
    r"|go ahead|don'?t ask|no need to (?:ask|confirm))"
)


def _fold(text: str) -> str:
    return " ".join(text.split()).casefold()


def _inferred_delegation(statement: str) -> str | None:
    """Why a print-mode `pursuit_found` without the flag counts as delegated, or None.

    Run R11's mimo, in `tau -p` with a prompt saying "use your judgement to do
    the setup without further discussion", sent `pursuit_found` eleven times,
    identical and without `user_delegated`, and the run ended unfounded.
    """
    said = DELEGATING_WORDS.search(_LAST_PROMPT)
    if said is not None:
        return f'the prompt that started this print-mode session says "{said.group(0)}"'
    if _fold(statement) == _FOUND_REFUSED_STATEMENT:
        return (
            "you sent the same goal again after this print-mode session's refusal, "
            "and no user is here to confirm it"
        )
    return None


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
        criteria, criteria_notes = _drop_setup_criteria(criteria)
        # Run R03's driver, refused for a setup first milestone, sent the same
        # call fourteen times: what founding can repair itself, it repairs.
        given = milestones
        milestones, repairs = _repair_milestones(given)
        if not milestones:
            # Run R07's driver named only a setup milestone and was refused
            # twelve times; the criteria it gave are milestones enough.
            milestones, repairs = _milestones_from_criteria(given, criteria, repairs)
            if not milestones:
                return _step_result(f"pursuit_found: nothing written — {repairs[0]}")
        repairs = [*criteria_notes, *repairs]
        repaired = "".join(f"{note}\n\n" for note in repairs)
        delegated = arguments.get("user_delegated") is True
        inferred = None
        if arguments.get("user_confirmed") is not True and not delegated:
            global _FOUND_AWAITS_USER, _FOUND_REFUSED_STATEMENT
            alone = not interactive()
            inferred = _inferred_delegation(statement) if alone else None
            if inferred is None:
                _FOUND_AWAITS_USER = alone
                if alone:
                    _FOUND_REFUSED_STATEMENT = _fold(statement)
                refusal = _unconfirmed_refusal(statement, criteria, interactive=not alone)
                return _step_result(f"{repaired}{refusal}")
            delegated = True
            _FOUND_AWAITS_USER = False
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
                "git has no user.name or user.email here, so commits will fail, and beagle's "
                "setup (.beagle/, .gitignore) is uncommitted. Tell the user now; do not set "
                "one yourself."
            )
        elif (why := _commit_setup(root)) is not None:
            notes.append(f"beagle's setup (.beagle/, .gitignore) is uncommitted: {why}")
        fetched, failed = references.get("fetched") or {}, references.get("failed") or {}
        if fetched or failed:
            got = ", ".join(f"{REFERENCES_DIR}/{name}" for name in fetched) or "none"
            missed = "".join(f"; could not fetch {url}: {why}" for url, why in failed.items())
            notes.append(
                f"References from the user's request, fetched for the workers: {got}{missed}. "
                "Every pursuit_step brief carries them and the request; leave reading them "
                "to the workers."
            )
        if inferred is not None:
            notes.append(
                f"Delegation was inferred, not given: {inferred}. In your reply, tell "
                "the user the criteria you chose, so they can correct them."
            )
        elif delegated:
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


def _uncommitted_in_scope(root: Path, task: str) -> tuple[list[str], list[str]]:
    """An open task's scope and the files git holds uncommitted in it, as it is split.

    R09: T0007 was split with tests/cases.json uncommitted, and T0009's commit
    took it beside src/itc/*.py, unlocked.
    """
    rc, out = _pursuit(["show", task], root)
    record = _json_reply(out) if rc == 0 else None
    if not isinstance(record, dict) or record.get("status") != "open":
        return [], []
    scope = _strings(record.get("scope"))
    if not scope:
        return [], []
    return scope, [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]


def _uncommitted_note(task: str, paths: list[str]) -> str:
    named = ", ".join(paths[:8])
    if len(paths) > 8:
        named += f", {len(paths) - 8} more"
    return (
        f"Uncommitted in {task}'s scope: {named}. Give each to the part that writes it, "
        "with locks when it is data; otherwise it goes out in a later part's commit."
    )


def _commit_before_split(
    root: Path, task: str, scope: list[str], paths: list[str], goal: Path | None = None
) -> str:
    """Commit a split task's uncommitted work when its check last passed; the note to give.

    R12: test_comprehensive.py passed under T0007 and was left to the last
    part, so the workspace-clean gate stayed red for every part before it.
    Work whose check failed, or was never run, stays a note for the parts.
    R28: the commit kept a stripped locked test, so locked files are put back
    first; the task being split no longer fixes them.
    """
    put_back = _put_back_drift(goal, root, but=task) if goal is not None else ""
    if put_back:
        paths = [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]
        if not paths:
            return put_back
        put_back += "\n\n"
    if _LAST_CHECK_EXIT.get((str(root), task)) != 0:
        return put_back + _uncommitted_note(task, paths)
    said = _commit(task, SPLIT_WIP_TITLE, scope, root)
    left = [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]
    if left:
        return f"{put_back}{said}\n\n{_uncommitted_note(task, left)}"
    return put_back + (
        f"{task}'s check passed at its last run, so its uncommitted work "
        f"({', '.join(paths[:8])}{', …' if len(paths) > 8 else ''}) was committed as "
        f"'{task}: {SPLIT_WIP_TITLE}' before the split: {said}"
    )


def _split_part_lines(parts: list[str]) -> tuple[list[str], list[str]]:
    """`parts` with each part of several lines split, in place, into one part per line.

    Run R15 sent one part of three lines, the last 'Run the check: …'. A line
    that only re-runs a check is dropped with a note; a plain part that does is
    left for the plan's own refusal.
    """
    kept: list[str] = []
    split_notes: list[str] = []
    dropped: list[str] = []
    for part in parts:
        lines = [line.strip() for line in part.splitlines() if line.strip()]
        if len(lines) < 2:
            kept.append(part)
            continue
        split = []
        for line in lines:
            why = _rerun_only_part([line])
            if why is None:
                split.append(line)
            else:
                dropped.append(f"Dropped a line of the part: {why}")
        if split:
            which = "The one part" if len(parts) == 1 else f"Part {_part_title(lines[0])!r}"
            split_notes.append(f"{which} held {len(lines)} lines, so each line became a part.")
        kept.extend(split)
    return kept, split_notes + dropped


def _is_leaf(task: str, nodes: list[dict[str, Any]]) -> bool:
    """True when the tree shows `task` as a leaf under a parent: no container, no child."""
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    if node is None or node.get("container") or not node.get("parent"):
        return False
    return not any(
        n.get("parent") == task and n.get("status") not in ("abandoned", "superseded")
        for n in nodes
    )


def _part_paths(part: str) -> list[str]:
    """The paths a plan part's text names: words with a directory or a file suffix."""
    return [word.rstrip(".") for word in _SCRIPT_PATH_WORD.findall(part)]


def _writes_known_answers(text: str) -> bool:
    """Whether a part or task's text names the known answers or their cases data file."""
    return _split_part(text)[0].lower().startswith("known answers") or any(
        _is_cases_data(path) for path in _part_paths(text)
    )


def _plan_order_problem(parts: list[str], task: str, goal: Path) -> str | None:
    """Why an ordered plan writes new source before the known answers that judge it, or None.

    Run R16 planned T0006 (interval_tree_clocks.py) before T0007-T0009 (the
    cases and their tests), each waiting on the one before; the code would
    have been written with nothing from the reference to judge it.
    """
    answers = next((i for i, part in enumerate(parts) if _writes_known_answers(part)), None)
    if answers is None:
        return None
    for index, part in enumerate(parts[:answers]):
        title = _part_title(part)
        if _cases_first_problem(_part_paths(part), task, title, goal) is None:
            continue
        first = _part_title(parts[answers])
        return (
            f"Cases first: part {index + 1} {title!r} writes new source before part "
            f"{answers + 1} {first!r} writes the known answers that judge it, and in an "
            f"ordered plan each part waits on the one before. Put part {answers + 1} "
            f"{first!r} first and send the plan again."
        )
    return None


def _ancestors(task: str, nodes: list[dict[str, Any]]) -> set[str]:
    """The ids above `task` in the tree."""
    parent = {str(n.get("id")): str(n.get("parent") or "") for n in nodes}
    seen: set[str] = set()
    up = parent.get(task, "")
    while up and up not in seen:
        seen.add(up)
        up = parent.get(up, "")
    return seen


def _is_container(task: str, nodes: list[dict[str, Any]]) -> bool:
    """True when the tree shows `task` as a container or with a live child."""
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    if node is not None and node.get("container"):
        return True
    return any(
        n.get("parent") == task and n.get("status") not in ("abandoned", "superseded")
        for n in nodes
    )


def _live_leaves(task: str, nodes: list[dict[str, Any]]) -> list[str]:
    """The pending or open leaves under `task`, depth first in tree order."""
    found: list[str] = []
    for n in nodes:
        nid = str(n.get("id"))
        if n.get("parent") != task or n.get("status") not in ("pending", "open"):
            continue
        found += _live_leaves(nid, nodes) if _is_container(nid, nodes) else [nid]
    return found


def _steppable(ids: list[str], nodes: list[dict[str, Any]]) -> list[str]:
    """`ids` without the containers the tree shows: those are not a task to step.

    Run R28 listed open container T0012 as workable; the driver stepped it
    seven times in a row and the breaker stopped the run.
    """
    return [t for t in ids if not _is_container(t, nodes)]


def _live_title_clash(task: str, parts: list[str], nodes: list[dict[str, Any]]) -> str | None:
    """Why a plan may not add `parts`, one titled as a live task off `task`'s subtree is, or None.

    Run R22's driver planned five parts on the root that repeated pending
    tasks, and they then ranked against the tasks they repeated. Run R25's
    split of T0006 repeated pending T0003-T0005 the same way, off the root.
    A part may not take `task`'s own title either; its descendants' titles stay free.
    Ancestors of `task` and containers are left out: neither is a task to step.
    Titles are compared case-folded with whitespace normalized.
    """
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    if node is None:
        return None
    # The root's subtree is the whole tree: there only the root is left out.
    subtree = {task}
    grew = bool(node.get("parent"))
    while grew:
        grew = False
        for n in nodes:
            nid = str(n.get("id"))
            if n.get("parent") in subtree and nid not in subtree:
                subtree.add(nid)
                grew = True
    # Run R28: a clash with pending container T0010 said work T0010, and
    # stepping T0010 said container; ancestors are no more steppable.
    ancestors = _ancestors(task, nodes)
    live = {
        _fold(str(n.get("title") or "")): n
        for n in nodes
        if n.get("status") in ("pending", "open")
        and n.get("id")
        and str(n.get("id")) not in subtree
        and str(n.get("id")) not in ancestors
        and not _is_container(str(n.get("id")), nodes)
    }
    # Run R26's split of T0006 added T0014 under T0006's own title.
    own = _fold(str(node.get("title") or ""))
    for part in parts:
        title = _part_title(part)
        if own and _fold(title) == own:
            return (
                f"part {title!r} has the title of {task}, the task being split. A part "
                f"is one piece of {task}: title it by the piece it does, and send the "
                "plan again."
            )
        same = live.get(_fold(title))
        if same is not None:
            other = str(same.get("id"))
            return (
                f"part {title!r} has the title of {other} ({same.get('status')}), which is "
                f'still to be done. Work {other} with pursuit_step task="{other}", and send '
                "the plan again without that part."
            )
    return None


def _bare_label_refusal(
    task: str, parts: list[str], unlabeled: list[str], nodes: list[dict[str, Any]]
) -> str:
    """Why parts that are only a label, with no intent for a title, are refused, and the call.

    The call leaves those parts out; where too few parts would be left to
    split `task`, it works `task` instead.
    """
    rest = [part for part in parts if part not in unlabeled]
    named = ", ".join(repr(part.strip()) for part in unlabeled)
    if len(rest) >= 2 or (rest and not _is_leaf(task, nodes)):
        call = f'pursuit_plan task="{task}", parts={json.dumps(rest, ensure_ascii=False)}'
    else:
        call = f'pursuit_step task="{task}"'
    return (
        f"{named} is only a label, with no intent to take a title from. Give each part "
        f"as 'Title::what it does', or call instead: {call}"
    )


#: beagle's note on a task it added that reads like another, with the bash it
#: suggests, which the driver's guard refuses.
_RESEMBLANCE_ROUTE = re.compile(
    r"If it is the same work, `beagle pursuit close (T\d+) --outcome abandoned --reason "
    r'"duplicate of (T\d+)"` retires this one\.'
    r"(?: If what it adds is an order, `beagle pursuit depend [^`]*` puts it on the task "
    r"that exists\.?)?"
)


def _steer_resemblance(out: str, root: Path) -> str:
    """`out` with beagle's bash route for a look-alike task replaced by the tool call.

    The call is offered only where `_abandon_problem` would take it; otherwise
    the route is left out, as is the `depend --hard` the guard refuses too.
    """
    if _RESEMBLANCE_ROUTE.search(out) is None:
        return out
    nodes = _tree_nodes(root)

    def route(match: re.Match[str]) -> str:
        added, like = match.group(1), match.group(2)
        why = f"duplicate of {like}"
        if _abandon_problem(added, why, nodes) is not None:
            return ""
        return f'If it is the same work, pursuit_step task="{added}", abandon="{why}" drops it.'

    return _RESEMBLANCE_ROUTE.sub(route, out)


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
        parts, split_notes = _split_part_lines(parts)
        if not parts:
            return _step_result(f"pursuit_plan: nothing added — {split_notes[0]}")
        cut = [part for part in parts if _fit_part(part) != part]
        parts = [_fit_part(part) for part in parts]
        for part in cut:
            split_notes.append(
                f"A part's title was over beagle's {MAX_TASK_TITLE} characters, so it is now "
                f"{_part_title(part)!r}, with the whole text as its intent."
            )
        setup = _setup_milestone(parts)
        if setup is not None:
            return _step_result(f"pursuit_plan: nothing added — {setup}")
        rerun = _rerun_only_part(parts)
        if rerun is not None:
            return _step_result(f"pursuit_plan: nothing added — {rerun}")
        ordered = arguments.get("ordered", True) is not False
        backwards = _plan_order_problem(parts, task, goal) if ordered else None
        if backwards is not None:
            return _step_result(f"pursuit_plan: nothing added — {backwards}")
        # Run R25 sent 'T0007::…' to `split` raw, and beagle titled the task
        # 'T0007': every part goes on as the title `_split_part` repairs.
        unlabeled = [
            part
            for part in parts
            if not _split_part(part)[1] and _BARE_LABEL.fullmatch(_split_part(part)[0])
        ]
        if unlabeled:
            why = _bare_label_refusal(task, parts, unlabeled, _tree_nodes(root))
            return _step_result(f"pursuit_plan: nothing added — {why}")
        for part in parts:
            label = part.partition("::")[0].strip()
            if _BARE_LABEL.fullmatch(label):
                split_notes.append(
                    f"Part {label!r} was only a label, so it is titled "
                    f"{_part_title(part)!r} from its intent."
                )
        parts = [
            f"{title}::{intent}" if intent else title for title, intent in map(_split_part, parts)
        ]
        reading = _reading_only_part(parts)
        if reading is not None:
            return _step_result(f"pursuit_plan: nothing added — {reading}")
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
        clash = _live_title_clash(task, parts, _tree_nodes(root))
        if clash is not None:
            return _step_result(f"pursuit_plan: nothing added — {clash}")
        one_step = (
            f"pursuit_plan: nothing added — {task} is already one step, so one "
            "part does not break it down: a plan needs two or more parts, which "
            f"split {task} into smaller tasks. Give two or more parts, or work it "
            f"with pursuit_step task={task}."
        )
        # beagle refuses a one-part split as a rename. A container or the root
        # still takes one more child; a leaf with one part is already a single
        # step. Run R15's beagle refused the part's title before it got there.
        if len(parts) == 1 and _is_leaf(task, _tree_nodes(root)):
            return _step_result(one_step)
        drift = _put_back_drift(goal, root, but=task)
        if drift:
            split_notes.append(drift)
        # Read before the split, which leaves the task a container.
        scope, uncommitted = _uncommitted_in_scope(root, task)
        uncommitted_note = _uncommitted_note(task, uncommitted) if uncommitted else ""
        moved_note = ""
        if len(parts) == 1:
            rc, out = _add_children(task, parts, root)
            # beagle says "a pending leaf" or, for one being worked, "a open
            # leaf": run R06's plan of one part on open T0002 came back raw.
            if rc != 0 and "leaf with work of its own" in out:
                return _step_result(one_step)
        else:
            if uncommitted:
                uncommitted_note = _commit_before_split(root, task, scope, uncommitted, goal)
            rc, out = _pursuit(["split", task, *parts, *(["--ordered"] if ordered else [])], root)
            if rc != 0 and "already has children" in out:
                rc, out = _add_children(task, parts, root)
            elif rc == 0:
                moved_note = _move_pending_locks(goal, task, parts[0], root)
        if rc != 0:
            refused = f"pursuit_plan: beagle refused (exit {rc}):\n{out}"
            if uncommitted_note:
                refused += f"\n\n{uncommitted_note}"
            return _step_result(refused)
        _forget_task(root, task)
        notes = "".join(f"{note}\n\n" for note in split_notes)
        if uncommitted_note:
            notes += f"{uncommitted_note}\n\n"
        if moved_note:
            notes += f"{moved_note}\n\n"
        if repeated:
            notes += f"Not added again, {task} already has: {', '.join(repeated)}.\n\n"
        if "--outcome abandoned" in out:
            notes += f"{ABANDON_HINT}\n\n"
        shown = _steer_resemblance(out, root)
        return _step_result(f"{shown}\n\n{_tree(root)}\n\n{notes}Next: pursuit_step.")

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
      `python3 -m json.tool cases.json`) and passes whatever it says;
    - a `bash -c '...'` script whose every `&&` part is one of the above.
    """
    try:
        words = shlex.split(command)
    except ValueError:
        return None  # beagle says why it will not split
    if not words:
        return None
    one_command = _ONE_COMMAND
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
            "more than one thing, name a new test file (e.g. tests/test_<name>.py) in "
            "scope and say in notes what it must check; the sub-agent writes it, not you. "
            "Call pursuit_step again with it."
        )
    program = Path(words[0]).name
    if program in _SHELLS and "-c" in words[1:-1]:
        # R13: `bash -c 'test -s A && test -s B'` passed this guard whole.
        segments = _and_segments(words[words.index("-c") + 1])
        if segments is None:
            return None
        left, objections = _judge_segments(segments)
        if not left:
            return _always_passes(command)
        return objections[0] if all(objections) else None
    if program in _ALWAYS_PASSES:
        return _always_passes(command)
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
    python = _past_runner(words)
    if not (python and Path(python[0]).name.startswith("python")):
        python = []
    if python and _only_imports(python[1:]):
        # Run R04 bound `python3 -c "from tests.test_case_data import
        # validate_fork_seed; print('OK')"`, which passes once the name exists.
        return (
            f"done_when `{command}` only imports and prints, so it passes as soon as the "
            f"file is there, whatever it says. {one_command}, testing what the code must "
            "do. Call pursuit_step again with that."
        )
    if python and _judges_nothing(python[1:]):
        # Run R14 closed T0007 on `t=IntervalTree(); t.insert(1, 5); t.search(3);
        # print('OK')`, which passes on any code that does not raise.
        return (
            f"done_when `{command}` only constructs and calls, with no assert, so it "
            "passes on any code that does not crash, whatever it returns. "
            f"{one_command}, asserting the values the reference gives. Call pursuit_step "
            "again with that."
        )
    if _key_only_json_check(command):
        # Run R12 closed T0002 on `assert 'title' in data and ...` over its
        # summary JSON, which held whatever the worker wrote under those keys.
        return (
            f"done_when `{command}` loads JSON and only asserts that keys are there, but a "
            "key check passes on any content; bind a test that compares values to the "
            "reference. " + one_command + ", asserting the values the reference gives. "
            "Call pursuit_step again with that."
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


_ONE_COMMAND = (
    "It must be ONE command over the project that exits 0 exactly when the task is "
    "done, such as `python3 -m pytest -q tests/test_greet.py`"
)


def _always_passes(command: str) -> str:
    return (
        f"done_when `{command}` exits 0 whatever the work does, so it cannot judge it. "
        f"{_ONE_COMMAND}. {ABANDON_HINT}"
    )


def _and_segments(command: str) -> list[list[str]] | None:
    """The shell words of `command` split on `&&`; None if it will not parse."""
    tokens = _shell_tokens(command)
    if tokens is None:
        return None
    segments: list[list[str]] = [[]]
    for token in tokens:
        if token == "&&":
            segments.append([])
        else:
            segments[-1].append(token)
    return segments


def _passes_anyway(argv: list[str]) -> bool:
    """Whether one `&&` part exits 0 whatever the work did: `true`, a plain `git diff`."""
    if not argv:
        return True
    program = Path(argv[0]).name
    if program in _ALWAYS_PASSES:
        return True
    if program != "git":
        return False
    sub = next((arg for arg in argv[1:] if not arg.startswith("-")), "")
    return sub == "diff" and not {"--exit-code", "--quiet"} & set(argv)


def _judge_segments(segments: list[list[str]]) -> tuple[list[list[str]], list[str | None]]:
    """The `&&` parts that can fail, and `_check_problem`'s objection to each.

    A part with its own shell operators (`echo ... | sha256sum -c`) runs under
    the shell it is in and is not judged here.
    """
    left = [segment for segment in segments if not _passes_anyway(segment)]
    objections = [
        None if any(_is_operator(t) for t in segment) else _check_problem(shlex.join(segment))
        for segment in left
    ]
    return left, objections


def _and_chain(command: str) -> tuple[str | None, str | None]:
    """The check to bind for `command` and why it cannot be bound; one is None.

    R13's driver resent a bare-`&&` check ten times against a refusal that gave
    it no move. A check whose only shell operator is `&&` is judged part by
    part: parts that pass anyway are dropped, one part left is quoted back as
    the check to send, and two or more that can judge the work are bound as
    `bash -c '<command>'`.
    """
    operators = _bare_operators(command)
    segments = _and_segments(command) if operators else None
    if segments is None or any(op != "&&" for op in operators):
        problem = _check_problem(command)
        return (None, problem) if problem is not None else (command, None)
    left, objections = _judge_segments(segments)
    if not left:
        return None, _always_passes(command)
    if all(objections):
        return None, objections[0]
    if len(left) == 1:
        return None, (
            "done_when joins commands with a bare '&&', which reaches the first as an "
            "argument, and only one of them can fail with the work; the rest pass "
            "whatever it does. Drop the rest and send this as done_when: "
            f"`{shlex.join(left[0])}`. Call pursuit_step again with it."
        )
    bound = f"bash -c {shlex.quote(command)}"
    problem = _check_problem(bound)
    return (None, problem) if problem is not None else (bound, None)


def _bound_note(done_when: str, bound: str) -> str:
    """What the result says when `_and_chain` rewrote the check, or ''."""
    if bound == done_when:
        return ""
    return f"done_when was bound through bash -c because of its bare '&&': `{bound}`.\n\n"


def _key_only_json_check(command: str) -> bool:
    """Whether a `python -c` check loads JSON and asserts only that keys are there."""
    code = _bash_find(command, _python_c_code)
    if code is None:
        return False
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    loads = any(
        isinstance(node, ast.Attribute)
        and node.attr in {"load", "loads"}
        and isinstance(node.value, ast.Name)
        and node.value.id == "json"
        for node in ast.walk(tree)
    )

    def key_check(test: ast.expr) -> bool:
        if isinstance(test, ast.Compare):
            return all(isinstance(op, (ast.In, ast.NotIn)) for op in test.ops)
        if isinstance(test, ast.BoolOp):
            return all(key_check(value) for value in test.values)
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            return key_check(test.operand)
        if (
            isinstance(test, ast.Call)
            and isinstance(test.func, ast.Name)
            and test.func.id in {"all", "any"}
            and len(test.args) == 1
            and isinstance(test.args[0], (ast.GeneratorExp, ast.ListComp))
        ):
            return key_check(test.args[0].elt)
        return False

    asserts = [node.test for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    return loads and bool(asserts) and all(key_check(test) for test in asserts)


_TEST_FRAMEWORKS = frozenset({"pytest", "unittest"})


def _runs_a_test_framework(tree: ast.AST) -> bool:
    """Whether code imports or calls pytest or unittest, not just names one in a string."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] in _TEST_FRAMEWORKS for alias in node.names
        ):
            return True
        if (
            isinstance(node, ast.ImportFrom)
            and (node.module or "").split(".")[0] in _TEST_FRAMEWORKS
        ):
            return True
        if isinstance(node, ast.Call):
            func = node.func
            while isinstance(func, ast.Attribute):
                func = func.value
            if isinstance(func, ast.Name) and func.id in _TEST_FRAMEWORKS:
                return True
    return False


def _judges_nothing(args: list[str]) -> bool:
    """Whether a python argv's `-c` code can fail only by raising.

    Code judges when it asserts, runs pytest or unittest, reaches `raise` or
    `sys.exit` through an `if`, or exits with a comparison it computed:
    `sys.exit(S().insert(1, 5))` exits with whatever the call returns.
    """
    if "-c" not in args or args.index("-c") + 1 >= len(args):
        return False
    code = args[args.index("-c") + 1]
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    if not tree.body or _runs_a_test_framework(tree):
        return False

    def exits(node: ast.AST) -> bool:
        if isinstance(node, ast.Raise):
            return True
        if not isinstance(node, ast.Call):
            return False
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        return name in {"exit", "_exit"}

    def compared(node: ast.AST) -> bool:
        return any(
            isinstance(n, (ast.Compare, ast.BoolOp, ast.IfExp))
            or (isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not))
            for n in ast.walk(node)
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            return False
        if isinstance(node, (ast.If, ast.While)) and any(
            exits(n) for stmt in node.body + node.orelse for n in ast.walk(stmt)
        ):
            return False
        if isinstance(node, ast.Call) and exits(node) and any(compared(arg) for arg in node.args):
            return False
        if isinstance(node, ast.Raise) and node.exc is not None and compared(node.exc):
            return False
    return True


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


def _under_references(path: str, root: Path | None) -> bool:
    """Whether a scope path, absolute or relative, is REFERENCES_DIR or inside it."""
    if root is None:
        return Path(path).parts[:1] == (REFERENCES_DIR,)
    folder = (root / REFERENCES_DIR).resolve()
    target = Path(path) if Path(path).is_absolute() else root / path
    return target.resolve().is_relative_to(folder)


def _scope_problem(
    scope: list[str],
    task: str = "",
    nodes: list[dict[str, Any]] | None = None,
    root: Path | None = None,
) -> str | None:
    """Why a task's scope is wrong, or None: it names beagle's own store or references/."""
    # Run R13: T0002 scoped references/NOTES.md, which founding git-ignores, so
    # the worker could write it but never commit it.
    refs = [path for path in scope if _under_references(path, root)]
    if refs:
        return (
            f"scope names {refs[0]}, but {REFERENCES_DIR}/ holds the fetched sources and "
            "is ignored by git, so nothing written there is committed; put the notes in "
            "docs/ (e.g. docs/NOTES.md)."
        )
    store = [path for path in scope if Path(path).parts[:1] == (".beagle",)]
    if not store:
        return None
    way_out = _setup_abandon_route(task) if _setup_abandonable(task, nodes or []) else ""
    return (
        f"scope names {store[0]}, beagle's own record of the pursuit. pursuit_found "
        "already set the pursuit up, and the tools keep its record; a task's work and "
        "scope are in the project. Name the project paths the task will touch." + way_out
    )


_SCOPE_WALK_SKIP = frozenset(
    {".git", ".beagle", "__pycache__", ".venv", "node_modules", ".tox", ".nox"}
)
_SCOPE_WALK_LIMIT = 2000


def _scope_dir_files(root: Path, rel: str) -> list[str]:
    """The files under a scope directory, relative to root, bounded and sorted."""
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root / rel):
        dirnames[:] = sorted(
            d for d in dirnames if d not in _SCOPE_WALK_SKIP and not d.endswith("_cache")
        )
        for name in sorted(filenames):
            found.append(Path(dirpath, name).relative_to(root).as_posix())
            if len(found) >= _SCOPE_WALK_LIMIT:
                return found
    return found


def _first_few(paths: list[str], few: int = 5) -> list[str]:
    return paths if len(paths) <= few else [*paths[:few], f"{len(paths) - few} more"]


def _module_names(rel: str) -> list[str]:
    """The dotted names `rel`, a .py file, may be imported as: each tail of its path."""
    parts = list(Path(rel).with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return [".".join(parts[i:]) for i in range(len(parts))]


def _judged_sources(
    entries: list[str], root: Path, check: str = ""
) -> tuple[list[str], list[str]]:
    """(source, helpers) among `entries`' non-test .py files.

    Run R31: a worker saved tests/casegen.py, a generator no test imported and the
    check did not name, beside tests/cases.json, and 51 calls were refused for
    holding "the code it judges". A .py under a test directory that is on disk
    counts as judged code only when a scope test, or one the check names,
    imports it or the check names it; otherwise it is a helper.
    """
    named = set(_check_path_words(check)) if check else set()
    tests = [
        rel
        for rel in dict.fromkeys([*entries, *named])
        if rel.endswith(".py") and _is_test_path(rel) and (root / rel).is_file()
    ]
    imported = {name for test in tests for name in _test_project_imports(root / test)}
    source: list[str] = []
    helpers: list[str] = []
    for rel in dict.fromkeys(e.rstrip("/") for e in entries):
        if not rel.endswith(".py") or _is_test_path(rel):
            continue
        names = _module_names(rel)
        used = rel in named or any(
            name == module or name.startswith(module + ".") or module.startswith(name + ".")
            for name in imported
            for module in names
        )
        if _in_tests_dir(rel) and (root / rel).is_file() and not used:
            helpers.append(rel)
        else:
            source.append(rel)
    return source, helpers


def _scope_entries(scope: list[str], root: Path) -> list[str]:
    """`scope`'s entries, each directory followed by its files."""
    entries: list[str] = []
    for rel in scope:
        entries.append(rel)
        # Run R09: scope src/, tests/ held tests/cases.json beside src/itc/*.py,
        # and a directory entry has neither suffix, so it is judged by its files.
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel.rstrip("/")))
    return entries


def _oracle_with_code_parts(
    scope: list[str], goal: Path, task: str = "", check: str = ""
) -> tuple[list[str], list[str], list[str]]:
    """(unlocked data, judged source, helpers) a scope holds."""
    # Run R31: the driver passed locks= 59 times; they were filed as the task's
    # pending locks, restored before each check as a manifest lock is.
    locked = set(_locked(goal)) | set(_pending_locks(goal, task) if task else [])
    root = goal.parent.parent
    entries = _scope_entries(scope, root)
    data = [
        rel.rstrip("/")
        for rel in entries
        if _is_test_path(rel.rstrip("/"))
        and Path(rel.rstrip("/")).suffix not in {"", ".py"}
        and rel.rstrip("/") not in locked
    ]
    source, helpers = _judged_sources(entries, root, check)
    return list(dict.fromkeys(data)), source, helpers


def _helper_note(helpers: list[str]) -> str:
    if not helpers:
        return ""
    return (
        f" {', '.join(_first_few(helpers))}: a helper script no test imports and the check "
        "does not name; delete it or leave it out of scope."
    )


def _oracle_with_code_problem(
    scope: list[str], goal: Path, task: str = "", check: str = ""
) -> str | None:
    """Why a scope writes known answers beside the code they judge, or None.

    Run R08: T0004's scope held itc/tests/cases.json, its test and the module,
    so the worker wrote wrong expected values to fit its code, and every later
    task was graded against them. A data file locked by an earlier task, or
    filed as this task's pending lock, is restored before each check, so it is
    no oracle the worker can bend.
    """
    data, source, helpers = _oracle_with_code_parts(scope, goal, task, check)
    if not data or not source:
        return None
    data, source = _first_few(data), _first_few(source)
    return (
        f"scope holds known-answer data ({', '.join(data)}) and the code it judges "
        f"({', '.join(source)}). Split it: first a task with only the data and its cases "
        f"test in scope, passing locks=[{', '.join(data)}]; then the code in a later task."
        + _helper_note(helpers)
    )


def _narrowed_scope(scope: list[str], goal: Path, task: str, check: str) -> list[str] | None:
    """`scope` without its judged source, when that leaves a scope the guard passes."""
    root = goal.parent.parent
    _, source, helpers = _oracle_with_code_parts(scope, goal, task, check)
    drop = set(source) | set(helpers)
    narrowed: list[str] = []
    for rel in scope:
        bare = rel.rstrip("/")
        if (root / bare).is_dir() and any(d.startswith(bare + "/") for d in drop):
            narrowed.extend(f for f in _scope_dir_files(root, bare) if f not in drop)
        elif bare not in drop:
            narrowed.append(rel)
    narrowed = list(dict.fromkeys(narrowed))
    if not narrowed or _oracle_with_code_problem(narrowed, goal, task, check) is not None:
        return None
    return narrowed


def _open_mixed_refusal(scope: list[str], goal: Path, task: str, check: str) -> str | None:
    """The open-task refusal for a mixed scope, naming the narrowed call that runs."""
    data, source, helpers = _oracle_with_code_parts(scope, goal, task, check)
    if not data or not source:
        return None
    narrowed = _narrowed_scope(scope, goal, task, check)
    held = (
        f"scope holds known-answer data ({', '.join(_first_few(data))}) and the code it "
        f"judges ({', '.join(_first_few(source))})."
    )
    if narrowed is None:
        return (
            f"{held} Narrow the scope to the data and its cases test, passing "
            f"locks=[{', '.join(_first_few(data))}]; the code goes to a later task."
            + _helper_note(helpers)
        )
    removed = [*source, *helpers]
    return (
        f"{held} This call runs a worker: pursuit_step task={task} "
        f"scope=[{', '.join(narrowed)}] notes=\"delete {', '.join(_first_few(removed))} if "
        "this task wrote it; the code belongs to a later task\"." + _helper_note(helpers)
    )


#: (root, task) -> (scope, text) of the last open-task mixed-scope refusal.
_LAST_MIXED_REFUSAL: dict[tuple[str, str], tuple[tuple[str, ...], str]] = {}


def _check_path_words(check: str) -> list[str]:
    """The relative paths a check's words name, inside one `sh -c` level, written or not."""
    try:
        words = shlex.split(check)
    except ValueError:
        return []
    found: list[str] = []
    for word in words:
        inner = shlex.split(word) if " " in word and not word.startswith("-") else [word]
        for part in inner:
            rel = part.split("::")[0].rstrip("/")
            if "/" not in rel or rel.startswith("-") or Path(rel).is_absolute():
                continue
            if ".." in Path(rel).parts or Path(rel).parts[0] == ".beagle":
                continue
            if rel not in found:
                found.append(rel)
    return found


def _scope_holds_code_or_cases(
    scope: list[str], root: Path, also: list[str] | None = None, tests_count: bool = True
) -> bool:
    """Whether `scope` (its directories walked) or `also` holds a .py file or cases data.

    With `tests_count` false, a test .py is not code: only source counts.
    """
    entries = [rel.rstrip("/") for rel in [*scope, *(also or [])]]
    for rel in list(entries):
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel))
    return any(
        _is_cases_data(rel) or (rel.endswith(".py") and (tests_count or not _is_test_path(rel)))
        for rel in entries
    )


def _doc_only_check_problem(check: str, scope: list[str], task: str, root: Path) -> str | None:
    """Why a task whose check reads only non-.py files under tests/ may not open, or None.

    Run R29 opened T0006 on a grep over a digest it wrote under tests/, with
    no code or cases data in scope: no defect could be put back to prove the
    check, so the task could never close done.
    """
    reads = _check_path_words(check)
    if not reads or not all(_in_tests_dir(rel) and not rel.endswith(".py") for rel in reads):
        return None
    if _scope_holds_code_or_cases(scope, root, reads, tests_count=False):
        return None
    return (
        f"{reads[0]} is under tests/, so nothing can witness it; fold reading the "
        f"reference into the known-answers task, or abandon {task}: "
        f'pursuit_step task="{task}", abandon="folded into the known-answers task".'
    )


def _no_scope_problem(scope: list[str], root: Path, locks: list[str], check: str) -> str | None:
    """Why a task may not open with no scope, or None.

    Run R17: T0002, T0008 and T0009 opened with scope [], so no worker on them
    was held to any path. With references/ fetched the pursuit is past founding,
    and every task it opens writes something nameable.
    """
    if scope or not (root / "references").is_dir():
        return None
    if not locks:
        return (
            "no scope given, so its sub-agent would write anywhere. Pass scope=[...] "
            "naming the paths this task writes, and call pursuit_step again."
        )
    named = re.findall(r"\S*test_\w*(?:case|data)\w*\.py", check)
    data_test = named[0] if named else "tests/test_case_data.py"
    paths = list(dict.fromkeys([*locks, data_test]))
    return (
        "no scope given, so its sub-agent would write anywhere, the code its known "
        f"answers judge included. Pass scope=[{', '.join(paths)}] (the locks and the "
        "data test), and call pursuit_step again."
    )


def _data_task(scope: list[str], goal: Path, check: str, locks: list[str]) -> bool:
    """Whether a task writes known-answer data and its cases test, not the code.

    Judged as `_oracle_with_code_problem` judges a scope's entries, with a
    directory judged by its files; a scope holding no data yet counts when its
    check names a cases or data test.
    """
    root = goal.parent.parent
    entries: list[str] = []
    for rel in scope:
        entries.append(rel)
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel.rstrip("/")))
    if any(rel.endswith(".py") and not _is_test_path(rel) for rel in entries):
        return False
    if locks:
        return True
    data = any(
        _is_test_path(rel.rstrip("/")) and Path(rel.rstrip("/")).suffix not in {"", ".py"}
        for rel in entries
    )
    return data or bool(re.search(r"test_\w*(case|data)", check))


#: Root-level directories that hold no package of the project's own.
_NOT_PACKAGES = frozenset(
    {"docs", "doc", "references", "tests", "test", "data", "examples", "scripts", "notes"}
)
#: Imports in a test that name no module of the project's.
_TEST_LIBRARIES = frozenset({"pytest", "_pytest", "hypothesis", "tests", "test", "conftest"})


def _head_files(root: Path) -> set[str] | None:
    """The files git holds at HEAD, or None when there is no HEAD to ask."""
    try:
        done = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    return set(done.stdout.splitlines()) if done.returncode == 0 else None


def _module_of(rel: str) -> str:
    """The dotted module a source path under src/ or the root holds."""
    path = rel.removeprefix("src/").removesuffix(".py").removesuffix("/__init__")
    return path.replace("/", ".")


def _new_modules(scope: list[str], root: Path) -> list[tuple[str, str]]:
    """Each new (absent at HEAD) source module a scope names: (entry, dotted name).

    A non-test .py file counts, and so does a package directory under src/ or
    the root; a bare `src/` names a module not yet known, given as "".
    """
    head = _head_files(root)

    def absent(rel: str) -> bool:
        if head is None:
            return not (root / rel).exists()
        return rel not in head and not any(f.startswith(f"{rel}/") for f in head)

    found: list[tuple[str, str]] = []
    for entry in scope:
        rel = entry.strip().rstrip("/")
        parts = Path(rel).parts
        if not rel or _is_test_path(rel) or Path(rel).name in {"tests", "test"}:
            continue
        if rel.endswith(".py"):
            if absent(rel):
                found.append((rel, _module_of(rel)))
            continue
        if Path(rel).suffix:
            continue
        if (root / rel).is_dir():
            files = [
                f
                for f in _scope_dir_files(root, rel)
                if f.endswith(".py") and not _is_test_path(f) and absent(f)
            ]
            found += [(f, _module_of(f)) for f in files]
            if files:
                continue
        package = (
            parts == ("src",)
            or (len(parts) == 2 and parts[0] == "src" and parts[1].isidentifier())
            or (len(parts) == 1 and parts[0].isidentifier() and parts[0] not in _NOT_PACKAGES)
        )
        if package and absent(rel):
            found.append((entry, "" if parts == ("src",) else parts[-1]))
    return found


#: Suffixes of a known-answers data file a cases test must read.
CASES_DATA_SUFFIXES = frozenset({".json", ".toml", ".yaml", ".yml", ".csv"})


def _is_cases_data(rel: str) -> bool:
    return Path(rel).suffix in CASES_DATA_SUFFIXES and _is_test_path(rel)


def _cases_test_reads(test_path: Path, data_basename: str) -> bool:
    """Whether the test's code, not a docstring or comment, opens the data file.

    Run R14: test_cases.py held hand-written asserts and never opened
    cases.json, so the locked known answers judged nothing. The read call
    (open, Path, read_text, json.load) must take the file: a string naming it,
    or a name assigned from one. A message string naming it elsewhere does not.
    Run R33: `<path>.open()` and `json.load(fh)` on a `with ... as fh` handle
    went uncounted, so the receiver of open/read_text/read_bytes counts as
    taken, and a `with ... as` target binds a name the way an assignment does.
    """
    try:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return False
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list):
            node.body = [  # type: ignore[attr-defined]
                stmt
                for stmt in body
                if not (
                    isinstance(stmt, ast.Expr)
                    and isinstance(stmt.value, ast.Constant)
                    and isinstance(stmt.value.value, str)
                )
            ]
    names: set[str] = set()

    def mentions(node: ast.AST) -> bool:
        return any(
            (
                isinstance(sub, ast.Constant)
                and isinstance(sub.value, str)
                and data_basename in sub.value
            )
            or (isinstance(sub, ast.Name) and sub.id in names)
            for sub in ast.walk(node)
        )

    bindings: list[tuple[ast.AST, list[ast.AST]]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            bindings.append((node.value, node.targets))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            bindings.append((node.value, [node.target]))
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            bindings.append((node.context_expr, [node.optional_vars]))
    grew = True
    while grew:
        grew = False
        for value, targets in bindings:
            if not mentions(value):
                continue
            for target in targets:
                if isinstance(target, ast.Name) and target.id not in names:
                    names.add(target.id)
                    grew = True
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        given: list[ast.AST] = [*node.args, *(k.value for k in node.keywords)]
        if isinstance(func, ast.Name):
            reads = func.id in {"open", "Path"}
        elif isinstance(func, ast.Attribute):
            reads = func.attr in {"read_text", "read_bytes", "open", "Path"} or (
                func.attr in {"load", "loads"}
                and isinstance(func.value, ast.Name)
                and func.value.id == "json"
            )
            if func.attr in {"read_text", "read_bytes", "open"}:
                given.append(func.value)
        else:
            reads = False
        if reads and any(mentions(arg) for arg in given):
            return True
    return False


def _test_project_imports(test_path: Path) -> list[str]:
    """The project modules a test file imports: not stdlib, test libraries or tests."""
    try:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return []
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names = [node.module]
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            if top in sys.stdlib_module_names or top in _TEST_LIBRARIES:
                continue
            if top.startswith("test_") or name in found:
                continue
            found.append(name)
    return found


def _unread_cases(root: Path, entries: list[str]) -> tuple[str, str] | None:
    """(test, data file) when the locks hold a cases data file the code's tests never read.

    Run R14 locked a data-shape test that loaded cases.json beside a test that
    imported the code and never read it. When a locked test imports the code,
    one such test must read each data file; a test importing nothing of the
    project does not count.
    """
    files = []
    for entry in entries:
        target = _project_file(root, entry)
        if target is not None and target.is_file():
            files.append(str(target.relative_to(root.resolve())))
    tests = [rel for rel in files if rel.endswith(".py") and _is_test_path(rel)]
    judges = [rel for rel in tests if _test_project_imports(root / rel)]
    readers = judges or tests
    for data in (rel for rel in files if _is_cases_data(rel)):
        name = Path(data).name
        if readers and not any(_cases_test_reads(root / test, name) for test in readers):
            return readers[0], data
    return None


#: Case keys that hold a case's label, inputs or provenance rather than its answer.
_CASE_NON_ANSWER_KEYS = frozenset(
    {
        "name", "id", "title", "case", "source", "sources", "citation", "description",
        "desc", "notes", "note", "comment", "input", "inputs", "in", "args", "arguments",
        "ops", "operations", "operation", "setup", "given",
    }
)


def _case_labels(cases: list[object]) -> set[str]:
    return {
        str(case[key])
        for case in cases
        if isinstance(case, dict)
        for key in ("name", "id")
        if isinstance(case.get(key), str | int)
    }


def _answer_keys(cases: list[object]) -> set[str]:
    keys = {key for case in cases if isinstance(case, dict) for key in case}
    return {
        key
        for key in keys
        if isinstance(key, str)
        and key.lower() not in _CASE_NON_ANSWER_KEYS
        and not any(part in key.lower() for part in SOURCE_KEY_PARTS)
    }


def _str_const(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _json_loaded_names(tree: ast.AST) -> set[str]:
    """Names assigned straight from a `json.load` or `json.loads` call."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign | ast.AnnAssign) or node.value is None:
            continue
        call = node.value
        if not (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr in {"load", "loads"}
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == "json"
        ):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names.update(t.id for t in targets if isinstance(t, ast.Name))
    return names


def _absent_case_lookup(tree: ast.AST, labels: set[str], keys: Collection[str] = ()) -> str | None:
    """The first case label the test looks up that the data does not hold, or None.

    Run R22: `cases["cases"]` took the list from {"cases": [...]}. A subscript
    by one of the data file's own top-level `keys`, or of a value straight
    from `json.load`, reads the file's container, not a case.
    """
    loaded = _json_loaded_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            sides = [node.left, *node.comparators]
            keyed = any(
                isinstance(side, ast.Subscript) and _str_const(side.slice) in {"name", "id"}
                for side in sides
            )
            if keyed:
                for side in sides:
                    named = _str_const(side)
                    if named is not None and named not in labels:
                        return named
        elif (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and "cases" in node.value.id.lower()
            and node.value.id not in loaded
        ):
            named = _str_const(node.slice)
            if named is not None and named not in labels and named not in keys:
                return named
    return None


def _method_and_value(tree: ast.AST) -> str | None:
    called = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            operands = [node.left, *node.comparators]
        elif isinstance(node, ast.BinOp):
            operands = [node.left, node.right]
        elif isinstance(node, ast.AugAssign):
            operands = [node.target, node.value]
        else:
            continue
        for operand in operands:
            if isinstance(operand, ast.Attribute) and operand.attr in called:
                return operand.attr
    return None


def _answers_compared(tree: ast.AST, answers: Collection[str]) -> bool:
    """Whether a value read under one of the `answers` keys reaches an assert or comparison.

    Run R30: the locked test loaded each case's answer and asserted only a
    roundtrip. A read is a subscript, `.get()` or attribute by an answer key; a
    name assigned or looped from one, or a function returning one, carries it.
    """

    def reads(node: ast.AST) -> bool:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Subscript) and _str_const(sub.slice) in answers:
                return True
            if isinstance(sub, ast.Attribute) and sub.attr in answers:
                return True
            if (
                isinstance(sub, ast.Call)
                and isinstance(sub.func, ast.Attribute)
                and sub.func.attr == "get"
                and sub.args
                and _str_const(sub.args[0]) in answers
            ):
                return True
            if isinstance(sub, ast.Name) and sub.id in carriers:
                return True
        return False

    def names(target: ast.AST) -> set[str]:
        return {sub.id for sub in ast.walk(target) if isinstance(sub, ast.Name)}

    carriers: set[str] = set()
    grew = True
    while grew:
        before = len(carriers)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and reads(node.value):
                carriers.update(n for target in node.targets for n in names(target))
            elif (
                isinstance(node, ast.AnnAssign | ast.AugAssign | ast.NamedExpr)
                and node.value is not None
                and reads(node.value)
            ) or (
                isinstance(node, ast.For | ast.AsyncFor | ast.comprehension) and reads(node.iter)
            ):
                carriers.update(names(node.target))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and any(
                isinstance(sub, ast.Return) and sub.value is not None and reads(sub.value)
                for sub in ast.walk(node)
            ):
                carriers.add(node.name)
        grew = len(carriers) > before
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert | ast.Compare) and reads(node):
            return True
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr.startswith("assert")
            and reads(node)
        ):
            return True
    return False


#: Names a module has bound without an import or assignment in its own source.
_MODULE_IMPLICIT_NAMES = frozenset(
    {*dir(builtins), "__file__", "__name__", "__doc__", "__spec__", "__loader__"}
)


def _test_structure_problem(tree: ast.Module) -> str | None:
    """What keeps a test module from judging anything, read from its AST alone.

    Run R33: a cases test defined only helpers, so pytest collected nothing,
    and called `name.attr(...)` on a module it never imported, so it could not
    run. Collected: a module-level `test*` function, or a `test*` method of a
    module-level `Test*` class.
    """

    def is_test(node: ast.AST) -> bool:
        return isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(
            "test"
        )

    imported: set[str] = set()
    star = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                star = star or alias.name == "*"
                imported.add(alias.asname or alias.name.split(".")[0])
    collectable = any(
        is_test(node)
        or (
            isinstance(node, ast.ClassDef)
            and node.name.startswith("Test")
            and any(is_test(sub) for sub in node.body)
        )
        for node in tree.body
    ) or any(name.startswith("test") for name in imported)
    if not collectable:
        return "defines no test function pytest collects (no test* function or Test* class)"
    if star:
        return None
    bound = set(imported) | _MODULE_IMPLICIT_NAMES
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store | ast.Del):
            bound.add(node.id)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(
            node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
        ) or (isinstance(node, ast.ExceptHandler | ast.MatchAs | ast.MatchStar) and node.name):
            bound.add(node.name)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            bound.add(node.rest)
        elif isinstance(node, ast.Global | ast.Nonlocal):
            bound.update(node.names)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id not in bound
        ):
            name = node.func.value.id
            return f"uses {name}.{node.func.attr}() without importing {name}"
    return None


def _cases_test_problem(root: Path, entries: list[str]) -> tuple[str, str] | None:
    """(test, what is wrong) when a locked test reading cases data could never judge it.

    Run R20 locked a test_cases.py that looked up three case names cases.json
    did not hold, never read a case's "expected", and used `.event` both as a
    method and as a number. Read from each test's AST; nothing is run. The
    unread-answers check applies only to tests importing the project, as the
    data's own shape test reads no answers.
    """
    files = []
    for entry in entries:
        target = _project_file(root, entry)
        if target is not None and target.is_file():
            files.append(str(target.relative_to(root.resolve())))
    tests = [rel for rel in files if rel.endswith(".py") and _is_test_path(rel)]
    for data in (rel for rel in files if _is_cases_data(rel) and rel.endswith(".json")):
        try:
            raw = json.loads((root / data).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        cases = _cases_list(raw)
        keys = {str(key) for key in raw} if isinstance(raw, dict) else set()
        labels = _case_labels(cases)
        answers = _answer_keys(cases)
        for test in tests:
            if not _cases_test_reads(root / test, Path(data).name):
                continue
            try:
                tree = ast.parse((root / test).read_text(encoding="utf-8"))
            except (OSError, SyntaxError, ValueError):
                continue
            broken = _test_structure_problem(tree)
            if broken is not None:
                return test, broken
            absent = _absent_case_lookup(tree, labels, keys) if labels else None
            if absent is not None:
                return test, f'looks up case "{absent}", which {data} does not hold'
            mentioned = {
                text
                for node in ast.walk(tree)
                for text in (_str_const(node), getattr(node, "attr", None))
                if isinstance(text, str)
            }
            if answers and _test_project_imports(root / test) and not answers & mentioned:
                keys = ", ".join(f'"{key}"' for key in sorted(answers))
                return test, f"never reads the cases' answers ({keys} in {data})"
            if (
                answers
                and _test_project_imports(root / test)
                and not _answers_compared(tree, answers)
            ):
                keys = ", ".join(f'"{key}"' for key in sorted(answers))
                return test, (
                    f"reads the cases' answers ({keys} in {data}) but never compares them: no "
                    "assert or comparison uses them, so a wrong result the test never checks "
                    "against an answer passes"
                )
            both = _method_and_value(tree)
            if both is not None:
                return test, (
                    f"uses .{both} both as a method, .{both}(), and as a value in a "
                    "comparison or arithmetic, so it cannot pass against any one code"
                )
    return None

#: Words a case's source must quote from references/*.txt to count as found.
SOURCE_QUOTE_MIN_WORDS = 4
#: Key fragments that mark where a case keeps its source text.
SOURCE_KEY_PARTS = ("source", "cite", "quote", "ref")
#: Pairs of marks a quote may sit between inside a longer source string.
_QUOTE_MARKS = re.compile(r'"([^"]+)"|“([^”]+)”|`([^`]+)`|\'([^\']{12,})\'')


def _normalised(text: str) -> str:
    return " ".join(text.split()).lower()


def _strings_in(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for item in value.values() for s in _strings_in(item)]
    if isinstance(value, list):
        return [s for item in value for s in _strings_in(item)]
    return []


def _source_strings(case: object) -> list[str]:
    """The strings under a case's source-like keys, at any depth; else all its strings."""
    found: list[str] = []
    keyed = False

    def walk(value: object) -> None:
        nonlocal keyed
        if isinstance(value, dict):
            for key, item in value.items():
                if any(part in str(key).lower() for part in SOURCE_KEY_PARTS):
                    keyed = True
                    found.extend(_strings_in(item))
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(case)
    return found if keyed else _strings_in(case)


def _quotes_reference(text: str, reference: str) -> bool:
    """Whether `text`, whole, quoted in it, or split at an ellipsis or colon, is in `reference`.

    Run R15: a leading label ('send: This operation is ...' against the
    reference's 'send This operation ...') and a formula after a colon that
    the reference's PDF extraction spaced differently hid verbatim quotes.
    """
    candidates = [text]
    candidates += [next(g for g in m.groups() if g) for m in _QUOTE_MARKS.finditer(text)]
    candidates += [part for c in list(candidates) for part in re.split(r"\.\.\.|…|:\s", c)]
    for candidate in candidates:
        quote = _normalised(candidate).strip(" \"'`“”.,;:")
        if len(quote.split()) >= SOURCE_QUOTE_MIN_WORDS and quote in reference:
            return True
    return False


def _cases_list(data: object) -> list[object]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        lists = [v for v in data.values() if isinstance(v, list) and v]
        if lists:
            return max(lists, key=len)
        if data and all(isinstance(v, dict) for v in data.values()):
            return [{"name": k, **v} for k, v in data.items()]
    return []


def _case_label(case: object, index: int) -> str:
    if isinstance(case, dict):
        for key in ("name", "id", "title", "case"):
            if isinstance(case.get(key), str | int) and str(case[key]).strip():
                return str(case[key])
    return f"#{index + 1}"


#: Key fragments that mark a case's expected result.
RESULT_KEY_PARTS = ("expect", "result", "output", "want", "answer")
#: A scalar or string result shorter than this is not searched for: "1", "ok"
#: or a bool occurs in, or is absent from, any source by chance.
RESULT_MIN_CHARS = 4
#: A number-like token in a source: decimal, hex with 0x or \x, or bare hex digits.
_VALUE_TOKEN = re.compile(r"(0x|\\x)?([0-9a-fA-F]+)(?![0-9a-zA-Z])", re.IGNORECASE)
#: What may sit between two tokens of one rendered sequence.
_VALUE_SEPARATOR = re.compile(r"[\s,;\[\]()\-]*")
_ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*[,;]?\s*")
_GAP = "…"


def _value_runs(text: str, base: int) -> list[list[int | str]]:
    """The runs of values `text` renders in `base` (10, or 16 as bytes), split where
    anything but a separator or an ellipsis (kept as _GAP) sits between tokens."""
    runs: list[list[int | str]] = []
    run: list[int | str] = []
    end = 0
    for match in _VALUE_TOKEN.finditer(text):
        between = text[end : match.start()]
        if _ELLIPSIS.fullmatch(between) and run:
            run.append(_GAP)
        elif not _VALUE_SEPARATOR.fullmatch(between):
            if run:
                runs.append(run)
            run = []
        end = match.end()
        prefix, digits = match.group(1), match.group(2)
        values: list[int | str] | None
        if match.start() > 0 and text[match.start() - 1].isalnum() and not prefix:
            values = None  # the tail of a word, not a token
        elif base == 10:
            values = [int(digits)] if not prefix and digits.isdigit() else None
        elif prefix:
            values = [int(digits, 16)]
        else:
            values = (
                [int(digits[i : i + 2], 16) for i in range(0, len(digits), 2)]
                if len(digits) % 2 == 0
                else None
            )
        if values is None:
            if run:
                runs.append(run)
            run = []
        else:
            run.extend(values)
    if run:
        runs.append(run)
    return runs


def _holds_sequence(run: list[int | str], want: list[int]) -> bool:
    """Whether `run` is `want` exactly, or its head and tail around an ellipsis.

    Whole runs, not a slice of one: run R34's wrong [1, 0] sits inside the
    reference's `01 01 00`.
    """
    pieces: list[list[int]] = [[]]
    for value in run:
        if value == _GAP:
            pieces.append([])
        else:
            pieces[-1].append(int(value))
    if len(pieces) == 1:
        return pieces[0] == want
    head, *middle, tail = pieces
    if not head or not tail or len(head) + len(tail) >= len(want):
        return False
    if want[: len(head)] != head or want[len(want) - len(tail) :] != tail:
        return False
    at, stop = len(head), len(want) - len(tail)
    for part in middle:
        found = next(
            (i for i in range(at + 1, stop - len(part)) if want[i : i + len(part)] == part), -1
        )
        if not part or found < 0:
            return False
        at = found + len(part)
    return True


def _renders_result(text: str, result: object) -> bool:
    """Whether `text` holds `result` as the reference would print it.

    A list of ints as decimal tokens or two-digit hex bytes (with or without 0x
    or \\x, with or without separators), a long one by its head and tail around
    an ellipsis; a number by str() or hex; a string by itself, whitespace aside,
    or as the bytes it spells in hex.
    """
    if isinstance(result, list):
        want = [int(v) for v in result]
        bases = (10, 16) if all(0 <= v <= 255 for v in want) else (10,)
        return any(
            _holds_sequence(run, want) for base in bases for run in _value_runs(text, base)
        )
    if isinstance(result, int | float):
        tokens = {str(v) for run in _value_runs(text, 10) for v in run}
        tokens |= {
            str(int(m.group(2), 16)) for m in _VALUE_TOKEN.finditer(text) if m.group(1)
        }
        return str(result) in tokens or str(result) in text
    flat = "".join(str(result).split()).lower()
    if flat in "".join(text.split()).lower():
        return True
    spelled = str(result).strip().lower()
    if not re.fullmatch(r"(?:(?:0x|\\x)?[0-9a-f]{2}[\s,:\-]*)+", spelled):
        return False
    digits = re.sub(r"0x|\\x", "", spelled)
    return _renders_result(text, [int(b, 16) for b in re.findall(r"[0-9a-f]{2}", digits)])


def _searchable_result(value: object) -> bool:
    """Whether a case's result has a rendering worth searching a source for."""
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, list):
        return bool(value) and all(
            isinstance(v, int) and not isinstance(v, bool) for v in value
        )
    if isinstance(value, int | float | str):
        return len(str(value).strip()) >= RESULT_MIN_CHARS
    return False


def _case_results(case: object) -> list[object]:
    """The searchable results under a case's result-like keys that are not one of its inputs.

    Run R34: expected_decoded equalled the input a source quoted, so it shows
    nothing about whether the source gives the result.
    """
    if not isinstance(case, dict):
        return []
    inputs = [
        value
        for key, value in case.items()
        if str(key).lower() in _CASE_NON_ANSWER_KEYS
        and not any(part in str(key).lower() for part in SOURCE_KEY_PARTS)
    ]
    results: list[object] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif _searchable_result(value) and value not in inputs:
            results.append(value)

    for key, value in case.items():
        name = str(key).lower()
        if name == "out" or any(part in name for part in RESULT_KEY_PARTS):
            walk(value)
    return results


def _lines_after(source: str, lines: list[str]) -> list[str]:
    """The next non-blank reference line after each line a quote in `source` ends on."""
    found: list[str] = []
    joined = " ".join(lines)
    starts = list(itertools.accumulate((len(line) + 1 for line in lines), initial=0))
    candidates = [source]
    candidates += [next(g for g in m.groups() if g) for m in _QUOTE_MARKS.finditer(source)]
    for candidate in candidates:
        quote = _normalised(candidate).strip(" \"'`“”.,;:")
        if not quote:
            continue
        at = joined.find(quote)
        while at >= 0:
            line = bisect.bisect_right(starts, at + len(quote) - 1) - 1
            if line + 1 < len(lines):
                found.append(lines[line + 1])
            at = joined.find(quote, at + 1)
    return found


def _result_unquoted(case: object, references: list[list[str]]) -> bool:
    """Whether `case` has a searchable result that neither its source nor the reference
    line after the quoted one holds."""
    results = _case_results(case)
    if not results:
        return False
    sources = _source_strings(case)
    texts = [*sources]
    for lines in references:
        for source in sources:
            texts += _lines_after(source, lines)
    return not any(_renders_result(text, result) for text in texts for result in results)


def _unquoted_cases(
    root: Path, entries: list[str]
) -> tuple[str, int, int, list[str], bool] | None:
    """(data file, unfound, total, up to 3 names, whether by result) for cases whose source
    does not tie them to references/*.txt.

    Runs R12 and R14: cases cited bare URLs, nothing, or `itc2008.txt:221`,
    a line that held a page number. A source counts as found when at least
    SOURCE_QUOTE_MIN_WORDS words of it occur, whitespace-normalised, in one
    reference text; most must be found.

    Run R34: every source was verbatim, but 11 of 13 quoted the case's input
    line or prose, and 8 expected values were wrong. Any case with a searchable
    result (`_case_results`) must have it in its source or the reference line
    after the one quoted; the last element is then True.
    """
    refs = root / REFERENCES_DIR
    texts = []
    references: list[list[str]] = []
    for path in sorted(refs.glob("*.txt")) if refs.is_dir() else []:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        texts.append(_normalised(raw))
        references.append([_normalised(line) for line in raw.splitlines() if line.strip()])
    if not texts:
        return None
    for entry in entries:
        target = _project_file(root, entry)
        if target is None or not target.is_file() or target.suffix != ".json":
            continue
        rel = str(target.relative_to(root.resolve()))
        if not _is_cases_data(rel):
            continue
        try:
            cases = _cases_list(json.loads(target.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
        unfound = [
            _case_label(case, i)
            for i, case in enumerate(cases)
            if not any(
                _quotes_reference(s, text) for s in _source_strings(case) for text in texts
            )
        ]
        if cases and 2 * len(unfound) > len(cases):
            return rel, len(unfound), len(cases), unfound[:3], False
        wrong = [
            _case_label(case, i)
            for i, case in enumerate(cases)
            if _result_unquoted(case, references)
        ]
        if wrong:
            return rel, len(wrong), len(cases), wrong[:3], True
    return None


def _reads_locked_data(root: Path, test: str, data: list[str]) -> bool:
    """Whether `test` reads one of the `data` files and imports a project module.

    The same AST reads as `_unread_cases`: the test opens the file by name, and
    imports a module that is neither stdlib, a test library nor a test.
    """
    names = {Path(rel).name for rel in data}
    path = root / test
    return (
        test.endswith(".py")
        and _is_test_path(test)
        and any(_cases_test_reads(path, name) for name in names)
        and bool(_test_project_imports(path))
    )


def _cases_tests_beside_locks(
    root: Path, goal: Path, changed: list[str], locks: list[str]
) -> list[str]:
    """The changed tests, not in `locks`, that read locked data and import the code.

    Run R22: T0002 locked tests/cases.json alone, and its committed
    tests/test_cases.py, which read it and imported cobs, stayed unlocked, so
    Cases first refused every code task after it.
    """
    named = set()
    for entry in locks:
        target = _project_file(root, entry)
        if target is not None:
            named.add(str(target.relative_to(root.resolve())))
    data = [rel for rel in [*named, *_locked(goal)] if _is_cases_data(rel)]
    if not data:
        return []
    held = named | set(_locked(goal))
    return [rel for rel in changed if rel not in held and _reads_locked_data(root, rel, data)]


def _locked_test_imports(goal: Path) -> dict[str, str]:
    """Each project module a locked test file imports, with the first test importing it.

    With a cases data file locked, a test that reads none of them is skipped:
    its own asserts, not the known answers, would judge the code.
    """
    store = goal.parent / LOCKED_DIR
    imported: dict[str, str] = {}
    locked = _locked(goal)
    data = [Path(rel).name for rel in locked if _is_cases_data(rel)]
    for rel in locked:
        if not rel.endswith(".py") or not _is_test_path(rel):
            continue
        if data and not any(_cases_test_reads(store / rel, name) for name in data):
            continue
        for name in _test_project_imports(store / rel):
            imported.setdefault(name, rel)
    return imported


def _runs_test_file(command: str, rel: str) -> bool:
    """Whether `command` runs pytest over `rel`: the file, a node id or `-k` in it, a
    directory holding it, or the whole suite; or runs `rel` as a python script."""
    try:
        words = shlex.split(command)
    except ValueError:
        return False
    tokens: list[str] = []
    for word in words:
        tokens.append(word)
        if " " in word:
            with contextlib.suppress(ValueError):
                tokens += shlex.split(word)
    runs = [i for i, t in enumerate(tokens) if Path(t).name in {"pytest", "py.test"}]
    for at in runs:
        paths = []
        for token in tokens[at + 1 :]:
            if token in {"&&", "||", ";", "|"} or token.endswith(";"):
                break
            if not token.startswith("-") and ("/" in token or token.endswith(".py")):
                paths.append(token.split("::")[0].rstrip("/"))
        if not paths or any(p in {"", "."} or p == rel or rel.startswith(f"{p}/") for p in paths):
            return True
    return any(
        _python_script(tokens[at + 1 :]) == rel
        for at, t in enumerate(tokens)
        if _PYTHON_NAME.fullmatch(Path(t).name)
    )


#: An interpreter name a check runs a test script with: python, python3, python3.N.
_PYTHON_NAME = re.compile(r"python(?:3(?:\.\d+)?)?")


def _python_script(args: list[str]) -> str | None:
    """The script an interpreter's arguments run, or None for `-c`, `-m` or none.

    Run R26 bound T0007-T0011 to `python3 tests/test_case_data.py`; pytest-only
    matching saw no test run and called the scope's proof a module mutation.
    """
    skip = False
    for token in args:
        if skip:
            skip = False
            continue
        if token in {"-c", "-m"} or token in {"&&", "||", ";", "|"}:
            return None
        if token in {"-W", "-X"}:
            skip = True
            continue
        if token.startswith("-"):
            continue
        return token.rstrip(";").removeprefix("./")
    return None


def _locked_test_problem(command: str, scope: list[str], goal: Path) -> str | None:
    """Why a part on a module a locked test judges is bound to a check that runs no
    locked test, or None.

    Run R14 closed T0007 and T0008, both scoped on interval_tree_clocks, on
    construct-and-call checks; the locked cases test that imports it never ran.
    """
    imported = _locked_test_imports(goal)
    if not imported or not scope:
        return None
    entries = [e.rstrip("/") for e in scope]

    def held(module: str) -> bool:
        rel = module.replace(".", "/")
        for base in ("", "src/"):
            for path in (f"{base}{rel}.py", f"{base}{rel}/__init__.py"):
                if any(e in {"", "."} or path == e or path.startswith(f"{e}/") for e in entries):
                    return True
            if any(e == f"{base}{rel}" or e.startswith(f"{base}{rel}/") for e in entries):
                return True
        return False

    judged = [(module, test) for module, test in imported.items() if held(module)]
    if not judged or any(_runs_test_file(command, test) for _, test in judged):
        return None
    module, test = judged[0]
    return (
        f"the scope holds {module}, which the locked {test} judges, but done_when runs "
        f"none of the locked tests, so the reference's answers would not judge this "
        f"part. Bind `python3 -m pytest -q {test}`. A selection of that file counts as "
        f"running it, so a small part can bind just the cases it makes pass: a node id "
        f"(`python3 -m pytest -q {test}::<test name>`) or `python3 -m pytest -q {test} "
        "-k <name>`. Call pursuit_step again with that."
    )


#: The known-answers task's scope and locks, as the cases-first hint gives them.
_CASES_FIRST_SCOPE = ("tests/cases.json", "tests/test_cases.py", "tests/test_case_data.py")

#: The known-answers task's scope, check and locks, as the cases-first hint gives them.
_CASES_FIRST_WORK = (
    f"with scope {', '.join(_CASES_FIRST_SCOPE)}; "
    'done_when="python3 -m pytest -q tests/test_case_data.py"; and '
    f"locks=[{', '.join(_CASES_FIRST_SCOPE)}]"
)


def _known_answers_siblings(task: str, nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The unfinished tasks beside `task`, under its parent, that write the known answers."""
    node = next((n for n in nodes if str(n.get("id")) == task), None)
    parent = node.get("parent") if node else None
    if not parent:
        return []
    return [
        n
        for n in nodes
        if n.get("parent") == parent
        and str(n.get("id")) != task
        and n.get("status") in ("pending", "open")
        and _writes_known_answers(f"{n.get('title') or ''}::{n.get('intent') or ''}")
    ]


_KNOWN_ANSWERS_FILE = re.compile(r"case|known_answer")


def _known_answers_on_disk(root: Path) -> list[str]:
    """The known-answers files under tests/ that git holds uncommitted."""
    return [
        rel
        for rel in _changed_files(root)
        if rel.startswith("tests/") and _KNOWN_ANSWERS_FILE.search(Path(rel).name)
    ]


def _cases_on_disk_route(
    task: str,
    title: str,
    named: str,
    unjudged_text: str,
    on_disk: list[str],
    existing: str,
    unwait: str,
    nodes: list[dict[str, Any]] | None = None,
    root: Path | None = None,
) -> str:
    """The Cases first refusal when the known answers are on disk, uncommitted.

    Run R18 #51: the hint ordered a fresh known-answers split whose data test
    had passed since t3.7 on W1's uncommitted files, and that open was then
    refused as "already passes". The route named here opens on those files.
    Run R26 E196: it told the driver to open T0011, already open and unprovable;
    an open holder gets the call that settles it instead.
    """
    holder = next((n for n in nodes or [] if str(n.get("id")) == existing), None)
    if existing and holder is not None and holder.get("status") == "open":
        check = str(holder.get("done_when") or "").strip()
        own = _strings(holder.get("scope"))
        stuck = root is not None and (
            (str(root), existing) in _UNPROVEN or _at_spawn_limit(existing, nodes)
        )
        settle = (
            _unproven_call(
                existing,
                check,
                own,
                root,
                _missing_data(check, own, root) if check else [],
                nodes,
            )
            if stuck and root is not None
            else f'pursuit_step task="{existing}"'
        )
        return (
            f"Cases first: {unjudged_text} The known answers are on disk already, "
            f"uncommitted, and {existing}, open already, holds them: do not split {task}. "
            f"{unwait}Settle {existing} first: {settle}. {task} opens once its cases are "
            f"locked, its test importing {named} by name."
        )
    data = next((rel for rel in on_disk if re.search(r"test_\w*data\w*\.py$", rel)), "")
    check = f"python3 -m pytest -q {data or 'tests/test_case_data.py'}"
    scope = sorted({*on_disk, data or "tests/test_case_data.py"})
    listed = ", ".join(on_disk[:8]) + (f", {len(on_disk) - 8} more" if len(on_disk) > 8 else "")
    work = f'with scope {", ".join(scope)}; done_when="{check}"; and locks=[{", ".join(scope)}]'
    opens = (
        f"`{check}` may pass already: it passes only on these uncommitted files, so the "
        "open accepts it, and the close judges them (its witness takes them away). Do "
        "not write the cases again."
    )
    head = (
        f"Cases first: {unjudged_text} The known answers are on disk already, "
        f"uncommitted: {listed}."
    )
    if existing:
        return (
            f"{head} {existing} holds them: do not split {task}. {unwait}Open {existing} first, "
            f'{work}: pursuit_step task="{existing}". {opens} {task} opens once its cases '
            f"are locked, its test importing {named} by name."
        )
    parts = [
        f"Known answers::the cases on disk ({listed}), locked",
        f"{_judged_label(title, task)}::the code, judged by the locked cases",
    ]
    clash = _live_title_clash(task, parts, nodes or [])
    if clash is not None:
        return f"{head} No task holds them yet, and a plan cannot add one: {clash}"
    return (
        f"{head} No task holds them yet. Add it before this one in one call: "
        f'pursuit_plan task="{task}" parts={json.dumps(parts, ensure_ascii=False)}. '
        f"Then open the known-answers task, {work}. {opens}"
    )


def _judged_label(title: str, task: str) -> str:
    """The code part's title in a cases-first plan: never `task`'s own title.

    Run R29: the plan's second part took the task's title, and the plan tool
    refused it as the title of the task being split.
    """
    base = title.replace("::", ":").replace('"', "'").strip() or task
    return f"{base}, judged by the cases"


def _locked_data_route(
    task: str,
    scope: list[str],
    named: str,
    unjudged_text: str,
    data: list[str],
    committed: list[tuple[str, str]],
    module: str,
    root: Path,
) -> str:
    """The Cases first refusal when the known answers are locked but no test of them is.

    Run R22: the hint planned a known-answers part over the locked
    tests/cases.json, and that part's work was refused as locked. With a done
    task's cases test committed, the route locks it on this step; else this
    task writes the test and its close locks it.
    """
    listed = ", ".join(data)
    head = (
        f"Cases first: {unjudged_text} The known answers ({listed}) are locked already: "
        "do not plan them again."
    )
    if committed:
        test, owner = committed[0]
        check = f"python3 -m pytest -q {test}"
        scoped = ", ".join(f'"{e}"' for e in scope)
        return (
            f"{head} {test} is {owner}'s committed work: it reads them and imports the "
            f"code, but it was never locked. Lock it on this step, scope kept: "
            f'pursuit_step task="{task}" scope=[{scoped}] done_when="{check}" '
            f'locks=["{test}"]. {test} is locked at once, as {owner} committed it, and '
            "then judges this task's code."
        )
    stem = module.split(".")[-1] if module else "cases"
    candidates = [
        "tests/test_cases.py",
        f"tests/test_{stem}_cases.py",
        f"tests/test_{stem}_known_answers.py",
    ]
    test = next((rel for rel in candidates if not (root / rel).exists()), candidates[-1])
    scoped = ", ".join(f'"{e}"' for e in [*scope, test])
    return (
        f"{head} No test that reads them imports {named} yet. Write that test in this "
        f'task and lock it at its close: pursuit_step task="{task}" scope=[{scoped}] '
        f'done_when="python3 -m pytest -q {test}" locks=["{test}"]. The test must load '
        f"{listed} and run every case against {named}, with no asserts of its own."
    )


def _committed_cases_tests(
    root: Path, goal: Path, task: str, nodes: list[dict[str, Any]]
) -> list[tuple[str, str]]:
    """(test, done task) for each unlocked test a done task committed that reads
    locked data and imports the code, unchanged since HEAD.

    Run R22: T0002 committed tests/test_cases.py beside the locked
    tests/cases.json but never locked it.
    """
    locked = _locked(goal)
    data = [rel for rel in locked if _is_cases_data(rel)]
    head = _head_files(root) if data else None
    found: list[tuple[str, str]] = []
    for rel in sorted(head or ()):
        if rel in locked or not _reads_locked_data(root, rel, data):
            continue
        try:
            unchanged = (root / rel).read_bytes() == _committed_bytes(root, "HEAD", rel)
        except OSError:
            continue
        owner = _done_task_in_log([rel], task, nodes, root) if unchanged else ""
        if owner:
            found.append((rel, owner))
    return found


def _live_data_holder(
    task: str, nodes: list[dict[str, Any]], data: list[str], goal: Path
) -> str:
    """The live leaf to work for `data`: the first open or pending task whose scope
    or pending locks name a `data` file, or the first live leaf under it when it is
    a container; "" when no live task holds the data.

    Run R24: the lookup skipped containers, so each new_route split off a fresh
    known-answers task (T0002, T0013, T0019) over files T0002 already held.
    """
    live = ("open", "pending")
    wanted = {os.path.normpath(rel) for rel in data}
    root = goal.parent.parent

    def holds(node: dict[str, Any]) -> bool:
        held = _strings(_shown(str(node.get("id")), root).get("scope"))
        held += _pending_locks(goal, str(node.get("id")))
        return any(os.path.normpath(entry.strip()) in wanted for entry in held)

    containers = {str(n.get("id")) for n in nodes if n.get("container")}

    def leaf(node_id: str, seen: set[str]) -> str:
        parts = [
            n
            for n in nodes
            if str(n.get("parent") or "") == node_id and n.get("status") in live
        ]
        if not parts:
            return "" if node_id in containers else node_id
        for part in parts:
            part_id = str(part.get("id"))
            if part_id in seen:
                continue
            found = leaf(part_id, seen | {part_id})
            if found and found != task:
                return found
        return ""

    holders = [n for n in nodes if str(n.get("id")) != task and n.get("status") in live]
    # A leaf that names the data outranks a container whose scope is wider.
    holders.sort(key=lambda n: bool(n.get("container")))
    for node in holders:
        if holds(node):
            node_id = str(node.get("id"))
            found = leaf(node_id, {node_id})
            if found and found != task:
                return found
    return ""


def _cases_first_problem(
    scope: list[str],
    task: str,
    title: str,
    goal: Path,
    nodes: list[dict[str, Any]] | None = None,
    locks: list[str] | None = None,
) -> str | None:
    """Why a task would write new source before known answers judge it, or None.

    Run R12: CASES_FIRST_NOTE was advice, the driver opened the implementation
    before any cases, and a plain-int event clock was built that nothing from
    the paper bound. With references/ there, a new source module waits for a
    locked test that imports it by name.

    Run R16's hint split T0006 under a new known-answers task although its
    siblings T0007-T0009 already held the cases: given the tree, a sibling
    that writes the known answers is named instead.
    """
    root = goal.parent.parent
    if not (root / REFERENCES_DIR).is_dir():
        return None
    new = _new_modules(scope, root)
    if not new:
        return None
    locked_data = [rel for rel in _locked(goal) if _is_cases_data(rel)]
    committed = _committed_cases_tests(root, goal, task, nodes or []) if locked_data else []
    asked = set(_lock_paths(locks or [], root))
    for rel, owner in committed:
        if rel in asked:
            # The route below asks for this: a done task's committed test,
            # locked as that task left it.
            _lock(goal, root, [rel], owner)
    named_scope = set(_lock_paths(scope, root))
    carried = [
        rel
        for rel in asked & named_scope
        if rel.endswith(".py") and _is_test_path(rel) and rel not in _locked(goal)
    ]
    if locked_data and carried:
        # Its close locks the cases test beside the locked data, or stays open.
        return None
    imported = _locked_test_imports(goal)

    def judged(module: str) -> bool:
        if not module:
            return bool(imported)
        return any(
            name == module or name.startswith(f"{module}.") or module.startswith(f"{name}.")
            for name in imported
        )

    unjudged = [(entry, module) for entry, module in new if not judged(module)]
    if not unjudged:
        return None
    entry, module = unjudged[0]
    if _names_known_answers(title) or asked & set(_CASES_FIRST_SCOPE):
        # Run R29: the known-answers task itself was told to split off known answers.
        rest = [e for e in scope if not _new_modules([e], root)] or list(_CASES_FIRST_SCOPE)
        return (
            f"Cases first: {task} is the known-answers task: drop {entry} from scope (the "
            f"code is a later task) and call pursuit_step again with scope "
            f"{json.dumps(rest)}."
        )
    if imported:
        name, test = next(iter(imported.items()))
        path = name.replace(".", "/")
        base = "src/" if (root / "src").is_dir() else ""
        return (
            f"Cases first: scope names new source {entry}, which no locked test imports, "
            f"so nothing from the reference judges it. The locked cases test {test} imports "
            f"`{name}`: put that module ({base}{path}.py or {base}{path}/) in this task's "
            f"scope instead of {entry}, and call pursuit_step again."
        )
    named = f"`{module}`" if module else "the module this task writes"
    unjudged_text = (
        f"Scope names new source {entry}, and no locked test imports it yet, so nothing "
        "from the reference would judge the code."
    )
    if locked_data:
        return _locked_data_route(
            task, scope, named, unjudged_text, locked_data, committed, module, root
        )
    on_disk = _known_answers_on_disk(root)
    siblings = _known_answers_siblings(task, nodes or [])
    if siblings:
        first = str(siblings[0].get("id"))
        listed = ", ".join(f"{n.get('id')} {str(n.get('title') or '')!r}" for n in siblings)
        drops = [
            f'    beagle pursuit depend {n.get("id")} {task} --drop --reason "known answers '
            'go before the code"'
            for n in siblings
            if task in [str(w) for w in n.get("waiting_on") or []]
        ]
        unwait = (
            f"They wait on {task}, so drop each wait first. Run in bash, exactly:\n\n"
            + "\n".join(drops)
            + "\n\n"
            if drops
            else ""
        )
        if on_disk:
            return _cases_on_disk_route(
                task, title, named, unjudged_text, on_disk, first, unwait, nodes, root
            )
        return (
            f"Cases first: {unjudged_text} The known answers are already planned beside "
            f"{task}: {listed}. Do not split {task}. {unwait}Then work {first} first, "
            f'{_CASES_FIRST_WORK}: pursuit_step task="{first}". {task} opens once its '
            f"cases are locked, its test importing {named} by name."
        )
    if on_disk:
        data = [rel for rel in on_disk if _is_cases_data(rel)] or on_disk
        existing = _live_data_holder(task, nodes or [], data, goal) or next(
            (
                str(n.get("id"))
                for n in nodes or []
                if str(n.get("id")) != task
                and n.get("status") in ("pending", "open")
                and not n.get("container")
                and _names_known_answers(str(n.get("title") or ""))
            ),
            "",
        )
        return _cases_on_disk_route(
            task, title, named, unjudged_text, on_disk, existing, "", nodes, root
        )
    # Not on disk: the data file is the one the known-answers work below writes.
    data = [rel for rel in _CASES_FIRST_SCOPE if _is_cases_data(rel)]
    holder = _live_data_holder(task, nodes or [], data, goal)
    if holder:
        return (
            f"Cases first: {unjudged_text} {holder} holds {', '.join(data)} already: do not "
            f"split {task}. Work {holder} first, {_CASES_FIRST_WORK}: "
            f'pursuit_step task="{holder}". {task} opens once its cases are locked, its '
            f"test importing {named} by name."
        )
    parts = [
        "Known answers::cases from references/ in tests/cases.json, and "
        f"tests/test_cases.py importing {named} by name",
        f"{_judged_label(title, task)}::the code, judged by the locked cases",
    ]
    clash = _live_title_clash(task, parts, nodes or [])
    if clash is not None:
        return f"Cases first: {unjudged_text} A known-answers milestone cannot be planned: {clash}"
    return (
        "Cases first: open the known-answers milestone before the code; its test imports "
        f"this module by name. {unjudged_text} Add the milestone "
        f'before this one in one call: pursuit_plan task="{task}" '
        f"parts={json.dumps(parts, ensure_ascii=False)}. Then work the known-answers "
        f"task first, {_CASES_FIRST_WORK}."
    )


def _python_c_code(argv: list[str]) -> str | None:
    """The code of a `python -c '...'` argv, or None for any other command."""
    if not Path(argv[0]).name.startswith("python") or "-c" not in argv[1:]:
        return None
    at = argv.index("-c") + 1
    return argv[at] if at < len(argv) else None


def _import_scope_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check imports a project module no task can make importable, or None.

    Run R08 scoped itc/src/interval_tree_clocks.py and checked `from
    itc.interval_tree_clocks import ...`; the worker made a second itc/ package
    to fit the check. A module is the project's when its top-level name is in
    the project or the scope (plain or under src/); it must then be in scope or
    on disk as a/b.py or a/b/__init__.py, plain or under src/.
    """
    code = _bash_find(command, _python_c_code)
    if code is None:
        return None
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    entries = [path.rstrip("/") for path in scope]
    modules: list[tuple[str, ...]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules += [(alias.name,) for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            subs = tuple(f"{node.module}.{alias.name}" for alias in node.names)
            modules.append((node.module, *subs))

    def candidates(name: str) -> list[str]:
        rel = name.replace(".", "/")
        return [f"{base}{rel}{tail}" for base in ("", "src/") for tail in (".py", "/__init__.py")]

    def present(name: str) -> bool:
        rel = name.replace(".", "/")
        for path in candidates(name):
            if any(path == e or path.startswith(f"{e}/") for e in entries):
                return True
            if (root / path).is_file():
                return True
        return any(
            (root / base / rel).is_dir() or any(e.startswith(f"{base}{rel}/") for e in entries)
            for base in ("", "src/")
        )

    def ours(name: str) -> bool:
        top = name.split(".")[0]
        for base in ("", "src/"):
            if (root / base / top).is_dir() or (root / base / f"{top}.py").is_file():
                return True
            if any(e == f"{base}{top}.py" or e.startswith(f"{base}{top}/") for e in entries):
                return True
        return False

    for names in modules:
        if not ours(names[0]) or any(present(name) for name in names):
            continue
        expected = candidates(names[0])[0]
        return (
            f"done_when imports {names[0]}, which would be {expected}, but that is "
            "neither in scope nor in the project, so no worker can make the check "
            f"pass. Put {expected} in scope, or change the import to the module the "
            "scope names. Call pursuit_step again with that."
        )
    return None


#: Fixtures pytest provides itself: none of them can bring in the project's code.
_PYTEST_FIXTURES = frozenset(
    {
        "cache",
        "capfd",
        "capfdbinary",
        "caplog",
        "capsys",
        "capsysbinary",
        "doctest_namespace",
        "monkeypatch",
        "pytestconfig",
        "pytester",
        "record_property",
        "record_testsuite_property",
        "record_xml_attribute",
        "recwarn",
        "request",
        "testdir",
        "tmp_path",
        "tmp_path_factory",
        "tmpdir",
        "tmpdir_factory",
    }
)


def _scope_source_modules(scope: list[str], root: Path) -> list[tuple[str, str]]:
    """(path, dotted name) of each source module `scope` names, as a file or a
    directory holding them; tests are not modules."""
    found: list[tuple[str, str]] = []
    for entry in scope:
        rel = entry.strip().rstrip("/")
        path = root / rel
        if rel.endswith(".py"):
            rels = [rel]
        elif rel and path.is_dir():
            rels = sorted(p.relative_to(root).as_posix() for p in path.rglob("*.py"))
        else:
            rels = []
        found += [
            (r, _module_of(r))
            for r in rels
            if not _is_test_path(r) and not _CACHE_DIRS & set(Path(r).parts)
        ]
    return found


def _names_from(tree: ast.Module, module: str) -> set[str] | None:
    """The names `tree` binds by importing `module` (plain or under src.), or None
    when a star import leaves them unknown."""

    def matches(name: str) -> bool:
        return any(name == m or name.startswith(f"{m}.") for m in (module, f"src.{module}"))

    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if matches(alias.name):
                    bound.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            for alias in node.names:
                if not (matches(node.module) or matches(f"{node.module}.{alias.name}")):
                    continue
                if alias.name == "*":
                    return None
                bound.add(alias.asname or alias.name)
    return bound


def _tainted(tree: ast.Module, bound: set[str]) -> tuple[set[str], bool]:
    """The module-level names whose definition reaches `bound`, and whether an
    autouse fixture among them runs for every test."""
    tainted = set(bound)
    autouse = False
    changed = True
    while changed:
        changed = False
        for node in tree.body:
            names: list[str] = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)]
            if not names or set(names) <= tainted or not _reaches(node, tainted):
                continue
            tainted.update(names)
            changed = True
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in tainted:
            autouse = autouse or any(
                isinstance(k.value, ast.Constant) and k.arg == "autouse" and k.value.value is True
                for d in node.decorator_list
                if isinstance(d, ast.Call)
                for k in d.keywords
            )
    return tainted, autouse


def _reaches(node: ast.AST, names: set[str]) -> bool:
    """Whether `node` reads one of `names`, or imports from the module itself."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and sub.id in names:
            return True
        if (
            isinstance(sub, (ast.Import, ast.ImportFrom))
            and sub is not node
            and any((a.asname or a.name.split(".")[0]) in names for a in sub.names)
        ):
            return True
    return False


def _parametrized(node: ast.AST) -> set[str]:
    """The argument names a test's `parametrize` decorators supply."""
    names: set[str] = set()
    for deco in getattr(node, "decorator_list", []):
        if (
            isinstance(deco, ast.Call)
            and isinstance(deco.func, ast.Attribute)
            and deco.func.attr == "parametrize"
            and deco.args
            and isinstance(deco.args[0], ast.Constant)
            and isinstance(deco.args[0].value, str)
        ):
            names.update(n.strip() for n in deco.args[0].value.split(","))
    return names


def _conftest_fixtures(test: Path, root: Path, module: str) -> tuple[set[str], set[str], bool]:
    """(every fixture function, those using `module`, any autouse one using it) in
    the conftest.py files from `test`'s directory up to the root."""
    defined: set[str] = set()
    using: set[str] = set()
    autouse = False
    folder = test.parent
    while True:
        conftest = folder / "conftest.py"
        if conftest.is_file():
            try:
                tree = ast.parse(conftest.read_text(encoding="utf-8"))
            except (OSError, SyntaxError, ValueError):
                tree = None
            if tree is not None:
                defined.update(
                    n.name
                    for n in tree.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
                bound = _names_from(tree, module)
                if bound is None:
                    return defined, defined, True
                tainted, auto = _tainted(tree, bound)
                using |= tainted & defined
                autouse = autouse or auto
        if folder == root or root not in folder.parents:
            break
        folder = folder.parent
    return defined, using, autouse


def _test_uses(
    node: ast.AST,
    tainted: set[str],
    defined: set[str],
    fixtures: tuple[set[str], set[str]],
) -> bool:
    """Whether a test function or class reads the module: in its body, or through a
    fixture it takes, one level. A fixture beagle cannot find counts as using it."""
    if _reaches(node, tainted):
        return True
    conftest_defined, conftest_using = fixtures
    funcs = (
        [node]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        else [n for n in ast.walk(node) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    )
    for func in funcs:
        args = func.args
        given = _parametrized(func) | {"self", "cls"}
        for arg in [*args.posonlyargs, *args.args, *args.kwonlyargs]:
            name = arg.arg
            if name in given or name in _PYTEST_FIXTURES:
                continue
            if name in defined:
                if name in tainted:
                    return True
                continue
            if name in conftest_defined:
                if name in conftest_using:
                    return True
                continue
            return True
    return False


def _pytest_node_import_only_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check's pytest test passes once the task's module imports, or None.

    Run R28: `python3 -c "from src.interval_tree_clock import ..."` was refused as
    import-only, and its resend `pytest -q tests/test_cases.py::test_multiple_cases`
    ran a test that never used the class: it failed only on the file's import. A
    bare test file counts as running all its tests, refused only when none of them
    uses the module. A file beagle cannot parse is not judged.
    """
    modules = _scope_source_modules(scope, root)
    if not modules:
        return None
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    parts: list[str] = []
    for word in words:
        parts.append(word)
        if " " in word:
            with contextlib.suppress(ValueError):
                parts += shlex.split(word)
    for part in parts:
        rel, _, node_id = part.partition("::")
        rel = rel.rstrip("/")
        if (
            not rel.endswith(".py")
            or not _is_test_path(rel)
            or Path(rel).is_absolute()
            or ".." in Path(rel).parts
            or not (root / rel).is_file()
            or not _runs_test_file(command, rel)
        ):
            continue
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        names = [n.split("[", 1)[0] for n in node_id.split("::")] if node_id else []
        if names:
            scopes: list[ast.AST] = [tree]
            for name in names:
                scopes = [
                    child
                    for parent in scopes
                    for child in getattr(parent, "body", [])
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                    and child.name == name
                ]
            tests = scopes
        else:
            tests = [
                n
                for n in tree.body
                if (
                    isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name.startswith("test")
                )
                or (isinstance(n, ast.ClassDef) and n.name.startswith("Test"))
            ]
        if not tests:
            continue
        defined = {
            n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        for source, module in modules:
            bound = _names_from(tree, module)
            if not bound:
                continue
            tainted, autouse = _tainted(tree, bound)
            conftest_defined, conftest_using, conftest_auto = _conftest_fixtures(
                root / rel, root, module
            )
            if autouse or conftest_auto:
                continue
            fixtures = (conftest_defined, conftest_using)
            if any(_test_uses(test, tainted, defined, fixtures) for test in tests):
                continue
            return (
                f"done_when `{command}` runs {part}, which uses nothing from {source}: it "
                f"passes once the import does, whatever {source} does. {_ONE_COMMAND}, "
                f"running a test that calls {source}'s code and asserts what it returns. "
                "Call pursuit_step again with that."
            )
    return None


def _pytest_node_missing_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check names a pytest node its task cannot make exist, or None.

    Run R34 #19: `pytest -q tests/test_cases.py::test_encode_decode_roundtrip` named
    a test the locked file did not hold, and every worker's check exited 4. A node
    in a test file the task may write is left alone: the worker may add it.
    """
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    parts: list[str] = []
    for word in words:
        parts.append(word)
        if " " in word:
            with contextlib.suppress(ValueError):
                parts += shlex.split(word)
    locked = set(_locked(root / ".beagle" / GOAL_BASENAME))
    named = {os.path.normpath(e.strip()) for e in scope}
    for part in parts:
        rel, _, node_id = part.partition("::")
        rel = rel.rstrip("/")
        if (
            not node_id
            or not rel.endswith(".py")
            or Path(rel).is_absolute()
            or ".." in Path(rel).parts
            or not (root / rel).is_file()
            or not _runs_test_file(command, rel)
        ):
            continue
        rel = os.path.normpath(rel)
        if _in_scope(rel, scope, root) and (rel not in locked or rel in named):
            continue
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        found: list[ast.AST] = [tree]
        for name in (n.split("[", 1)[0] for n in node_id.split("::")):
            found = [
                child
                for parent in found
                for child in getattr(parent, "body", [])
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and child.name == name
            ]
        if found:
            continue
        tests = [
            n.name
            for n in tree.body
            if (
                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and n.name.startswith("test")
            )
            or (isinstance(n, ast.ClassDef) and n.name.startswith("Test"))
        ]
        why = "it is locked" if rel in locked else "it is outside the task's scope"
        held = f"its tests are: {', '.join(tests[:5])}" if tests else "it holds no tests"
        return (
            f"done_when `{command}` names `{node_id}`, which is not in {rel}; {held}. "
            f"No worker can add it, since {why}. Name a test that exists, or a test file "
            "in the task's scope, and call pursuit_step again with that."
        )
    return None


def _test_imports(test_path: Path) -> list[tuple[str, ...]]:
    """Each absolute import of a test file: (module,) or (module, module.name, ...)."""
    try:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return []
    found: list[tuple[str, ...]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [(alias.name,) for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.append((node.module, *(f"{node.module}.{a.name}" for a in node.names)))
    return found


def _module_written(name: str, root: Path, beside: Path, scope: list[str]) -> bool:
    """Whether `name` resolves under the project root or beside the test, as a.py or
    a/__init__.py, would be written by a path in `scope`, or is stdlib or installed.

    A scope path beside the test does not count: code written into tests/ to satisfy
    an import is run R09's implementation in tests, not the module. Nor does a file
    on disk beside a test in a tests dir: run R24's tests/interval_tree_clocks.py stub
    made the cases test's import count as written, and the data-only rebind never fired.
    """
    rel = name.replace(".", "/")
    top = name.split(".")[0]
    if top in sys.stdlib_module_names or top in _TEST_LIBRARIES:
        return True
    entries = [e.rstrip("/") for e in scope]
    bases = ["", "src/"]
    with contextlib.suppress(ValueError):
        bases.append(f"{beside.relative_to(root).as_posix()}/")
    ours = False
    for base in bases:
        for path in (f"{base}{rel}.py", f"{base}{rel}/__init__.py"):
            if (root / path).is_file() and not _in_tests_dir(path):
                return True
            if base in {"", "src/"} and any(
                e in {"", "."} or path == e or path.startswith(f"{e}/") for e in entries
            ):
                return True
        ours = ours or (root / f"{base}{top}").exists() or (root / f"{base}{top}.py").exists()
    if ours:
        return False
    try:
        return importlib.util.find_spec(top) is not None
    except (ImportError, ValueError):
        return False


def _check_test_files(command: str, root: Path) -> list[str]:
    """The test .py files a check runs under pytest or as a script, named directly or
    as a directory holding them; a file the check only reads (grep, cat) is not run."""
    found: list[str] = []
    for rel in _check_targets(command, root):
        target = root / rel
        if target.is_file():
            paths = [rel] if rel.endswith(".py") and _is_test_path(rel) else []
        else:
            paths = sorted(
                p.relative_to(root).as_posix()
                for p in target.rglob("*.py")
                if not _CACHE_DIRS & set(p.relative_to(root).parts)
                and (p.name.startswith("test_") or p.name.endswith("_test.py"))
            )
        found += [p for p in paths if p not in found and _runs_test_file(command, p)]
    return found


def _imports_unwritten(command: str, scope: list[str], root: Path) -> tuple[str, str] | None:
    """(test, module) when the check runs a test importing a module that does not
    exist and that no path in `scope` would create, or None.

    Run R15 E9 amended the known-answers task's check to run tests/test_cases.py,
    which imports itc_clocks.itc that only a later task writes; no worker on the
    tests/ scope could pass it. A later part whose scope holds the module may bind
    the same test.
    """
    if not scope:
        return None
    for rel in _check_test_files(command, root):
        test = root / rel
        for names in _test_imports(test):
            if names[0].split(".")[0].startswith("test_"):
                continue
            if not any(_module_written(n, root, test.parent, scope) for n in names):
                return rel, names[0]
    return None


def _data_test(test: str, scope: list[str], root: Path) -> str:
    """The test in `scope`, other than `test`, that imports no unwritten code."""
    data_tests = [
        rel
        for entry in scope
        for rel in ([entry.rstrip("/")] if entry.endswith(".py") else [])
        + _check_test_files(f"pytest {shlex.quote(entry)}", root)
        if rel != test
        and _is_test_path(rel)
        and _imports_unwritten(f"pytest {shlex.quote(rel)}", scope, root) is None
    ]
    return data_tests[0] if data_tests else "tests/test_case_data.py"


def _data_test_route(
    command: str, scope: list[str], root: Path
) -> tuple[str, str, str, list[str]] | None:
    """For a check that runs a test importing unwritten code: the test, the module, the
    data-test command to bind instead, and the scope that command needs; or None.

    The scope gains the data test when no entry holds it: run R16's escalation proposed
    tests/test_case_data.py for T0010, whose scope could not write it.
    """
    found = _imports_unwritten(command, scope, root)
    if found is None:
        return None
    test, module = found
    data_test = _data_test(test, scope, root)
    if data_test == test:
        return None
    needs = scope if _in_scope(data_test, scope, root) else [*scope, data_test]
    return test, module, f"python3 -m pytest -q {data_test}", needs


def _self_import_note(command: str, scope: list[str], root: Path) -> str:
    """The worker note for a check whose data test itself imports unwritten code, or "".

    Run R26 W5 put `import cobs` into tests/test_case_data.py; `_data_test_route`
    then proposed binding that same test, and no worker ran to drop the import.
    """
    found = _self_import(command, scope, root)
    if found is None:
        return ""
    test, module = found
    return (
        f"\n\n{test} imports {module}, which no path in this scope creates; a data test "
        "reads only the data file and imports none of the code: remove that import."
    )


def _self_import(command: str, scope: list[str], root: Path | None) -> tuple[str, str] | None:
    """(test, module) for a check whose data test imports unwritten code, or None."""
    found = _imports_unwritten(command, scope, root) if scope and root and command else None
    if found is None or _data_test(found[0], scope, root) != found[0]:
        return None
    return found


def _data_self_import(
    command: str, scope: list[str], root: Path | None
) -> tuple[str, str] | None:
    """`_self_import` for a scope of data and tests only, where the test is a data test."""
    if not (_scope_has_data(scope) and _only_data_and_tests(scope)):
        return None
    return _self_import(command, scope, root)


def _drop_self_import_restore(notes: str, command: str, scope: list[str], root: Path | None) -> str:
    """`notes`, or the self-import note in their place when they name the module the
    check's data test must not import, together with an import.

    Run R27 #15/#16 asked to "restore the module-level `from cobs import …`", and E32's
    offered call carried that note verbatim against the self-import note.
    """
    found = _data_self_import(command, scope, root)
    if found is None or root is None:
        return notes
    module = found[1].split(".")[0]
    if re.search(rf"\b{re.escape(module)}\b", notes) and "import" in notes.lower():
        return _self_import_note(command, scope, root).strip()
    return notes


def _module_on_disk(name: str, root: Path) -> bool:
    """Whether module `name` is a project file, a.py or a/__init__.py, outside tests."""
    rel = name.replace(".", "/")
    return any(
        (root / path).is_file() and not _in_tests_dir(path)
        for base in ("", "src/")
        for path in (f"{base}{rel}.py", f"{base}{rel}/__init__.py")
    )


def _project_imports(test_path: Path, root: Path) -> list[tuple[str, bool]]:
    """Each project module the test's AST imports, with whether it is on disk now.

    Stdlib, test libraries, sibling tests and installed packages are not project
    modules; a name that resolves to nothing installed is one not yet written.
    """
    found: list[tuple[str, bool]] = []
    for names in _test_imports(test_path):
        top = names[0].split(".")[0]
        if top in sys.stdlib_module_names or top in _TEST_LIBRARIES or top.startswith("test_"):
            continue
        if any(_module_on_disk(n, root) for n in names):
            found.append((names[0], True))
            continue
        ours = any(
            (root / f"{b}{top}").exists() or (root / f"{b}{top}.py").exists() for b in ("", "src/")
        )
        if not ours:
            try:
                if importlib.util.find_spec(top) is not None:
                    continue
            except (ImportError, ValueError):
                pass
        found.append((names[0], False))
    return found


def _check_imports_code(command: str, root: Path) -> bool:
    """Whether a test the check runs imports a project module."""
    return any(_project_imports(root / rel, root) for rel in _check_test_files(command, root))


def _cases_test_close_note(test: str, data: str, scope: list[str], root: Path) -> str:
    """What the close requires of the cases test: `test` when it reads `data`, else
    the other test in scope; empty when there is none."""
    name = Path(data).name
    if (root / test).is_file() and _cases_test_reads(root / test, name):
        cases = test
    else:
        entries = [e.rstrip("/") for e in scope]
        others = [e for e in entries if e.endswith(".py") and _is_test_path(e)] + [
            p.relative_to(root).as_posix()
            for e in entries
            if (root / e).is_dir()
            for p in sorted((root / e).rglob("*.py"))
            if _is_test_path(p.relative_to(root).as_posix()) and _cases_test_reads(p, name)
        ]
        cases = next((o for o in others if o != test), "")
    if not cases:
        return ""
    return (
        f"{cases} is the cases test, whether or not this check runs it: the close "
        f"requires it to load {data} and run every case in it against the code, with no "
        "hand-written asserts of its own. "
    )


def _known_answers_note(command: str, scope: list[str], root: Path) -> str:
    """The brief's proof note for a scope of data and tests: what the data test imports.

    Run R27 W3's brief held only `WITNESS_NOTE`, pointing at "the code they test", and
    W3 wrote `from cobs import …` into tests/test_case_data.py. Run R28 W3's brief said
    a test with `from src.interval_tree_clock import …`, a module on disk, imported
    none, and W3 deleted the import; so that is said only of a test whose AST imports
    no project module.
    """
    data = next(r.rstrip("/") for r in scope if Path(r.rstrip("/")).suffix not in {"", ".py"})
    runs = [rel for rel in _check_test_files(command, root) if rel.endswith(".py")]
    # Run R32: on a fresh repository the check's test was not on disk yet, and the
    # note named the other test in scope as the check.
    runs += [
        rel
        for rel in _check_run_files(command, root)
        if rel.endswith(".py")
        and rel not in runs
        and _is_test_path(rel)
        and _runs_test_file(command, rel)
    ]
    test = next(
        (t for t in runs if _cases_test_reads(root / t, Path(data).name)),
        next((t for t in runs if _in_scope(t, scope, root)), runs[0] if runs else ""),
    ) or _data_test("", scope, root)
    proof = _cases_test_close_note(test, data, scope, root) + _tests_only_proof_note(
        command, scope, root
    )
    imports = _project_imports(root / test, root)
    present = [module for module, here in imports if here]
    if present:
        return (
            f"{test} is the check: it reads {data}. {test} imports {present[0]}, which "
            f"exists: keep that import; this task changes only {', '.join(scope)}. " + proof
        )
    if imports:
        said = _self_import_note(command, scope, root).strip() or (
            f"{test} imports {imports[0][0]}, which is not on disk yet; this task "
            f"changes only {', '.join(scope)}."
        )
        return f"{test} is the check: it reads {data}. {said} " + proof
    beside = (root / test).parent
    written = any(
        here
        for other in (beside.glob("test_*.py") if beside.is_dir() else [])
        for _, here in _project_imports(other, root)
    )
    unwritten = "" if written else " (no task has written it yet)"
    return (
        f"{test} is the check: it reads {data} and imports none of the code{unwritten}; "
        "a test that imports the code is not run by this check. " + proof
    )


def _absent_test_route(
    command: str, scope: list[str], root: Path
) -> tuple[list[str], str, list[str]] | None:
    """For a known-answers open whose check names, beside a data test, a test in
    scope not yet on disk: the absent tests, the data-test command to bind instead,
    and the scope it needs; or None.

    Run R24 #4 opened T0002 on `pytest tests/test_case_data.py tests/test_cases.py`
    before tests/test_cases.py existed, so `_data_test_route` had no imports to read;
    the cases test then imported a module no scope path could hold. The data test is
    told apart by existence: the named tests on disk that import nothing unwritten,
    or with none on disk, the first named.
    """
    if not (_scope_has_data(scope) and _only_data_and_tests(scope)):
        return None
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    if any(" " in w or w in {"&&", "||", ";", "|"} for w in words):
        return None
    named = sorted(
        (
            rel
            for rel in _check_run_files(command, root)
            if rel.endswith(".py") and _is_test_path(rel) and _runs_test_file(command, rel)
        ),
        key=command.find,
    )
    absent = [rel for rel in named if not (root / rel).exists()]
    if len(named) < 2 or not absent or not all(_in_scope(r, scope, root) for r in absent):
        return None
    data = [
        rel
        for rel in named
        if rel not in absent
        and _imports_unwritten(f"pytest {shlex.quote(rel)}", scope, root) is None
    ]
    if not data and len(absent) == len(named):
        data, absent = named[:1], named[1:]
    if not data or len(data) + len(absent) != len(named):
        return None
    needs = [*scope, *(rel for rel in data if not _in_scope(rel, scope, root))]
    return absent, f"python3 -m pytest -q {' '.join(data)}", needs


def _scope_note(needs: list[str], scope: list[str]) -> str:
    """What to send as scope when the data test is outside `scope`, or nothing."""
    if needs == scope:
        return ""
    return f" Its scope must hold that test too: scope={json.dumps(needs)}."


def _data_only_bind(
    command: str, scope: list[str], root: Path, *, unwritten: bool = False
) -> tuple[str, list[str], str] | None:
    """For a known-answers check that runs, beside a data test, a test that cannot pass
    on this scope: the data-test command to bind instead, its scope, and the lead that
    says so; or None.

    A named test absent from disk is the open's case (`_absent_test_route`, run R24 #4).
    With `unwritten`, a test on disk that imports a module no scope path creates is
    one too (`_data_test_route`): run R25 #5 resent the open's check naming the cases
    test, and the amend bound it.
    """
    absent_route = _absent_test_route(command, scope, root) if scope else None
    if absent_route is not None:
        absent, data_check, needs = absent_route
        return (
            data_check,
            needs,
            f"Bound the data test only: `{data_check}`. {', '.join(absent)} "
            f"{'is' if len(absent) == 1 else 'are'} in scope but not on disk yet, so "
            "nothing shows whether the code it will import is one this scope can "
            "write; a later task whose scope holds that code runs it.\n\n",
        )
    route = _data_test_route(command, scope, root) if unwritten and scope else None
    if route is None or not (_scope_has_data(scope) and _only_data_and_tests(scope)):
        return None
    test, module, data_check, needs = route
    return (
        data_check,
        needs,
        f"Bound the data test only: `{data_check}`. {test} imports {module}, which no "
        "path in this scope creates, so it fails with ImportError until a later task "
        "whose scope holds that code runs it.\n\n",
    )


def _check_data_reads(command: str, root: Path) -> list[str]:
    """The data files that tests run by `command`, importing no project module, open.

    Run R21: T0005's check ran tests/test_case_data.py, which read tests/cases.json
    and imported nothing; the scope held only the test, so the data file's absence,
    the one proof such a test has, was out of reach. Found from the test's code (the
    file it opens, by `_cases_test_reads`) and `CASES_DATA_SUFFIXES`; a bare name
    resolves beside the test.
    """
    found: list[str] = []
    for rel in _check_test_files(command, root):
        test = root / rel
        if _test_project_imports(test):
            continue
        try:
            tree = ast.parse(test.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
                continue
            named = Path(node.value.strip())
            if named.suffix not in CASES_DATA_SUFFIXES or named.is_absolute():
                continue
            if not _cases_test_reads(test, named.name):
                continue
            beside = (test.parent / named.name).relative_to(root).as_posix()
            data = (
                named.as_posix()
                if len(named.parts) > 1 and (root / named).is_file()
                else beside
            )
            if data not in found:
                found.append(data)
    return found


def _missing_data(command: str, scope: list[str], root: Path) -> list[str]:
    """The data files the check's tests read that `scope` does not hold."""
    return [rel for rel in _check_data_reads(command, root) if not _in_scope(rel, scope, root)]


def _changed_locked_only(scope: list[str], goal: Path, root: Path) -> list[str]:
    """The locked, tracked files in `scope` the work changed, when it changed nothing else
    there: a known-answers fix, whose data file's absence proves nothing."""
    changed = [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]
    locked = set(_locked(goal))
    if not changed or any(
        rel not in locked or not _in_commit("HEAD", rel, root) for rel in changed
    ):
        return []
    return changed


def _locked_data_proof_note(held: list[str]) -> str:
    """Said instead of TESTS_ONLY_PROOF_NOTE for a fix to tracked locked data.

    Run R34 E66-E68: the note asked for a check failing with tests/cases.json
    removed; that check already passed, and the open refused it.
    """
    rels = ", ".join(held)
    return (
        f"The check must fail on the locked version of {rels}: assert the cases that "
        f"change. {rels} is tracked, so taking it away proves nothing; the close puts "
        "its locked version back as the defect, and the check must refuse it."
    )


def _tests_only_proof_note(command: str, scope: list[str], root: Path | None) -> str:
    """The proof note for a tests-only scope: the data file's absence where the scope
    or the check's tests hold one, else a defect in the module the test imports.

    Run R21 E76 said "mutate the module the test imports" of a test that imported
    none and read tests/cases.json, outside its scope.
    """
    reads = _check_data_reads(command, root) if root is not None and command else []
    if not _scope_has_data(scope) and not reads:
        return TESTS_ONLY_MUTATE_NOTE
    missing = [rel for rel in reads if not _in_scope(rel, scope, root)]
    if not missing:
        return TESTS_ONLY_PROOF_NOTE
    return (
        f"{TESTS_ONLY_PROOF_NOTE} The test this check runs reads {', '.join(missing)}, "
        f"which this scope does not hold: add it to the scope, "
        f"scope={json.dumps([*scope, *missing])}."
    )


def _imports_unwritten_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check cannot pass on this scope because a test it runs imports unwritten
    code, naming the data-only test to bind instead; or None."""
    route = _data_test_route(command, scope, root)
    if route is None:
        return None
    test, module, data_check, needs = route
    return (
        f"{test} fails with ImportError until a later task writes {module}, and no path "
        "in this scope creates it, so no sub-agent on this scope can pass it. This task's "
        f"check runs the data test only (`{data_check}`): a test of the data file itself, "
        f"importing none of the code.{_scope_note(needs, scope)} Call pursuit_step again "
        "with that."
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
#: A title naming beagle or the pursuit with one of `_SETUP_ACTS` sets the
#: pursuit up, whatever else it names: R10's 'Setup beagle pursuit infrastructure',
#: R19's 'Found the pursuit: implement …'. A founding verb alone is not setup:
#: 'Create the clock type' names neither, so it is kept.
_PURSUIT_NAMES = frozenset({"beagle", "pursuit"})
_SETUP_ACTS = frozenset(
    {
        "setup",
        "set",
        "found",
        "founding",
        "founded",
        "start",
        "create",
        "init",
        "initialize",
        "initialise",
        "configure",
        "config",
        "configuration",
        "infrastructure",
        "install",
        "bootstrap",
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
        # `title::purpose` is asked for, but `title: purpose` (run 11) and
        # `title - purpose` (R10) are what came.
        title = re.split(r":| - | — ", _split_part(part)[0], maxsplit=1)[0]
        words = set(re.findall(r"[a-z]+", title.lower()))
        names_setup = bool(words & _PURSUIT_NAMES) and bool(words & _SETUP_ACTS)
        if (words and words <= _SETUP_WORDS) or names_setup or ".beagle" in part:
            return (
                f"{title.strip()!r} is not part of the goal's work: pursuit_found is what "
                "sets the pursuit up, and it is done once it is founded. Leave it out. If "
                "the project itself needs scaffolding, name what, e.g. 'package layout::"
                "pyproject.toml, src/ and tests/ so the later parts have a home'."
            )
    return None


#: Verbs a part that only re-runs or confirms a check opens with.
_RERUN_VERBS = frozenset({"re", "rerun", "run", "confirm", "verify", "check", "ensure", "validate"})
#: Words naming the check such a part re-runs, one of which it must name.
#: 'check' is left out: as a verb it opens real work ('check the stamp is
#: normalised'), and a false refusal costs the driver a turn.
_CHECK_WORDS = frozenset(
    {"test", "tests", "checks", "suite", "pass", "passes", "exit", "green", "pytest"}
)
#: Verbs that make something: a part with one has work of its own.
_MAKING_WORDS = frozenset(
    {
        "write",
        "add",
        "create",
        "implement",
        "fix",
        "move",
        "change",
        "update",
        "refactor",
        "edit",
        "build",
        "port",
        "derive",
        "make",
        "remove",
        "delete",
        "rename",
        "replace",
        "extend",
        "record",
        "generate",
    }
)


def _rerun_only_part(parts: list[str]) -> str | None:
    """Why one of `parts` only re-runs or confirms a check, or None.

    Run R09 planned 'P5::Re-run the case-data test and confirm exit 0': a
    part with nothing to change, whose check every close already runs. Such a
    part opens with a re-run verb, names a check, and has no making verb.
    """
    for part in parts:
        title, sep, purpose = part.partition("::")
        if not sep:
            title, _, purpose = part.partition(":")
        title_words = re.findall(r"[a-z0-9]+", title.lower())
        purpose_words = re.findall(r"[a-z0-9]+", purpose.lower())
        words = title_words + purpose_words
        # The title may be a label ('P5'); the purpose then opens with the verb.
        opening = {w[0] for w in (title_words, purpose_words) if w}
        if opening & _RERUN_VERBS and not set(words) & _MAKING_WORDS and set(words) & _CHECK_WORDS:
            return (
                f"{title.strip()!r} only re-runs or confirms a check: a part must change "
                "something, and the check runs at every close anyway. Fold it into the "
                "part before it, and plan the parts that do the work."
            )
    return None


#: Words of a milestone that only reads the reference or works out a design.
_READ_DESIGN_WORDS = frozenset(
    {
        "read",
        "reread",
        "study",
        "understand",
        "review",
        "analyse",
        "analyze",
        "research",
        "learn",
        "explore",
        "investigate",
        "notes",
        "design",
        "choose",
    }
)
#: Words naming something such a milestone would deliver besides reading.
_DELIVERABLE_WORDS = _MAKING_WORDS | {
    "case",
    "cases",
    "test",
    "tests",
    "code",
    "extract",
    "answers",
    "readme",
    "doc",
    "docs",
    "document",
    "documenting",
}
KNOWN_ANSWERS_TITLE = "Known answers from the reference"


def _read_or_design_only(part: str) -> bool:
    """Whether milestone `part` only reads the reference or chooses a design.

    Run R15 founded with 'Read the reference material ... and choose a design.'
    as its only milestone; the known-answers task opened under that title and
    its worker set up a project and designed instead of writing the cases.
    """
    words = set(re.findall(r"[a-z0-9]+", part.lower()))
    return bool(words & _READ_DESIGN_WORDS) and not words & _DELIVERABLE_WORDS


def _names_known_answers(part: str) -> bool:
    """Whether milestone `part` already names the known answers or a cases file."""
    text = part.lower()
    return "known answer" in text or bool(re.search(r"\bcases\b", text))


def _design_only_milestone(part: str) -> bool:
    """Whether milestone `part` only works out a design, judged by its head.

    Run R19 kept 'Design: settle the data structure and API — … (typing,
    tests, docs)' as its own task: the deliverable words in its parenthesis
    are the implementation's, not the milestone's. The head, before ':' or
    ' — ', decides, and the text outside parentheses must agree.
    """
    if _names_known_answers(part):
        return False
    head = re.split(r":| - | — ", part, maxsplit=1)[0]
    bare = re.sub(r"\([^)]*\)", "", part)
    return _read_or_design_only(head) and _read_or_design_only(bare)


def _reading_only_part(parts: list[str]) -> str | None:
    """Why one of `parts` only reads the reference or chooses a design, or None.

    Run R29 planned 'Read both references: extract … into a short digest': its
    head only reads, and the task it became could never be proved. The head,
    before ':' or ' — ', decides, as for a founding milestone.
    """
    for part in parts:
        if _names_known_answers(part):
            continue
        head = re.split(r":| - | — ", part, maxsplit=1)[0].strip()
        if _read_or_design_only(head):
            return (
                f"{head!r} only reads the reference or chooses a design: a sub-agent "
                f"reads the reference and writes the cases file and its test in the "
                f"known-answers task ({KNOWN_ANSWERS_TITLE!r}), and the design is part "
                "of the implementation, not a part of its own. Fold it into the part "
                "that uses it, and plan the parts that do the work."
            )
    return None


def _fold_design_milestones(kept: list[str]) -> tuple[list[str], list[str]]:
    """`kept` with each design-only milestone folded into the next one's intent.

    With known answers planned, a design milestone is part of the
    implementation: its text joins the following milestone's intent, or the
    one before it when none follows.
    """
    folded = list(kept)
    notes: list[str] = []
    index = 0
    while index < len(folded):
        part = folded[index]
        if len(folded) < 2 or not _design_only_milestone(part):
            index += 1
            continue
        del folded[index]
        into = index if index < len(folded) else index - 1
        target = folded[into]
        joiner = "; " if "::" in target else "::"
        folded[into] = f"{target}{joiner}{part.strip()}"
        notes.append(
            f"Folded the design milestone {part.split(':', 1)[0].strip()!r} into "
            f"{target.split(':', 1)[0].strip()!r}: the design is part of the "
            "implementation, not a milestone of its own."
        )
    return folded, notes


def _repair_milestones(milestones: list[str]) -> tuple[list[str], list[str]]:
    """`milestones` with what founding can fix fixed, and a note for each fix.

    A setup milestone and one that only re-runs a check are dropped, the first
    milestone that only reads the reference or chooses a design is retitled as
    the known answers (or, with known answers planned, a design-only one is
    folded into the next milestone's intent), and an over-long title is cut at
    a word, its whole text moved after '::'. With
    every milestone dropped, nothing is left: the list comes back empty and
    the one note says why.
    """
    kept: list[str] = []
    dropped: list[str] = []
    reruns: list[tuple[str, str]] = []
    for part in milestones:
        if _setup_milestone([part]) is not None:
            dropped.append(part)
        elif (why := _rerun_only_part([part])) is not None:
            reruns.append((part, why))
        else:
            kept.append(part)
    if not kept:
        if reruns and not dropped:
            return [], [reruns[0][1]]
        return [], [_setup_milestone(dropped) or "every milestone sets the pursuit up."]
    notes = []
    if dropped:
        named = ", ".join(repr(part.split(":", 1)[0].strip()) for part in dropped)
        notes.append(
            f"Dropped the setup milestone {named}: founding is the setup, so it is not "
            "part of the goal's work. The milestones are the rest."
        )
    for _part, why in reruns:
        notes.append(f"Dropped a milestone: {why}")
    repaired: list[str] = []
    # Run R17 retitled its docs milestone as a second known-answers task
    # although milestone 1 already wrote tests/cases.json.
    retitled = any(_names_known_answers(part) for part in kept)
    # 'edge cases' (R10) names no known answers: fold only beside real ones.
    if any(re.search(r"known answer|\bcases(\.json| file)\b", p.lower()) for p in kept):
        kept, fold_notes = _fold_design_milestones(kept)
        notes.extend(fold_notes)
    for index, part in enumerate(kept, 1):
        title, sep, intent = part.partition("::")
        title = title.strip()
        if not retitled and _read_or_design_only(part):
            retitled = True
            detail = f"{title} — {intent.strip()}" if sep and intent.strip() else title
            repaired.append(f"{KNOWN_ANSWERS_TITLE}::{detail}")
            notes.append(
                f"Milestone {index} {title!r} only reads the reference or chooses a "
                f"design, so it is now {KNOWN_ANSWERS_TITLE!r}, with its text after "
                "'::': a sub-agent reads the reference and writes the cases file and "
                "its test. The design is part of the implementation, not a milestone "
                "of its own."
            )
            continue
        labelled = _split_part(part)[0]
        if sep and len(title) <= MAX_TASK_TITLE and title != labelled:
            repaired.append(f"{labelled}::{intent.strip()}")
            continue
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


_SETUP_CRITERION = re.compile(r"\.beagle|beagle pursuit", re.IGNORECASE)


def _drop_setup_criteria(criteria: list[str]) -> tuple[list[str], list[str]]:
    """`criteria` without those about beagle's own setup, and a note if any went.

    Run R09 kept 'packaged as a beagle pursuit project (.beagle/ present,
    tracked)' and a step then named .beagle/ in scope. Founding is that setup,
    so such a criterion is not the goal's. With every criterion about it, all
    are kept: a goal needs criteria.
    """
    kept = [c for c in criteria if not _SETUP_CRITERION.search(c)]
    if not kept or len(kept) == len(criteria):
        return criteria, []
    named = ", ".join(repr(c) for c in criteria if _SETUP_CRITERION.search(c))
    return kept, [
        f"Dropped the setup criterion {named}: founding is the setup, so it is not "
        "part of the goal's work. The criteria are the rest."
    ]


def _milestones_from_criteria(
    dropped: list[str], criteria: list[str], refusal: list[str]
) -> tuple[list[str], list[str]]:
    """One milestone per criterion, for a milestone list that was only setup.

    A criterion that is itself setup is left out. With none left, the list
    comes back empty with `refusal`, the note `_repair_milestones` gave.
    """
    seeded = [f"{_task_title(c)}::{c}" for c in criteria if _setup_milestone([c]) is None]
    milestones, notes = _repair_milestones(seeded) if seeded else ([], [])
    if not milestones:
        return [], refusal
    named = ", ".join(repr(part.split(":", 1)[0].strip()) for part in dropped)
    return milestones, [
        f"Dropped the setup milestone {named}: founding is the setup, so it is not part "
        "of the goal's work. That left none, so the milestones are now one per "
        "criterion, each titled from it with the criterion after '::'.",
        *notes,
    ]


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


#: The seconds each check's last run that finished took, by (project root,
#: command): a run that was killed records nothing here.
_CHECK_SECONDS: dict[tuple[str, str], float] = {}
#: Each check whose last run was killed, by (project root, command): what
#: stopped it ("the 4G memory cap", "the 60s timeout") and after how many seconds.
_CHECK_KILLED: dict[tuple[str, str], tuple[str, float]] = {}
#: The least timeout `_check_timeout` gives a check with a recorded run, and
#: the multiple of that run's seconds it allows.
CHECK_TIMEOUT_FLOOR = 60.0
CHECK_TIMEOUT_FACTOR = 20.0


def _check_timeout(command: str, root: Path, timeout: float) -> float:
    """`timeout`, cut to max(CHECK_TIMEOUT_FLOOR, CHECK_TIMEOUT_FACTOR x the check's
    last finished run) when one is recorded.

    Run R30: a check that had taken 0.01 s ran 4.6 min, eleven times, before the
    memory cap killed it; a timeout from its earlier run ends a hang first.
    """
    earlier = _CHECK_SECONDS.get((str(root), command))
    if earlier is None:
        return timeout
    return min(timeout, max(CHECK_TIMEOUT_FLOOR, CHECK_TIMEOUT_FACTOR * earlier))


def _check_stopped(command: str, root: Path) -> tuple[str, float, float | None] | None:
    """What killed the check's last run, after how many seconds, and the seconds
    its last finished run took (None when none is recorded); None if not killed."""
    key = (str(root), command)
    killed = _CHECK_KILLED.get(key)
    if killed is None:
        return None
    return killed[0], killed[1], _CHECK_SECONDS.get(key)


async def _run_check(command: str, root: Path, timeout: float) -> tuple[int, str]:
    """Run a task's `done_when` the way its close will, before the close does.

    A done close that the check refuses blocks the task for good, so the step
    learns the verdict first and keeps a failing task open for another try.
    Beagle runs the check as words, not through a shell, and so does this: a
    check that only passes under `bash -c` would pass here and block there.
    The timeout is cut by `_check_timeout`, and each run is recorded for it.
    """
    try:
        argv = _check_argv(command, root)
    except ValueError as exc:
        return 2, f"the check will not split into arguments ({exc})"
    if not argv:
        return 2, "the check is empty"
    limit = _memory_max()
    key = (str(root), command)
    timeout = _check_timeout(command, root, timeout)
    started = time.monotonic()
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
        _CHECK_KILLED[key] = (f"the {timeout:.0f}s timeout", time.monotonic() - started)
        return 124, f"the check timed out after {timeout:.0f}s"
    seconds = time.monotonic() - started
    out = (stdout or b"").decode("utf-8", "replace").strip()
    note = _killed_note(-9 if proc.returncode == 137 else proc.returncode, limit)
    if note:
        _CHECK_KILLED[key] = (f"the {limit} memory cap", seconds)
    else:
        _CHECK_KILLED.pop(key, None)
        _CHECK_SECONDS[key] = seconds
    return proc.returncode or 0, f"{out}\n{note}".strip() if note else out


def _check_broke(rc: int, output: str) -> str | None:
    """The first error line of a check run that could not run at all, or None.

    R13 bound `git diff --stat: x.md`, which exits 129 on the option before
    reading any file, and spent two workers on it. Exit 129 (git usage), 127
    (command not found), 2 or 64 with a `usage:` line, or a SyntaxError in an
    inline script mean no work can make the check pass; exit 1 is a check that
    fails, as it should before the work.
    """
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    raw = output.splitlines()
    for i, line in enumerate(raw):
        if not line.startswith("SyntaxError"):
            continue
        frames = [f for f in raw[:i] if f.lstrip().startswith('File "')]
        if frames and frames[-1].lstrip().startswith(('File "<string>"', 'File "<stdin>"')):
            return line.strip()
    usage = rc in (2, 64) and any(line.lower().startswith("usage:") for line in lines)
    if rc not in (127, 129) and not usage:
        return None
    errors = [line for line in lines if "error" in line.lower()]
    return (errors or lines or [f"exit {rc}"])[0]


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
ON_DISK_WITNESS_NOTE = (
    "The check passes already on the uncommitted work; do not change the "
    "implementation. Add or name a mutation that shows the check can refuse: a line "
    "whose change makes it fail, given as the WITNESS block above."
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


def _in_tests_dir(rel: str) -> bool:
    return bool({"test", "tests"} & set(Path(rel).parts[:-1]))


def _is_test_path(rel: str) -> bool:
    """Whether `rel` is a test: a test_*.py, *_test.py or conftest.py anywhere, a
    package's __init__.py under a tests dir, or any non-.py file under one.

    Run R24: tests/interval_tree_clocks.py, the module a test imported, counted as
    a test for prove and as misplaced implementation at the close.
    """
    parts = Path(rel).parts
    name = parts[-1] if parts else rel
    if name.startswith("test_") or name.endswith("_test.py") or name == "conftest.py":
        return True
    if name.endswith(".py"):
        return name == "__init__.py" and _in_tests_dir(rel)
    return _in_tests_dir(rel)


def _module_beside_tests(rel: str) -> bool:
    """Whether `rel` is a .py under a tests dir that is not a test: a module."""
    rel = rel.strip().rstrip("/")
    return rel.endswith(".py") and _in_tests_dir(rel) and not _is_test_path(rel)


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
    small function is let through as a helper. Run R24: a long helper in a data
    test that imports no project module held a passing, proven known-answers
    task open; there is no module to move it to, so only its classes count.
    """
    found: list[str] = []
    for rel in changed:
        tested = _is_test_path(rel) or _module_beside_tests(rel)
        if not (tested and rel.endswith(".py")) or rel.endswith("conftest.py"):
            continue
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"), filename=rel)
        except (OSError, SyntaxError, ValueError):
            continue
        imports_project = bool(_test_project_imports(root / rel))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith("Test"):  # pytest's test grouping
                    found.append(f"{rel}: class {node.name}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not imports_project:
                    continue
                if node.name.startswith(("test_", "_", "pytest_")):
                    continue
                if any(_is_fixture(d) for d in node.decorator_list):
                    continue
                if (node.end_lineno or node.lineno) - node.lineno + 1 <= _HELPER_MAX_LINES:
                    continue
                found.append(f"{rel}: def {node.name}")
    return found


def _check_test_reach(check: str, root: Path) -> set[str] | None:
    """The test files `check` runs (looking one level into a shell script it runs) and
    the project files those tests import; None when it names no test file to go by."""
    commands = [check]
    for script in re.findall(r"[\w./-]+\.sh\b", check):
        with contextlib.suppress(OSError, ValueError):
            commands += (root / script).read_text(encoding="utf-8").splitlines()
    tests: list[str] = []
    for command in commands:
        tests += [t for t in _check_test_files(command, root) if t not in tests]
    if not tests:
        return None
    files = set(tests)
    for test in tests:
        beside = Path(test).parent.as_posix()
        for names in _test_imports(root / test):
            for name in names:
                path = name.replace(".", "/")
                for base in ("", "src/", f"{beside}/" if beside != "." else ""):
                    files.update(f"{base}{path}{end}" for end in (".py", "/__init__.py"))
    return files


def _implementation_in_tests_lead(root: Path, scope: list[str], check: str = "") -> str:
    """The line a not-done result leads with when its worker wrote code into tests/.

    Run R09: W4 wrote the library to tests/itc/ once src/ was refused, and the
    not-done results only listed tests/itc/clock.py among the changed files. Run
    R25 named tests/test_cases.py's `def main`, which the bound check no longer
    ran, and the driver passed it on to the workers: with a `check` that names its
    tests, only files it runs or they import are listed.
    """
    runs = _check_test_reach(check, root) if check else None
    changed = [
        rel
        for rel in _changed_files(root)
        if _in_scope(rel, scope, root)
        and (root / rel).is_file()
        and (runs is None or rel in runs)
    ]
    by_file: dict[str, list[str]] = {}
    for where in _implementation_in_tests(root, changed):
        rel, _, name = where.partition(": ")
        by_file.setdefault(rel, []).append(name)
    if not by_file:
        return ""

    def listed(kind: str) -> str:
        return "; ".join(
            f"{rel}: {', '.join(n for n in names if n.startswith(kind))}"
            for rel, names in by_file.items()
            if any(n.startswith(kind) for n in names)
        )

    lead = ""
    classes, runners = listed("class "), listed("def ")
    if classes:
        lead += (
            f"The sub-agent wrote implementation into tests/ ({classes}), which is not this "
            "task's work.\n\n"
        )
    if runners:
        # Run R16: run_case only dispatched cases.json's ops to the module, and
        # calling it implementation sent the driver after the module itself.
        lead += (
            f"The sub-agent wrote a case runner into the test ({runners}), which cases "
            "first forbids: each case should call the module directly. Logic shared by "
            "the cases belongs in the code (or in a helper the module exports), not in "
            "the test file.\n\n"
        )
    return lead


def _module_home(rel: str, root: Path) -> str:
    """The path a module written under a tests dir imports from outside it: its path
    below the last tests dir, at the project root (or under src/ if there is one)."""
    parts = Path(rel.strip().rstrip("/")).parts
    last = max(i for i, part in enumerate(parts[:-1]) if part in {"test", "tests"})
    base = "src/" if (root / "src").is_dir() else ""
    return base + Path(*parts[last + 1 :]).as_posix()


def _rehomed_scope(scope: list[str], root: Path) -> list[str] | None:
    """`scope` with each module under a tests dir moved to its home, or None if no
    entry is such a module."""
    if not any(_module_beside_tests(entry) for entry in scope):
        return None
    moved = [_module_home(e, root) if _module_beside_tests(e) else e for e in scope]
    return list(dict.fromkeys(moved))


def _module_under_tests_problem(
    scope: list[str], task: str, done_when: str, root: Path, refusal: str | None
) -> str | None:
    """Why a scope entry that is a module under a tests dir is refused, with the call
    that scopes it at its home; or None.

    Run R24 #8/#9 scoped tests/interval_tree_clocks.py: pytest's rootdir import made
    every later check import that stub, prove took it for a test, and the close held
    it as misplaced implementation. `refusal` is what the rehomed scope would itself
    be refused with, so the call offered is one this step accepts.
    """
    fixed = _rehomed_scope(scope, root)
    if fixed is None:
        return None
    moves = ", ".join(
        f"{e.strip().rstrip('/')} -> {_module_home(e, root)}"
        for e in scope
        if _module_beside_tests(e)
    )
    lead = (
        f"scope names a module under a tests dir ({moves}). A .py there that is not "
        "test_*.py, *_test.py or conftest.py is neither a test nor the module: the test "
        "imports it by name, and its home is outside the tests dir."
    )
    if refusal is not None:
        return f"{lead} With it at that path, the step is still refused: {refusal}"
    return (
        f"{lead} Call pursuit_step task={json.dumps(task)}, done_when={json.dumps(done_when)}, "
        f"scope={json.dumps(fixed)}, with the same criteria."
    )


def _missing_scoped_test(rc: int, output: str, scope: list[str], root: Path) -> str | None:
    """The path of a pytest exit 4 "file or directory not found" that is in `scope`
    and not on disk: the work not yet done, not a wrong check. Run R15 E8 offered a
    new done_when for tests/test_case_data.py, which the task was there to write."""
    if rc != 4 or not scope:
        return None
    for match in re.finditer(r"file or directory not found:\s*(\S+)", output):
        rel = match.group(1).split("::")[0].rstrip("/")
        if _in_scope(rel, scope, root) and not (root / rel).exists():
            return rel
    return None


def _pytest_collected_none(rc: int, check: str) -> str | None:
    """The lead for a pytest check that exited 5 (no tests collected), or None.

    Run R17 showed T0009's `exit 5: no tests ran` raw, beside "Fix the work, not
    the check", to the driver and to three workers. Exit 5 is pytest's own code
    for an empty collection, so the test files the check names are not written yet.
    """
    if rc != 5:
        return None
    try:
        words = shlex.split(check)
    except ValueError:
        return None
    parts: list[str] = []
    for word in words:
        if " " in word and not word.startswith("-"):
            with contextlib.suppress(ValueError):
                parts.extend(shlex.split(word))
                continue
        parts.append(word)
    names = [Path(part).name for part in parts]
    runs = any(n in ("pytest", "py.test") for n in names) or any(
        a == "-m" and b == "pytest" for a, b in itertools.pairwise(parts)
    )
    if not runs:
        return None
    files: list[str] = []
    for part in parts:
        rel = part.split("::")[0]
        if rel.endswith(".py") and not rel.startswith("-") and rel not in files:
            files.append(rel)
    named = ", ".join(files) if files else "the paths it was given"
    return (
        f"pytest collected no tests from {named}: it defines no test_ function; adding "
        "them is the work, not a different check."
    )


def _missing_locked_file(output: str, locks: list[str], root: Path) -> str | None:
    """A locked path the check failed on for want of it, not on disk: the work not yet
    done, not a wrong check. Run R17 E26 failed on FileNotFoundError for
    tests/cases.json, locked for the task, and was told to pass a corrected done_when."""
    missing = [lock.rstrip("/") for lock in locks if not (root / lock).exists()]
    if not missing:
        return None
    named = re.findall(r"No such file or directory: '([^']+)'", output)
    named += [m.split("::")[0] for m in re.findall(r"file or directory not found:\s*(\S+)", output)]
    for path in named:
        path = path.rstrip("/")
        for lock in missing:
            if path == lock or path.endswith(f"/{lock}"):
                return lock
    return None


def _absent_locks(locks: list[str], root: Path) -> list[str]:
    """The lock entries that are not a file on disk: the task's work not yet done."""
    return [lock for lock in locks if not (root / lock.rstrip("/")).is_file()]


_COLLECT_ONLY = re.compile(r"(?<![\w-])--(?:collect-only|co)(?![\w-])")


def _reads_a_lock(check: str, locks: list[str], root: Path) -> bool:
    """Whether `check` names a locked file, or a test (or a directory of them) that
    reads one, as `_cases_test_reads` judges it.

    Run R29: a test lock the check names counts though it is not on disk yet;
    it is the test the task will write.
    """
    locks = _lock_paths(locks, root)
    if any(lock.rstrip("/") in check for lock in locks):
        return True
    named = {os.path.normpath(word.split("::")[0]) for word in _check_words(check)}
    if any(_is_test_path(lock) and os.path.normpath(lock) in named for lock in locks):
        return True
    names = {Path(lock.rstrip("/")).name for lock in locks}
    for rel in _check_targets(check, root):
        path = root / rel
        tests = sorted(path.rglob("test_*.py")) if path.is_dir() else [path]
        for test in tests:
            if test.suffix == ".py" and any(_cases_test_reads(test, n) for n in names):
                return True
    return False


def _amend_problem(check: str, bound: str, locks: list[str], root: Path) -> str | None:
    """Why `check` may not replace a task's bound check, judged before it runs.

    Run R17 #26 swapped T0008's check, which loaded tests/cases.json, for
    `pytest --collect-only -q tests/`, which passed before any work.
    """
    keep = (
        f" Keep the bound check `{bound}`: leave done_when out to keep it."
        if bound and _check_problem(bound) is None
        else ""
    )
    if _COLLECT_ONLY.search(check):
        return (
            f"`{check}` runs pytest --collect-only, which only imports the tests and runs "
            f"none, so it passes whatever the work does.{keep}"
        )
    locks = _lock_paths(locks, root)
    if locks and not _reads_a_lock(check, locks, root):
        return (
            f"this task has locked known answers ({', '.join(locks)}), and `{check}` "
            "names none of them and runs no test that reads one, so it passes whatever "
            f"the known answers say.{keep}"
        )
    return None


def _cwd_relative_data_lead(output: str, scope: list[str], root: Path) -> str:
    """The line a not-done result leads with when a test opened scoped data by a bare name.

    Run R15: tests/test_case_data.py ran `open("cases.json")`; the check runs from
    the project root, so collection failed with FileNotFoundError.
    """
    for match in re.finditer(
        r"FileNotFoundError: \[Errno 2\] No such file or directory: '([^'/\\]+)'", output
    ):
        name = match.group(1)
        data = [entry.rstrip("/") for entry in scope if Path(entry.rstrip("/")).name == name]
        data += [
            p.relative_to(root).as_posix()
            for entry in scope
            if (root / entry).is_dir()
            for p in (root / entry).rglob(name)
        ]
        if not data:
            continue
        tests = re.findall(r"([\w./-]*\.py)", output[: match.start()])
        tests = [t for t in tests if _is_test_path(t) and (root / t).is_file()]
        test = tests[-1] if tests else "the test"
        return (
            f"{test} opens '{name}' relative to the working directory, and the check runs "
            f"from the project root, so it is not found. Open it beside the test: "
            f"`Path(__file__).with_name('{name}')` ({data[0]}).\n\n"
        )
    return ""


def _changed_files(root: Path) -> list[str]:
    """Paths git sees changed or new, beagle's record and caches left out."""
    # -z, read unstripped: _run's strip would eat the leading space of " M path".
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
            cwd=str(root),
            input="",
            capture_output=True,
            text=True,
            timeout=30.0,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0:
        return []
    fields = proc.stdout.split("\0")
    paths = []
    i = 0
    while i < len(fields):
        record = fields[i]
        i += 1
        if len(record) < 4:
            continue
        rel = record[3:]
        if record[0] in "RC" or record[1] in "RC":
            i += 1  # the rename or copy source follows as its own field
        parts = Path(rel).parts
        if not parts or parts[0] == ".beagle" or _CACHE_DIRS & set(parts):
            continue
        paths.append(rel)
    return paths


def _root_relative(entry: str, root: Path) -> str | None:
    """`entry` relative to `root`: as given when relative, None when absolute outside it.

    Run R23: the driver scoped /home/choong/cobs/docs/reference-notes.md, and git's
    root-relative paths never matched it, so prove took nothing away and the
    passing task was never committed.
    """
    text = entry.strip()
    if not text or not Path(text).expanduser().is_absolute():
        return entry
    path = Path(text).expanduser()
    for base in (root, _resolved(root)):
        for candidate in (path, _resolved(path)):
            try:
                rel = candidate.relative_to(base).as_posix()
            except ValueError:
                continue
            return (rel or ".") + ("/" if text.endswith("/") and rel else "")
    return None


def _root_relative_scope(
    scope: list[str], root: Path, kind: str = "scope"
) -> tuple[list[str], str | None]:
    """`scope` with absolute entries under `root` made root-relative, or why one is refused.

    `kind` names the argument in the refusal: "scope", or "locks" for the locks.
    """
    entries: list[str] = []
    for entry in scope:
        rel = _root_relative(entry, root)
        if rel is None:
            return scope, (
                f"pursuit_step: {kind} entry {entry} is outside the project root {root}. "
                f"{kind.capitalize()} names paths in the project, relative to {root} "
                '(e.g. "src/module.py"); call pursuit_step again with those.'
            )
        entries.append(rel)
    return entries, None


def _lock_path(entry: str, root: Path) -> str:
    """Lock `entry` root-relative and normalized; an entry outside `root` is kept as given."""
    rel = _root_relative(entry.strip(), root)
    if rel is None:
        return entry.strip()
    return os.path.normpath(rel) + ("/" if rel.endswith("/") and rel != "/" else "")


def _lock_paths(locks: list[str], root: Path) -> list[str]:
    """`locks` root-relative and normalized, each once, in order.

    Run R29: absolute locks never matched a relative check, and
    reference_digest.md was listed twice.
    """
    return list(dict.fromkeys(_lock_path(e, root) for e in locks if e.strip()))


def _in_scope(rel: str, scope: list[str], root: Path | None = None) -> bool:
    if not scope:
        return True
    if root is not None:
        scope = [e for e in (_root_relative(s, root) for s in scope) if e is not None]
    return any(rel == s.rstrip("/") or rel.startswith(s.rstrip("/") + "/") for s in scope)


def _scope_has_data(scope: list[str]) -> bool:
    """Whether `scope` names a data file (a file with a suffix other than .py)."""
    return any(Path(rel.rstrip("/")).suffix not in {"", ".py"} for rel in scope)


def _imported_modules(root: Path, scope: list[str]) -> list[str]:
    """Project source files (under src/ or the root) that the scoped tests import.

    Run R12: T0008's tests/test_cases.py imported src/interval_tree_clock.py, a
    defect there was the proof, and nothing offered it.
    """
    tests: list[Path] = []
    for rel in scope:
        path = root / rel.rstrip("/")
        found = sorted(path.rglob("*.py")) if path.is_dir() else [path]
        tests += [p for p in found if p.is_file() and _is_test_path(str(p.relative_to(root)))]
    modules: list[str] = []
    for test in tests:
        try:
            tree = ast.parse(test.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        names = [
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ] + [
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module and not node.level
        ]
        for name in names:
            base = name.replace(".", "/")
            for rel in (f"src/{base}.py", f"{base}.py", f"src/{base}/__init__.py"):
                if (root / rel).is_file() and not _is_test_path(rel):
                    if rel not in modules:
                        modules.append(rel)
                    break
    return modules


#: beagle's THRASH_LIMIT (beagle/pursuit.py), a constant there and not configurable:
#: `pursuit spawn` refuses a task whose retry chain holds more attempts than this.
SPAWN_LIMIT = 3


def _retry_chain(task: str, nodes: list[dict[str, Any]]) -> set[str]:
    """Every attempt at `task`'s intent: `sibling_of` back to the first route, then
    everything descended from it, as beagle's `_sibling_family` counts them."""
    by_id = {str(n.get("id")): n for n in nodes}
    origin, seen = task, {task}
    while (up := str((by_id.get(origin) or {}).get("sibling_of") or "")) and up not in seen:
        origin = up
        seen.add(up)
    chain = {origin}
    growing = True
    while growing:
        growing = False
        for n in nodes:
            if str(n.get("sibling_of") or "") in chain and str(n.get("id")) not in chain:
                chain.add(str(n.get("id")))
                growing = True
    return chain


def _at_spawn_limit(task: str, nodes: list[dict[str, Any]] | None) -> bool:
    """Whether beagle refuses another route for `task`: its retry chain is at the limit."""
    return bool(nodes) and len(_retry_chain(task, nodes or [])) > SPAWN_LIMIT


def _infeasible_call(task: str, check: str, scope: list[str], why: str = "") -> str:
    """The pursuit_step call that closes an open, unprovable `task` infeasible."""
    why = why or (
        f"`{check or 'its check'}` passes, and no defect put back into "
        f"{', '.join(scope[:4]) or 'its scope'} fails it"
    )
    return f"pursuit_step task={json.dumps(task)}, abandon={json.dumps('infeasible: ' + why)}"


def _replan_parent_call(task: str, nodes: list[dict[str, Any]]) -> str:
    """The pursuit_plan call that re-plans `task`'s parent once `task` closes infeasible."""
    node = next((n for n in nodes if str(n.get("id")) == task), {})
    parent = str(node.get("parent") or "")
    if not parent:
        return ""
    title = str(node.get("title") or task).replace("::", ":").replace('"', "'").strip()
    return (
        f'pursuit_plan task="{parent}", parts=["{title}::by a route other than '
        f"{task}'s, which was found infeasible\"]"
    )


def _spawn_limit_offer(
    task: str, check: str, scope: list[str], nodes: list[dict[str, Any]], why: str = ""
) -> str:
    """What a result says for `task` at beagle's spawn limit: no new route, and the
    infeasible close with the parent's re-plan to make instead."""
    chain = ", ".join(sorted(_retry_chain(task, nodes)))
    replan = _replan_parent_call(task, nodes)
    return (
        f"Its retry chain ({chain}) is at beagle's limit of {SPAWN_LIMIT} attempts, so "
        f"beagle refuses a new route. Close it infeasible instead: "
        f"{_infeasible_call(task, check, scope, why)}"
        + (f"; then re-plan its parent: {replan}." if replan else ".")
    )


def _unproven_call(
    task: str,
    check: str,
    scope: list[str],
    root: Path,
    missing_data: list[str],
    nodes: list[dict[str, Any]] | None = None,
) -> str:
    """The pursuit_step call that gives an unproven task a check a defect can fail,
    with its values taken from the tree, or a split when none can be.

    Audit 11: three branches of that refusal put prose ("a done_when running the
    data file's test") where the values go, so the call could not be sent as given.
    Run R26: at beagle's spawn limit a new route is refused, so the call is a close
    the tree allows: the known-answers amend for a data scope, else infeasible.
    """
    limited = _at_spawn_limit(task, nodes)
    tests_only = _only_data_and_tests(scope)
    tests = [rel.rstrip("/") for rel in scope if _is_test_path(rel) and rel.endswith(".py")]
    tests += [rel for rel in _check_test_files(check, root) if rel not in tests]
    done_when = ""
    added: list[str] = []
    notes = ""
    if tests_only and missing_data:
        done_when, added = check, missing_data
        notes = f"New route: {', '.join(missing_data)}, which the check reads, is in scope"
    elif tests_only and _scope_has_data(scope):
        data = next(r.rstrip("/") for r in scope if Path(r.rstrip("/")).suffix not in {"", ".py"})
        test = next(
            (t for t in tests if _cases_test_reads(root / t, Path(data).name)),
            _data_test("", scope, root),
        )
        done_when, added = f"python3 -m pytest -q {test}", [test]
        notes = f"New route: {test} fails once {data} is taken away"
    elif tests_only:
        base = "src/" if (root / "src").is_dir() else ""
        for test in tests:
            found = _imported_modules(root, [test]) or [
                f"{base}{name.replace('.', '/')}.py"
                for name in _test_project_imports(root / test)
            ]
            if found:
                done_when, added = f"python3 -m pytest -q {test}", found[:1]
                notes = f"New route: a defect put into {found[0]} fails {test}"
                break
    else:
        code = [
            rel.rstrip("/")
            for rel in scope
            if rel.rstrip("/").endswith(".py") and not _is_test_path(rel)
        ]
        modules = {_module_of(rel): rel for rel in code}
        on_disk = sorted(
            p.relative_to(root).as_posix()
            for p in (root / "tests").rglob("test_*.py")
            if not _CACHE_DIRS & set(p.relative_to(root).parts)
        )
        importing = next(
            (
                (t, modules[name])
                for t in on_disk
                for name in _test_project_imports(root / t)
                if name in modules
            ),
            None,
        )
        if importing is None:
            stem = Path(code[0]).stem if code else task.lower()
            importing = (f"tests/test_{stem}.py", code[0] if code else ", ".join(scope) or task)
        test, module = importing
        done_when, added = f"python3 -m pytest -q {test}", [test]
        notes = f"New route: {test} runs {module}, so a defect there fails it"
    if limited:
        if (
            tests_only
            and _scope_has_data(scope)
            and done_when
            and " ".join(done_when.split()) != " ".join(check.split())
        ):
            routed = [*scope, *[rel for rel in added if rel not in scope]]
            return (
                f"pursuit_step task={json.dumps(task)}, done_when={json.dumps(done_when)}, "
                f"scope={json.dumps(routed)}"
            )
        return _infeasible_call(task, check, scope)
    if not done_when:
        # Run R26: the test imports no module, so no defect outside it can fail it;
        # the new route keeps the check and has the test import what it tests.
        test = tests[0] if tests else "the test"
        done_when = check or (f"python3 -m pytest -q {tests[0]}" if tests else "")
        notes = f"Make {test} import the module it tests, from a file added to scope"
    notes = _drop_self_import_restore(notes, check, scope, root)
    routed = [*scope, *[rel for rel in added if rel not in scope]]
    call = (
        f'pursuit_step task="{task}", new_route=true, done_when={json.dumps(done_when)}, '
        f"scope={json.dumps(routed)}, notes="
    )
    lead = f"pursuit_step: {task} not run — call instead: "
    tail = "; or split it with pursuit_plan."
    full = json.dumps(notes, ensure_ascii=False)
    if len(lead) + len(call) + len(full) + len(tail) > ESCALATION_HEAD_CHARS:
        full = '"…"'
    return call + full


@dataclass(frozen=True)
class _Proof:
    """What `prove` said of a passing check, or why it could not be asked."""

    proven: bool
    text: str
    #: A defect was put back and the check still passed: the check, not the
    #: work, is what falls short.
    weak: bool = False
    #: A tests-only task had no WITNESS in the module its tests import, named in
    #: `text`: another worker can give one, so the task is not unproven.
    ask_module: bool = False
    #: Proven only by taking away a source file: that shows the check needs the
    #: import, not that it tests the behaviour.
    by_absent_source: bool = False


def _opened_commit(task: str, root: Path) -> str:
    """The commit `task` opened on: its record's, else the parent of its first
    commit, else HEAD; "" when git has none."""
    rc, out = _pursuit(["show", task], root)
    record = _json_reply(out) if rc == 0 else None
    if isinstance(record, dict) and str(record.get("opened_commit") or "").strip():
        return str(record["opened_commit"]).strip()
    rc, out = _run(["git", "log", "--format=%H", f"--grep=^{task}:"], root, timeout=30.0)
    own = out.split() if rc == 0 else []
    rev = f"{own[-1]}^" if own else "HEAD"
    rc, out = _run(["git", "rev-parse", "--verify", "--quiet", rev], root, timeout=30.0)
    return out.strip() if rc == 0 else ""


def _in_commit(sha: str, rel: str, root: Path) -> bool:
    """Whether `rel` was in the tree at commit `sha`."""
    if not sha:
        return False
    return _run(["git", "cat-file", "-e", f"{sha}:{rel}"], root, timeout=30.0)[0] == 0


#: A pytest summary line naming where a run went wrong: `FAILED <node>` or `ERROR <path>`.
_PYTEST_OUTCOME = re.compile(r"\b(FAILED|ERROR) (\S+\.py\S*)")
_IMPORT_FAILURE = re.compile(r"\b(?:ModuleNotFoundError|ImportError)\b|No module named")


def _import_error_only(output: str) -> bool:
    """Whether a refusal `prove` reports is only pytest failing to import a module.

    Run R28: T0008's witness took src/interval_tree_clock.py away, and the check
    refused at ERROR on the test file's import. That shows the test imports the
    file, not that any test runs its code.
    """
    outcomes = _PYTEST_OUTCOME.findall(output)
    return (
        bool(outcomes)
        and all(kind == "ERROR" for kind, _ in outcomes)
        and _IMPORT_FAILURE.search(output) is not None
    )


async def _prove(
    task: str,
    report: str,
    scope: list[str],
    root: Path,
    timeout: float,
    locks: list[str] | None = None,
) -> _Proof | None:
    """Ask `beagle pursuit prove` whether the passing check can refuse at all.

    A check that passes over a defect put back into the work is not about the
    work: run 11d closed two tasks on import-only checks. The worker names the
    defect (`WITNESS_NOTE`); a missing or misshapen one falls back to taking
    away the source files the task changed that were not in the tree when it
    opened, or with none, its data files; a task with locks it wrote takes those
    away. None
    when neither can be tried — no witness and no changed file — and the close
    decides.
    """
    attempts: list[list[str]] = []
    refused: list[str] = []
    witness = _witness(report)
    modules = _imported_modules(root, scope) if _only_data_and_tests(scope) else []
    ask_module = bool(modules) and (witness is None or _is_test_path(witness[0]))
    if ask_module:
        # Run R12: a tests-only task's witness in its test was refused, and it
        # had no source of its own to take away; the module it tests has one.
        where = f"{witness[0]}: the WITNESS is in a test file. " if witness else ""
        refused.append(
            f"{where}Give a WITNESS in {' or '.join(modules)}, the module the test imports: "
            "a NEEDLE there that the test must catch. Leave the test as it is."
        )
    elif witness is not None and _is_test_path(witness[0]):
        # Run R04: W24's witness was in tests/test_case_data.py, and beagle
        # answered about the needle's count, not the check.
        refused.append(
            f"{witness[0]}: the WITNESS is in a test file; name a defect in the code the "
            "test runs, and leave the test as it is."
        )
    elif witness is not None:
        path, needle, replacement = witness
        attempts.append(["--mutate", path, "--needle", needle, "--replacement", replacement])
    # Run R17: T0008's locked cases.json was never written, and the fallback
    # took away itc.py instead; for a known-answers task the data is the work.
    opened = _opened_commit(task, root)
    changed = _changed_files(root)
    reverted = _locked_fix_reversion(task, scope, root, changed)
    if reverted:
        attempts.insert(0, reverted)
    sources = [
        rel
        for rel in (lock.rstrip("/") for lock in locks or [])
        if rel in changed and (root / rel).is_file() and not _in_commit(opened, rel, root)
    ]
    if not sources:
        sources = [
            rel
            for rel in changed
            if _in_scope(rel, scope, root) and not _is_test_path(rel) and (root / rel).is_file()
        ]
    if not sources:
        # A known-answers task changes only data and tests: taking its data
        # file away is the defect (beagle proves it when the task wrote it).
        sources = [
            rel
            for rel in changed
            if _in_scope(rel, scope, root) and not rel.endswith(".py") and (root / rel).is_file()
        ]
    if sources:
        # Run R14: both witnesses took away interval_tree_clocks.py, which T0003
        # wrote, so removing it showed only that the import was needed.
        sources = [rel for rel in sources if not _in_commit(opened, rel, root)]
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
            by_absent_source = "--absent" in how and any(
                rel.endswith(".py") and not _is_test_path(rel) for rel in sources
            )
            if by_absent_source and _import_error_only(out):
                refused.append(
                    f"{tail}\n\nNot proof: with {', '.join(sources)} taken away the check "
                    "failed only on importing it, which any file of that name passes. Give "
                    "a WITNESS: a NEEDLE in that code which a test the check runs must catch."
                )
                continue
            return _Proof(proven=True, text=tail, by_absent_source=by_absent_source)
        if verdicts.get(task) == "NOT PROVEN" and "STILL PASSES" in out:
            # The check passed over the defect: a real answer, not one a
            # different witness should be asked to overturn.
            return _Proof(proven=False, text=tail, weak=True)
        refused.append(tail)
    if ask_module:
        return _Proof(proven=False, text="\n\n".join(refused), ask_module=True)
    if not attempts and not refused:
        if not _requires_witness(root):
            return None
        return _Proof(
            proven=False,
            text="The worker gave no WITNESS block, and changed no source file in the "
            "task's scope that is new since it opened and could be taken away instead.",
        )
    return _Proof(proven=False, text="\n\n".join(refused))


def _reversion_edit(current: str, locked: str) -> tuple[str, str] | None:
    """(needle, replacement) that turns `current` back into `locked`: the differing
    span, widened to whole lines until it occurs once in `current`; None if equal."""
    if current == locked:
        return None
    head = 0
    limit = min(len(current), len(locked))
    while head < limit and current[head] == locked[head]:
        head += 1
    tail = 0
    while (
        tail < limit - head and current[len(current) - 1 - tail] == locked[len(locked) - 1 - tail]
    ):
        tail += 1
    start, end = current.rfind("\n", 0, head) + 1, len(current) - tail
    newline = current.find("\n", end)
    end = len(current) if newline < 0 else newline + 1
    while True:
        needle = current[start:end]
        if needle and current.count(needle) == 1:
            break
        if start == 0 and end == len(current):
            return None
        start = current.rfind("\n", 0, max(start - 1, 0)) + 1
        newline = current.find("\n", end)
        end = len(current) if newline < 0 else newline + 1
    replacement = locked[start : len(locked) - (len(current) - end)]
    return needle, replacement


def _locked_fix_reversion(
    task: str, scope: list[str], root: Path, changed: list[str]
) -> list[str] | None:
    """`prove` arguments putting each locked file a known-answers fix changed back to
    its locked version: the defect the fix's check must refuse.

    Run R34 E66: T0011 fixed the locked tests/cases.json, which was tracked, so no
    file new since it opened could be taken away and the fix could not be proved.
    """
    goal = root / ".beagle" / GOAL_BASENAME
    manifest = _lock_manifest(goal)
    held = [
        rel
        for rel in _locked_in_scope(scope, goal)
        if rel in changed and (root / rel).is_file() and rel in manifest
    ]
    if not held:
        return None
    rc, out = _pursuit(["show", task], root)
    record = _json_reply(out) if rc == 0 else None
    title = str(record.get("title") or "") if isinstance(record, dict) else ""
    if not _fixes_known_answers_in(title, scope, goal):
        return None
    argv: list[str] = []
    for rel in held:
        locked = _locked_bytes(root, goal.parent / LOCKED_DIR, rel, manifest[rel])
        if locked is None:
            continue
        try:
            current = (root / rel).read_text(encoding="utf-8")
            edit = _reversion_edit(current, locked.decode("utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if edit is not None:
            argv += ["--mutate", rel, "--needle", edit[0], "--replacement", edit[1]]
    return argv or None


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
    paths = [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]
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
#: Under `.beagle/`: for each locked path, its sha256 and the commit that holds
#: it. Run R14: a worker's `ruff format .` rewrote a locked test and its copy in
#: the store alike, so comparing the two restored nothing.
LOCK_MANIFEST = "locks.json"


def _locked(goal: Path) -> list[str]:
    """The project paths locked so far: in the lock manifest, with a known copy.

    Run R22: a copy put into the store by hand locked a file nothing had locked;
    only beagle writes the manifest, so a copy it does not name is not a lock.
    """
    store = goal.parent / LOCKED_DIR
    try:
        return sorted(rel for rel in _lock_manifest(goal) if (store / rel).is_file())
    except (OSError, ValueError):
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


def _lock(
    goal: Path, root: Path, entries: list[str], task: str = "", relock: Collection[str] = ()
) -> tuple[list[str], list[str]]:
    """Copy each named file to the locked store; (locked, why the rest were not).

    A path in `relock` is locked again from its new content: a known-answers
    fix task's close.
    """
    store = goal.parent / LOCKED_DIR
    held = set(_locked(goal)) - set(relock)
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
    if locked:
        manifest = _lock_manifest(goal)
        for rel in locked:
            data = (store / rel).read_bytes()
            manifest[rel] = {"sha256": _sha256(data), "commit": _head_holding(root, rel, data)}
            if task:
                manifest[rel]["task"] = task
        _write_lock_manifest(goal, manifest)
    return locked, skipped


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _lock_manifest(goal: Path) -> dict[str, dict[str, Any]]:
    """The lock manifest: each locked path's sha256 and the commit holding it."""
    try:
        raw = json.loads((goal.parent / LOCK_MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return {
        rel: entry
        for rel, entry in raw.items()
        if isinstance(entry, dict) and isinstance(entry.get("sha256"), str)
    }


def _write_lock_manifest(goal: Path, manifest: dict[str, dict[str, Any]]) -> None:
    with contextlib.suppress(OSError):
        (goal.parent / LOCK_MANIFEST).write_text(
            json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8"
        )


def _committed_bytes(root: Path, commit: str, rel: str) -> bytes | None:
    """`rel` as `commit` holds it, or None."""
    try:
        shown = subprocess.run(
            ["git", "show", f"{commit}:{rel}"],
            cwd=root,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return shown.stdout if shown.returncode == 0 else None


def _head_holding(root: Path, rel: str, data: bytes) -> str | None:
    """The HEAD commit's id when it holds `rel` as `data`, else None."""
    if _committed_bytes(root, "HEAD", rel) != data:
        return None
    rc, out = _run(["git", "rev-parse", "HEAD"], root, timeout=10.0)
    commit = out.strip()
    return commit if rc == 0 and re.fullmatch(r"[0-9a-f]{40,64}", commit) else None


def _locked_bytes(root: Path, store: Path, rel: str, entry: dict[str, Any]) -> bytes | None:
    """The bytes `rel` was locked as, from its lock commit or the store; None if lost."""
    want = entry["sha256"]
    commit = entry.get("commit")
    if isinstance(commit, str) and commit:
        data = _committed_bytes(root, commit, rel)
        if data is not None and _sha256(data) == want:
            return data
    with contextlib.suppress(OSError):
        data = (store / rel).read_bytes()
        if _sha256(data) == want:
            return data
    data = _committed_bytes(root, "HEAD", rel)
    if data is not None and _sha256(data) == want:
        return data
    return None


def _restore_locked(goal: Path, root: Path, spare: Collection[str] = ()) -> list[str]:
    """Put back every locked file a worker changed or removed; the ones it did.

    A path in `spare` is left as the worker wrote it: a known-answers fix
    task's own scope.

    A path in the lock manifest is held to its recorded sha256 and restored
    from its lock commit, the store copy rewritten with it: a tool run over
    the whole tree changes the store too.
    """
    store = goal.parent / LOCKED_DIR
    manifest = _lock_manifest(goal)
    changed_manifest = False
    restored = []
    for rel in _locked(goal):
        if rel in spare:
            continue
        target = root / rel
        entry = manifest[rel]
        try:
            current = target.read_bytes() if target.is_file() else None
            known = _locked_bytes(root, store, rel, entry)
            if known is None:
                continue  # neither the commit nor the store holds it any more
            if not entry.get("commit"):
                commit = _head_holding(root, rel, known)
                if commit is not None:
                    entry["commit"] = commit
                    changed_manifest = True
            copy = store / rel
            if not copy.is_file() or copy.read_bytes() != known:
                copy.write_bytes(known)
            if current == known:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(known)
        except OSError:
            continue
        restored.append(rel)
    if changed_manifest:
        _write_lock_manifest(goal, manifest)
    return restored


def _put_back_drift(
    goal: Path, root: Path, nodes: list[dict[str, Any]] | None = None, but: str = ""
) -> str:
    """Put back each locked file that differs from its lock; one line saying so, or "".

    Run R28: W3 stripped the locked tests/test_cases.py after the last put-back, the
    split's WIP commit kept it, and T0026 closed done on a check that passed only on
    the stripped file. An open known-answers fix task other than `but` keeps the
    locked files in its scope as it wrote them; its close locks them again.
    """
    if not _locked(goal):
        return ""
    spare: list[str] = []
    for node in _tree_nodes(root) if nodes is None else nodes:
        task = str(node.get("id") or "")
        if task == but or node.get("status") != "open":
            continue
        title = str(node.get("title") or "")
        rc, out = _pursuit(["show", task], root)
        shown = _json_reply(out) if rc == 0 else None
        scope = _strings(shown.get("scope")) if isinstance(shown, dict) else []
        if not _fixes_known_answers_in(title, scope, goal):
            continue
        if not scope:
            return ""  # a fix whose scope is unknown may hold any of them
        spare += _locked_in_scope(scope, goal)
    restored = _restore_locked(goal, root, spare)
    if not restored:
        return ""
    return (
        f"{len(restored)} locked file(s) were put back, since they differed from their "
        f"lock: {', '.join(restored)}."
    )


def _pending_locks(goal: Path, task: str, add: list[str] | None = None) -> list[str]:
    """The locks `task` asked for, adding `add`; kept until the task closes done."""
    path = goal.parent / PENDING_LOCKS
    root = goal.parent.parent
    try:
        pending = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pending = {}
    if not isinstance(pending, dict):
        pending = {}
    # Run R29 filed absolute paths; they are read, and stored, root-relative.
    entries = _lock_paths([e for e in pending.get(task) or [] if isinstance(e, str)], root)
    if add:
        entries = _lock_paths(entries + add, root)
        pending[task] = entries
        with contextlib.suppress(OSError):
            path.write_text(json.dumps(pending, indent=1), encoding="utf-8")
    return entries


def _lockable(rel: str) -> bool:
    """Whether `rel` may be filed as a pending lock: a test or a data file.

    Run R24 #14 filed tests/interval_tree_clocks.py, the module, as a lock, and
    the workers after it were refused the file their task was to write.
    """
    return _is_test_path(rel) or Path(rel).suffix.lower() in CASES_DATA_SUFFIXES


def _drop_pending_locks(goal: Path, task: str) -> None:
    path = goal.parent / PENDING_LOCKS
    with contextlib.suppress(OSError, ValueError, AttributeError):
        pending = json.loads(path.read_text(encoding="utf-8"))
        if pending.pop(task, None) is not None:
            path.write_text(json.dumps(pending, indent=1), encoding="utf-8")


def _move_pending_locks(goal: Path, task: str, first_part: str, root: Path) -> str:
    """Move `task`'s pending locks to the task split from `first_part`; a note, or "".

    Run R17 split T0002 and its three pending locks stayed behind: only a
    done close drops them, and a container is never closed that way.
    """
    locks = _pending_locks(goal, task)
    if not locks:
        return ""
    heir = _children(task, root).get(_part_title(first_part).lower())
    if heir is None:
        return ""
    _pending_locks(goal, heir, locks)
    _drop_pending_locks(goal, task)
    return f"{task}'s pending locks ({', '.join(locks)}) moved to its first part, {heir}."


def _fixes_known_answers(title: str) -> bool:
    """Whether a task titled `title` fixes the known answers, and so may hold them.

    Audit 9 on T0171: matching any title that named the cases let "Implement the
    clock so it passes the cases" hold, edit and re-lock the locked test.
    """
    text = title.strip().lower()
    if text.startswith(("known answers: fix", "known answers fix")):
        return True
    head = text.split("::", 1)[0]
    return bool(re.search(r"\bfix", head)) and "known answer" in head


def _fixes_known_answers_in(title: str, scope: list[str], goal: Path) -> bool:
    """Whether a task titled `title` on `scope` fixes the known answers.

    Run R34 #27: T0007, made as the fix and scoped to the locked file alone, was
    refused as locked for lacking the title's words. A scope of nothing but
    locked files has no other work to do, whatever the title says.
    """
    if _fixes_known_answers(title):
        return True
    named = {os.path.normpath(entry.strip()) for entry in scope if entry.strip()}
    return bool(named) and named <= set(_locked(goal))


def _locked_in_scope(scope: list[str], goal: Path) -> list[str]:
    """The locked files `scope` names, itself or by a directory holding them."""
    held = []
    for rel in _locked(goal):
        for entry in scope:
            path = os.path.normpath(entry.strip())
            if path == "." or rel == path or rel.startswith(path.rstrip("/") + "/"):
                held.append(rel)
                break
    return held


def _known_answers_fix_route(
    rel: str,
    goal: Path,
    task: str,
    title: str,
    nodes: list[dict[str, Any]] | None = None,
    rest: list[str] | None = None,
    done_when: str = "",
) -> str:
    """Who locked `rel`, that its changes are put back, and how a wrong one is fixed.

    Run R28 offered a fix part titled as pending container T0010, which the
    plan refused as a clash; a live fix leaf is offered instead, and a title
    already in the tree is made distinct. Run R34: with only that route offered,
    seven steps were refused on a scope whose one file to write was not locked;
    `rest`, the scope without its locked files, is offered first as the same call.
    """
    owner = _lock_manifest(goal).get(rel, {}).get("task")
    head = (
        f"{rel} is locked as the known answers{f' ({owner})' if owner else ''}: a "
        "worker's change to it is put back before every check. "
    )
    if rest:
        call = f'pursuit_step task="{task}", scope={json.dumps(rest)}'
        if done_when:
            call += f", done_when={json.dumps(done_when)}"
        head += (
            f"Send the same call without the locked files: {call}, the rest as it was. "
            "The locked files stay readable to the worker and judge its work. "
        )
    if nodes is None:
        nodes = _tree_nodes(goal.parent.parent)
    fix = f"Known answers: fix {rel}"
    same = [n for n in nodes if _fold(str(n.get("title") or "")) == _fold(fix)]
    titled = {str(m.get("id")): str(m.get("title") or "") for m in nodes}
    for n in same:
        nid = str(n.get("id"))
        if n.get("status") not in ("pending", "open"):
            continue
        leaves = _live_leaves(nid, nodes) if _is_container(nid, nodes) else [nid]
        leaf = next((t for t in leaves if _fixes_known_answers(titled.get(t, ""))), None)
        if leaf is not None:
            return (
                f'{head}If the locked test is wrong, fix it in {leaf}: pursuit_step task="'
                f'{leaf}", scope={json.dumps([rel])}. Its close re-locks the file.'
            )
    if same:
        fix = f"{fix} for {task}"
    # The second part may not take {task}'s own title: the plan refuses that (T0240).
    return (
        f"{head}If the locked test is wrong, split {task} with a fix first: "
        f'pursuit_plan task="{task}" parts=["{fix}::<what is wrong in it>", "{title}, on '
        f'the fixed answers::<what {task} is for>"]; then run the fix step with pursuit_step, '
        f"{rel} in its scope. Its close re-locks the file."
    )


def _locked_scope_problem(
    scope: list[str], root: Path, task_title: str, task: str, done_when: str = ""
) -> str | None:
    """Why `scope` may not name a locked file, or None.

    Run R20: T0010 and T0011 scoped the locked tests/test_cases.py, and every
    edit the worker made to it was put back before the check. A directory
    holding a locked file is allowed: put-back still guards the file, and later
    tasks add their own tests beside it.
    """
    goal = root / ".beagle" / GOAL_BASENAME
    if _fixes_known_answers_in(task_title, scope, goal):
        return None
    named = {os.path.normpath(entry.strip()) for entry in scope}
    held = [rel for rel in _locked(goal) if rel in named]
    if not held:
        return None
    rest = [entry for entry in scope if os.path.normpath(entry.strip()) not in held]
    return _known_answers_fix_route(
        held[0], goal, task, task_title, rest=rest, done_when=done_when
    )


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


def _with_spawn_notice(
    result: AgentToolResult, predecessor: str, successor: str, spawned: str
) -> AgentToolResult:
    """`result`, led by the spawn of `successor` when the reply would drop it.

    Run R18 #20 and #54 asked about T0002 and T0006 and were told only "T0005 not
    opened" and "T0008 not opened": the spawn that superseded each was lost.
    """
    text = "".join(getattr(c, "text", "") for c in result.content)
    if spawned.strip() and spawned.strip() in text:
        return result
    refusal = text.removeprefix(f"pursuit_step: {successor} not opened — ")
    return _step_result(
        f"{predecessor} was superseded by {successor} (new route); {successor} was not "
        f"opened: {refusal}\n\n{predecessor} is closed to work now: send {successor} next, "
        f'with pursuit_step task="{successor}".'
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
    rc, out = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
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


def _without_beagle_habits(brief: str, bound: str = f"timeout {COMMAND_TIMEOUT}") -> str:
    """beagle's brief without the lines that tell a worker to run `beagle`.

    The worker guard refuses every `beagle` command. Run R06: W2 and W4 ran the
    "Working habits" line's `RUN_CONTAINED_FOREGROUND=1 beagle contain run heavy
    -- …` and were refused. That line is said again with a plain capped,
    redirected command; the standing-checks line (`beagle pursuit recheck`) is
    dropped, and the `beagle pursuit show` aside is cut. `bound` is the
    command's prefix, from `_command_bound`.
    """
    lines: list[str] = []
    for line in brief.splitlines(keepends=True):
        if "beagle contain run" in line:
            match = _HABIT_LOG.search(line)
            log = match.group(1) if match else _DEFAULT_TEST_LOG
            bullet = "- " if line.lstrip().startswith("- ") else ""
            ending = "\n" if line.endswith("\n") else ""
            alone = (
                " The command gets a memory cap of its own, below yours: exit 137 means it "
                "was killed for going over it, which is a finding to report."
                if bound.startswith("systemd-run")
                else ""
            )
            lines.append(
                f"{bullet}Run every test, build and check capped and redirected, as a plain "
                f'command: `{bound} <cmd> > {log} 2>&1; echo "exit $?"` (e.g. '
                f"`{bound} python3 -m pytest -q tests/ > {log} 2>&1; "
                f'echo "exit $?"`), then read the tail of {log}.{alone}{ending}'
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


#: An abandon that closes a task infeasible, with the evidence after the colon.
_INFEASIBLE = re.compile(r"(?is)^\s*infeasible\s*:\s*(.*)$")


def _close_infeasible(
    task: str,
    evidence: str,
    nodes: list[dict[str, Any]],
    roots: list[str],
    root: Path,
    goal: Path,
) -> str:
    """Close `task` infeasible in beagle, and name the parent to re-plan.

    Run R26: T0011 was open, its check passing and unprovable, its retry chain at
    beagle's spawn limit; no pursuit_step argument closed it, so the driver
    hand-edited .beagle/.
    """
    node = next((n for n in nodes if str(n.get("id")) == task), {})
    if not evidence:
        return (
            f"pursuit_step: {task} not closed infeasible — say why after the colon: "
            f'abandon="infeasible: <what makes it so>".'
        )
    if task in roots:
        return (
            f"pursuit_step: {task} not closed infeasible — it is the root, the goal "
            "itself, and the goal is the user's."
        )
    if node.get("status") != "open":
        return (
            f"pursuit_step: {task} not closed infeasible — it is "
            f"{node.get('status') or 'not in the tree'}; only an open task closes this "
            "way, as beagle refuses an infeasible close on a task not yet worked."
            + (
                f' Work it first: pursuit_step task="{task}".'
                if node.get("status") == "pending"
                else ""
            )
        )
    if not _at_spawn_limit(task, nodes):
        chain = ", ".join(sorted(_retry_chain(task, nodes)))
        return (
            f"pursuit_step: {task} not closed infeasible — its retry chain ({chain}) "
            f"holds {len(_retry_chain(task, nodes))} attempt(s), below beagle's limit of "
            f"{SPAWN_LIMIT}, so a hard task is not yet shown infeasible. Call instead: "
            f'pursuit_step task="{task}", new_route=true and notes saying how the new '
            f'route differs, or pursuit_step task="{task}" with notes saying what to fix.'
        )
    argv = [
        "close", task, "--outcome", "infeasible",
        "--reason", f"infeasible: {evidence}"[:500],
        "--evidence", evidence[:1000],
    ]  # fmt: skip
    rc, out = _pursuit(argv, root)
    if rc != 0:
        return (
            f"pursuit_step: `beagle pursuit close {task} --outcome infeasible` refused "
            f"(exit {rc}):\n{out}"
        )
    _drop_pending_locks(goal, task)
    _forget_task(root, task)
    parent = str(node.get("parent") or "")
    replan = (
        f"Re-plan its parent {parent} with a route the finding does not rule out: "
        f"{_replan_parent_call(task, nodes)}."
        if parent
        else "Next: call pursuit_step with no arguments for the next task."
    )
    return (
        f"{out.splitlines()[0] if out else task + ' closed infeasible'}\n\n"
        f"{_tree(root)}\n\n{replan}"
    )


#: Open tasks whose passing check `prove` could not show to refuse, by (project
#: root, task). A further step on the task runs no worker, whatever check or
#: scope it is sent with: run R04's driver got past a (check, scope) key by
#: changing the scope. A new route or a plan of the task clears it.
_UNPROVEN: set[tuple[str, str]] = set()

#: The exit status of each open task's check at its last run in a step, by
#: (project root, task): a split commits the task's work when it was 0.
_LAST_CHECK_EXIT: dict[tuple[str, str], int] = {}

#: The last failing run of each open task's check, by (project root, task): the
#: check, its exit status and the tail of its output. Run R25: only a step's
#: second worker heard why the first one's check failed, so W4, W6, W8 and W10
#: each started blind on a test pytest collected nothing from.
_LAST_CHECK_FAILURE: dict[tuple[str, str], tuple[str, int, str]] = {}


def _note_check_run(key: tuple[str, str], check: str, verdict: tuple[int, str]) -> None:
    """Remember a check run of the task at `key`: its exit, and its tail if it failed."""
    _LAST_CHECK_EXIT[key] = verdict[0]
    if verdict[0] == 0:
        _LAST_CHECK_FAILURE.pop(key, None)
    else:
        _LAST_CHECK_FAILURE[key] = (check, verdict[0], verdict[1][-CHECK_TAIL_CHARS:])


def _last_failure_note(key: tuple[str, str], check: str) -> str:
    """The brief note for a step's first worker when the task's check last failed."""
    last = _LAST_CHECK_FAILURE.get(key)
    if last is None or not check or last[0] != check:
        return ""
    _, rc, tail = last
    no_tests = _pytest_collected_none(rc, check)
    return (
        (f"\n\n{no_tests}" if no_tests else "")
        + f"\n\nThe check failed last step (exit {rc}). Its output ends:\n{tail}\n"
        + "Fix the work, not the check."
    )


def _close_demand(text: str) -> str:
    """The demand of a result whose check passed but whose close kept the task open:
    its "the sub-agent must …" clause, else the reason after "the check passes, but"."""
    for para in text.split("\n\n"):
        _, passes, reason = para.partition("the check passes, but ")
        if not passes:
            continue
        if reason.startswith("the task "):
            reason = reason.partition(": ")[2] or reason
        _, must, demand = reason.partition("the sub-agent must ")
        said = (demand if must else reason).strip()
        return said[:1].lower() + said[1:]
    return ""


def _last_close_note(key: tuple[str, str]) -> str:
    """The brief note for a rerun after a close whose check passed kept the task open."""
    demand = _NOT_DONE_DEMAND.get(key)
    if not demand:
        return ""
    return (
        f"\n\nThe last close kept this task open: {demand.rstrip('.')}. Fix that; "
        "the check alone is not enough."
    )


SPLIT_WIP_TITLE = "work in progress before split"

#: Step results that left a task not done (stays open or blocked, not run,
#: unproven), by (project root, task), and the scope it was worked in. Run
#: R04 sent 14 such steps at one task, none of which offered another way.
_NOT_DONE: dict[tuple[str, str], int] = {}
_NOT_DONE_SCOPE: dict[tuple[str, str], tuple[str, ...]] = {}
#: Why the last close whose check passed kept the task open, by (project root,
#: task). Run R32: the rerun's worker never heard what the close refused.
_NOT_DONE_DEMAND: dict[tuple[str, str], str] = {}
#: Tasks a not-done step left with their check failing, by (project root, task).
_NOT_DONE_CHECK_FAILED: set[tuple[str, str]] = set()

#: Not-done results after which a further step on the task dispatches no worker.
ESCALATE_AFTER = 3
#: Not-done results after which an escalation no longer offers a notes-only rerun
#: of a task only the close's own judge kept open.
JUDGE_NOTES_UNTIL = 2 * ESCALATE_AFTER
# The breaker quotes a refused result's first line up to 300 characters
# (REPEATED_CALL_QUOTE in tau core); an escalation's call must fit in it.
ESCALATION_HEAD_CHARS = 290

#: Not-done results after which the driver may not read the task's files.
DRIVER_READS_UNTIL = 2


def _carried_criteria(predecessor: str, root: Path) -> str:
    """The criteria of the task a successor follows, which its own must keep."""
    rc, out = _pursuit(["show", predecessor], root)
    record = _json_reply(out) if rc == 0 else None
    return str(record.get("criteria") or "").strip() if isinstance(record, dict) else ""


def _already_passes(
    check: str, task: str = "", nodes: list[dict[str, Any]] | None = None, done_by: str = ""
) -> str:
    """Why a check that passes before any work is not bound.

    A part of a non-root container gets no abandon hint, which
    `_abandon_problem` would refuse: run R09's driver sent that refused call
    nine times. A done sibling closed on the same check is named instead.
    With `done_by`, a done task whose commit is in the scope's history, the
    done-by abandon is offered: run R14 was told to bind the goal's test,
    which was the same passing check.
    """
    if done_by:
        return (
            f"`{check}` already passes, before any work, so it cannot tell this task's "
            f"work from none. If {done_by}'s work already did this, call pursuit_step "
            f'task="{task}" abandon="done by {done_by}" done_when="{check}": it closes '
            f"done on {done_by}'s commit, with no sub-agent. If work is left, bind a check "
            "that fails now: name a new test file for what is left, put it in scope, and "
            "say in the notes what it should test; do not write it yourself."
        )
    text = (
        f"`{check}` already passes, before any work, so it cannot tell this task's work "
        "from none. Bind a check that fails now: name a new test file for what this task "
        "adds, e.g. `python3 -m pytest -q tests/test_<this task>.py`, put it in scope, and "
        "say in the notes what it should test. It fails until the sub-agent writes it; do "
        "not write it yourself. If the work is there already, bind the goal criterion's "
        "test, which imports and runs the code."
    )
    nodes = nodes or []
    parent = {str(n.get("id")): str(n.get("parent") or "") for n in nodes}
    roots = [t for t, p in parent.items() if not p]
    container = parent.get(task, "")
    if not container or container in roots:
        return f"{text} {ABANDON_HINT}"
    same = " ".join(check.split())
    for node in nodes:
        sibling = str(node.get("id"))
        if (
            sibling != task
            and parent.get(sibling) == container
            and node.get("status") == "done"
            and " ".join(str(node.get("done_when") or "").split()) == same
        ):
            return (
                f"{text} {sibling} closed done on this same check; {task} must add "
                "something beyond it: bind a test of what is left (e.g. the goal's cases "
                "test that imports the code), or call pursuit_step {} for other work."
            )
    return text


async def _passes_without_own_work(check: str, scope: list[str], root: Path) -> bool:
    """Whether `check` still passes with the uncommitted files in `scope` put back as committed.

    Run R12: T0008's new route was refused as already passing, five times, when
    only its own uncommitted test made the check pass.
    """
    own = [rel for rel in _changed_files(root) if scope and _in_scope(rel, scope, root)]
    if not own:
        return True
    saved: dict[str, bytes | None] = {}
    try:
        for rel in own:
            path = root / rel
            saved[rel] = path.read_bytes() if path.is_file() else None
            head = subprocess.run(
                ["git", "show", f"HEAD:{rel}"], cwd=root, capture_output=True, check=False
            )
            if head.returncode == 0:
                path.write_bytes(head.stdout)
            elif path.is_file():
                path.unlink()
        return (await _run_check(check, root, DEFAULT_CHECK_TIMEOUT))[0] == 0
    finally:
        for rel, data in saved.items():
            path = root / rel
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)


async def _passes_only_by_uncommitted(check: str, scopes: list[list[str]], root: Path) -> bool:
    """Whether `check`, passing now, passes only because of uncommitted files in `scopes`.

    The task's own scope and its predecessor's: the close's witness takes those
    files away, so the close judges them. Run R18 refused T0005's open as
    "already passes" seven times, on W1's uncommitted known-answers files.
    """
    combined = [entry for scope in scopes for entry in scope]
    if not combined:
        return False
    return not await _passes_without_own_work(check, combined, root)


def _predecessor_scope(record: dict[str, Any], root: Path) -> list[str]:
    """The scope of the task `record` succeeds, or [] when it succeeds none."""
    predecessor = str(record.get("sibling_of") or "").strip()
    if not predecessor:
        return []
    rc, out = _pursuit(["show", predecessor], root)
    shown = _json_reply(out) if rc == 0 else None
    return _strings(shown.get("scope")) if isinstance(shown, dict) else []


def _check_reach(check: str, root: Path) -> list[str]:
    """The project files a check runs: the paths its words name (the .py files
    under a directory), and the project modules each .py file among them imports."""
    reached: list[str] = []
    for rel in _check_targets(check, root):
        target = root / rel
        files = (
            [rel]
            if target.is_file()
            else sorted(
                p.relative_to(root).as_posix()
                for p in target.rglob("*.py")
                if not _CACHE_DIRS & set(p.relative_to(root).parts)
            )
        )
        for found in files:
            reached.append(found)
            if not found.endswith(".py"):
                continue
            beside = Path(found).parent.as_posix()
            bases = ["", "src/"] + ([f"{beside}/"] if beside != "." else [])
            for names in _test_imports(root / found):
                for name in names:
                    base = name.replace(".", "/")
                    reached += [
                        path
                        for prefix in bases
                        for path in (f"{prefix}{base}.py", f"{prefix}{base}/__init__.py")
                        if (root / path).is_file()
                    ]
    return list(dict.fromkeys(reached))


def _uncommitted_reach(check: str, scopes: list[list[str]] | None, root: Path) -> list[str]:
    """The uncommitted files (changed or untracked, per git) the check runs, kept
    to those inside one of `scopes`; all of them when `scopes` is None."""
    changed = set(_changed_files(root))
    combined = [entry for scope in scopes or [] for entry in scope]
    if scopes is not None and not combined:
        return []
    return [
        rel
        for rel in _check_reach(check, root)
        if rel in changed and (scopes is None or _in_scope(rel, combined, root))
    ]


def _hang_note(paths: list[str], stopped: tuple[str, float, float | None]) -> str:
    """The brief note for a check killed while running uncommitted code in scope."""
    what, seconds, earlier = stopped
    named = ", ".join(paths)
    before = f", earlier run {earlier:.2f}s" if earlier is not None else ""
    return (
        f"The check's run of {named} does not finish (killed at {what} after "
        f"{seconds:.0f}s{before}). Find the loop or growth in {named} that never ends, "
        "and make it finish: a check cannot judge code that does not return.\n\n"
    )


#: The task whose last pursuit_step was refused on a killed check, by project
#: root, and the pursuit_step call that opens it. Run R30: the driver edit
#: guard pointed back at the call that had just been refused, for 51 minutes.
_KILLED_NOT_OPENED: dict[str, tuple[str, str]] = {}


def _killed_open_call(task: str, check: str, scope: list[str], notes: str, root: Path) -> str:
    """The pursuit_step call that opens `task` after its check was killed on code
    outside its scope: one whose scope holds the uncommitted code the check runs,
    or, with none, one with a check that finishes."""
    reached = _uncommitted_reach(check, None, root)
    say = json.dumps(notes or "<what the check runs that does not finish>")
    if reached:
        wider = list(dict.fromkeys([*scope, *reached]))
        return (
            f"pursuit_step task={json.dumps(task)}, scope={json.dumps(wider)}, "
            f"done_when={json.dumps(check)}, notes={say}: with the uncommitted code the "
            "check runs in its scope, it opens, and the sub-agent is told to find what "
            "does not finish"
        )
    return (
        f'pursuit_step task={json.dumps(task)}, done_when="<a check that finishes on '
        f'the committed code>", notes={say}: the check runs no uncommitted code, so '
        "no task's work can make this one finish"
    )


def _on_disk_note(check: str, task: str) -> str:
    """The note on a check that passes only on uncommitted work in the task's scope."""
    return (
        f"`{check}` passes already, but only on uncommitted files in {task}'s scope: the "
        "work is on disk, and the close judges it (its witness takes those files away, "
        "and the check must then fail).\n\n"
    )


def _cases_close_problem(root: Path, entries: list[str]) -> tuple[str, str] | None:
    """(what keeps the task open, the notes that fix it) when the close's cases
    judgements, `_unread_cases` then `_cases_test_problem`, refuse the files on disk."""
    unread = _unread_cases(root, entries)
    if unread is not None:
        test, data = unread
        return (
            f"{test} does not read {data}, so the known answers judge nothing",
            f"{test} must load {data} and run every case in it against the code, with no "
            "hand-written asserts of its own.",
        )
    flawed = _cases_test_problem(root, entries)
    if flawed is not None:
        test, problem = flawed
        return (
            f"{test} {problem}, so the known answers could never judge the code",
            f"{test} {problem}: make it look up only cases the data holds, compare the "
            "code's results with each case's expected value, and use each attribute one way.",
        )
    return None


def _bound_is_data_check(bound: str, data_check: str, root: Path) -> bool:
    """Whether the bound check already is `data_check`, the data test it would propose."""
    if not bound:
        return False
    if _same_check(bound, data_check):
        return True
    data_test = data_check.split()[-1]
    return _check_targets(bound, root) == [data_test]


async def _data_route_on_disk(
    task: str,
    route: tuple[str, str, str, list[str]],
    root: Path,
    extra: list[str] | None = None,
    *,
    bound: str = "",
    locks: list[str] | None = None,
    is_open: bool = False,
) -> str | None:
    """What to say in place of "bind the data test" when that test already passes; or None.

    Run R18: told to bind `pytest tests/test_case_data.py`, which W1's uncommitted
    files made pass, the driver was refused as "already passes" for 14 minutes.
    Run R32: told an open task "closes on that work" that the close's cases
    judgements still refused, and to bind the check it was already bound to.
    """
    test, module, data_check, needs = route
    if (await _run_check(data_check, root, DEFAULT_CHECK_TIMEOUT))[0] != 0:
        return None
    same = _bound_is_data_check(bound, data_check, root)
    rebind = "" if same else f", done_when={json.dumps(data_check)}"
    if needs and not same:
        rebind += f", scope={json.dumps(needs)}"
    leave = " The bound check already is that data test; leave done_when out." if same else ""
    if await _passes_only_by_uncommitted(data_check, [needs, extra or []], root):
        why = (
            f"{test} imports {module}, which a later task writes, so {task} closes on its "
            f"data test `{data_check}`. That already passes, on the known-answers work on "
            "disk, uncommitted in this scope"
        )
        kept = _cases_close_problem(root, list(dict.fromkeys([*needs, *(locks or [])])))
        if kept is not None:
            problem, notes = kept
            return (
                f"Send pursuit_step task={json.dumps(task)}{rebind}, notes={json.dumps(notes)}: "
                f"the close keeps {task} open while {problem}. {why}, but the close also "
                f"judges the cases test.{leave}"
            )
        opens = "its check is amended" if is_open and not same else "it opens"
        if is_open and same:
            opens = "it runs"
        opens += ", and the close judges the files on disk"
        return (
            f"Send pursuit_step task={json.dumps(task)}{rebind}: {opens}. {why}: {task} "
            f"closes on that work.{leave}"
        )
    return (
        f"If a done task already did this work, call pursuit_step task={json.dumps(task)} "
        f'abandon="done by <that task>" done_when="{data_check}"; if work is left, name a '
        "new data test file for it that fails now, put it in scope, and say in the notes "
        f"what it should test. {test} imports {module}, which a later task writes, and the "
        f"data test `{data_check}` already passes on the committed tree, so neither check "
        f"can tell {task}'s work from none."
    )


async def _unwritten_check_problem(
    command: str,
    scope: list[str],
    task: str,
    root: Path,
    extra: list[str] | None = None,
    *,
    bound: str = "",
    locks: list[str] | None = None,
    is_open: bool = False,
) -> str | None:
    """`_imports_unwritten_problem`, unless the data test it prescribes already passes."""
    route = _data_test_route(command, scope, root)
    if route is None:
        return None
    on_disk = await _data_route_on_disk(
        task, route, root, extra, bound=bound, locks=locks, is_open=is_open
    )
    return on_disk or _imports_unwritten_problem(command, scope, root)


def _kept_data_check(done_when: str, scope: list[str], bound: str, root: Path) -> str | None:
    """The note for keeping the bound check when `done_when` runs a test importing
    unwritten code and the data test tau would propose instead is the bound check; or None.

    Run R32 #12: the notes that would have fixed the task were refused together
    with such a done_when.
    """
    if not bound or _check_problem(bound) is not None:
        return None
    route = _data_test_route(done_when, scope, root)
    if route is None or not _bound_is_data_check(bound, route[2], root):
        return None
    test, module = route[0], route[1]
    return (
        f'Kept done_when="{bound}" (the data test); {test} imports {module}, which a '
        f"later task writes, so `{done_when}` is not bound.\n\n"
    )


def _shown(task: str, root: Path) -> dict[str, Any]:
    """`task`'s record from `beagle pursuit show`, or {}."""
    rc, out = _pursuit(["show", task], root)
    shown = _json_reply(out) if rc == 0 else None
    return shown if isinstance(shown, dict) else {}


def _own_files(task: str, rel: str, root: Path) -> bool:
    """Whether `task`'s declared scope names `rel`.

    Run R22: T0019, with no scope, was titled "Known answers: run
    tests/test_case_data.py", and the title made T0002's committed test its own.
    """
    named = {
        os.path.normpath(rel)
        for s in _strings(_shown(task, root).get("scope"))
        if s.strip() and (rel := _root_relative(s, root)) is not None
    }
    return os.path.normpath(rel) in named


def _sibling_owned_check_problem(
    check: str, scope: list[str], task: str, nodes: list[dict[str, Any]], root: Path
) -> str | None:
    """Why `task`'s check may not run a file a task waiting on it owns, or None.

    Run R21 bound T0005, scope tests/cases.json, to T0006's tests/test_case_data.py;
    T0006 waited on T0005, so only T0005's worker could touch the failing test, and
    its scope forbade it. A file a done task committed is that task's work, not the
    waiter's to write.
    """
    if not check or not scope:
        return None
    runs = [rel for rel in _check_test_files(check, root) if not _in_scope(rel, scope, root)]
    if not runs:
        return None
    for waiter, waits in _hard_waits(nodes).items():
        if waiter == task or not any(task in (w[1], w[2]) for w in waits):
            continue
        for rel in runs:
            if _own_files(waiter, rel, root) and not _done_task_in_log([rel], task, nodes, root):
                return (
                    f"{task}'s check runs {rel}, which {waiter} writes after {task}, so "
                    f"nothing can fix {rel} before {task} closes. Put {rel} in {task}'s "
                    f"scope beside {', '.join(scope)} (scope={json.dumps([*scope, rel])}), "
                    f"or bind a check {task}'s own files decide."
                )
    return None


#: An abandon naming the done task whose commit did this one's work:
#: "done by T0008", "Done by T0008's commit".
_DONE_BY = re.compile(r"(?i)^\s*done\s+by\s+(t\d{4,})\b")


def _check_words(check: str) -> list[str]:
    """A check's words, inside one `sh -c` level too."""
    try:
        words = shlex.split(check)
    except ValueError:
        return []
    found: list[str] = []
    for word in words:
        try:
            found += shlex.split(word) if " " in word and not word.startswith("-") else [word]
        except ValueError:
            found.append(word)
    return found


def _check_targets(check: str, root: Path) -> list[str]:
    """The project paths a check's words name, inside one `sh -c` level too."""
    try:
        words = shlex.split(check)
    except ValueError:
        return []
    found: list[str] = []
    for word in words:
        inner = shlex.split(word) if " " in word and not word.startswith("-") else [word]
        for part in inner:
            rel = part.split("::")[0].rstrip("/")
            if not rel or rel.startswith("-") or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if Path(rel).parts[0] == ".beagle":
                continue
            if (root / rel).exists() and rel not in found and rel != ".":
                found.append(rel)
    return found


def _commit_paths(sha: str, root: Path) -> list[str]:
    rc, out = _run(["git", "show", "--format=", "--name-only", sha], root, timeout=30.0)
    return [line.strip() for line in out.splitlines() if line.strip()] if rc == 0 else []


def _task_commits(done: str, root: Path) -> list[str]:
    """The commits `done` landed: the record's, then those whose message starts `Tnnnn:`."""
    shas: list[str] = []
    rc, out = _pursuit(["show", done], root)
    record = _json_reply(out) if rc == 0 else None
    if isinstance(record, dict):
        for key in ("commit", "closed_commit", "result_commit"):
            sha = str(record.get(key) or "").strip()
            if sha:
                shas.append(sha)
    rc, out = _run(["git", "log", "--format=%H", f"--grep=^{done}:"], root, timeout=30.0)
    if rc == 0:
        shas += [line.strip() for line in out.splitlines() if line.strip()]
    return list(dict.fromkeys(shas))


def _done_task_in_log(paths: list[str], task: str, nodes: list[dict[str, Any]], root: Path) -> str:
    """The latest done task, not `task`, whose `Tnnnn:` commit touches `paths`; else ""."""
    if not paths:
        return ""
    done = {str(n.get("id")) for n in nodes if n.get("status") == "done"} - {task}
    rc, out = _run(["git", "log", "--format=%s", "--", *paths], root, timeout=30.0)
    if rc != 0:
        return ""
    for subject in out.splitlines():
        named = re.match(rf"({_TASK_ID.pattern}):", subject.strip())
        if named and named.group(1) in done:
            return named.group(1)
    return ""


async def _done_by(
    task: str,
    done: str,
    arguments: Mapping[str, Any],
    nodes: list[dict[str, Any]],
    root: Path,
) -> str:
    """Close pending `task` done on `done`'s commit, or say which condition failed.

    Run R14: T0003's commit made the cases test pass, so T0004 and T0009 could
    not bind it, could not be abandoned, and had no move left. A task closes
    done here only on a done task's commit that touches its scope (or its
    check's targets) and a check that passes now, with no sub-agent.
    """
    refused = f"pursuit_step: {task} not closed done by {done} — "
    status = {str(n.get("id")): n.get("status") for n in nodes}
    if status.get(task) != "pending":
        return (
            f"{refused}only a pending task closes this way, and {task} is "
            f"{status.get(task) or 'not in the tree'}. Work it with pursuit_step task="
            f'"{task}"; its check decides.'
        )
    if status.get(done) != "done":
        return (
            f"{refused}{done} is not a done task in the tree "
            f"({status.get(done) or 'no such task'}). Name the done task whose commit did "
            "this task's work."
        )
    rc, out = _pursuit(["show", task], root)
    record = _json_reply(out) if rc == 0 else None
    if not isinstance(record, dict):
        return f"pursuit_step: cannot read {task} (exit {rc}):\n{out}"
    given = str(arguments.get("done_when") or "").strip()
    check = given or str(record.get("done_when") or "").strip()
    if not check:
        return (
            f"{refused}it has no check: pass done_when, ONE command that exits 0 on "
            f"{done}'s work, and call again."
        )
    chained, prose = _and_chain(check)
    if prose is not None or chained is None:
        return f"{refused}{prose}"
    check = chained
    title = str(record.get("title") or "")
    changes = _changes_done_work(task, done, title, record, nodes)
    if changes:
        return (
            f"{refused}{task} is to change {done}'s work ({changes}); it cannot be done by "
            f'it. Work it with pursuit_step task="{task}", with a done_when that fails until '
            "that change is made."
        )
    done_record = _shown(done, root)
    if _same_check(check, str(done_record.get("done_when") or "")) and not _created_before(
        record, done_record
    ):
        return (
            f"{refused}its check `{check}` is {done}'s own, which passed when {done} closed, "
            f"before {task} was made, so it cannot tell {task}'s work from none. Work it "
            f'with pursuit_step task="{task}", with a done_when that fails until its work '
            "is done."
        )
    scope = _strings(arguments.get("scope")) or _strings(record.get("scope"))
    paths = scope or _check_targets(check, root)
    if not paths:
        return (
            f"{refused}it has no scope and its check names no project path, so nothing "
            f"shows {done}'s commit did its work. Pass scope: the paths that work is in."
        )
    shas = _task_commits(done, root)
    if not shas:
        return (
            f"{refused}no commit of {done} is found: its record names none and "
            f'`git log --grep "{done}:"` finds none.'
        )
    sha = next(
        (s for s in shas if any(_in_scope(rel, paths, root) for rel in _commit_paths(s, root))), ""
    )
    if not sha:
        return (
            f"{refused}{done}'s commit ({shas[0][:12]}) touches none of "
            f"{', '.join(paths)}, so it did not do this task's work."
        )
    # Run R28: T0026 closed done on a check that passed only on a stripped locked test.
    put_back = _put_back_drift(root / ".beagle" / GOAL_BASENAME, root, nodes)
    check_rc, check_out = await _run_check(check, root, DEFAULT_CHECK_TIMEOUT)
    if check_rc != 0:
        return (
            (f"{put_back}\n\n" if put_back else "")
            + f"{refused}its check `{check}` does not pass now (exit {check_rc}), so the "
            f"work is not there yet: work it with pursuit_step.\n"
            f"{check_out[-CHECK_TAIL_CHARS:]}"
        )
    if not await _passes_without_own_work(check, scope, root):
        return (
            f"{refused}its check passes only with uncommitted changes in its scope, not "
            f"on {done}'s commit: work it with pursuit_step."
        )
    # Run R22: the close refused T0018 for want of a witness and left it open, and
    # six workers then ran on its empty scope. A witness here takes away a file
    # `done` committed in this task's paths; with none, the close cannot be met.
    witness: list[str] = []
    if _requires_witness(root):
        committed = list(dict.fromkeys(rel for s in shas for rel in _commit_paths(s, root)))
        witness = [
            rel
            for rel in committed
            if _in_scope(rel, paths, root) and _can_witness(rel) and (root / rel).is_file()
        ]
        if not witness:
            named = f"{title}\n{record.get('criteria') or ''}\n{arguments.get('criteria') or ''}"
            return _done_by_unwitnessed(task, done, check, paths, committed, root, named)
    criteria = (
        str(arguments.get("criteria") or "").strip()
        or str(record.get("criteria") or "").strip()
        or f"`{check}` passes on {done}'s work"
    )
    argv = ["open", task, "--criteria", criteria, "--done-when", check]
    if scope:
        argv += ["--scope", *scope]
    if witness:
        argv += ["--confirms", done]
    rc, opened = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    if rc != 0:
        return f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{opened}"
    if witness:
        argv = ["prove", task, *(a for rel in witness for a in ("--absent", rel))]
        argv += ["--check-timeout", f"{DEFAULT_CHECK_TIMEOUT:.0f}"]
        rc, proved = _pursuit(argv, root, timeout=2 * DEFAULT_CHECK_TIMEOUT + 120)
        verdicts = {m.group(1): m.group(2) for m in _PROVE_VERDICT.finditer(proved)}
        if rc != 0 or verdicts.get(task) != "PROVEN":
            why = (
                f"its check passes on {done}'s commit but was not shown to refuse with "
                f"{', '.join(witness)} taken away (prove exit {rc})"
            )
            return _done_by_released(task, why, proved, root)
        if any(rel.endswith(".py") for rel in witness) and _import_error_only(proved):
            why = (
                f"its check refused with {', '.join(witness)} taken away only on importing "
                "it, which shows the test imports the file, not that it runs its code"
            )
            return _done_by_released(task, why, proved, root)
    because = f"satisfied by {done}'s commit {sha[:12]}; no sub-agent ran"
    argv = ["close", task, "--outcome", "done", "--body", because]
    argv += ["--spent", "0", "--spent-because", because]
    rc, closed = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    if rc != 0:
        why = f"`beagle pursuit close` refused the done close (exit {rc})"
        return _done_by_released(task, why, closed, root)
    _forget_task(root, task)
    return (
        f"{task} — {title}: closed done, {because}.\n\n{closed}\n\n{_tree(root)}\n\n"
        "Next: call pursuit_step with no arguments for the next task."
    )


def _changes_done_work(
    task: str, done: str, title: str, record: Mapping[str, Any], nodes: list[dict[str, Any]]
) -> str:
    """How `task` is to change `done`'s work, by tau's own fix-route titles or the
    tree; "" when neither says so.

    Run R28: "Fix known answers" and "Known answers: fix tests/cases.json" closed
    as satisfied by T0002's commit, the work they were made to change.
    """
    if _fixes_known_answers(title):
        return f"{title!r} is a known-answers fix"
    by_id = {str(n.get("id")): n for n in nodes}
    seen = {task}
    up = str(record.get("sibling_of") or (by_id.get(task) or {}).get("sibling_of") or "")
    while up and up not in seen:
        if up == done:
            return f"it is a new route for {done}"
        seen.add(up)
        up = str((by_id.get(up) or {}).get("sibling_of") or "")
    return ""


def _same_check(check: str, other: str) -> bool:
    """Whether two checks are one command, spacing aside."""
    try:
        return bool(other.strip()) and shlex.split(check) == shlex.split(other)
    except ValueError:
        return check.split() == other.split()


def _created_before(record: Mapping[str, Any], done_record: Mapping[str, Any]) -> bool:
    """Whether the record shows the task was made before `done` closed; False when
    it cannot tell."""
    try:
        made = datetime.fromisoformat(str(record.get("created_at") or ""))
        closed = datetime.fromisoformat(str(done_record.get("closed_at") or ""))
        return made < closed
    except (TypeError, ValueError):
        return False


def _can_witness(rel: str) -> bool:
    """Whether taking `rel` away can witness a check: a source or data file, not a test."""
    return not (_is_test_path(rel) and rel.endswith(".py"))


def _done_by_unwitnessed(
    task: str,
    done: str,
    check: str,
    paths: list[str],
    committed: list[str],
    root: Path,
    named: str = "",
) -> str:
    """The up-front refusal of a done-by close the witness rule would refuse.

    Run R28: the offer widened eleven tasks' scope with tests/cases.json, T0002's
    data, and each then closed as done by T0002. A file outside the paths is
    offered only when the task's title or criteria (`named`) names it.
    """
    outside = [
        rel
        for rel in committed
        if not _in_scope(rel, paths, root)
        and _can_witness(rel)
        and (root / rel).is_file()
        and (rel in named or re.search(rf"(?<![\w./-]){re.escape(Path(rel).name)}\b", named))
    ]
    said = (
        f"pursuit_step: {task} not closed done by {done} — this pursuit closes done only on "
        f"a witnessed check, and no file {done} committed in {', '.join(paths)} is a source "
        "or data file whose absence could show the check refuses, so the close would "
        f"refuse and leave {task} open. Nothing was opened."
    )
    if outside:
        return (
            f"{said} {done} committed {', '.join(outside)}, outside those paths: call "
            f'pursuit_step task="{task}", abandon="done by {done}", '
            f"done_when={json.dumps(check)}, scope={json.dumps([*paths, *outside])}."
        )
    return (
        f"{said} No file {done} wrote that this task names could show it either, so "
        f"{done}'s commit is not shown to have done this work: call pursuit_step "
        f'task="{task}" and bind a check that fails now, with a scope naming the files '
        "the work changes."
    )


def _done_by_released(task: str, why: str, out: str, root: Path) -> str:
    """Close `task`, opened for a done-by close that did not go through, as blocked.

    beagle has no verb that returns an open task to pending, and an abandoned part
    stalls its container; a blocked task stays accountable and is reworked by its
    own check or a new route.
    """
    reason = f"done-by close not taken: {why}"[:500]
    argv = ["close", task, "--outcome", "blocked", "--reason", reason]
    if out.strip():
        argv += ["--body", out]
    argv += ["--spent", "0", "--spent-because", "no sub-agent ran: a done-by close"]
    rc, closed = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    _forget_task(root, task)
    if rc != 0:
        return (
            f"pursuit_step: {task} not closed done — {why}:\n{out[-CHECK_TAIL_CHARS:]}\n\n"
            f"It is still open: closing it blocked exited {rc}:\n{closed}"
        )
    return (
        f"pursuit_step: {task} not closed done — {why}. It was closed blocked rather than "
        f"left open:\n{out[-CHECK_TAIL_CHARS:]}\n\n{closed}\n\n{_tree(root)}\n\n"
        f'Next: give it a new route, pursuit_step task="{task}", new_route=true, with a '
        "done_when that fails until the work is done and notes saying what that work is; "
        "or call pursuit_step with no arguments for the next task."
    )


def _escalation(
    task: str,
    count: int,
    arguments: dict[str, Any] | None = None,
    record: dict[str, Any] | None = None,
    root: Path | None = None,
    data_test_passes: bool = False,
    bound_fails: bool = False,
) -> str:
    """The refusal of a step on a task `count` steps have left not done.

    Given the refused call's `arguments` and the task's `record`, it first says
    what that call lacks: run R15 sent twelve calls, E19-E41, that the same
    option list alone had refused. `data_test_passes` says the data test its
    bound check would give way to passes on the committed tree, so it is not
    offered (see `_offered_data_test_passes`). `bound_fails` says the bound
    check fails on the tree now, so a sub-agent can make it pass.
    """
    if arguments is None:
        return _escalation_options(
            task, count, f"pursuit_step: {task} not run: {count} steps on it have left it not done."
        )
    demand = _judge_kept_open(task, root)
    if demand:
        return _judge_escalation(task, count, demand)
    lacks = _escalation_lacks(task, arguments, record, root, data_test_passes, bound_fails)
    # Run R16 E34 dropped the done_when line, and the driver resent without it.
    call = _working_call(task, arguments, record, root, data_test_passes, bound_fails)
    # Run R23 E34-E46: the breaker quotes only a result's first line, so the call
    # goes there, short enough to survive its quote, with notes elided if need be.
    lead = f"pursuit_step: {task} not run — call instead: "
    short = _working_call(
        task, arguments, record, root, data_test_passes, bound_fails, bare=True
    )
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _working_call(
            task, arguments, record, root, data_test_passes, bound_fails, bare=True,
            notes="…",
        )
    head = f"{lead}{short}\n{count} steps on it have left it not done."
    if lacks:
        head += "\n" + "\n".join(f"- {line}" for line in lacks)
    head += "\nThe call that works, whole: " + call
    return _escalation_options(task, count, head)


def _escalation_options(task: str, count: int, head: str, rerun: str | None = None) -> str:
    """An escalation's `head`, then the options a task left not done has.

    `rerun`, given for a task only the close's own judge kept open, stands in for
    the new route with a rewritten done_when; "" offers neither.
    """
    if rerun is None:
        rerun = (
            f'- pursuit_step task="{task}", new_route=true, with a rewritten done_when and '
            "notes saying what the new route does differently (the criteria stay);\n"
        )
        why = (
            "another sub-agent on it, however its scope or notes are put, would only add "
            "one more"
        )
    else:
        why = "its check passes each time, and only the close keeps it open"
    return (
        f"{head}\n{task} has had {count} steps without a pass, and {why}. Choose one:\n"
        f'- pursuit_plan task="{task}" with two or more parts, to split it into smaller '
        "tasks (a plan of one part is refused: the task is already one step);\n"
        f"{rerun}"
        "- stop, and tell the user what blocks it."
    )


def _judge_kept_open(task: str, root: Path | None) -> str:
    """The close judge's reason, when every not-done step on `task` passed its check
    and only that judge kept the task open; else ""."""
    if root is None:
        return ""
    key = (str(root), task)
    if key in _NOT_DONE_CHECK_FAILED or _LAST_CHECK_EXIT.get(key, 0) != 0:
        return ""
    return _NOT_DONE_DEMAND.get(key, "")


def _notes_only_call(task: str, notes: str) -> str:
    """The rerun of `task` with the bound check kept and `notes` saying what to fix."""
    return f"pursuit_step task={json.dumps(task)}, notes={json.dumps(notes, ensure_ascii=False)}"


def _judge_escalation(task: str, count: int, demand: str) -> str:
    """The escalation of a task only the close's own judge kept open.

    Run R33 #13-#24: every not-done step had passed its check, yet the escalation
    asked for a new done_when, which the data-route rewrite put back to the bound
    one; no call passed both, and the driver resent one call 12 times.
    """
    reason = demand.rstrip(".")
    said = (
        f"\n{count} steps on it have left it not done, each with its check passing: the "
        f"close kept it open because {reason}. A new done_when would not change that, so "
        "keep the bound one (leave done_when and new_route out)."
    )
    if count >= JUDGE_NOTES_UNTIL:
        head = f"pursuit_step: {task} not run — split it or stop.{said}"
        return _escalation_options(task, count, head, rerun="")
    call = _notes_only_call(task, reason)
    lead = f"pursuit_step: {task} not run — call instead: "
    short = call
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _notes_only_call(task, "…")
    head = f"{lead}{short}{said}\nThe call that works, whole: {call}"
    rerun = f"- {call}, a sub-agent at what the close refused, with the bound check kept;\n"
    return _escalation_options(task, count, head, rerun=rerun)


def _judge_notes_rerun(
    task: str, arguments: Mapping[str, Any], record: Mapping[str, Any], root: Path
) -> bool:
    """Whether a step on an escalated task is the notes-only rerun `_judge_escalation`
    offers: notes given, no new route, and the bound check kept or put back."""
    if not _judge_kept_open(task, root) or _NOT_DONE.get((str(root), task), 0) >= JUDGE_NOTES_UNTIL:
        return False
    if arguments.get("new_route") is True or not str(arguments.get("notes") or "").strip():
        return False
    return _kept_bound(arguments, record, root)


def _kept_bound(arguments: Mapping[str, Any], record: Mapping[str, Any], root: Path | None) -> bool:
    """Whether the call's done_when is absent, the bound check, or one
    `_kept_data_check` puts back to the bound check."""
    done_when = " ".join(str(arguments.get("done_when") or "").split())
    bound = " ".join(str(record.get("done_when") or "").split())
    if done_when in ("", bound):
        return True
    if root is None:
        return False
    scope = _strings(arguments.get("scope")) or _strings(record.get("scope"))
    return _kept_data_check(done_when, scope, bound, root) is not None


def _escalation_lacks(
    task: str,
    arguments: dict[str, Any],
    record: dict[str, Any] | None,
    root: Path | None,
    data_test_passes: bool = False,
    bound_fails: bool = False,
) -> list[str]:
    """What a step refused by the escalation lacks to be taken as a new route."""
    record = record or {}
    lacks = []
    if arguments.get("new_route") is not True:
        lacks.append(
            "This call has no new_route=true, so it asks for another sub-agent on the "
            "same route."
        )
    criteria = " ".join(str(arguments.get("criteria") or "").split())
    bound_criteria = " ".join(str(record.get("criteria") or "").split())
    if criteria and bound_criteria and criteria != bound_criteria:
        lacks.append(
            f"Its criteria differ from {task}'s: leave criteria out, since a new route "
            "keeps them."
        )
    bound_check = " ".join(str(record.get("done_when") or "").split())
    done_when = " ".join(str(arguments.get("done_when") or "").split())
    if done_when and _kept_bound(arguments, record, root):
        # Run R33 #12: `_kept_data_check` puts such a done_when back to the bound one.
        done_when = bound_check
    scope = _strings(arguments.get("scope")) or _strings(record.get("scope"))
    unproven = _unproven_data_route(task, bound_check, scope, root)
    if unproven is not None:
        if unproven:
            lacks.append(
                f"Its scope lacks {', '.join(unproven)}, the data file the bound check's "
                f"test reads. That check, `{bound_check}`, passes, so keep it (leave "
                "done_when out) and add the data file, whose absence is the proof: "
                f"scope={json.dumps([*scope, *unproven])}."
            )
        return lacks
    if bound_check and done_when in ("", bound_check):
        route = _data_test_route(bound_check, scope, root) if root is not None else None
        if route is not None and data_test_passes:
            lacks.append(
                f"Its done_when is the bound check `{bound_check}`, which runs {route[0]}: "
                f"that fails with ImportError until a later task writes {route[1]}. The data "
                f"test `{route[2]}` already passes on the committed tree, so it cannot judge "
                "the work either: a new route needs a check that fails now."
            )
        elif route is not None:
            test, module, data_check, needs = route
            lacks.append(
                f"Its done_when is the bound check `{bound_check}`, which runs {test}: "
                f"that fails with ImportError until a later task writes {module}, and no "
                "path in this scope creates it. The check a sub-agent can pass is the data "
                f"test only: done_when=\"{data_check}\".{_scope_note(needs, scope)}"
            )
        elif done_when and not _keeps_bound_check(bound_check, scope, root, bound_fails):
            lacks.append(
                "Its done_when is the bound one: a new route needs a check a sub-agent on "
                "this scope can pass."
            )
    return lacks


def _working_call(
    task: str,
    arguments: dict[str, Any],
    record: dict[str, Any] | None,
    root: Path | None,
    data_test_passes: bool = False,
    bound_fails: bool = False,
    *,
    bare: bool = False,
    notes: str | None = None,
) -> str:
    """The new-route call an escalation takes, spelled out with every argument it needs.

    `bare` leaves out what to add to it; `notes` stands in for the call's own.
    """
    record = record or {}
    record_scope = _strings(record.get("scope"))
    bound_check = " ".join(str(record.get("done_when") or "").split())
    done_when = " ".join(str(arguments.get("done_when") or "").split())
    if done_when and _kept_bound(arguments, record, root):
        # Run R33 #12: `_kept_data_check` puts such a done_when back to the bound one.
        done_when = bound_check
    scope = _strings(arguments.get("scope")) or _strings(record.get("scope"))
    unproven = _unproven_data_route(task, bound_check, scope, root)
    route = (
        _data_test_route(bound_check, scope, root)
        if root is not None and bound_check and not data_test_passes and unproven is None
        else None
    )
    needs = scope
    check = ""
    if unproven is not None:
        # Run R21: the bound check passed; only the data file it reads was missing.
        check = done_when or bound_check
        needs = [*scope, *unproven]
    elif done_when and done_when != bound_check:
        check = done_when
        if route is not None and done_when == route[2]:
            needs = route[3]
    elif route is not None:
        check, needs = route[2], route[3]
    elif _keeps_bound_check(bound_check, scope, root, bound_fails):
        # Run R23 E30: the model's own amended check failed on the tree and ran a
        # test in its scope, and the escalation called it the bound one.
        check = bound_check
    given = _drop_self_import_restore(
        str(arguments.get("notes") or "").strip(), bound_check, record_scope or scope, root
    )
    call = f"pursuit_step task={json.dumps(task)}, new_route=true"
    if check:
        call += f", done_when={json.dumps(check)}"
    if needs != scope or needs != record_scope or unproven is not None:
        call += f", scope={json.dumps(needs)}"
    if given:
        call += f", notes={json.dumps(given if notes is None else notes, ensure_ascii=False)}"
    if bare:
        return call
    # Run R21: a `<…>` placeholder in this call was sent as is; say what to add instead.
    supply = []
    if not check:
        supply.append(
            "done_when, a check a sub-agent on this scope can pass that fails until the "
            "work is done"
        )
    if not given:
        supply.append("notes, saying what the new route does differently")
    if supply:
        call += ". Add to it: " + "; ".join(supply) + "."
    return call


async def _bound_check_fails(
    task: str, arguments: dict[str, Any], record: dict[str, Any], root: Path
) -> bool:
    """Whether the task's bound check, which the call leaves as is, fails on the tree
    now: by its last run, or else by a run now that `_check_broke` does not refuse."""
    bound_check = " ".join(str(record.get("done_when") or "").split())
    done_when = " ".join(str(arguments.get("done_when") or "").split())
    if not bound_check or done_when not in ("", bound_check):
        return False
    last = _LAST_CHECK_EXIT.get((str(root), task))
    if last is not None:
        return last != 0
    rc, out = await _run_check(bound_check, root, DEFAULT_CHECK_TIMEOUT)
    return rc != 0 and _check_broke(rc, out) is None


def _keeps_bound_check(
    bound_check: str, scope: list[str], root: Path | None, bound_fails: bool
) -> bool:
    """Whether a new route keeps `bound_check`: it fails on the tree now, every file
    it runs is in `scope`, and it does not wait on a module no path there writes."""
    if not (bound_fails and bound_check and root is not None):
        return False
    runs = _check_run_files(bound_check, root)
    return (
        bool(runs)
        and all(_in_scope(rel, scope, root) for rel in runs)
        and _imports_unwritten(bound_check, scope, root) is None
    )


def _check_run_files(check: str, root: Path) -> list[str]:
    """The project paths a check names, with the .py files it names not yet written."""
    found = _check_targets(check, root)
    try:
        words = shlex.split(check)
        parts = [
            part
            for word in words
            for part in (shlex.split(word) if " " in word and not word.startswith("-") else [word])
        ]
    except ValueError:
        return found
    for part in parts:
        rel = part.split("::")[0].rstrip("/")
        path = Path(rel)
        if (
            rel.endswith(".py")
            and not path.is_absolute()
            and ".." not in path.parts
            and rel not in found
        ):
            found.append(rel)
    return found


def _unproven_data_route(
    task: str, bound_check: str, scope: list[str], root: Path | None
) -> list[str] | None:
    """For a task whose bound check passed unproven and runs a test reading a data
    file: the data files that test reads and `scope` lacks; or None.

    Run R21: T0005's check passed but could not be shown to refuse, and every
    escalation asked for a new check. The check was right; the scope lacked
    tests/cases.json, whose absence is the proof.
    """
    if root is None or not bound_check:
        return None
    key = (str(root), task)
    if key not in _UNPROVEN or _LAST_CHECK_EXIT.get(key, 0) != 0:
        return None
    reads = _check_data_reads(bound_check, root)
    if not reads:
        return None
    return [rel for rel in reads if not _in_scope(rel, scope, root)]


async def _offered_data_test_passes(
    arguments: Mapping[str, Any], record: Mapping[str, Any], root: Path
) -> bool:
    """Whether the data test an escalation would offer passes on the committed tree.

    The pre-run refuses such a check as "already passes"; one passing only on the
    task's own uncommitted work (or its predecessor's) opens, so is offered.
    """
    bound_check = " ".join(str(record.get("done_when") or "").split())
    scope = _strings(arguments.get("scope")) or _strings(record.get("scope"))
    route = _data_test_route(bound_check, scope, root) if bound_check else None
    if route is None:
        return False
    if (await _run_check(route[2], root, DEFAULT_CHECK_TIMEOUT))[0] != 0:
        return False
    return not await _passes_only_by_uncommitted(
        route[2], [route[3], _predecessor_scope(dict(record), root)], root
    )


def _forget_task(root: Path, task: str) -> None:
    """Drop what the step tool remembers of `task`: closed, re-routed or planned."""
    key = (str(root), task)
    _UNPROVEN.discard(key)
    _LAST_CHECK_EXIT.pop(key, None)
    _LAST_CHECK_FAILURE.pop(key, None)
    _NOT_DONE.pop(key, None)
    _NOT_DONE_SCOPE.pop(key, None)
    _NOT_DONE_DEMAND.pop(key, None)
    _NOT_DONE_CHECK_FAILED.discard(key)


def _killed_attempt_context(
    run: _WorkerRun,
    shown: str,
    verdict: tuple[int, str],
    check: str,
    root: Path,
    scope: list[str],
) -> str:
    """What a killed worker's step result keeps: the attempt before it, and the tree.

    Run R15's second worker was killed at the wall, and the result named only
    the timeout: the first worker's report and the check's output were dropped,
    so the driver went on believing the tests were unwritten.
    """
    parts: list[str] = []
    if shown:
        parts.append(f"The attempt before it reported:\n{shown}")
        if check and verdict[1]:
            parts.append(
                f"`{check}` exit {verdict[0]} after that attempt:\n"
                f"{verdict[1][-CHECK_TAIL_CHARS:]}"
            )
    if run.transcript is not None:
        changes = _scope_changes(root, scope)
        if changes:
            parts.append("In the tree now:\n" + "\n".join(changes))
    return "".join(f"{part}\n\n" for part in parts)


def _not_done(
    root: Path, task: str, scope: list[str], text: str, *, ran: bool = True
) -> AgentToolResult:
    """Count a result that left `task` not done, and return it.

    Only a result where a sub-agent ran counts toward ESCALATE_AFTER: run R23
    counted two refusals that ran nothing, and escalated after one worker run.
    """
    key = (str(root), task)
    count = _NOT_DONE.get(key, 0) + (1 if ran else 0)
    if ran:
        _NOT_DONE[key] = count
    if scope:
        _NOT_DONE_SCOPE[key] = tuple(scope)
    demand = _close_demand(text)
    if demand:
        _NOT_DONE_DEMAND[key] = demand
    elif ran:
        _NOT_DONE_DEMAND.pop(key, None)
        if _LAST_CHECK_EXIT.get(key, 0) != 0:
            _NOT_DONE_CHECK_FAILED.add(key)
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


def _escalated_calls(workable: list[str], root: Path | None) -> str:
    """For each of `workable` at the escalation count, the new-route call that runs it.

    Run R21 pointed its driver at "Workable now: T0005" thirteen times; T0005 had
    three not-done steps, so only a new route would run it.
    """
    if root is None:
        return ""
    said = ""
    for t in workable:
        count = _NOT_DONE.get((str(root), t), 0)
        if count >= ESCALATE_AFTER:
            call = _working_call(t, {}, _shown(t, root), root)
            said += f"\n{t} has had {count} steps and runs only by a new route: {call}"
    return said


def _check_runs_own_file(
    task: str, predecessor: str, nodes: list[dict[str, Any]], root: Path | None
) -> str:
    """The pursuit_step putting `task`'s own file, run by `predecessor`'s check, in
    `predecessor`'s scope beside its own files; or ""."""
    if root is None:
        return ""
    shown = _shown(predecessor, root)
    check = str(shown.get("done_when") or "")
    scope = _strings(shown.get("scope"))
    for rel in _check_test_files(check, root) if check else []:
        if scope and not _in_scope(rel, scope, root) and _own_files(task, rel, root):
            return (
                f"{predecessor}'s check runs {rel}, {task}'s own file, which {predecessor}'s "
                f"scope cannot change: put {rel} in {predecessor}'s scope with its own files, "
                f"pursuit_step task={json.dumps(predecessor)}, "
                f"scope={json.dumps([*scope, rel])}."
            )
    return ""


def _locked_fix_leaf(task: str, nodes: list[dict[str, Any]], root: Path | None) -> str:
    """The step for the first live fix leaf under container `task` while files are locked.

    Run R28: T0010's parts needed the locked test, and its container answer
    named only T0012, itself a container, so no worker ran.
    """
    if root is None:
        return ""
    locked = _locked(root / ".beagle" / GOAL_BASENAME)
    if not locked:
        return ""
    titled = {str(n.get("id")): str(n.get("title") or "") for n in nodes}
    leaf = next(
        (t for t in _live_leaves(task, nodes) if _fixes_known_answers(titled.get(t, ""))), None
    )
    if leaf is None:
        return ""
    return (
        f" If its parts are held back by the locked {', '.join(locked)}, fix that first "
        f'in {leaf}: pursuit_step task="{leaf}", scope={json.dumps(locked)}.'
    )


def _not_workable(
    task: str, nodes: list[dict[str, Any]], workable: list[str], root: Path | None = None
) -> str:
    """Why `task`, neither open nor ready, is not worked now: what it waits on, or its parts.

    Run R16 told its driver "it is a container, done when its parts are, or it
    waits on another task" for T0011, which waited on T0010; the driver read a
    container, then a deadlock, and went off-tool.
    """
    return _not_workable_text(task, nodes, workable, root) + _escalated_calls(workable, root)


def _not_workable_text(
    task: str, nodes: list[dict[str, Any]], workable: list[str], root: Path | None
) -> str:
    listed = ", ".join(workable)
    waits = _hard_waits(nodes).get(task, [])
    if waits:
        named = [w[2] for w in waits]
        ready = [t for t in named if t in workable]
        said = "; ".join(
            (f"through {w[0]}, " if w[0] != task else "") + _wait_text(w, nodes) for w in waits
        )
        demand = _NOT_DONE_DEMAND.get((str(root), ready[0]), "") if ready and root else ""
        with_notes = f", notes={json.dumps(demand)}" if demand else ""
        then = (
            _check_runs_own_file(task, ready[0], nodes, root)
            or f'work {ready[0]} first: pursuit_step task="{ready[0]}"{with_notes}.'
            if ready
            else f"none of those is workable yet. Workable now: {listed}."
        )
        return f"{task} is not a task to work now: it {said}; {then}"
    parts = [
        str(n.get("id"))
        for n in nodes
        if n.get("parent") == task and n.get("status") not in ("abandoned", "superseded")
    ]
    if parts:
        return (
            f"{task} is not a task to work now: it is a container of {', '.join(parts)}, "
            f"done when its parts are. Workable now: {listed}. Call pursuit_step with no "
            "arguments." + _locked_fix_leaf(task, nodes, root)
        )
    return (
        f"{task} is not a task to work now. Workable now: {listed}. Call pursuit_step "
        "with no arguments."
    )


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
    stepped: list[str] = []
    #: This call's new-route spawn: (predecessor, successor, what beagle said).
    spawns: list[tuple[str, str, str]] = []

    #: The lead for this call's refusals, set once the task is a setup milestone.
    lead: list[str] = []
    #: Leads for every result of this call: the scope and locks it did not keep.
    kept_lead: list[str] = []

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
        if _strings(arguments.get("scope")):
            scope, outside = _root_relative_scope(_strings(arguments.get("scope")), root)
            if outside is not None:
                return _step_result(outside)
            arguments = {**arguments, "scope": scope}
        if _strings(arguments.get("locks")):
            # Run R29: absolute locks never matched the relative check.
            locks, outside = _root_relative_scope(_strings(arguments.get("locks")), root, "locks")
            if outside is not None:
                return _step_result(outside)
            arguments = {**arguments, "locks": _lock_paths(locks, root)}
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
        drift = _put_back_drift(goal, root, nodes)
        if drift:
            kept_lead.append(f"{drift}\n\n")
        open_ids = _steppable(open_ids, nodes)
        ready_ids = _steppable(ready_ids, nodes)
        left = _unfinished(nodes)
        cycle = _wait_cycle(nodes)
        dead = _dead_waits(nodes)
        if cycle:
            after = _cycle_break(cycle, nodes)
        elif dead:
            after = _dead_wait_drops(dead, nodes)
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
        stepped[:] = [task]
        abandon = str(arguments.get("abandon") or "").strip()
        if abandon:
            if not task:
                return _step_result("pursuit_step: abandon names the task to drop; pass task too.")
            done_by = _DONE_BY.match(abandon)
            roots = [str(n.get("id")) for n in nodes if not n.get("parent")]
            infeasible = _INFEASIBLE.match(abandon)
            if infeasible is not None:
                return _step_result(
                    _close_infeasible(task, infeasible.group(1).strip(), nodes, roots, root, goal)
                )
            if done_by is not None and task not in roots:
                return _step_result(
                    await _done_by(task, done_by.group(1).upper(), arguments, nodes, root)
                )
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
            stepped[:] = [task]
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
                return _step_result(_not_workable(task, nodes, open_ids + ready_ids, root))
            return _step_result(f"{task} is not a task to work now. {nothing_ready}")

        rc, out = _pursuit(["show", task], root)
        record = _json_reply(out) if rc == 0 else None
        if not isinstance(record, dict):
            return _step_result(f"pursuit_step: cannot read {task} (exit {rc}):\n{out}")
        title = str(record.get("title") or "")
        if _setup_milestone([title]) is not None:
            lead[:] = [_setup_lead(task)]
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
        opened = route = taken = ""
        retrying = False
        passed_on_disk: tuple[int, str] | None = None
        killed_run: tuple[int, str] | None = None
        hang = ""
        status = record.get("status")
        new_route = arguments.get("new_route") is True
        bound_check = str(record.get("done_when") or "").strip()
        data_route = (
            _data_test_route(bound_check, scope or _strings(record.get("scope")), root)
            if status == "open" and bound_check
            else None
        )
        # Run R18 #20 and #54: resending the data test tau suggested for an open
        # task superseded it with a successor the pre-run then refused. Without
        # new_route=true, an open task whose check is rewritten is amended; the
        # spawn is kept for an escalated one (ESCALATE_AFTER steps not done).
        amends_open = (
            not new_route
            and status == "open"
            and bool(done_when)
            and " ".join(done_when.split()) != " ".join(bound_check.split())
            and _NOT_DONE.get((str(root), task), 0) < ESCALATE_AFTER
        )
        if amends_open:
            if data_route is not None and " ".join(done_when.split()) == data_route[2]:
                done_when, scope = data_route[2], data_route[3]
            # Run R25 #5: the open bound the data test only, and resending its check,
            # cases test and all, amended to the cases test, which could not pass. A
            # resend whose unwritten import leaves the bound data test as it is keeps
            # the amend's refusal, which names that test.
            own = scope or _strings(record.get("scope"))
            data_only = _data_only_bind(done_when, own, root)
            if data_only is None:
                data_only = _data_only_bind(done_when, own, root, unwritten=True)
                if data_only is not None and data_only[0] == " ".join(bound_check.split()):
                    data_only = None
            if data_only is not None:
                done_when, scope, data_note = data_only
                route += data_note
        elif (
            not new_route
            and data_route is not None
            and " ".join(done_when.split()) == data_route[2]
        ):
            # Run R16 #15 sent the escalation's own data-test done_when without
            # new_route=true, and was refused eleven times until the breaker stopped it.
            test, module, done_when, scope = data_route
            new_route = True
            notes = notes or (
                f"Bind the data test only: {test} imports {module}, which a later task writes."
            )
            taken = (
                f"Took done_when=\"{done_when}\" as {task}'s new route without new_route=true: "
                f"it is the data test tau proposed, since the bound check runs {test}, which "
                f"imports {module} that no path in its scope creates. Scope: {json.dumps(scope)}."
                "\n\n"
            )
        if status == "blocked" or new_route:
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
                if done_when:
                    # Run R23 #10: open and amend bound a bare '&&' that this refused.
                    chained, prose = _and_chain(done_when)
                    if prose is not None or chained is None:
                        return _step_result(f"pursuit_step: no new route for {task} — {prose}")
                    taken += _bound_note(done_when, chained)
                    done_when = chained
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
                route_scope = scope or _strings(record.get("scope"))
                kept_check = (
                    _kept_data_check(done_when, route_scope, old_check, root)
                    if done_when and status == "open"
                    else None
                )
                if kept_check is not None:
                    # Run R32 #12: the notes went down with a done_when whose data
                    # test was the bound check already.
                    taken += kept_check
                    done_when = ""
                scoped = (
                    _scope_problem(route_scope, task, nodes, root)
                    or _locked_scope_problem(
                        route_scope, root, title, task, done_when or old_check
                    )
                    or _sibling_owned_check_problem(
                        done_when or old_check, route_scope, task, nodes, root
                    )
                    or _oracle_with_code_problem(route_scope, goal, task, done_when or old_check)
                    or _locked_test_problem(done_when or old_check, route_scope, goal)
                    or _import_scope_problem(done_when or old_check, route_scope, root)
                    or _pytest_node_missing_problem(done_when or old_check, route_scope, root)
                    or _pytest_node_import_only_problem(done_when or old_check, route_scope, root)
                ) or await _unwritten_check_problem(
                    done_when or old_check,
                    route_scope,
                    task,
                    root,
                    _strings(record.get("scope")),
                    bound=old_check,
                    locks=_pending_locks(goal, task) + _strings(arguments.get("locks")),
                    is_open=status == "open",
                )
                if scoped is not None:
                    return _step_result(f"pursuit_step: no new route for {task} — {scoped}")
                new_check = done_when or old_check
                rehearsed = await _run_check(new_check, root, DEFAULT_CHECK_TIMEOUT)
                if rehearsed[0] != 0 and _check_stopped(new_check, root) is not None:
                    # Run R30 #22: a -9 here fell through to the open, which ran the
                    # check to the cap a second time.
                    killed_run = rehearsed
                if rehearsed[0] == 0 and not (
                    await _passes_only_by_uncommitted(new_check, [route_scope], root)
                ):
                    return _step_result(
                        f"pursuit_step: no new route for {task}, which stays as it is — "
                        + _already_passes(new_check, task, _tree_nodes(root))
                    )
                successor, spawned = _spawn(task, record, notes, done_when, root)
                if successor is None:
                    return _step_result(
                        f"pursuit_step: `beagle pursuit spawn {task}` refused:\n{spawned}\n\n"
                        + (
                            _spawn_limit_offer(
                                task,
                                old_check,
                                _strings(record.get("scope")),
                                nodes,
                                f"{len(_retry_chain(task, nodes))} routes were tried and "
                                "beagle refuses another",
                            )
                            if _at_spawn_limit(task, nodes)
                            else "Say more specifically in notes how this route differs."
                        )
                    )
                route = f"{taken}{spawned}\n\n"
                spawns[:] = [(task, successor, spawned)]
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
        if (
            not route
            and tried >= ESCALATE_AFTER
            and not _judge_notes_rerun(task, arguments, record, root)
        ):
            return _step_result(
                _escalation(
                    task,
                    tried,
                    arguments,
                    record,
                    root,
                    await _offered_data_test_passes(arguments, record, root),
                    await _bound_check_fails(task, arguments, record, root),
                )
            )
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
            if done_when and not criteria:
                # Run R14 sent task and done_when without criteria three times and
                # got the next-task prompt back with no word of what was missing.
                return _step_result(
                    f"pursuit_step: {task} not opened — criteria is missing: say what will "
                    "be true when it is done, and call pursuit_step again with task, "
                    "criteria and done_when."
                )
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
            chained, prose = _and_chain(done_when)
            if prose is not None or chained is None:
                return _step_result(f"pursuit_step: {task} not opened — {prose}")
            route += _bound_note(done_when, chained)
            done_when = chained
            data_only = _data_only_bind(done_when, scope, root)
            if data_only is not None:
                # Run R24 #4: the cases test, not yet written, later imported a
                # module no path in this scope could hold.
                done_when, scope, data_note = data_only
                route += data_note
            if not scope and record.get("sibling_of"):
                # Run R18 #56: T0008, spawned with no scope, was refused "no scope given".
                scope = _predecessor_scope(record, root)

            async def scope_refusal(scope: list[str]) -> str | None:
                return (
                    _no_scope_problem(
                        scope,
                        root,
                        _pending_locks(goal, task) + _strings(arguments.get("locks")),
                        done_when,
                    )
                    or _scope_problem(scope, task, nodes, root)
                    or _locked_scope_problem(scope, root, title, task, done_when)
                    or _sibling_owned_check_problem(done_when, scope, task, nodes, root)
                    or _oracle_with_code_problem(scope, goal, task, done_when)
                    or _doc_only_check_problem(done_when, scope, task, root)
                    or _cases_first_problem(
                        scope, task, title, goal, nodes, _strings(arguments.get("locks"))
                    )
                    or _locked_test_problem(done_when, scope, goal)
                    or _import_scope_problem(done_when, scope, root)
                    or _pytest_node_missing_problem(done_when, scope, root)
                    or _pytest_node_import_only_problem(done_when, scope, root)
                ) or await _unwritten_check_problem(
                    done_when,
                    scope,
                    task,
                    root,
                    _predecessor_scope(record, root),
                    locks=_pending_locks(goal, task) + _strings(arguments.get("locks")),
                )

            rehomed = _rehomed_scope(scope, root)
            scoped = (
                _module_under_tests_problem(
                    scope, task, done_when, root, await scope_refusal(rehomed)
                )
                if rehomed is not None
                else await scope_refusal(scope)
            )
            if scoped is not None:
                return _step_result(f"pursuit_step: {task} not opened — {scoped}")
            # A check bound once it already passes closes the task on no work:
            # run 9 bound `cat docs/design.md` and a test an earlier task had
            # made pass. One that passes only on uncommitted files in this
            # task's scope (or its predecessor's) is the work, and the close
            # judges it.
            pre_rc, pre_out = killed_run or await _run_check(done_when, root, DEFAULT_CHECK_TIMEOUT)
            if pre_rc == 0 and await _passes_only_by_uncommitted(
                done_when, [scope, _predecessor_scope(record, root)], root
            ):
                route += _on_disk_note(done_when, task)
                passed_on_disk = (pre_rc, pre_out)
            elif pre_rc == 0:
                now = _tree_nodes(root)
                paths = scope or _check_targets(done_when, root)
                done_by = _done_task_in_log(paths, task, now, root)
                return _step_result(
                    f"pursuit_step: {task} not opened — "
                    + _already_passes(done_when, task, now, done_by)
                )
            broke = _check_broke(pre_rc, pre_out)
            if broke is not None:
                return _step_result(
                    f"pursuit_step: {task} not opened — the check could not run: `{broke}` "
                    f"(exit {pre_rc}). Correct the command and call pursuit_step again."
                )
            stopped = _check_stopped(done_when, root) if pre_rc != 0 else None
            own_hang = (
                _uncommitted_reach(done_when, [scope, _predecessor_scope(record, root)], root)
                if stopped is not None
                else []
            )
            killed = _killed_note(-9 if pre_rc in (-9, 137) else pre_rc, _memory_max())
            if stopped is not None and own_hang:
                # Run R30: killed at the cap on the chain's own uncommitted code,
                # the check says that code does not finish, and finding why is the
                # work; refused, the open deadlocked the driver for 51 minutes.
                hang = _hang_note(own_hang, stopped)
                route += hang
            elif killed:
                # R22: beagle's open rehearses the check again, and a second
                # run past the cap outlived the open's timeout.
                call = _killed_open_call(task, done_when, scope, notes, root)
                _KILLED_NOT_OPENED[str(_resolved(root))] = (task, call)
                return _step_result(
                    f"pursuit_step: {task} not opened — the check was killed before it "
                    f"finished (exit {pre_rc}). {killed} It runs no uncommitted code in "
                    f"{task}'s scope or its predecessor's, so no work here can make it "
                    f"finish, and opening would run it again. Call {call}."
                )
            argv = ["open", task, "--criteria", criteria, "--done-when", done_when]
            if scope:
                argv += ["--scope", *scope]
            budget = str(arguments.get("budget") or "").strip()
            if budget:
                argv += ["--budget", budget]
            rc, opened = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
            if rc != 0:
                return _step_result(
                    f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{opened}"
                )
            if _KILLED_NOT_OPENED.get(str(_resolved(root)), ("",))[0] == task:
                del _KILLED_NOT_OPENED[str(_resolved(root))]
            rc, out = _pursuit(["show", task], root)
            record = _json_reply(out) if rc == 0 else record
        elif (
            done_when
            and notes
            and done_when != bound_check
            and (
                kept_check := _kept_data_check(
                    done_when, scope or _strings(record.get("scope")), bound_check, root
                )
            )
            is not None
            and _locked_scope_problem(scope or _strings(record.get("scope")), root, title, task)
            is None
        ):
            # Run R32 #12: an open task's notes were refused with a done_when whose
            # data test was the bound check already; the bound check stays and the
            # notes run. Without notes, the refusal below says to leave done_when out.
            route += kept_check
            done_when = bound_check
        elif done_when and done_when != str(record.get("done_when") or "").strip():
            # Open already, with a check the model now writes differently: the
            # bound one could not judge the work (prose, a usage error), and
            # repeating the old one forever is the loop this breaks.
            chained, prose = _and_chain(done_when)
            if prose is not None or chained is None:
                if (
                    prose is not None
                    and "has a bare" in prose
                    and bound_check
                    and _check_problem(bound_check) is None
                ):
                    # Run R17 #23-#25 were told to name a new test in scope; the
                    # bound check was one valid command all along.
                    prose += (
                        f" The bound check `{bound_check}` stands: it is one valid "
                        "command; leave done_when out to keep it."
                    )
                return _step_result(f"pursuit_step: {task}'s check not changed — {prose}")
            route += _bound_note(done_when, chained)
            done_when = chained
            amend_problem = _amend_problem(
                done_when,
                bound_check,
                _pending_locks(goal, task) + _strings(arguments.get("locks")),
                root,
            )
            if amend_problem is not None:
                return _step_result(f"pursuit_step: {task}'s check not changed — {amend_problem}")
            own_scope = scope or _strings(record.get("scope"))
            unwritten = (
                _locked_scope_problem(own_scope, root, title, task, done_when)
                or _sibling_owned_check_problem(done_when, own_scope, task, nodes, root)
                or _pytest_node_missing_problem(done_when, own_scope, root)
                or _pytest_node_import_only_problem(done_when, own_scope, root)
            ) or (
                await _unwritten_check_problem(
                    done_when,
                    own_scope,
                    task,
                    root,
                    _predecessor_scope(record, root),
                    bound=bound_check,
                    locks=_pending_locks(goal, task) + _strings(arguments.get("locks")),
                    is_open=True,
                )
            )
            if unwritten is not None:
                return _step_result(f"pursuit_step: {task}'s check not changed — {unwritten}")
            pre_rc, pre_out = await _run_check(done_when, root, DEFAULT_CHECK_TIMEOUT)
            if pre_rc == 0 and await _passes_only_by_uncommitted(
                done_when, [own_scope, _predecessor_scope(record, root)], root
            ):
                # Run R18: the T0151 refusal had the open's blind spot.
                route += _on_disk_note(done_when, task)
            elif pre_rc == 0:
                keep = (
                    f" Keep the bound check `{bound_check}`: leave done_when out to keep it."
                    if bound_check and _check_problem(bound_check) is None
                    else ""
                )
                return _step_result(
                    f"pursuit_step: {task}'s check not changed — `{done_when}` already passes "
                    f"before any work, so it would close {task} on no work.{keep}"
                )
            broke = _check_broke(pre_rc, pre_out)
            if broke is not None:
                return _step_result(
                    f"pursuit_step: {task}'s check not changed — the check could not run: "
                    f"`{broke}` (exit {pre_rc}). Correct the command and call pursuit_step again."
                )
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
            # Run R23 #11: the old check's unproven mark refused the new check as
            # already passing. `beagle pursuit amend` takes no --scope, so the
            # record keeps its scope and this step runs on the call's.
            _UNPROVEN.discard((str(root), task))
            _LAST_CHECK_EXIT.pop((str(root), task), None)
            _LAST_CHECK_FAILURE.pop((str(root), task), None)
            kept = _strings(record.get("scope"))
            route += f"{task}'s check is now `{done_when}`, run on scope {json.dumps(own_scope)}"
            route += (
                f"; its record keeps scope {json.dumps(kept)}.\n\n"
                if scope and kept and list(scope) != kept
                else ".\n\n"
            )
        elif not retrying and data_route is not None:
            # Run R16 resent T0002 and T0010 on such a check (#5, #6, #12, #13): the
            # open check had passed only because the test was not written yet.
            problem = _imports_unwritten_problem(
                bound_check, scope or _strings(record.get("scope")), root
            )
            data_check = data_route[2]
            on_disk = await _data_route_on_disk(
                task,
                data_route,
                root,
                _predecessor_scope(record, root),
                bound=bound_check,
                locks=_pending_locks(goal, task) + _strings(arguments.get("locks")),
                is_open=True,
            )
            if on_disk is not None:
                return _step_result(f"pursuit_step: {task} not run — {on_disk}")
            return _step_result(
                f"pursuit_step: {task} not run — its bound check `{bound_check}` cannot pass: "
                f"{problem}"
                f' Sent as pursuit_step task="{task}", done_when="{data_check}", it is taken '
                "as this task's new route."
            )
        check = str(record.get("done_when") or done_when).strip()
        prose = _check_problem(check) if check else None
        if prose is not None:
            # Bound before this guard, or by hand: no worker can make it pass.
            return _step_result(
                f"pursuit_step: {task} is open, but its bound check `{check}` cannot pass "
                f"whatever the work does — {prose} Pass the corrected done_when with "
                f'task="{task}"; it is amended.'
            )
        if status == "open" and not new_route and not _strings(record.get("scope")):
            # Run R22: six workers ran on T0018, opened with scope [], and
            # rewrote files no task of theirs held.
            targets = _check_targets(check, root) if check else []
            call = f"pursuit_step task={json.dumps(task)}, new_route=true"
            supply = ["notes, saying what the new route does differently"]
            if targets:
                call += f", scope={json.dumps(targets)}"
            else:
                supply.insert(0, "scope, the paths the work changes")
            return _not_done(
                root,
                task,
                [],
                f"pursuit_step: {task} not run — it is open with no scope, so a sub-agent "
                "could change any file and nothing would hold the change to this task. Give "
                f"it a new route that names its files: {call}. Add to it: "
                + "; ".join(supply)
                + ".",
                ran=False,
            )
        if status == "open" and not new_route and not amends_open and scope:
            # Run R34 #22: an open task's call scope held the locked files, passed
            # unchecked, and W6 and W7 spent 11 min on edits that were put back.
            locked_scope = _locked_scope_problem(scope, root, title, task)
            if locked_scope is not None:
                return _step_result(f"pursuit_step: {task} not run — {locked_scope}")

        if retrying:
            # beagle briefs only an open task; a blocked one is briefed from its record.
            brief = _blocked_brief(task, record)
        else:
            rc, brief = _pursuit(["brief", task], root)
            if rc != 0:
                return _step_result(f"pursuit_step: `beagle pursuit brief {task}` failed:\n{brief}")
            brief = _without_beagle_habits(
                _without_commit_steps(brief),
                _command_bound(_memory_max(), _worker_timeout(arguments.get("timeout"))[0]),
            )
        references = _references_brief(
            root,
            _data_task(
                scope or _strings(record.get("scope")),
                goal,
                check,
                _pending_locks(goal, task) + _strings(arguments.get("locks")),
            ),
        )
        if references:
            brief = f"{brief}\n\n{references}"
        brief += _last_close_note((str(root), task))
        if notes:
            brief = f"{brief}\n\nFrom the driver (who has not read the reference):\n{notes}"
        if hang:
            brief = f"{brief}\n\n{hang.rstrip()}"
        brief += "\n\n" + NO_BEAGLE_NOTE + "\n\n" + _turn_cap_note()
        held = set(_locked(goal))
        asked = [e for e in _strings(arguments.get("locks")) if os.path.normpath(e) not in held]
        locks = _pending_locks(goal, task, [e for e in asked if _lockable(e)])
        unlocked = [e for e in asked if not _lockable(e)]
        if unlocked:
            kept_lead.append(
                f"Not filed as locks: {', '.join(unlocked)} (only tests and data files "
                "are locked; code stays open to the task that writes it).\n\n"
            )
        # A known-answers fix may change the locked files in its scope; its
        # close locks them again from what it wrote.
        fixing = (
            _locked_in_scope(scope or _strings(record.get("scope")), goal)
            if _fixes_known_answers_in(title, scope or _strings(record.get("scope")), goal)
            else []
        )
        locked = [rel for rel in _locked(goal) if rel not in fixing]
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
        retry_note = _last_failure_note((str(root), task), check) if status == "open" else ""
        restored: set[str] = set()
        attempt = 0
        proof: _Proof | None = None
        cannot_pass: tuple[str, str, str, list[str]] | None = None
        scope = scope or _strings(record.get("scope"))
        unproven_key = (str(root), task)
        tests_only = _only_data_and_tests(scope)
        proof_note = _tests_only_proof_note(check, scope, root)
        self_import = _self_import_note(check, scope, root) if check else ""
        retry_note = self_import + retry_note
        missing_data = _missing_data(check, scope, root) if check else []
        mixed = _open_mixed_refusal(scope, goal, task, check)
        if mixed is not None:
            # Opened before this guard, or by hand: still no worker on it.
            # Run R31: the same refusal came back 49 times while only locks grew.
            refusal_key = (str(root), task)
            if _LAST_MIXED_REFUSAL.get(refusal_key) == (tuple(scope), mixed):
                mixed += (
                    " This is the same answer as last time for this scope: locks do not "
                    "change it; the scope, or deleting the flagged file, does."
                )
            else:
                _LAST_MIXED_REFUSAL[refusal_key] = (tuple(scope), mixed)
            return _step_result(f"pursuit_step: {task} not run — {mixed}")
        _LAST_MIXED_REFUSAL.pop((str(root), task), None)
        if unproven_key in _UNPROVEN:
            # Run R23: the breaker quotes only a result's first line; the call goes there.
            call = _unproven_call(task, check, scope, root, missing_data, nodes)
            if _at_spawn_limit(task, nodes):
                rebinds = (
                    "That call rebinds this task to the data file's test, so taking the "
                    "data file away proves the check and the task closes done; if it "
                    "cannot: "
                    if "abandon=" not in call
                    else ""
                )
                return _not_done(
                    root,
                    task,
                    scope,
                    f"pursuit_step: {task} not run — call instead: {call}.\n"
                    "This check already passes and cannot be shown to refuse, since no "
                    f"defect could be put back into a file in its scope "
                    f"({', '.join(scope) or 'none'}). {rebinds}"
                    + _spawn_limit_offer(task, check, scope, nodes),
                    ran=False,
                )
            if tests_only and missing_data:
                how = (
                    TESTS_ONLY_PROOF_NOTE
                    + f" The test it runs reads {', '.join(missing_data)}, outside this "
                    f"scope: the new route keeps its done_when, `{check}`, which passes, "
                    "and adds that file to its scope"
                )
            elif tests_only and _scope_has_data(scope):
                how = (
                    TESTS_ONLY_PROOF_NOTE
                    + " The new route's done_when runs that file's test and its scope "
                    "names the data file"
                )
            elif tests_only:
                how = (
                    TESTS_ONLY_MUTATE_NOTE
                    + " The new route's done_when runs the test that imports it"
                )
            else:
                how = (
                    "The new route's done_when imports the code this task tests and runs "
                    "it (e.g. `python3 -m pytest -q tests/test_<this task>.py`, a test "
                    "that imports the module), with that code's source file in scope"
                )
            return _not_done(
                root,
                task,
                scope,
                f"pursuit_step: {task} not run — call instead: {call}; or split it with "
                "pursuit_plan.\n"
                "This check already passes and cannot be "
                f"shown to refuse, since no defect could be put back into a file in its "
                f"scope ({', '.join(scope) or 'none'}). Another sub-agent would change "
                "nothing, whatever check or scope this task is sent with. "
                + how
                + ". Its notes say what the new route does differently.",
                ran=False,
            )
        if not (tests_only and _scope_has_data(scope)):
            brief += "\n\n" + WITNESS_NOTE
        elif not (
            _fixes_known_answers_in(title, scope or _strings(record.get("scope")), goal)
            and _check_imports_code(check, root)
        ):
            # Run R28: a fix task's check ran a test importing code, and the note
            # told W3 it imported none.
            brief += "\n\n" + _known_answers_note(check, scope, root)
        asked_scope = _strings(arguments.get("scope"))
        kept = _strings(record.get("scope"))
        if (
            status == "open"
            and not new_route
            and not amends_open
            and asked_scope
            and kept
            and {os.path.normpath(e) for e in asked_scope} != {os.path.normpath(e) for e in kept}
        ):
            # Run R24 #14: an unchanged done_when is not amended, and `beagle
            # pursuit amend` takes no --scope, so the call's scope went unsaid.
            kept_lead.insert(
                0,
                f"{task} is worked on this call's scope {json.dumps(scope)}; its record keeps "
                f"scope {json.dumps(kept)}, since the done_when is unchanged. To make the "
                f"call's scope {task}'s own: pursuit_step task=\"{task}\", new_route=true, "
                f"scope={json.dumps(asked_scope)}, done_when={json.dumps(check)}, "
                'notes="…".\n\n',
            )
        if retrying:
            # The work may have been done since, under another task.
            verdict = await _run_check(check, root, check_timeout)
            _note_check_run(unproven_key, check, verdict)
            if verdict[0] == 0:
                proof = await _prove(task, "", scope, root, check_timeout, locks)
        elif passed_on_disk is not None and check == done_when:
            # Run R20: T0007's check passed at open on T0003's leftovers, and W11
            # passed at turn 2 and spent 29 more: the work was done; prove and close.
            verdict = passed_on_disk
            _note_check_run(unproven_key, check, verdict)
            proof = await _prove(task, "", scope, root, check_timeout, locks)
            if proof is not None and (not proof.proven or proof.by_absent_source):
                if proof.proven:
                    proof = _Proof(proven=False, text=proof.text)
                attempts = 1
                retry_note = "\n\n" + ON_DISK_WITNESS_NOTE
        worker_ran = False
        unreported: list[tuple[int, _WorkerRun, list[str]]] = []
        for attempt in range(1, attempts + 1):
            if (
                verdict[0] == 0
                and (proof is None or proof.proven)
                and not _absent_locks(locks, root)
            ):
                break
            if on_update is not None:
                with contextlib.suppress(Exception):
                    on_update(_step_result(f"{task}: sub-agent attempt {attempt} of {attempts}"))
            run = await _run_worker(
                brief + retry_note, root, model, provider, timeout, signal, task, scope
            )
            worker_ran = True
            undone = _restore_locked(goal, root, fixing)
            restored.update(undone)
            if run.spent is not None:
                spent = (spent or 0) + run.spent
            if run.problem is not None:
                return _not_done(
                    root,
                    task,
                    scope,
                    _implementation_in_tests_lead(root, scope, check)
                    + f"pursuit_step: {task} stays open — {run.problem}\n\n"
                    + _killed_attempt_context(run, shown, verdict, check, root, scope)
                    + f'Call pursuit_step with task="{task}" to send it again.',
                )
            if run.unreported:
                unreported.append((attempt, run, _scope_changes(root, scope)))
            report, shown = run.report, _capped_report(run)
            # Run R17: W4, W9 and W11 claimed files they never wrote.
            missing = _report_missing_paths(report, root)
            if missing:
                shown = f"{shown}\n\n{missing.rstrip()}"
            helpers_left = _helpers_left_in_scope(root, scope, check)
            if helpers_left:
                shown = f"{shown}\n\n{helpers_left.rstrip()}"
            if not check:
                verdict = (0, "")
                break
            verdict = await _run_check(check, root, check_timeout)
            _note_check_run(unproven_key, check, verdict)
            if verdict[0] == 0:
                if _absent_locks(locks, root):
                    break
                proof = await _prove(task, report, scope, root, check_timeout, locks)
                if proof is None or proof.proven:
                    break
                if not proof.weak and not proof.ask_module:
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
                        else "Give that WITNESS block; its NEEDLE must occur exactly once "
                        "in that module."
                        if proof.ask_module
                        else "Give a WITNESS block whose NEEDLE occurs exactly once in a "
                        "source file you changed (not a test)."
                    )
                )
                continue
            retry_note = (
                f"\n\nAn earlier attempt reported back, but the check still fails (exit "
                f"{verdict[0]}). Its output ends:\n{verdict[1][-CHECK_TAIL_CHARS:]}\n"
            )
            cannot_pass = _data_test_route(check, scope, root)
            if cannot_pass is not None:
                # Run R16 sent W4, W6, W8, W10 and W12 after this was already known.
                break
            retry_note = _self_import_note(check, scope, root) + retry_note
            no_tests = _pytest_collected_none(verdict[0], check)
            if no_tests is not None:
                retry_note = f"\n\n{no_tests}" + retry_note
            retry_note += "Fix the work, not the check."
            if undone:
                retry_note += (
                    f" It also changed locked files ({', '.join(undone)}); they were put "
                    "back. Make the code pass them as they are."
                )
                if any(rel in verdict[1] for rel in undone):
                    retry_note += (
                        " If a locked test is itself wrong, say which and why in your "
                        "report: the driver can open a known-answers fix for it."
                    )
            if missing:
                retry_note += "\n\n" + missing.rstrip()
            notes = report.strip()
            preamble = len(notes) < PREAMBLE_REPORT_CHARS and not _REPORT_FILE_NAME.search(notes)
            if notes and not notes.startswith(NO_REPORT) and not preamble:
                # Run R15: W5 and W6 re-read both references from line 1, though
                # the reports before them (W2, W4) already held the semantics.
                cut = notes[:RETRY_REPORT_CHARS]
                retry_note += (
                    "\n\nAn earlier attempt read the references; its notes:\n"
                    + cut
                    + ("\n[... cut]" if len(cut) < len(notes) else "")
                    + "\nStart from these rather than reading the references again."
                )
        undid = (
            f"The sub-agent changed locked files ({', '.join(sorted(restored))}); they "
            "were put back before the check.\n\n"
            if restored
            else ""
        )
        failing_locked = [rel for rel in sorted(restored) if verdict[0] and rel in verdict[1]]
        if failing_locked:
            # Run R20: T0010 and T0011 had the locked test put back every check
            # and no route out when it was the test that was wrong.
            undid += _known_answers_fix_route(failing_locked[0], goal, task, title) + "\n\n"

        absent = _absent_locks(locks, root)
        if verdict[0] == 0 and absent:
            # Run R17: T0008 closed done and its lock became "Not locked:
            # tests/cases.json: not a file in the project".
            state = "stays blocked" if retrying else "stays open"
            named = ", ".join(lock.rstrip("/") for lock in absent)
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but {named}: it is "
                f"locked for this task and not written, so that is the work; the task "
                f"{state}, since a done close needs its locked files on disk.\n\n"
                f"Last report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying to write {named}.',
            )
        if check and verdict[0] != 0:
            state = "stays blocked" if retrying else "stays open"
            fix_check = (
                "pass a corrected done_when with notes saying what this route does "
                "differently; a new route is spawned with it."
                if retrying
                else "pass a corrected done_when too; it is amended."
            )
            if_wrong = (
                "the check itself is wrong — it says how it was called (a usage error, a "
                "file it treats as an argument) rather than what is missing — "
                f"{fix_check}"
            )
            missing = _missing_scoped_test(verdict[0], verdict[1], scope, root)
            if missing is not None:
                if_wrong = (
                    f"the check names {missing}: it is in the scope and not written, so "
                    "that is the work, not a wrong check."
                )
            if_line = f"If {if_wrong} "
            missing_lock = _missing_locked_file(verdict[1], locks, root)
            if missing_lock is not None:
                if_line = (
                    f"The check names {missing_lock}: it is locked for this task and not "
                    "written, so that is the work, not a wrong check. "
                )
            no_tests = _pytest_collected_none(verdict[0], check)
            if no_tests is not None:
                if_line = ""
            unpassable = ""
            on_disk = (
                await _data_route_on_disk(
                    task,
                    cannot_pass,
                    root,
                    bound=check,
                    locks=_pending_locks(goal, task) + _strings(arguments.get("locks")),
                    is_open=True,
                )
                if cannot_pass is not None
                else None
            )
            if on_disk is not None:
                unpassable = f"The check cannot pass. {on_disk}\n\n"
            elif cannot_pass is not None:
                test, module, data_check, needs = cannot_pass
                unpassable = (
                    f"The check cannot pass: {test} imports {module}, which no task in reach "
                    f"writes; amend done_when to `{data_check}`.{_scope_note(needs, scope)} "
                    f'Sent as pursuit_step task="{task}", done_when="{data_check}", it is '
                    "taken as this task's new route.\n\n"
                )
            return _not_done(
                root,
                task,
                scope,
                (f"{no_tests}\n\n" if no_tests else "")
                + unpassable
                + _cwd_relative_data_lead(verdict[1], scope, root)
                + f"{route}{undid}{task} — {title}: the check still fails after {attempt} "
                f"sub-agent run(s), so the task {state}.\n\n`{check}` exit {verdict[0]}:\n"
                f"{verdict[1][-CHECK_TAIL_CHARS:]}\n\n"
                + _implementation_in_tests_lead(root, scope, check)
                + _unreported_runs(unreported, attempt)
                + f"Last report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying what to fix. '
                + (
                    f"{if_line}If this route is wrong: "
                    + _spawn_limit_offer(task, check, scope, fresh)
                    if _at_spawn_limit(task, fresh := _tree_nodes(root))
                    else f"{if_line}If this route is wrong, pursuit_step with "
                    f'task="{task}", new_route=true and notes saying what to do instead.'
                ),
            )
        if proof is not None and not proof.proven:
            state = "stays blocked" if retrying else "stays open"
            held = _changed_locked_only(scope, goal, root)
            if held:
                proof_note = _locked_data_proof_note(held)
            # The new route the Next offers keeps this check only where the route's
            # open would not refuse it as already passing: one rule for both.
            keeps = (
                tests_only
                and missing_data
                and await _passes_only_by_uncommitted(check, [[*scope, *missing_data]], root)
            )
            fresh_check = (
                "a done_when that runs a new test file, e.g. `python3 -m pytest -q "
                f"tests/test_<this task>.py`, in scope: `{check}` passes on the committed "
                "files too, so a route on it is refused as already passing. "
            )
            why = (
                "the check passes even with a defect put back into the work, so it does "
                "not test what this task built"
                if proof.weak
                else "no WITNESS named a defect in the module the test imports"
                if proof.ask_module
                else "no defect could be put back to show the check can fail"
            )
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but {why}; the task "
                f"{state}, since a done close needs a check shown to refuse.\n\n"
                f"`prove` said:\n{proof.text}\n\n"
                + _implementation_in_tests_lead(root, scope, check)
                + f"Last report:\n{shown}\n\n"
                + (
                    f"Next: nothing in this scope ({', '.join(scope)}) is a module or "
                    "cases data, so no defect can be put back into it and no "
                    "route on it can close done. Fold its work into the task that writes "
                    f'the code or the known answers, then pursuit_step task="{task}", '
                    'abandon="folded into <that task>".'
                    if tests_only
                    and all(Path(rel.rstrip("/")).suffix not in {"", ".py"} for rel in scope)
                    and not _scope_holds_code_or_cases(scope, root)
                    else f'Next: pursuit_step with task="{task}" and notes saying what to '
                    f"fix. {proof_note}"
                    if tests_only and proof.weak
                    else f'Next: pursuit_step with task="{task}" and notes asking for a '
                    "WITNESS in the module the test imports, named above."
                    if proof.ask_module
                    else f'Next: pursuit_step with task="{task}" and a done_when that runs '
                    "a test of the behaviour itself, e.g. `python3 -m pytest -q "
                    "tests/test_<this task>.py`, with notes saying what that test must "
                    "check. A bare import or file-exists check cannot be shown to refuse."
                    if proof.weak
                    else f"Next: {_spawn_limit_offer(task, check, scope, fresh)}"
                    if _at_spawn_limit(task, fresh := _tree_nodes(root))
                    else f'Next: a new route, pursuit_step with task="{task}", '
                    "new_route=true, notes and "
                    + (
                        f"its done_when, `{check}`, which passes, kept. {proof_note}"
                        if keeps
                        else fresh_check + proof_note
                        if tests_only and (held or missing_data)
                        else f"a done_when that runs that file's test. {proof_note}"
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
            rel
            for rel in _changed_files(root)
            if _in_scope(rel, scope, root) and (root / rel).is_file()
        ]
        # Run R26: the gate counted tests/test_cases.py, which the bound check never
        # ran, and held a passing, proven known-answers task open five times.
        reach = _check_test_reach(check, root) if check else None
        misplaced = _implementation_in_tests(
            root, [rel for rel in changed if reach is None or rel in reach]
        )
        unrun_note = ""
        if (
            tests_only
            and verdict[0] == 0
            and proof is not None
            and proof.proven
            and not proof.by_absent_source
            and reach is not None
        ):
            unrun = _implementation_in_tests(root, [rel for rel in changed if rel not in reach])
            if unrun:
                unrun_note = (
                    "Note for the next task whose check runs these files: they define "
                    "implementation a test file should not hold, to move into the module "
                    "the test imports or delete:\n"
                    + "\n".join(f"- {where}" for where in unrun)
                    + "\n\n"
                )
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
                ran=worker_ran,
            )
        if not locks and _only_data_and_tests(changed):
            # Run R04: the driver passed no locks for its known-answers task.
            locks = changed
        if locks:
            locks = [*locks, *_cases_tests_beside_locks(root, goal, changed, locks)]
        # The data locked earlier counts: a cases test locked now must read it.
        judged = [*locks, *(rel for rel in _locked(goal) if _is_cases_data(rel))]
        judged = list(dict.fromkeys(judged))
        unread = _unread_cases(root, judged) if locks else None
        if unread:
            state = "stays blocked" if retrying else "stays open"
            test, data = unread
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but the task {state} "
                f"and nothing is locked: {test} does not read {data}, so the known answers "
                f"judge nothing: the sub-agent must make {test} load {data} and run every "
                "case in it against the code, with no hand-written asserts of its own."
                f"\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying {test} must load '
                f"{data} and run every case against the code.",
            )
        flawed = _cases_test_problem(root, judged) if locks else None
        if flawed:
            state = "stays blocked" if retrying else "stays open"
            test, problem = flawed
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but the task {state} "
                f"and nothing is locked: {test} {problem}, so the known answers could "
                "never judge the code: the sub-agent must make it look up only cases "
                "the data holds, compare the code's results with each case's expected "
                "value, and use each attribute one way."
                f"\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying {test} {problem}.',
            )
        unquoted = _unquoted_cases(root, locks) if locks else None
        if unquoted and unquoted[4]:
            state = "stays blocked" if retrying else "stays open"
            data, missing, total, named, _ = unquoted
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but the task {state} "
                f"and nothing is locked: {missing} of {total} cases in {data} have a source "
                "that does not give the case's expected result, so a wrong answer would be "
                f"locked as known: case {named[0]}'s source quotes its input or prose, not "
                "its expected result: quote the line that gives the result"
                + (f" (also {', '.join(named[1:])})" if named[1:] else "")
                + f". A source holds the result when it, or the line of {REFERENCES_DIR}/*.txt "
                "after the one it quotes, gives every value of it, as decimal, hex bytes or "
                "the string; a long sequence may be elided with `...` between its head "
                "and tail. Where the reference gives a different result, the case's "
                "expected value is wrong: change it to the reference's."
                f"\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying case {named[0]}\'s '
                f"source in {data} quotes its input, not its expected result: quote the line "
                "that gives the result, and make the expected value match it.",
            )
        if unquoted:
            state = "stays blocked" if retrying else "stays open"
            data, missing, total, named, _ = unquoted
            return _not_done(
                root,
                task,
                scope,
                f"{route}{undid}{task} — {title}: the check passes, but the task {state} "
                f"and nothing is locked: {missing} of {total} cases in {data} have no source "
                f"quoting {REFERENCES_DIR}/*.txt (e.g. {', '.join(named)}), so nothing ties "
                "them to the reference: the sub-agent must give each case a `source` that "
                f"copies, verbatim, at least {SOURCE_QUOTE_MIN_WORDS} words of a line of "
                f"{REFERENCES_DIR}/*.txt it comes from. A bare file:line, page number or URL "
                "is not a source."
                f"\n\nLast report:\n{shown}\n\n"
                f'Next: pursuit_step with task="{task}" and notes saying each case in {data} '
                f"must quote, verbatim, the line of {REFERENCES_DIR}/*.txt it comes from, "
                f"starting with {named[0]}.",
            )
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
            body = (unrun_note + report)[:CLOSE_BODY_CHARS] or "-"
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
        if rc == 0 and (locks or fixing):
            now, skipped = _lock(
                goal, root, [*locks, *(rel for rel in fixing if rel not in locks)], task, fixing
            )
            _drop_pending_locks(goal, task)
            if now:
                lock_note += (
                    f"Locked: {', '.join(now)}. No later sub-agent can change them; make "
                    "the later tasks' done_when run them.\n\n"
                )
            if skipped:
                lock_note += f"Not locked: {'; '.join(skipped)}.\n\n"
        superseded = _SUPERSEDED_REPORT_NOTE if rc == 0 and _report_claims_failure(shown) else ""
        return _step_result(
            f"{route}{task} — {title}: {state}.\n\n{committed}\n\n{closed}\n\n"
            f"{undid}{lock_note}{unrun_note}"
            f"{superseded}Sub-agent report:\n{shown}\n\n"
            "Next: call pursuit_step with no arguments for the next task."
        )

    async def execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        stepped.clear()
        spawns.clear()
        lead.clear()
        kept_lead.clear()
        result = await _execute(tool_call_id, arguments, signal, on_update)
        refusal = "".join(getattr(c, "text", "") for c in result.content)
        if lead and refusal.startswith("pursuit_step:"):
            # Run R19: the .beagle/ refusal came five times for setup T0002
            # and never said that founding was its work.
            result = _step_result(lead[0] + refusal)
        if kept_lead:
            text = "".join(getattr(c, "text", "") for c in result.content)
            result = _step_result("".join(kept_lead) + text)
        if spawns:
            result = _with_spawn_notice(result, *spawns[0])
        result = _with_note(result, _worker_timeout(arguments.get("timeout"))[1])
        if stepped and stepped[0]:
            text = "".join(getattr(c, "text", "") for c in result.content)
            _LAST_STEP_RESULT[stepped[0]] = text[-LAST_STEP_RESULT_CHARS:]
        return result

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
    # Run R16: W4, refused a copy into tests/, linked it there with os.symlink.
    r"""|os\.(?:symlink|link|makedirs|mkdir)\(|\.(?:symlink_to|hardlink_to|mkdir)\("""
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
            refused = _KILLED_NOT_OPENED.get(str(store.parent))
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        call = (
            "Call pursuit_step, with what you meant to change in its notes"
            if refused is None
            else f"{refused[0]} was last refused on a killed check, and the same call is "
            f"refused again; call {refused[1]}"
        )
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to {what} from the driving session: in a pursuit the work, and "
                f"its commits, are done by sub-agents. {call}; a sub-agent does it and the "
                "task's check decides. For work no task covers (a failing gate, a lint fix), "
                "add a task with pursuit_plan. Reading and running (tests, `ruff check` "
                "without `--fix`, `git status`) is fine."
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
        argv = _unwrapped(segment)
        segment = []
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


#: Runner options that take a value as the next word: `uv run --with pytest python ...`.
_RUNNER_VALUE_OPTIONS = frozenset(
    {
        "--with",
        "--with-editable",
        "--with-requirements",
        "--python",
        "-p",
        "--project",
        "--directory",
        "--extra",
        "--group",
        "--package",
        "--env-file",
        "--index",
    }
)


def _past_runner(argv: list[str]) -> list[str]:
    """`argv` past a `uv run`, `poetry run` or `pipenv run` prefix and its options."""
    if len(argv) < 2 or Path(argv[0]).name not in ("uv", "poetry", "pipenv") or argv[1] != "run":
        return argv
    args = argv[2:]
    while args and args[0].startswith("-"):
        if args[0] == "--":
            return args[1:]
        args = args[2:] if args[0] in _RUNNER_VALUE_OPTIONS else args[1:]
    return args


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


#: `ruff` options that take a value as the next word, so it is not read as a path.
_RUFF_VALUE_OPTIONS = frozenset(
    {
        "--config",
        "--select",
        "--ignore",
        "--extend-select",
        "--extend-ignore",
        "--fixable",
        "--unfixable",
        "--exclude",
        "--extend-exclude",
        "--per-file-ignores",
        "--line-length",
        "--target-version",
        "--output-format",
        "--stdin-filename",
        "--cache-dir",
        "--range",
    }
)


def _ruff_argv(argv: list[str]) -> list[str] | None:
    """`argv` from its `ruff` subcommand on, past `uv run`, `uvx` or `python -m`; else None."""
    args = argv
    if args and _named(args, "uv") and len(args) > 1 and args[1] == "run":
        args = args[2:]
        while args and args[0].startswith("-"):
            args = args[1:]
    elif args and Path(args[0]).name in ("uvx", "pipx"):
        args = args[2:] if len(args) > 1 and args[1] == "run" else args[1:]
    elif args and Path(args[0]).name.startswith("python") and args[1:3] == ["-m", "ruff"]:
        return args[3:]
    if not args or not _named(args, "ruff"):
        return None
    return args[1:]


def _ruff_rewrite_paths(argv: list[str]) -> tuple[str, list[str]] | None:
    """For a `ruff format` or `ruff check --fix` argv: (what it runs, its paths); else None."""
    args = _ruff_argv(argv)
    if not args:
        return None
    sub, rest = args[0], args[1:]
    if sub == "format":
        what = "ruff format"
    elif sub == "check" and {"--fix", "--fix-only"} & set(rest):
        what = "ruff check --fix"
    else:
        return None
    paths: list[str] = []
    skip = False
    for arg in rest:
        if skip:
            skip = False
        elif arg in _RUFF_VALUE_OPTIONS:
            skip = True
        elif not arg.startswith("-"):
            paths.append(arg)
    return what, paths


def _ruff_over_locked(command: str, cwd: Path, root: Path, locked: list[str]) -> str | None:
    """The `ruff` rewrite in `command` that reaches past named files to locked ones, or None.

    Run R14: W5 ran `uv run ruff format .` and `ruff check --fix .`, which
    rewrote the locked tests. Refused: no path, `.`, or a directory that holds
    a locked file. Named files pass; the scope guard holds those.
    """

    def match(argv: list[str]) -> str | None:
        found = _ruff_rewrite_paths(argv)
        if found is None:
            return None
        what, paths = found
        if not paths:
            return f"`{what}` with no path"
        for raw in paths:
            target = _resolved(cwd / raw)
            if target == root:
                return f"`{what} {raw}`"
            if target.is_dir() and any(target in (root / rel).parents for rel in locked):
                return f"`{what} {raw}`"
        return None

    return _bash_find(command, match)


#: Why a worker is kept from beagle and its store.
NO_BEAGLE_REASON = (
    "the brief already holds what the task needs; do the task. A worker does not "
    "inspect .beagle/ or run beagle: the session that sent you does that."
)
#: What a worker is told in its brief, to the same end.
NO_BEAGLE_NOTE = "Do not inspect .beagle/ or run beagle."
#: Programs that only show what a path holds: a worker reading `.beagle/` with one
#: is orienting, not working. A check script under it (`bash .beagle/checks/...`)
#: is run, not read, and passes.
_READERS = frozenset(
    {
        "cat", "ls", "head", "tail", "less", "more", "find", "tree", "grep", "rg", "wc",
        "stat", "sed", "awk", "gawk", "nl", "cut", "od", "xxd", "strings", "sort", "uniq",
    }
)  # fmt: skip
#: `git` subcommands that print what a path holds.
_GIT_READS = frozenset({"show", "cat-file", "diff", "grep", "blame"})
#: What an inline script does to read a file it names.
_SCRIPT_READS = re.compile(r"\bopen\(|\.read_(?:text|bytes)\(")
#: `git log` options that print each commit's diff.
_GIT_LOG_PATCH = frozenset({"-p", "-u", "--patch"})
#: The path an inline script opens or writes, as its source says it.
_SCRIPT_PATH = re.compile(
    r"""open\(\s*['"](?P<open>[^'"]+)['"]\s*,\s*['"][wax]"""
    r"""|Path\(\s*['"](?P<path>[^'"]+)['"]\s*\)\s*\.write_(?:text|bytes)\("""
    r"""|writeFileSync\(\s*['"](?P<node>[^'"]+)['"]"""
    r"""|os\.(?:makedirs|mkdir)\(\s*['"](?P<dir>[^'"]+)['"]"""
    r"""|Path\(\s*['"](?P<made>[^'"]+)['"]\s*\)\s*\.(?:mkdir|symlink_to|hardlink_to)\("""
)
#: A link an inline script makes, and what it points at, as its source says them.
_SCRIPT_LINK = re.compile(
    r"""os\.(?P<os>symlink|link)\(\s*['"](?P<source>[^'"]+)['"]\s*,\s*['"](?P<link>[^'"]+)['"]"""
    r"""|Path\(\s*['"](?P<path_link>[^'"]+)['"]\s*\)\s*\.(?P<to>symlink_to|hardlink_to)\("""
    r"""\s*['"](?P<path_source>[^'"]+)['"]"""
)
#: An inline script that hands a command to the shell.
_SCRIPT_SHELL = re.compile(r"""\bos\.(?:system|popen)\(|\bsubprocess\.\w+\(""")
#: The plain string literal a shell-out is called with, when it is one.
_SCRIPT_SHELL_ARG = re.compile(
    r"""\b(?:os\.(?:system|popen)|subprocess\.\w+)\(\s*"""
    r"""(?:r?(?P<q>['"])(?P<cmd>(?:[^'"\\]|\\.|(?!(?P=q))['"])*)(?P=q))?"""
)
#: A literal word that names a path: one with a directory or a file suffix.
_SCRIPT_PATH_WORD = re.compile(r"[\w.~-]*/[\w./~-]*|[\w~-][\w./~-]*\.\w+")
#: A string literal in a script's source.
_SCRIPT_LITERAL = re.compile(r"'([^'\n]*)'" r'|"([^"\n]*)"')


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
        if _script_reads_store(argv):
            return f"run `{' '.join(argv)}`"
        if _named(argv, "git") and _git_reads_store(argv[1:]):
            return f"run `{' '.join(argv)}`"
        return None

    found = _bash_find(command, match)
    if found is not None:
        return found
    # Run R31: W1, refused `cat .beagle/...` four times, printed both task
    # records with `python3 - <<'EOF'`; a heredoc body is not in the shell words.
    for opener, body in _split_heredocs(command)[1]:
        python = _bash_find(opener, lambda argv: argv[0] if _reads_stdin_script(argv) else None)
        if python is not None and _source_reads_store(body):
            return f"run a `{Path(python).name}` script fed by a heredoc that reads `.beagle/`"
    return None


def _reads_stdin_script(argv: list[str]) -> bool:
    """Whether `argv` is Python running the script on its stdin: `python3 -` or bare."""
    if argv[:2] == ["uv", "run"]:
        argv = argv[2:]
    if not argv or not Path(argv[0]).name.startswith("python"):
        return False
    words = [a for a in argv[1:] if not a.startswith("-") or a == "-"]
    return not words or words[0] == "-"


def _git_reads_store(args: list[str]) -> bool:
    """Whether `git <args>` prints a `.beagle/` file: `show`, `cat-file`, `diff`,
    `grep` or `blame` of one, or `log -p` over one.

    Run R15: W3 and W4, refused `cat .beagle/tree/T0002.md`, spent 11 and 13
    turns on `git show HEAD:.beagle/tree/T0002.md | grep ...` instead.
    """
    if not args or args[0] not in _GIT_READS | {"log"}:
        return False
    paths = [a.split(":", 1)[1] if ":" in a else a for a in args[1:] if not a.startswith("-")]
    if not any(p and _in_store(p) for p in paths):
        return False
    return args[0] in _GIT_READS or bool(_GIT_LOG_PATCH & set(args[1:]))


def _script_reads_store(argv: list[str]) -> bool:
    """Whether `argv` is an inline Python script that opens a `.beagle/` path it names.

    Audit 7: `python3 -c "print(open('.beagle/tree/T0002.md').read())"` read
    what `cat` of the same path is refused. Running a script file is not this.
    """
    if argv[:2] == ["uv", "run"]:
        argv = argv[2:]
    if not argv or not Path(argv[0]).name.startswith("python") or "-c" not in argv[1:-1]:
        return False
    return _source_reads_store(argv[argv.index("-c", 1) + 1])


def _source_reads_store(script: str) -> bool:
    """Whether Python source `script` opens a `.beagle/` path it names."""
    if not _SCRIPT_READS.search(script):
        return False
    return any(_in_store(a or b) for a, b in _SCRIPT_LITERAL.findall(script))


def _script_write_targets(command: str, cwd: Path) -> list[Path]:
    """The paths an inline script in `command` writes, as its source names them.

    Run R04: W9, refused a write to src/__init__.py, wrote it with
    `python3 -c "open('src/__init__.py','w').write(...)"`. A path the script
    does not spell out is not guessed at: the guard fails open on it.
    """
    found = [next(g for g in m.groups() if g is not None) for m in _SCRIPT_PATH.finditer(command)]
    found += [link for link, _ in _script_links(command, cwd)]
    targets = [Path(os.path.normpath(cwd / Path(p).expanduser())) for p in found]
    return targets + _script_shell_targets(command, cwd)


def _script_links(command: str, cwd: Path) -> list[tuple[Path, Path]]:
    """Each link an inline script makes, unresolved, with the path it points at.

    A symbolic link's relative target is read from the link's directory, a
    hard link's from `cwd`, as the calls themselves read them.
    """
    found: list[tuple[Path, Path]] = []
    for m in _SCRIPT_LINK.finditer(command):
        raw_link = m.group("link") or m.group("path_link")
        raw_source = m.group("source") or m.group("path_source")
        link = Path(os.path.normpath(cwd / Path(raw_link).expanduser()))
        symbolic = "symlink" in (m.group("os") or m.group("to") or "")
        base = link.parent if symbolic else cwd
        found.append((link, _resolved(base / Path(raw_source).expanduser())))
    return found


def _script_shell_targets(command: str, cwd: Path) -> list[Path]:
    """The paths a command an inline script runs through the shell writes.

    Run R12: W10, refused about ten writes to src/, deleted from it with
    `python3 -c "import os; os.system('sed -i ... src/x.py')"`. A shell-out
    called with a plain string is read as bash; one called with anything else
    (a list, a variable) stands for every path-like literal in the script.
    """
    tokens = _shell_tokens(command) or []
    sources = [command, *(t for t in tokens if _SCRIPT_SHELL.search(t))]
    found: list[Path] = []
    unreadable = False
    for source in sources:
        for m in _SCRIPT_SHELL_ARG.finditer(source):
            if m.group("cmd") is None:
                unreadable = True
                continue
            nested = _bash_write_targets(re.sub(r"\\(.)", r"\1", m.group("cmd")), cwd)
            if nested is None:
                unreadable = True
            else:
                found += nested
    if unreadable:
        for source in sources:
            for m in _SCRIPT_LITERAL.finditer(source):
                for word in (m.group(1) or m.group(2) or "").split():
                    if not _SCRIPT_PATH_WORD.fullmatch(word) or word.startswith("-"):
                        continue
                    found.append(Path(os.path.normpath(cwd / Path(word).expanduser())))
    return found


#: Path parts a worker reads its toolchain through, wherever that lives.
_TOOLCHAIN_PARTS = frozenset({"site-packages", "dist-packages", ".venv", "venv"})
#: Why a worker is kept out of the trees beside its project.
SIBLING_REASON = (
    "other trees beside the project are not this task's. Work from the brief "
    "and the project's own files."
)


def _beside(path: Path, root: Path) -> bool:
    """Whether `path`, resolved, lies under the project's parent directory but
    not under the project: another tree beside it.

    Run R16: W2 found and read an earlier run's implementation at
    ~/itc.r08/itc/src/. A virtualenv or site-packages there is the toolchain,
    not another tree, and is not beside the project.
    """
    path = _resolved(path)
    if root.parent not in path.parents or path == root or root in path.parents:
        return False
    if _TOOLCHAIN_PARTS & set(path.parts):
        return False
    below = [p for p in (path, *path.parents) if root.parent in p.parents]
    if any((p / "pyvenv.cfg").is_file() for p in below):
        return False  # a virtualenv under another name, such as beagle's own
    for prefix in (sys.prefix, os.environ.get("VIRTUAL_ENV")):
        env = _resolved(Path(prefix)) if prefix else None
        if env is not None and env in path.parents and env not in (root, *root.parents):
            return False
    return True


def _own_path(path: Path, root: Path) -> Path:
    """`path` with its directories resolved and its last part not followed,
    when that lies in the project; fully resolved otherwise.

    Run R16: W4 linked tests/interval_tree_clocks.py to /tmp, and W5's `rm`
    of it passed, judged by where the link points. A link in the project is
    the project's file.
    """
    own = _resolved(path.parent) / path.name if path.name else _resolved(path)
    return own if own == root or root in own.parents else _resolved(path)


def _sibling_read(tool: str, args: Mapping[str, Any], cwd: Path, root: Path) -> str | None:
    """The path a read or a reading command names beside the project, or None."""

    def beside(word: str) -> bool:
        try:
            return _beside(cwd / Path(word).expanduser(), root)
        except RuntimeError:  # `~user` with no such user
            return False

    if tool == "read":
        raw = str(args.get("path") or "")
        return raw if raw.strip() and beside(raw) else None
    if tool != "bash":
        return None

    def match(argv: list[str]) -> str | None:
        if Path(argv[0]).name not in _READERS:
            return None
        return next((a for a in argv[1:] if a and not a.startswith("-") and beside(a)), None)

    return _bash_find(str(args.get("command", "")), match)


def _worker_scope() -> tuple[str, tuple[str, ...]] | None:
    """The task and scope this worker was sent with, or None when it has no scope."""
    scope = tuple(
        line.strip() for line in os.environ.get(WORKER_SCOPE_ENV, "").splitlines() if line.strip()
    )
    if not scope:
        return None
    return os.environ.get(WORKER_TASK_ENV, "").strip() or "this task", scope


_SCRATCH_DIRS = frozenset({"tmp", "temp", "log", "logs", "scratch"})


#: Words in a file's name that mark a probe kept for the worker's own use.
_SCRATCH_WORDS = frozenset({"scratch", "explore", "exploration", "probe", "tmp", "temp"})


def _scratch_like(rel: Path) -> bool:
    """Whether a refused project path looks like scratch: a log or temp file, a
    hidden script, or a script whose name says it is a probe.

    Run R21: explore.py, scratch_ref.py and .verify_citations.py were told the
    implementation does not go under tests/, and W6 kept no derivation at all.
    """
    if rel.suffix in {".log", ".tmp"} or _SCRATCH_DIRS & {p.lower() for p in rel.parts}:
        return True
    if rel.name.startswith(".") and rel.suffix == ".py":
        return True
    return bool(_SCRATCH_WORDS & set(re.split(r"[^a-z0-9]+", rel.stem.lower())))


def _task_check(goal: Path, task: str) -> str:
    """The task's bound `done_when`, read from its record in the pursuit's tree; or ""."""
    try:
        text = (goal.parent / "tree" / f"{task}.md").read_text(encoding="utf-8")
        record = tomllib.loads(text.split("+++")[1])
    except (OSError, IndexError, ValueError):
        return ""
    return str(record.get("done_when") or "")


def _check_imports(check: str, root: Path, rel: Path) -> bool:
    """Whether a test the check runs imports the module at `rel`, looking one level
    into a shell script the check runs."""
    commands = [check]
    for script in re.findall(r"[\w./-]+\.sh\b", check):
        with contextlib.suppress(OSError, ValueError):
            commands += (root / script).read_text(encoding="utf-8").splitlines()
    wanted = rel.as_posix()
    for command in commands:
        for test in _check_test_files(command, root):
            for names in _test_imports(root / test):
                for name in names:
                    path = name.replace(".", "/")
                    if wanted in {
                        f"{base}{path}{end}"
                        for base in ("", "src/")
                        for end in (".py", "/__init__.py")
                    }:
                        return True
    return False


def _link_out(links: list[tuple[Path, Path]], root: Path) -> ToolCallHookResult | None:
    """The refusal for a link in the project that points out of it, or None.

    Run R16: W4 linked tests/interval_tree_clocks.py to /tmp, and the check
    imported a file the project does not hold.
    """
    for link, source in links:
        own = _own_path(link, root)
        if (own == root or root in own.parents) and not (source == root or root in source.parents):
            return ToolCallHookResult(
                block=True,
                reason=(
                    f"refusing to link {own.relative_to(root)} to {source}: a link in the "
                    "project to a file outside it is a file the project does not hold. "
                    "Write the file where it belongs, or report it as follow-up."
                ),
            )
    return None


def _ordinal(n: int) -> str:
    """`n` as "1st", "2nd", "3rd", "4th", "11th", "22nd"."""
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _truncated_call(arguments: Mapping[str, Any], earlier: int = 0) -> str | None:
    """Why a call whose arguments are only unparsed text is refused, or None.

    Run R21: W3's `write` calls were cut off mid-JSON and reached the tool as
    `{"_raw_arguments": ...}`; told "path must be a string", W3 rewrote the
    same 30k-character file four times. Run R27: told to write "a few hundred
    lines", W2 resent the same 10k characters four times; the budget is now
    in characters, and `earlier` (this worker's cut-off calls before this
    one) says from the second on that the same size is cut off again. Run R31:
    told to generate data with a script, W2 saved its generator in the scope.
    Run R33: told "parts of at most 13644 characters", W2 sent ~28k again; a
    part is now at most a quarter of the output limit, about one character per
    token, so it fits well inside a turn.
    """
    if set(arguments) != {"_raw_arguments"}:
        return None
    text = str(arguments["_raw_arguments"])
    try:
        json.loads(text)
    except ValueError as exc:
        error = str(exc)
    else:
        error = "not an object of named arguments"
    part = min(len(text) // 2, _worker_output_tokens())
    refusal = (
        f"{CUT_OFF_REFUSAL} after {len(text)} characters and are not valid JSON ({error}), "
        f"so nothing was written. Write it in parts of at most {part} characters, one "
        "write per part, appending: `write` the first part, then append the rest with "
        "`edit`, one call per part; data with a pattern is "
        "shorter to generate with a short script run inline by bash (`python3 - <<'EOF'` "
        "... `EOF`) or saved to a scratch path outside the project, never saved in scope."
    )
    if earlier:
        refusal += (
            f" This is the {_ordinal(earlier + 1)} call cut off at the output limit; "
            "the same size will be cut off again."
        )
    return refusal


def _reread_refusal(
    tool: str, arguments: Mapping[str, Any], cwd: Path, scope: tuple[str, ...], calls: int
) -> str | None:
    """Why a worker's read is refused once half its calls went with nothing written, or None.

    Run R33: W3 and W7 spent their calls re-reading references in short windows
    and wrote their file at the last call, or never ran the check. A read of a
    file in the scope still passes: a write may need it.
    """
    cap = _worker_max_turns()
    if tool != "read" or calls <= cap // 2:
        return None
    path = arguments.get("path")
    goal = _find_goal(cwd)
    if not isinstance(path, str) or not path or goal is None:
        return None
    root = _resolved(goal.parent.parent)
    target = _own_path(cwd / Path(path).expanduser(), root)
    if (target == root or root in target.parents) and _scope_hit(target, root, scope) is not None:
        return None
    return (
        f"refusing to read {path}: {calls - 1} of {cap} calls used and nothing written. "
        f"Write {', '.join(scope)} now; re-read only what a write needs."
    )


def make_worker_scope_guard() -> Any:
    """Build the `tool_call` guard that keeps a worker's writes inside its task's scope.

    The scope was recorded and not enforced: in run R02 a worker wrote
    `tests/` over .gitignore with two turns left, and the next three steps went
    to repairing it. A worker sent with a scope (`BEAGLE_TAU_WORKER_SCOPE`) may
    write in it, outside the project (/tmp), in beagle's store (the record guard
    has that) and `.git/beagle/` (the task's log). A link in the project is
    judged by its own path, and one an inline script makes may not point out
    of the project. A worker with no scope is not held. Any worker sent on a
    task is kept from reading the trees beside its project. Fails open.
    """

    cut_offs = 0
    calls = 0
    wrote = False

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        nonlocal cut_offs, calls, wrote
        calls += 1
        try:
            cwd = Path(context.cwd)
            arguments = event.arguments or {}
            cut_off = _truncated_call(arguments, cut_offs)
            if cut_off is not None:
                cut_offs += 1
                return ToolCallHookResult(block=True, reason=cut_off)
            sent_on_task = bool(os.environ.get(WORKER_TASK_ENV, "").strip())
            orientation = (
                _worker_orientation(event.tool_name, arguments, cwd) if sent_on_task else None
            )
            if orientation is not None:
                return ToolCallHookResult(
                    block=True,
                    reason=f"refusing to {orientation}: {NO_BEAGLE_REASON}",
                )
            home = _find_goal(cwd) if sent_on_task and event.tool_name in ("read", "bash") else None
            beside = (
                _sibling_read(event.tool_name, arguments, cwd, _resolved(home.parent.parent))
                if home is not None
                else None
            )
            if beside is not None:
                return ToolCallHookResult(
                    block=True, reason=f"refusing to read {beside}: {SIBLING_REASON}"
                )
            sent = _worker_scope()
            command = str(arguments.get("command", "")) if event.tool_name == "bash" else ""
            goal = _find_goal(cwd) if command and sent_on_task else None
            if goal is not None:
                root = _resolved(goal.parent.parent)
                ruff = _ruff_over_locked(command, cwd, root, _locked(goal))
                if ruff is not None:
                    files = ", ".join(sent[1]) if sent is not None else "the files you changed"
                    return ToolCallHookResult(
                        block=True,
                        reason=(
                            f"refusing {ruff}: it reaches the pursuit's locked tests, which "
                            f"no sub-agent may change. Name the files instead: {files}."
                        ),
                    )
            if sent is None:
                return None
            task, scope = sent
            reread = (
                None if wrote else _reread_refusal(event.tool_name, arguments, cwd, scope, calls)
            )
            if reread is not None:
                return ToolCallHookResult(block=True, reason=reread)
            script = _bash_find(command, _driver_change) if command else None
            scripted = (
                script is not None
                and script.startswith(_INTERPRETERS)
                and (_SCRIPT_WRITE.search(command) or _SCRIPT_SHELL.search(command)) is not None
            )
            targets = _write_targets(event.tool_name, arguments, cwd, resolve=False)
            links = _script_links(command, cwd) if scripted else []
            if scripted:
                targets += _script_write_targets(command, _cwd_after_cd(command, cwd))
            goal = _find_goal(cwd) if targets else None
            if goal is None:
                return None
            root = _resolved(goal.parent.parent)
            allowed = [_resolved(goal.parent), root / ".git" / "beagle"]
            hits = 0
            for target in targets:
                target = _own_path(target, root)
                if target != root and root not in target.parents:
                    continue  # outside the project: /tmp, /dev/null
                if any(target == a or a in target.parents for a in allowed):
                    continue
                if _CACHE_DIRS & set(target.parts):
                    continue
                if _scope_hit(target, root, scope) is None:
                    break
                hits += 1
            else:
                refused = _link_out(links, root)
                wrote = wrote or (hits > 0 and refused is None)
                return refused
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        rel = target.relative_to(root) if target != root else target
        source = (
            # Run R09: refused src/, W4 wrote the library to tests/itc/ instead.
            " The implementation does not go under tests/ either: it is a later "
            "task's work, so report it instead."
            if rel.suffix == ".py" and not _is_test_path(rel.as_posix())
            else ""
        )
        if _scratch_like(rel):
            return ToolCallHookResult(
                block=True,
                reason=(
                    f"refusing to write {rel}: it is outside {task}'s scope "
                    f"({', '.join(scope)}); name it in your report as follow-up. Scratch "
                    "files go in /tmp."
                ),
            )
        # Run R20: W1 and W2, refused the module, built it in /tmp, where it was lost.
        imported = ""
        needed = f", and report that {rel} is needed."
        with contextlib.suppress(Exception):
            bound = _task_check(goal, task)
            # Run R27 W4-W6: "the check imports cobs/__init__.py" kept the data test's
            # import that the self-import note said to remove.
            if _data_self_import(bound, scope, root):
                needed = "."
                imported = " " + _self_import_note(bound, scope, root).strip()
            elif _check_imports(bound, root, rel):
                imported = (
                    f" {task}'s check imports {rel}, so the check cannot pass while it is "
                    "outside the scope: say so in your report."
                )
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to write {rel}: it is outside {task}'s scope "
                f"({', '.join(scope)}). Work written outside {task}'s scope is not its work "
                f"and is lost when the step ends: do what the scope holds{needed}"
                f"{imported}{source}"
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
    "next": (
        "pursuit_step with no arguments, which picks the ready task and says what to send"
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
                "The tool runs it with the checks around it that the bare verb skips."
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
                f"it. Files inside the project, {REFERENCES_DIR}/ aside, are yours to read."
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
        LOCK_MANIFEST,
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
    global _SEEN_CWD, _STARTED_SESSION, _OFF_PURSUIT_CALLS, _FOUND_REFUSED_STATEMENT
    del event
    _SEEN_CWD = context.cwd
    _STARTED_SESSION = context.session_id
    _OFF_PURSUIT_CALLS = 0
    _FOUND_REFUSED_STATEMENT = None
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
    "references or design the solution first: the first milestone is the known "
    "answers, which a `pursuit_step` sub-agent does: it reads the reference and "
    "writes the cases file and its test. The design is part of the implementation, "
    "not a milestone of its own. Name the "
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
        nodes = _tree_nodes(root)
        ready_ids = _steppable(_ids(ready.get("ready")) if isinstance(ready, dict) else [], nodes)
        open_ids = _steppable(_ids(ready.get("open")) if isinstance(ready, dict) else [], nodes)
        if ready_ids:
            now = f"Ready now: {', '.join(ready_ids)}."
        elif open_ids:
            now = f"Open now: {', '.join(open_ids)}."
        else:
            now = "Nothing is ready now."
        tree = _tree(root)
        last = ""
        for task in ready_ids + open_ids:
            if task in _LAST_STEP_RESULT:
                last += f"\n\nLast pursuit_step on {task} said:\n{_LAST_STEP_RESULT[task]}"
        tau.send_custom_message(
            "The conversation was just compacted. Where the pursuit stands, from beagle "
            f"itself (trust this over the summary):\n\n{tree}\n\n{now} Next: call "
            "pursuit_step with no arguments. Work no task covers goes in with "
            f"pursuit_plan; this session does not do it itself.{last}",
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
                "designing and building are work for pursuit_step's sub-agents."
            ),
        )

    return gate


#: Non-`pursuit_` tool calls in a row the driver may make once the goal exists.
DRIVER_OFF_PURSUIT_CALLS = 8

_REDIRECT_TARGET = re.compile(r"(?<![<>=-])[0-9&]?>>?\|?\s*['\"]?([^\s;|&<>'\"]+)")
_SED_IN_PLACE = re.compile(r"\bsed\b(?=[^;|&\n]*\s(?:-[a-zA-Z]*i|--in-place))[^;|&\n]*\.beagle")
_PYTHON_INLINE = re.compile(r"\bpython[0-9.]*\b[^;|&\n]*(?:\s-c\b|<<)")


def _bash_writes_dot_beagle(command: str) -> bool:
    """Whether a shell command writes a `.beagle/` file, judged conservatively."""
    if ".beagle" not in command:
        return False
    if any(".beagle" in target for target in _REDIRECT_TARGET.findall(command)):
        return True
    if re.search(r"\btee\b[^;|&\n]*\.beagle", command) or _SED_IN_PLACE.search(command):
        return True
    if _PYTHON_INLINE.search(command) and re.search(r"open\(|write|toml", command):
        return True
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        if words and words[0] in ("cp", "mv"):
            operands = [w for w in words[1:] if not w.startswith("-")]
            if len(operands) >= 2 and ".beagle" in operands[-1]:
                return True
    return False


def _bash_runs_beagle_pursuit(command: str) -> bool:
    """Whether a shell command runs `beagle pursuit …`, judged by each segment's argv."""
    if "pursuit" not in command:
        return False
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        for i, word in enumerate(words[:-1]):
            if Path(word).name == "beagle" and words[i + 1] == "pursuit":
                return True
    return False


def make_driver_seat_gate() -> Any:
    """Build the `tool_call` gate that keeps the driver in the directing seat.

    Run R10's driver spent 53 calls after founding hand-editing `.beagle/*.toml`
    and broke gates.toml. The driver may not write `.beagle/` at all, and once
    the goal exists it may not go more than `DRIVER_OFF_PURSUIT_CALLS` calls in
    a row without a pursuit tool.
    """

    async def gate(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        global _OFF_PURSUIT_CALLS
        try:
            if _STARTED_SESSION is None or context.session_id != _STARTED_SESSION:
                return None
            tool = event.tool_name
            if tool.startswith("pursuit_"):
                _OFF_PURSUIT_CALLS = 0
                return None
            cwd = Path(context.cwd)
            args = event.arguments or {}
            writes = False
            if tool in ("write", "edit"):
                target = _goal_path_from_args(args, cwd)
                store = _resolved(cwd / ".beagle")
                writes = target is not None and (target == store or store in target.parents)
            elif tool == "bash":
                writes = _bash_writes_dot_beagle(str(args.get("command", "")))
            founded = _find_goal(cwd) is not None
            if writes and founded:
                return ToolCallHookResult(
                    block=True,
                    reason=(
                        f"refusing {tool}: the pursuit tools own .beagle/, and the driver "
                        "does not write it by hand. Work goes through pursuit_step; put what "
                        "you meant to change in its notes."
                    ),
                )
            # Run R26's driver wrote pursuit.toml by hand seven times before
            # founding, each time told to use pursuit_step, which needs a pursuit.
            # A `beagle pursuit` verb is refused only once `beagle init` made a
            # store: outside one, the project may not be a pursuit at all.
            stored = any((d / ".beagle").is_dir() for d in (cwd, *cwd.parents))
            if not founded and (
                writes
                or (
                    tool == "bash"
                    and stored
                    and _bash_runs_beagle_pursuit(str(args.get("command", "")))
                )
            ):
                return ToolCallHookResult(
                    block=True,
                    reason=(
                        f"refusing {tool}: the pursuit tools own .beagle/, and there is no "
                        "pursuit here yet. The pursuit begins with pursuit_found: call it "
                        "with the goal, its criteria and the milestones."
                    ),
                )
            if not founded:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        _OFF_PURSUIT_CALLS += 1
        if _OFF_PURSUIT_CALLS <= DRIVER_OFF_PURSUIT_CALLS:
            return None
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing {event.tool_name}: {_OFF_PURSUIT_CALLS} tool calls in a row without "
                f"a pursuit tool (the limit is {DRIVER_OFF_PURSUIT_CALLS}). The driver directs; "
                "call pursuit_step for the ready task, and the work runs there."
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
    "tests/cases.json is removed). That test reads only the data file, opened beside "
    "it: `Path(__file__).with_name('cases.json')`, not `open('cases.json')`, which "
    "looks in the working directory."
)

#: Said instead of TESTS_ONLY_PROOF_NOTE when the scope holds no data file. Run
#: R12: that note pointed T0008 at tests/cases.json, another task's locked file.
TESTS_ONLY_MUTATE_NOTE = (
    "This scope holds only tests, so mutate the module the test imports: a WITNESS "
    "in that module, a NEEDLE there that the test must catch."
)

CASES_FIRST_NOTE = (
    "Cases first. Make the first milestone after the reference the known answers: a "
    "sub-agent reads the reference and writes, without any implementation, (a) a data "
    "file of small inputs and the exact results the reference gives for them, each "
    "with a `source` quoting the reference's own words verbatim, at least four of them "
    "copied from a line of references/*.txt where the references are fetched there; a "
    "bare file:line or URL is not a source (e.g. `tests/cases.json`), and (b) "
    "a test that runs every case against the code (e.g. `tests/test_cases.py`). That "
    "test imports the module later tasks will write, by name (e.g. `from <package> "
    "import …`), and defines no class or helper of its own: it fails with ImportError "
    "until the code exists. Both tests load the data file beside them: load it as "
    "`Path(__file__).with_name('cases.json')`, since the check runs from the project "
    "root. Its done_when checks only the data, with a small "
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
        "anything: the first milestone is the known answers: a sub-agent reads the "
        "reference and writes the cases file and its test; the design is part of the "
        "implementation, not a milestone of its own. Your part is to steer, a few "
        "steps at a time.",
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
                    "says'). Returns the executor's report; the worker closes nothing. Once "
                    "a pursuit is founded this tool is refused: pursuit_step has the task done, "
                    "runs its check and closes it. Use for roughly ten tool calls or more of "
                    "mechanical work, not one-line edits or open-ended exploration."
                ),
                parameters=DISPATCH_PARAMETERS,
                execute_fn=make_dispatch(),
                prompt_snippet="Delegate one pursuit task to a headless step-executor sub-agent.",
                prompt_guidelines=(
                    "Hand pursuit_dispatch a self-contained brief; the worker sees no "
                    "conversation.",
                    "The worker does the work and closes nothing; in a founded pursuit, "
                    "pursuit_step runs the task's check and closes it.",
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
        tau.on("tool_call", make_driver_seat_gate())
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
