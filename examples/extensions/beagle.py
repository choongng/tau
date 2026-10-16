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
  target dir set with `--cwd`, and the worker's model chosen in order: the
  call's model/provider/thinking, the environment, the project's
  `.beagle/dispatch.toml` entry for the role (beagle hands Tau only entries
  with a Tau provider, never a Claude Code alias), else the session's live
  model, provider and thinking level (a `/model` switch mid-session included).
  The file's `model_rules` follow each result, for the driver to choose by.
  `pursuit_step` and its audit choose the same way. Because the worker is
  Tau too, the ground-truth guard stays live inside it — a sub-agent is not a
  way around it.
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
  result while one stands names the `beagle loop tick` that releases it.
- **ended drivers** — workers and the wakeup end with the Tau session that
  started them, so a run whose driver session has ended is stopped at the
  next session start (`beagle loop stop`), and the next `/pursuit-run` is
  told where the cancelled worker's partial work is. Each session records
  its pid under the Tau home, since beagle trusts no Tau pid.
- **orientation** — the driver's system prompt holds how to work a pursuit,
  fixed at load: a project with no pursuit yet also gets how to found one
  (the CLI is already on PATH, founding goes through `pursuit_found`). It
  holds no pursuit state, so it stays true when a pursuit is founded
  mid-session, and the prompt prefix never changes. The state (goal,
  criteria, task tree, ready tasks) comes from beagle as a message: in
  `pursuit_found`'s result, at the first run of each session (with Beagle's
  `loop-report` SessionStart hook output), and after each compaction. A
  worker's prompt carries the goal and criteria: its session never outlives
  the pursuit's founding.
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
import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import tomllib
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tau_agent.messages import REASONING_LOOP_CUT, REASONING_TIME_CUT, TextContent
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
from tau_coding.provider_config import (
    load_provider_settings,
    provider_model_max_tokens,
    resolve_provider_selection,
)
from tau_coding.resources import parse_markdown_resource
from tau_coding.session import MAX_OUTPUT_LIMIT_CONTINUATIONS, MAX_TIME_CUT_CONTINUATIONS
from tau_coding.skills import Skill, format_skill_invocation
from tau_coding.tool_buffers import WINDOW_LINES, read_request
from tau_coding.tools import BASH_TIMEOUT_ENV_VAR

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
#: Seconds a worker's turn may reason before its first tool call; tau then cuts
#: the turn and asks it to act (TAU_TURN_REASONING_SECONDS). S04-S06 (q35): one
#: worker turn in each run reasoned to the 16k output limit, about 11 min, over
#: values one `python3 -c` settles; 95% of turns reasoned under 2k tokens.
WORKER_REASONING_SECONDS = 240.0
#: The cases worker's budget. R128 (q35 wrenfold): its three cases workers took
#: 7.6, 6.1 and 7+ of the run's 30 min against ~3 per code worker; the long turns
#: had the test file drafted in their first quarter and re-drafted it to 240 s.
#: Replayed with that turn cut at 120 s, the nudge's reply wrote the whole file
#: in 4 of 4 samples within 17 s; cut at 60 s, in 2 of 3.
CASES_REASONING_SECONDS = 120.0
TURN_REASONING_ENV = "TAU_TURN_REASONING_SECONDS"
#: Maximal turns (the model's max_tokens each) the worker wall holds at the decode
#: rate measured on earlier workers, when that is longer than the default. q38fn
#: 10-11: at ~20 tok/s and max_tokens 16384 one turn took 650-850 s, and 5 of 9
#: workers were killed at 900 s.
WALL_MAXIMAL_TURNS = 3
#: Output tokens measured before a decode rate sizes the wall.
DECODE_MIN_TOKENS = 1000
#: How the tool descriptions say the wall grows past the default.
WALL_DESCRIPTION = (
    f"or longer once earlier sub-agents measured the model's decode rate: {WALL_MAXIMAL_TURNS} "
    "turns at its output limit"
)

#: Pin the worker's model/provider for every dispatch without editing code.
#: Left unset, the project's `.beagle/dispatch.toml` entry for the role decides
#: (`_dispatch_pin`), and without one the worker runs the driver session's live
#: provider/model, read off the context of the session's last tool call — not
#: tau's configured default, which a `/model` switch does not change (run
#: itc-35b-test: the driver switched to the 35B, and its workers came up on the
#: catalog default). Beagle's Claude tier names like `sonnet` are not Tau
#: catalog ids; beagle hands Tau only the entries with a provider of its own.
WORKER_MODEL_ENV = "BEAGLE_TAU_DISPATCH_MODEL"
WORKER_PROVIDER_ENV = "BEAGLE_TAU_DISPATCH_PROVIDER"

#: Turns a worker gets before it is told to stop and report (`tau --max-turns`).
#: R01's 9B workers ran 43 and 51 turns into the kill and handed back nothing;
#: a turn cap ends the run with a report instead.
#: R94: 3 of 7 contract workers ended at a 30-turn cap mid-edit while the
#: worker's wall clock (~900 s) already bounds it, so the cap is 60.
WORKER_MAX_TURNS_ENV = "BEAGLE_TAU_WORKER_MAX_TURNS"
DEFAULT_WORKER_MAX_TURNS = 60

#: The worker's output limit in tokens, which sizes the parts a call cut off at
#: it is told to write in. Runs R15 and R33 were cut off at 8192.
WORKER_OUTPUT_TOKENS_ENV = "BEAGLE_TAU_WORKER_OUTPUT_TOKENS"
DEFAULT_WORKER_OUTPUT_TOKENS = 8192

#: Seconds a worker's bash command runs when the call names no `timeout`, passed
#: to the worker's tau as its bash default. Run R34: W2's inline encoder never
#: ended and held tau's 600 s default, 10 of its 13 minutes.
WORKER_BASH_TIMEOUT_ENV = "BEAGLE_TAU_WORKER_BASH_TIMEOUT"
DEFAULT_WORKER_BASH_TIMEOUT = 120.0

#: The worker's thinking level. Unset, a worker on the session's own model runs
#: the session's level, and one on a pinned model runs thinking off, since most
#: of R01's worker time went to reasoning spirals. `default` is tau's own level
#: for "the catalog's thinking_default, else the server's", the one level tau
#: takes for every model: a model with no thinking modes rejects every other
#: level, `off` included, and a worker spawn that passes one then exits 2 before
#: reading a token (trial T01, qwen3.8-flash-next-iq4 with no thinking metadata)
#: — so an inherited level is sent only when the session's model lists it, and
#: `default` is never swapped for `off` after a reasoning cut-off.
WORKER_THINKING_ENV = "BEAGLE_TAU_DISPATCH_THINKING"
WORKER_THINKING_DEFAULT = "default"
#: `_worker_thinking`'s answer for "send no `--thinking`".
WORKER_THINKING_OMIT = ""
#: Every level a worker may be started with: tau's `--thinking` choices.
WORKER_THINKING_LEVELS = (
    WORKER_THINKING_DEFAULT,
    "off",
    "minimal",
    "low",
    "medium",
    "high",
    "xhigh",
    "max",
)

#: The `.beagle/dispatch.toml` roles a worker runs as: a task's work, and the
#: audit, which is a review that did not write the work.
EXECUTOR_ROLE = "executor"
REVIEWER_ROLE = "reviewer"
DISPATCH_CONFIG_REL = Path(".beagle") / "dispatch.toml"

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
#: The role a `pursuit_step` worker was sent in: `EXECUTOR_ROLE` for the task's
#: work, `CASES_ROLE` for the worker that writes a spec-tied task's cases before
#: it opens. Only the cases worker may run `beagle pursuit open … --dry-run`.
WORKER_ROLE_ENV = "BEAGLE_TAU_WORKER_ROLE"
#: beagle 0.48's `pursuit rules 2e`: a task built from a source has its cases
#: written, before the code, by "a worker that will not write the code". Its
#: model is the executor's pin: `.beagle/dispatch.toml` has no role for it.
CASES_ROLE = "cases"

#: R0002's lean arm: set (to anything but "" or "0"), the mechanisms that caught
#: nothing across the q35 runs do not fire: known-answers locks, the plan guards,
#: abandon and done-by gating, the escalation demand, the audit cadence, the
#: own-copy rule, the already-passes refusal, cases-first and the worker's read
#: guards. Read at call time, so the driver and its workers, which inherit the
#: environment, agree; set at launch and never changed within a session.
LEAN_ENV = "BEAGLE_TAU_LEAN"
#: What founding adds to the goal file under lean (see `_lean`).
LEAN_AUDIT_OFF = "\n[audit]\nevery = 0\n"

#: Where founding puts the references the user's prompt links to, as text.
REFERENCES_DIR = "references"

#: How a milestone's `source` is kept in its beagle task record: the last words
#: of its intent, so a restarted session reads it back from `pursuit show`.
SOURCE_LEAD = "Source:"
_SOURCE_IN_INTENT = re.compile(r"(?:^|\s)Source:\s*(\S.*?)\s*$")
#: A source that names none. Run R121 (lfm24, bare-goal semver): every milestone
#: came with "source": "N/A", and T0002's cases workers wrote cases from it.
_NO_SOURCE = re.compile(
    r"(?i)^(?:n/?a|none|null|nil|tbd|unknown|not applicable|no source|[-\u2013\u2014]+)\.?$"
)
#: A `beagle-case:` marker and its `cite=`, as `pursuit rules 2e` spells it.
_CASE_CITE = re.compile(r"beagle-case:\s*\S+.*?\bcite=(\S+)")


def _lean() -> bool:
    """Whether `LEAN_ENV` is on: set to anything but "" or "0"."""
    return os.environ.get(LEAN_ENV, "") not in ("", "0")


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
#: What `beagle hook loop-report` said at load, for each session's state note.
_LOOP_REPORT = ""
#: Sessions already told where the pursuit stands, at their start or founding.
_STATE_NOTED: set[str] = set()


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
    quote = ""
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
        openers, quote = _heredoc_openers(line, quote)
        pending += [(m.group(3), bool(m.group(1)), line, []) for m in openers]
    return "\n".join(kept), bodies


def _heredoc_openers(line: str, quote: str) -> tuple[list[re.Match[str]], str]:
    """The `<<WORD` openers in `line` that stand outside quotes, and the quote
    still open at its end; `quote` is the one open at its start.

    Run R28: in a `bash -c 'cat > f << "EOF"` whose script goes on for more
    lines, the `<<` is inside the script's quotes, so those lines are still the
    script, not a body: dropping them left the quote unclosed and the command
    unreadable.
    """
    found: list[re.Match[str]] = []
    i = 0
    while i < len(line):
        c = line[i]
        if quote:
            if c == "\\" and quote == '"':
                i += 1
            elif c == quote:
                quote = ""
        elif c == "\\":
            i += 1
        elif c in "'\"":
            quote = c
        elif c == "#" and (i == 0 or line[i - 1] in " \t;&|("):
            break  # a comment runs to the end of the line
        elif (m := _HEREDOC.match(line, i)) is not None:
            found.append(m)
            i = m.end()
            continue
        i += 1
    return found, quote


def _shell_tokens(command: str) -> list[str] | None:
    """Shell words and operators, heredoc bodies dropped; None if unparseable."""
    # A newline ends a command only outside quotes: inside a `bash -c '...'`
    # script it is the script's own, and its heredocs need it kept.
    lines = _strip_heredocs(command).replace("\\\n", " ").split("\n")
    text, quote = lines[0], _heredoc_openers(lines[0], "")[1]
    for line in lines[1:]:
        text += ("\n" if quote else " ; ") + line
        quote = _heredoc_openers(line, quote)[1]
    lexer = shlex.shlex(_word_hashes_literal(text), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:  # an unclosed quote: not a command this can read
        return None


def _word_hashes_literal(text: str) -> str:
    """`text` with each `#` inside a word escaped, as bash reads it.

    shlex starts a comment at any `#`; bash only at a word's start. A cite's
    anchor, `spec:2#ff4`, cut the cases worker's `open --dry-run` at its first
    cite (T0601).
    """
    out: list[str] = []
    quote = ""
    escaped = False
    for at, char in enumerate(text):
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            quote = "" if char == quote else quote
        elif char in "'\"":
            quote = char
        elif char == "#" and at and not text[at - 1].isspace() and text[at - 1] not in "();<>|&":
            out.append("\\")
        out.append(char)
    return "".join(out)


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
        # Record cwd and model for the dispatch tool, which receives no context.
        with contextlib.suppress(Exception):  # a stale/retired generation, ignore
            _SEEN_CWD = context.cwd
        _record_session_model(context)

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
class _SessionModel:
    """The driver session's live model, for the worker spawns (which get no context)."""

    provider: str
    model: str
    thinking: str
    #: The thinking modes `model` supports; None when this tau cannot say.
    thinking_levels: tuple[str, ...] | None


#: The session model last seen on a context: a `/model` switch is picked up at
#: the next tool call, which is always before the dispatch that call makes.
_SEEN_MODEL: _SessionModel | None = None


def _record_session_model(context: Any) -> None:
    """Keep the context's live model for the worker spawns; never raises."""
    global _SEEN_MODEL
    try:
        provider, model = str(context.provider_name), str(context.model)
        thinking = str(context.thinking_level)
    except Exception:  # noqa: BLE001 - a retired generation or an unbound runtime
        return
    try:
        levels: tuple[str, ...] | None = tuple(context.available_thinking_levels)
    except Exception:  # noqa: BLE001 - a tau too old to list them
        levels = None
    if provider and model:
        _SEEN_MODEL = _SessionModel(provider, model, thinking, levels)


@dataclass(frozen=True)
class _DispatchPin:
    """A role's model in `.beagle/dispatch.toml` for this host, and the project's rules.

    Empty `model` means the file pins nothing Tau can run for the role, so the
    worker inherits. `rules` is the project's own prose for choosing a model per
    dispatch, which the driver follows by passing model/provider/thinking.
    """

    provider: str = ""
    model: str = ""
    thinking: str = ""
    rules: str = ""


def _dispatch_pin(role: str, root: Path) -> _DispatchPin:
    """`beagle dispatch model --for <role> --json` as Tau's host; never raises.

    Beagle filters the entries by host, so a `claude-code` alias like `opus` is
    never handed to a Tau worker. No file is the default install and costs no
    subprocess; a beagle too old for `--json`, or a file it refuses, inherits.
    """
    if not (root / DISPATCH_CONFIG_REL).is_file():
        return _DispatchPin()
    cmd = [BEAGLE_BIN, "dispatch", "model", "--for", role, "--json", "--host", "tau"]
    rc, out = _run(cmd, root, timeout=30.0)
    said = _json_reply(out) if rc == 0 else None
    if not isinstance(said, dict):
        return _DispatchPin()
    fields = {key: str(said.get(key) or "").strip() for key in ("provider", "model", "thinking")}
    if said.get("inherit") or not fields["model"]:
        fields = {}
    return _DispatchPin(**fields, rules=str(said.get("rules") or "").strip())


def _rules_note(pin: _DispatchPin, tool: str) -> str:
    """The project's model rules, for a result the driver reads; "" when none."""
    if not pin.rules:
        return ""
    return (
        f"\n\nThis project's model rules ({DISPATCH_CONFIG_REL}) win over its pinned "
        f"line when one fits a task: follow one by passing model, provider and thinking "
        f"to {tool}.\n{pin.rules}"
    )


@dataclass(frozen=True)
class _AwaitedScope:
    """What the driver session is waiting on, and the open tasks' scope."""

    awaiting: str
    tasks: tuple[str, ...]
    scope: tuple[str, ...]
    #: The `beagle loop tick` that releases the wait (`_live_wait`).
    release: str = "beagle loop tick --clear-awaiting"


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


#: Where the extension logs what it read past in beagle's output, one JSON line each.
BEAGLE_LOG_NAME = "beagle-extension.jsonl"
#: Where a JSON reply may start: `{` or `[` opening a line, as json.dumps prints one.
_JSON_LINE_START = re.compile(r"^[{\[]", re.MULTILINE)


def _log_beagle_remainder(argv: list[str], remainder: str) -> None:
    """Append what `beagle <argv>` printed besides its JSON to Tau's diagnostic log."""
    entry = {"at": datetime.now(UTC).isoformat(), "argv": argv, "remainder": remainder}
    with contextlib.suppress(OSError, ValueError):
        logs = TauPaths().logs_dir
        logs.mkdir(parents=True, exist_ok=True)
        with (logs / BEAGLE_LOG_NAME).open("a", encoding="utf-8") as log:
            log.write(json.dumps(entry) + "\n")


def _json_out(argv: list[str], root: Path) -> Any:
    """The JSON `beagle <argv>` prints, or None when it fails or prints none.

    The output holds stderr too, and beagle 0.48 adds lines around its JSON: a
    `next: <move>` last (on stderr after a refusal), notes and warnings. The JSON
    is read from the first line opening with `{` or `[` that parses, as
    `_json_reply` reads a reply, and whatever else was printed is logged
    (`BEAGLE_LOG_NAME`), not taken as a failed read: a strict parse here read
    every such reply as None, and an awaited worker's scope as empty.
    """
    rc, out = _run([BEAGLE_BIN, *argv, "--root", str(root)], root, HOOK_TIMEOUT)
    if rc != 0:
        return None
    for opened in _JSON_LINE_START.finditer(out):
        start = opened.start()
        try:
            value, end = json.JSONDecoder().raw_decode(out[start:])
        except ValueError:
            continue  # a note's `[T0003]`, not the reply
        remainder = (out[:start] + out[start + end :]).strip()
        if remainder:
            _log_beagle_remainder(argv, remainder)
        return value
    if out.strip():
        _log_beagle_remainder(argv, out.strip())
    return None


def _live_wait(root: Path, session_id: str) -> tuple[str, str] | None:
    """What this session's run declares it is awaiting, while a lease holds, and
    the `beagle loop tick` that releases it.

    None unless a run is in flight, this session is its recorded driver (a
    subagent's own session never is), and a declared wait is in its lease.
    0.48 keeps the unnamed wait (`--awaiting`, released by `--clear-awaiting`)
    beside named ones (`--wait-id`, each released by `--clear-wait ID`), and a
    bare tick releases neither.
    """
    record = _json_out(["loop", "read", "--json"], root)
    if not isinstance(record, dict):
        return None
    if not session_id or record.get("driver_session") != session_id:
        return None
    live: list[tuple[str, str]] = []
    if record.get("awaiting") and _lease_live(record):
        live.append((str(record["awaiting"]), "beagle loop tick --clear-awaiting"))
    for wait in record.get("waits") or ():
        if isinstance(wait, dict) and wait.get("awaiting") and wait.get("id") and _lease_live(wait):
            live.append((str(wait["awaiting"]), f"beagle loop tick --clear-wait {wait['id']}"))
    if not live:
        return None
    if len(live) == 1:
        return live[0][0], f"`{live[0][1]}`"
    awaiting = '", "'.join(what for what, _ in live)
    return awaiting, ", ".join(f'`{release}` for "{what}"' for what, release in live)


def _read_awaited_scope(root: Path, session_id: str) -> _AwaitedScope | None:
    """The scope this session's run is waiting on a worker in, or None.

    None without a live wait (`_live_wait`). The scope is every open task's:
    `awaiting` is free text, so which open task the worker holds cannot be
    read off it reliably.
    """
    wait = _live_wait(root, session_id)
    if wait is None:
        return None
    awaiting, release = wait
    listing = _json_out(["pursuit", "tree", "--json", "--status", "open"], root)
    tasks = [row["id"] for row in listing or () if isinstance(row, dict) and row.get("id")]
    scope: list[str] = []
    for task in tasks:
        node = _json_out(["pursuit", "show", str(task)], root)
        entries = node.get("scope") if isinstance(node, dict) else None
        scope += [e for e in entries or () if isinstance(e, str) and e.strip()]
    if not scope:
        return None
    return _AwaitedScope(awaiting, tuple(tasks), tuple(scope), release)


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
                "and take the task back; if the worker is gone, release its wait first: "
                f"{waiting.release}."
            ),
        )

    return scope_guard


#: Appended to a `stop_subagent` result while this session's run declares a wait.
STOPPED_WORKER_NOTE = """

beagle: this session's pursuit run still declares it is awaiting \
"{awaiting}". If that was the worker just stopped, nothing will arrive to \
release it: release it now with {release} (a bare `beagle loop tick` does \
not), then take the task back or dispatch it again."""


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
            wait = await asyncio.to_thread(_live_wait, root, session)
            if wait is None:
                return None
            awaiting, release = wait
            text = event.result.text + STOPPED_WORKER_NOTE.format(
                awaiting=awaiting, release=release
            )
        except Exception:  # noqa: BLE001 - fail open; a note must not break the tool
            return None
        return ToolResultHookResult(content=text)

    return note


# --------------------------------------------------------------------------- #
# dispatch tool: the headless step-executor
# --------------------------------------------------------------------------- #


def _worker_target(
    model: Any = None, provider: Any = None, pin: _DispatchPin | None = None
) -> tuple[str, str]:
    """The worker's (model, provider): explicit args, else env, else the project's
    dispatch.toml pin, else the session's.

    Either one named, by argument or env, keeps the pin's and the session's pair
    out of it: a provider under another model may not serve it. Nothing named and
    no session seen gives ('', ''), which leaves both to tau's configured default.
    """

    def named(explicit: Any, env: str) -> str:
        if isinstance(explicit, str) and explicit.strip():
            return explicit.strip()
        return os.environ.get(env, "").strip()

    model, provider = named(model, WORKER_MODEL_ENV), named(provider, WORKER_PROVIDER_ENV)
    if model or provider:
        return model, provider
    if pin is not None and pin.model:
        return pin.model, pin.provider
    if _SEEN_MODEL is None:
        return model, provider
    return _SEEN_MODEL.model, _SEEN_MODEL.provider


def _worker_thinking(
    model: str, provider: str, explicit: Any = None, pin: _DispatchPin | None = None
) -> str:
    """The worker's thinking level, or WORKER_THINKING_OMIT to send no flag.

    An explicit level wins, then the env, then the dispatch.toml pin's when the
    worker runs the pin's model. Otherwise a worker on the session's own model
    runs the session's level when that model lists it, and no flag when it lists
    none (T01); a worker on any other model runs thinking off (R01).
    """
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    pinned = os.environ.get(WORKER_THINKING_ENV, "").strip()
    if pinned:
        return pinned
    if pin is not None and pin.thinking and (model, provider) == (pin.model, pin.provider):
        return pin.thinking
    seen = _SEEN_MODEL
    if seen is None or (model, provider) != (seen.model, seen.provider):
        return "off"
    if seen.thinking_levels is not None and seen.thinking in seen.thinking_levels:
        return seen.thinking
    return WORKER_THINKING_OMIT


def _bad_thinking(raw: Any) -> str:
    """Why a tool call's thinking level cannot start a worker; "" when it can."""
    if raw is None or (isinstance(raw, str) and raw.strip() in ("", *WORKER_THINKING_LEVELS)):
        return ""
    return f"thinking {raw!r} is not one of {', '.join(WORKER_THINKING_LEVELS)}."


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


def _worker_bash_timeout() -> float:
    """The worker's bash default timeout: env, else DEFAULT_WORKER_BASH_TIMEOUT."""
    raw = os.environ.get(WORKER_BASH_TIMEOUT_ENV, "").strip()
    try:
        value = float(raw) if raw else DEFAULT_WORKER_BASH_TIMEOUT
    except ValueError:
        return DEFAULT_WORKER_BASH_TIMEOUT
    return value if value > 0 else DEFAULT_WORKER_BASH_TIMEOUT


def _worker_timeout(raw: Any, wall: float = DEFAULT_DISPATCH_TIMEOUT) -> tuple[float, str]:
    """A model-supplied worker timeout, clamped to `wall` (`_worker_wall`), its default.

    Returns the timeout and a note for the tool result, empty unless clamped.
    A longer wall clock bought R01 only a longer spiral; the turn cap is what
    ends a worker with a report.
    """
    try:
        asked = float(raw or wall)
    except (TypeError, ValueError):
        return wall, ""
    if asked <= 0:
        return wall, ""
    if asked > wall:
        return wall, (
            f"(timeout {asked:.0f}s was clamped to {wall:.0f}s, the most a "
            "worker gets; split a task that needs longer.)"
        )
    return asked, ""


#: Worker decode measured this session, by (project root, provider, model): output
#: tokens and the milliseconds after each turn's first output, so a long prompt
#: read does not count as slow decoding.
_DECODE: dict[tuple[str, str, str], tuple[int, int]] = {}


def _decode_key(root: Path, model: str, provider: str) -> tuple[str, str, str]:
    return str(_resolved(root)), provider, model


def _model_max_tokens(model: str, provider: str) -> int | None:
    """The catalog's output limit for the worker's model, or None when tau has none."""
    try:
        selection = resolve_provider_selection(
            load_provider_settings(), provider_name=provider or None, model=model or None
        )
        return provider_model_max_tokens(selection.provider, selection.model)
    except Exception:  # noqa: BLE001 - an unknown model or unreadable settings: no limit known
        return None


def _decode_rate(root: Path, model: str, provider: str) -> float | None:
    """Output tokens per second measured on earlier workers, once there are enough."""
    tokens, ms = _DECODE.get(_decode_key(root, model, provider), (0, 0))
    if tokens < DECODE_MIN_TOKENS or ms <= 0:
        return None
    return tokens * 1000 / ms


def _worker_wall(root: Path, model: str, provider: str) -> float:
    """A worker's default and largest wall clock: DEFAULT_DISPATCH_TIMEOUT, or
    WALL_MAXIMAL_TURNS turns of the model's max_tokens at the measured decode
    rate when that is longer.

    q38fn 10-11: 5 of 9 workers were killed at 900 s at ~20 tok/s with
    max_tokens 16384, one of them in a single 818 s turn.
    """
    rate = _decode_rate(root, model, provider)
    max_tokens = _model_max_tokens(model, provider) if rate else None
    if not rate or not max_tokens:
        return DEFAULT_DISPATCH_TIMEOUT
    return max(DEFAULT_DISPATCH_TIMEOUT, float(math.ceil(WALL_MAXIMAL_TURNS * max_tokens / rate)))


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
    #: A run killed at its wall: what it said last, as (kind, text), for the step result.
    said_last: tuple[str, str] = ("", "")
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
#: How much of a worker killed at its wall's last words the step result shows;
#: the next brief keeps the longer _WORKER_TAIL_CHARS.
KILLED_WORDS_CHARS = 600


#: How tau's repeat breaker words a refused call's tool result, and the stop.
_REFUSED = "Not run: "
_BREAKER_STOP = "Not run, and the run is stopped"
#: How the refusal of a call cut off at the output limit begins (`_truncated_call`).
CUT_OFF_REFUSAL = "This call's arguments were cut off"
#: The turns over a run cut off at the output limit that end the worker. q35
#: R91: a worker was ended at its second, two 16384-token turns of hand-tracing
#: an encoder, when the reply after a cut-off can act on its reasoning (tau
#: replays it).
WORKER_CUT_OFFS = 3
CUT_OFF_ENDED = f"cut off {WORKER_CUT_OFFS} times at the output limit"
#: How a kill note and the next worker's note say reasoning alone filled the limit.
REASONING_FILLED = "its reasoning filled the output limit before any reply or call"
#: What filled a cut-off turn: reasoning with no reply or call, reply text with no
#: call, or a call's arguments.
CUT_THINKING, CUT_REPLY, CUT_CALL = "thinking", "reply", "call"
REPLY_FILLED = "its reply text filled the output limit before any call"
NOTHING_FILLED = "the output limit came before any reply or call"
#: The kill note's advice when no call was cut off. Run R43: W13 spent two turns
#: on reply text with no call and was told to write in parts, which the driver
#: passed on to the next worker's notes. q35 R56: W3 made 9 calls between its
#: two cut-offs, so a worker that made calls gets only the last sentence.
NO_CALL_CUT_ONLY = "No call was cut off, so writing in smaller pieces would not help."
NO_CALL_CUT = (
    "It spent its turns reasoning in prose without acting: the next notes should say "
    f"what to do first. {NO_CALL_CUT_ONLY}"
)
#: The task whose last worker was ended on reasoning-only cut-offs, by project
#: root: its next worker runs thinking-off, once. Run R41: W1-W6 each spent two
#: 8192-token turns reasoning and were ended with nothing to report.
_THINKING_OFF_NEXT: dict[str, str] = {}
#: How tau words the tool result of a call an extension blocked.
_BLOCKED = "Tool call blocked: "
#: The countdown sentence tau appends to each refusal's problem.
_REFUSAL_COUNTDOWN = re.compile(r"\s*\d+ more refused calls? in a row stop the run\.\s*$")


def _blocks(message: Mapping[str, Any]) -> list[dict[str, Any]]:
    content = message.get("content")
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def _said(blocks: list[dict[str, Any]]) -> tuple[str, str]:
    """A message's text and its thinking, each joined and stripped."""

    def joined(kind: str) -> str:
        return "\n".join(str(b.get(kind, "")) for b in blocks if b.get("type") == kind).strip()

    return joined("text"), joined("thinking")


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
    #: How many of those turns were reasoning only: no text and no tool call (R41).
    reasoning_cut_offs: int = 0
    #: What filled each cut-off turn, in order: CUT_THINKING, CUT_REPLY or CUT_CALL.
    cut_fills: list[str] = field(default_factory=list)
    #: The milliseconds the cut-off turns took, as tau timed them: the wall does
    #: not count them (q35 R91: two 16384-token turns took 10 of a 15 min wall).
    cut_ms: int = 0
    #: How many tool calls its turns made, over the whole run (q35 R56).
    calls: int = 0
    #: Output tokens, and the milliseconds after each turn's first output: its decode.
    decode_tokens: int = 0
    decode_ms: int = 0
    #: The last assistant message's text, else its thinking, and which it was.
    said: tuple[str, str] = ("", "")
    #: The count before the last turn, and whether that turn was counted as cut off.
    _before_turn: int = 0
    _turn_cut: bool = False
    #: The last turn's milliseconds, as tau timed it.
    _turn_ms: int = 0
    #: The last `message_update` line since the last message ended: the turn in flight.
    _in_flight: bytes = b""

    def feed(self, line: bytes) -> None:
        if b'"message_update"' in line[:64]:
            self._in_flight = line
            return
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
        self._in_flight = b""
        usage = message.get("usage")
        total = usage.get("totalTokens") if isinstance(usage, dict) else None
        if isinstance(total, int):
            # Each request re-sends the conversation, so a sum counts the start
            # of the run once per turn. The largest request is what the run
            # held at its peak, which is how Claude Code reports a subagent.
            self.spent = max(self.spent or 0, total)
        timing = message.get("timing")
        self._note_decode(usage, timing)
        took = timing.get("totalDurationMs") if isinstance(timing, dict) else None
        self._turn_ms = took if isinstance(took, int) and took > 0 else 0
        blocks = _blocks(message)
        text, self.thinking = _said(blocks)
        if text:
            self.report = text
        if text or self.thinking:
            self.said = ("reply text", text) if text else ("reasoning", self.thinking)
        calls = [block for block in blocks if block.get("type") == "toolCall"]
        self.calls += len(calls)
        arguments = calls[-1].get("arguments") if calls else None
        command = arguments.get("command") if isinstance(arguments, dict) else None
        self.pending_command = (
            command if isinstance(command, str) else str(calls[-1].get("name", "")) if calls else ""
        )
        stop = message.get("stopReason")
        self.stop_reason = stop if isinstance(stop, str) else None
        self._before_turn = self.length_stops
        self._turn_cut = stop == "length"
        self.length_stops = self._before_turn + 1 if self._turn_cut else 0
        self.cut_offs += self._turn_cut
        self.cut_ms += self._turn_ms if self._turn_cut else 0
        self.reasoning_cut_offs += self._turn_cut and bool(self.thinking) and not (text or calls)
        if self._turn_cut:
            self.cut_fills.append(CUT_CALL if calls else CUT_REPLY if text else CUT_THINKING)
        error = message.get("errorMessage")
        self.error = str(error) if stop == "error" and error else None

    def _note_decode(self, usage: object, timing: object) -> None:
        output = usage.get("output") if isinstance(usage, dict) else None
        if not isinstance(output, int) or output <= 0 or not isinstance(timing, dict):
            return
        total, first = timing.get("totalDurationMs"), timing.get("timeToFirstOutputMs") or 0
        if isinstance(total, int) and isinstance(first, int) and total > first:
            self.decode_tokens += output
            self.decode_ms += total - first

    def last_said(self) -> tuple[str, str]:
        """What the run said last, as (kind, text): its turn in flight, else its last message.

        q38fn 10-11: a worker killed at the wall lost its turn in flight, ~7 min of
        reasoning that only its `message_update` events held.
        """
        try:
            event = json.loads(self._in_flight) if self._in_flight else None
        except ValueError:
            event = None
        message = event.get("message") if isinstance(event, dict) else None
        if isinstance(message, dict):
            text, thinking = _said(_blocks(message))
            if text or thinking:
                return ("reply text", text) if text else ("reasoning", thinking)
        return self.said

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
        if text.removeprefix(_BLOCKED).startswith(CUT_OFF_REFUSAL):
            if self._turn_cut:
                self.cut_fills[-1:] = [CUT_CALL]
            else:
                self._turn_cut = True
                self.length_stops = self._before_turn + 1
                self.cut_offs += 1
                self.cut_ms += self._turn_ms
                self.cut_fills.append(CUT_CALL)
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


#: A tool call written out as text, which a turn-capped worker can end on: the
#: angle form (`<tool_call><function=…>`) and the pipe-delimited form, whose
#: call and channel tokens ended Run R36's worker descriptions and founding
#: statement (`<tool_call|><|channel>thought…<|tool_call>call:bash{…`). q35 R55:
#: W9's reports were calls with closing tags only, the function a bare tag
#: (`<read>\n<parameter=path>…</parameter>\n</function>\n</tool_call>`); the
#: close is tau core's TEMPLATE_TOOL_CALL_TOKEN's, and the bare tag cuts there.
_TOOL_CALL_MARKUP = re.compile(
    r"<tool_call>|<function=|<\|(?:tool_call|channel)>|<(?:tool_call|channel)\|>"
    r"|<[\w.-]+>\s*<parameter=|</function>\s*</tool_call>"
)


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


def _record_decode(cwd: Path, model: str, provider: str, events: _WorkerEvents) -> None:
    """Add a worker's measured decode to `_DECODE`, for `_worker_wall`."""
    if events.decode_tokens <= 0 or events.decode_ms <= 0:
        return
    key = _decode_key(cwd, model, provider)
    tokens, ms = _DECODE.get(key, (0, 0))
    _DECODE[key] = (tokens + events.decode_tokens, ms + events.decode_ms)


#: What a worker killed at its wall left, by (project root, task): the brief
#: note for the task's next worker (`_killed_progress`), taken by its next step.
_KILLED_PROGRESS: dict[tuple[str, str], str] = {}


def _killed_progress(events: _WorkerEvents, cwd: Path, scope: list[str], timeout: float) -> str:
    """The next attempt's brief note from a worker killed at its wall: the tail of
    what it said last and the uncommitted files in its scope; "" when it left neither.

    q38fn 10-11: the driver copied a killed worker's partial reasoning into the
    notes by hand, and the worker after it finished in 4 min.
    """
    kind, said = events.last_said()
    files = [rel for rel in _changed_files(cwd) if _in_scope(rel, scope, cwd)]
    if not said and not files:
        return ""
    lines = [
        f"\n\nThe last sub-agent on this task was killed at its {timeout:.0f}s wall before "
        "it reported. Continue from where it stopped rather than starting over."
    ]
    if said:
        tail = said[-_WORKER_TAIL_CHARS:]
        cut = "[...] " if len(tail) < len(said) else ""
        lines.append(f"Its last {kind}, the end of it:\n{cut}{tail}")
    if files:
        lines.append("Uncommitted in its scope: " + ", ".join(files))
    return "\n".join(lines)


def _wall_problem(
    timeout: float, events: _WorkerEvents, task: str, cwd: Path, model: str, provider: str
) -> str:
    """Why a worker killed at its wall came back, and what its next run gets.

    q38fn 10-11: the result said "Split the task, or lower its turn cap", but the
    workers ran out of wall in long turns at ~20 tok/s, not in many turns.
    """
    problem = f"the step-executor exceeded its wall-clock budget of {timeout:.0f}s"
    if events.cut_ms:
        problem += (
            f", not counting {events.cut_ms / 1000:.0f}s in turns cut off at the output limit,"
        )
    problem += " and was killed"
    if events.length_stops:
        problem += (
            f": its last {events.length_stops} turn(s) ended at the output limit, writing "
            "more than one reply holds. Split the task, or say in the notes to write files "
            "in smaller pieces."
        )
    else:
        problem += "."
    wall, rate = _worker_wall(cwd, model, provider), _decode_rate(cwd, model, provider)
    if rate and wall > timeout:
        problem += (
            f" At the {rate:.0f} tok/s measured, the next sub-agent's wall is {wall:.0f}s "
            f"({WALL_MAXIMAL_TURNS} turns at the model's output limit)."
        )
    if task:
        problem += (
            f" What it said last and the files it changed go into the next brief on {task}, "
            "to continue from."
        )
    return problem


async def _run_worker(
    brief: str,
    cwd: Path,
    model: str,
    provider: str,
    timeout: float,
    signal: ToolCancellationToken | None = None,
    task: str = "",
    scope: list[str] | None = None,
    thinking: str | None = None,
    role: str = EXECUTOR_ROLE,
    resume: str = "",
) -> _WorkerRun:
    """Run one step-executor as a nested `tau -p --mode json` and read its report.

    A task's scope and the worker's role ride in the worker's environment, where
    its guards hold the worker's writes to the scope and its beagle calls to the
    role's. `thinking` is a level the caller already chose (`_worker_thinking`);
    None chooses it here.

    The brief rides on stdin (tau prepends it to the prompt); the persona is
    appended to tau's base system prompt, not swapped for it, so the worker
    keeps the built-in tool guidance and only gains the persona. JSON mode is
    for the usage figures: `pursuit close --spent` wants what the work cost,
    and beagle cannot see it from a subprocess. `resume` is an earlier worker's
    session id: this run continues it, with `brief` as its next prompt.
    """
    step_executor = _LAYOUT.step_executor
    if step_executor is None:
        return _WorkerRun(
            problem=f"no beagle plugin ships {STEP_EXECUTOR_REL} "
            f"(looked in {_LAYOUT.found_by or BEAGLE})."
        )
    session_id = resume or uuid.uuid4().hex
    transcript = TauPaths().project_session_dir(cwd) / f"{session_id}.jsonl"
    cmd = [
        TAU_BIN,
        "-p",
        "--mode",
        "json",
        "--session" if resume else "--session-id",
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
    if thinking is None:
        thinking = _worker_thinking(model, provider)
    root_key = str(_resolved(cwd))
    can_turn_off = bool(task) and thinking not in (
        "off",
        WORKER_THINKING_DEFAULT,
        WORKER_THINKING_OMIT,
    )
    thinking_off_note = ""
    if can_turn_off and _THINKING_OFF_NEXT.get(root_key) == task:
        del _THINKING_OFF_NEXT[root_key]
        thinking = "off"
        thinking_off_note = (
            f"(this sub-agent ran thinking-off: the one before it on {task} was ended "
            f"because {REASONING_FILLED}.)"
        )
    if thinking:
        cmd += ["--thinking", thinking]

    limit = _memory_max()
    env = {**os.environ, WORKER_ENV: "1", BASH_TIMEOUT_ENV_VAR: f"{_worker_bash_timeout():g}"}
    reasoning = CASES_REASONING_SECONDS if role == CASES_ROLE else WORKER_REASONING_SECONDS
    env.setdefault(TURN_REASONING_ENV, f"{reasoning:g}")
    env.pop(WORKER_TASK_ENV, None)
    env.pop(WORKER_SCOPE_ENV, None)
    env.pop(WORKER_ROLE_ENV, None)
    if task:
        env[WORKER_TASK_ENV] = task
        env[WORKER_ROLE_ENV] = role
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
    walled = False
    while not talk.done():
        if events.cut_offs >= WORKER_CUT_OFFS:
            # Run R33: W2 was cut off three times, not in a row, and ran to the wall.
            with contextlib.suppress(ProcessLookupError):
                proc.kill()
            with contextlib.suppress(Exception):
                await talk
            _record_decode(cwd, model, provider, events)
            retry = ""
            if events.reasoning_cut_offs and can_turn_off and not thinking_off_note:
                _THINKING_OFF_NEXT[root_key] = task
                retry = f"; the next sub-agent on {task} runs thinking-off"
            fills = events.cut_fills
            filled = ["a call was cut off mid-argument"] if CUT_CALL in fills else []
            filled += [REPLY_FILLED] if CUT_REPLY in fills else []
            filled += [REASONING_FILLED] if events.reasoning_cut_offs else []
            advice = (
                "Split the task or have the notes say to write in parts."
                if CUT_CALL in fills
                else NO_CALL_CUT_ONLY
                if events.calls
                else NO_CALL_CUT
            )
            cause = "; ".join(filled) or NOTHING_FILLED
            ended = f"(the sub-agent was ended: {CUT_OFF_ENDED}: {cause}{retry}. {advice})"
            return _WorkerRun(
                returncode=proc.returncode,
                report=f"{events.report}\n\n{ended}\n\n{thinking_off_note}".strip(),
                spent=events.spent,
                transcript=transcript,
                stop_reason="length",
                last_words=events.report,
            )
        if signal is not None and signal.is_cancelled():
            problem = "cancelled; the worker was killed and its partial work is in the tree."
            break
        remaining = deadline + events.cut_ms / 1000 - loop.time()
        if remaining <= 0:
            walled = True
            break
        await asyncio.wait({talk}, timeout=min(_WORKER_POLL_SECONDS, remaining))
    if problem is not None or walled:
        with contextlib.suppress(ProcessLookupError):
            proc.kill()
        with contextlib.suppress(Exception):
            await talk
        _record_decode(cwd, model, provider, events)
        if walled:
            kept = _killed_progress(events, cwd, scope or [], timeout) if task else ""
            if kept:
                _KILLED_PROGRESS[(root_key, task)] = kept
            problem = _wall_problem(timeout, events, task if kept else "", cwd, model, provider)
        problem = f"{problem} {thinking_off_note}".strip()
        return _WorkerRun(
            returncode=proc.returncode,
            problem=problem,
            transcript=transcript,
            said_last=events.last_said() if walled else ("", ""),
        )

    stderr = talk.result()
    _record_decode(cwd, model, provider, events)
    note = _killed_note(proc.returncode, limit)
    if note and events.stop_reason == "toolUse" and events.pending_command:
        note += f" It was killed while its own command `{events.pending_command}` was running."
    if _TOOL_CALL_MARKUP.search(events.report):
        report = _report_before_markup(events.report, cwd, scope or [])
    else:
        report = events.final_report(f"{stderr}\n{note}".strip() if note else stderr)
    if note and note not in report:
        report = f"{report}\n\n{note}".strip()
    if thinking_off_note:
        report = f"{report}\n\n{thinking_off_note}".strip()
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


def _offered_task(root: Path) -> str:
    """The task `beagle pursuit next` offers: the open one, else the first ready.

    Empty when it offers neither or fails; a refusal that names it stands
    without it.
    """
    with contextlib.suppress(Exception):
        rc, ready, _raw = _next_ready(root)
        if rc in (0, 3) and isinstance(ready, dict):
            return (_ids(ready.get("open")) + _ids(ready.get("ready")) or [""])[0]
    return ""


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
    task = _offered_task(goal.parent.parent)
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

        bad_thinking = _bad_thinking(arguments.get("thinking"))
        if bad_thinking:
            return _make_dispatch_result(f"pursuit_dispatch: {bad_thinking}")
        pin = _dispatch_pin(EXECUTOR_ROLE, cwd)
        model, provider = _worker_target(arguments.get("model"), arguments.get("provider"), pin)
        thinking = _worker_thinking(model, provider, arguments.get("thinking"), pin)
        timeout, clamped = _worker_timeout(
            arguments.get("timeout"), _worker_wall(cwd, model, provider)
        )

        run = await _run_worker(brief, cwd, model, provider, timeout, signal, thinking=thinking)
        if run.problem is not None:
            return _with_note(_make_dispatch_result(f"pursuit_dispatch: {run.problem}"), clamped)
        header = (
            f"[pursuit_dispatch] step-executor "
            f"(model={model or 'inherit'} provider={provider or 'inherit'}) "
            f"cwd={cwd} rc={run.returncode}\n\n"
        )
        footer = _dispatch_footer(_SEEN_CWD or Path.cwd()) + _rules_note(pin, "pursuit_dispatch")
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
        "thinking": {
            "type": "string",
            "enum": list(WORKER_THINKING_LEVELS),
            "description": (
                "The worker's thinking level; `default` is the catalog's, else the "
                f"server's. Omit to inherit. Env default: {WORKER_THINKING_ENV}."
            ),
        },
        "timeout": {
            "type": "number",
            "description": (
                "Wall-clock seconds before the worker is killed. "
                f"Default and maximum: {DEFAULT_DISPATCH_TIMEOUT:.0f}, {WALL_DESCRIPTION}."
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
#: One `pursuit_step` call's wall-clock budget across its attempts, as a multiple
#: of the step's worker timeout. Run R39: W8 (7.4 min), its check and W9 (10.5 min)
#: each had a full timeout, and the call ate the last 19 min of a 60-min run. The
#: first attempt keeps its whole timeout; later ones get what remains of this.
STEP_BUDGET_FACTOR = 1.5
#: A later attempt left less than this many seconds of the step budget (or less
#: than the worker timeout, if that is shorter) is not run.
STEP_ATTEMPT_FLOOR = 180.0
#: The clock the step budget is measured on; tests replace it.
_step_clock: Callable[[], float] = time.monotonic
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
#: What pursuit_step says to locks a driver passes: the parameter stays in the
#: schema, and nothing takes them.
LOCKS_NOTE = "locks are not taken here: nothing is locked, and a later task may change them.\n\n"
#: Fallback for a check with no recorded timeout.
DEFAULT_CHECK_TIMEOUT = 600.0

_TASK_ID = re.compile(r"\bT\d{4,}\b")
#: beagle's refusal to open a task ranked below a ready one, up to its remedy.
_RANKED_BELOW = re.compile(
    r"ranks below (.+?)(?: \(`pursuit next` lists them\))?\. If this one should go first", re.S
)


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


#: What founding recorded there: the request, and each URL's file or failure.
REFERENCES_INDEX = "index.json"
#: What `beagle refs fetch` may take per URL: a 30 s try, the 90 s one beagle
#: makes after a timeout (R09's itc2008.pdf timed out at 30 s and every worker
#: re-downloaded it to /tmp), and pdftotext's 120 s.
REFS_FETCH_SECONDS_PER_URL = 240.0
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


def _references_index(root: Path) -> dict[str, Any] | None:
    try:
        index = json.loads((root / REFERENCES_DIR / REFERENCES_INDEX).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return index if isinstance(index, dict) else None


def _fetch_references(root: Path, prompt: str) -> dict[str, Any]:
    """Fetch each URL in the user's `prompt` into `references/`, as text.

    R02's workers never saw the paper: the driver, barred from the
    reference, wrote the domain into its step notes from the name alone.
    The request itself, and each URL's file or why it could not be fetched,
    go in `references/index.json`, which every worker brief is built from.
    `beagle refs fetch` does the fetching, so Claude Code fills references/
    the same way; it keeps a reference already on disk. A failed fetch, or a
    beagle with no `refs`, is recorded against each URL, never fatal.
    """
    urls = _prompt_urls(prompt)
    if not prompt.strip():
        return {}
    folder = root / REFERENCES_DIR
    index: dict[str, Any] = {"request": prompt, "fetched": {}, "failed": {}}
    if urls:
        rc, out = _run(
            [BEAGLE_BIN, "refs", "fetch", *urls, f"--request={prompt}", "--no-exclude"],
            root,
            timeout=60.0 + REFS_FETCH_SECONDS_PER_URL * len(urls),
        )
        written = _references_index(root)
        if written is not None and written.get("request") == prompt:
            index = {**written, "fetched": dict(written.get("fetched") or {})}
            index["failed"] = dict(written.get("failed") or {})
        last = (out.strip().splitlines() or [""])[-1]
        fetched = set(index["fetched"].values())
        unaccounted = [url for url in urls if url not in fetched and url not in index["failed"]]
        for url in unaccounted:
            index["failed"][url] = f"`beagle refs fetch` exited {rc}: {last}".rstrip(": ")
        if written is not None and not unaccounted:
            _ignore(root, [REFERENCES_DIR])
            return index
    with contextlib.suppress(OSError):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / REFERENCES_INDEX).write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    _ignore(root, [REFERENCES_DIR])
    return index


def _fetched_source(source: str, root: Path) -> tuple[str, str]:
    """`source` as the reference file a cases worker reads, and why it is not one.

    Run R105: founding named T0003's source as https://semver.org/ and nothing
    fetched it; the cases worker, barred from `beagle refs fetch`, searched an
    empty references/ for 5 min. A URL is fetched here (`refs fetch` keeps a
    reference already on disk) and comes back as `references/<file>`; anything
    else comes back as it is.
    """
    if not _PROMPT_URL.fullmatch(source):
        return source, ""
    # R125 (q35 semver): v2.0.0.html, its #spec-item-11 and its #spec-item-9 came
    # back as three copies of one page. A fragment names a place in the page.
    page = source.partition("#")[0]

    def on_disk() -> str:
        index = _references_index(root) or {}
        for name, url in (index.get("fetched") or {}).items():
            if str(url).partition("#")[0] == page and (root / REFERENCES_DIR / name).is_file():
                return f"{REFERENCES_DIR}/{name}"
        return ""

    if held := on_disk():
        return held, ""
    rc, out = _run(
        [BEAGLE_BIN, "refs", "fetch", page, "--no-exclude"],
        root,
        timeout=60.0 + REFS_FETCH_SECONDS_PER_URL,
    )
    if held := on_disk():
        return held, ""
    index = _references_index(root) or {}
    failed = str((index.get("failed") or {}).get(page) or "").strip()
    last = (out.strip().splitlines() or [""])[-1]
    return source, failed or f"`beagle refs fetch` exited {rc}: {last}".rstrip(": ")


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
#: A reference up to this long the steer shows whole. Run R120 (g26 wrenfold):
#: shown 1500 characters of a 2586-character spec, the driver founded without
#: `count`, which only the cut part (section 5) names.
REFERENCE_WHOLE_CHARS = 6000
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


#: A numbered section title on a line of its own: `5.3.2    Fork`, not `1. A sentence, ...`.
_NUMBERED_HEADING = re.compile(r"^\s*(\d+(?:\.\d+)*)\.?[ \t]+([A-Z][^\n.:;,]{1,60}?)\s*$")


def _numbered_sections(text: str) -> list[str]:
    """The numbered section titles of a reference, in order, or [] for fewer than two.

    Run R122 (q35 itc): shown the ITC paper's introduction, the driver founded
    intervals with counters; "3 Fork-Event-Join Model" and "5.3 Operations over
    ITC" were past the cut, and named what the paper defines.
    """
    titles = [
        f"{m[1]} {' '.join(m[2].split())}"
        for line in text.splitlines()
        if (m := _NUMBERED_HEADING.match(line))
    ]
    return titles[:60] if len(titles) > 1 else []


def _references_note(index: Mapping[str, Any], root: Path) -> str:
    """The found-first steer's part on the request's references: each whole when
    short, else an extract."""
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
        if len(text) <= REFERENCE_WHOLE_CHARS:
            shown = f"the whole of it:\n<<<\n{text.strip()}\n>>>"
        else:
            lines = len(text.splitlines())
            shown = f"its opening, of {lines} lines:\n<<<\n{_reference_extract(text)}\n>>>"
            if sections := _numbered_sections(text):
                shown += f"\nIts numbered sections: {'; '.join(sections)}."
        parts.append(f"From {url} ({REFERENCES_DIR}/{name}), {shown}")
    parts += [f"Could not fetch {url}: {why}" for url, why in failed.items()]
    return (
        "The references in the request, fetched for you:\n\n"
        + "\n\n".join(parts)
        + "\n\nThe statement and criteria you give pursuit_found must describe this in "
        "the reference's own terms, not from the name alone: a name can mean more than "
        "one thing, and the reference says which."
    )


def _reference_search(words: str = "<words>") -> str:
    """The shell command that finds the lines of references/*.txt holding `words`.

    Run R40: workers re-read whole references 6-20 times and still invented
    values, and drivers refused a re-read fell back on grep. tilth prints each
    match with its line number; without it, `grep -n` does.
    """
    if shutil.which("tilth"):
        return f'tilth "{words}" --scope {REFERENCES_DIR}'
    return f'grep -n -i -F "{words}" {REFERENCES_DIR}/*.txt'


def _reference_search_note() -> str:
    """The sentence saying how to find the reference line that gives a value."""
    return (
        "To find the line that gives a value, search for words from it with bash, "
        f"`{_reference_search()}`, rather than reading the reference through."
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
        parts.append(_reference_search_note())
        parts.append(
            "Read only the lines you cite, by line range (offset and limit), not the whole file."
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


def _turn_cap_note(work_note: str | None = None) -> str:
    """The worker's tool-call cap, as pursuit_step's brief states it (R21-R25),
    then `work_note` (WORK_IT_OUT_NOTE unless given)."""
    cap = _worker_max_turns()
    return (
        f"You have {cap} tool calls in all. Write the files by about call {cap // 2}, "
        "then use the rest to run the check and fix them. A bash command is stopped "
        f"after {_worker_bash_timeout():g} s unless the call passes a longer `timeout`. "
        + (WORK_IT_OUT_NOTE if work_note is None else work_note)
    )


#: Run S04: each q35 worker's longest turn was 16k tokens of reasoning cut at the
#: output limit, about 8 min each; the code worker's was bit layouts by hand
#: ("15 zeros + 23 bits = 38"), wrong, then checked by one `python3 -c` in seconds.
WORK_IT_OUT_NOTE = (
    "Work out arithmetic, bit layouts and expected outputs by running them "
    "(`python3 -c`), not in your reasoning: a long turn of reasoning is cut at the "
    "output limit, costs minutes, and is no surer than the run."
)
#: The cases worker's form of it. Run R104: told both to work expected outputs
#: out by running them and to assert no output it works out (CASES_VALUES_NOTE),
#: a cases worker spent a 241 s turn weighing the two. Run R119 (q35 cobs): both
#: cases workers wrote their own encoder to check the source's table, chased
#: where it disagreed (the rows shortened with `...`), and wrote no test in 24 min.
CASES_WORK_IT_OUT_NOTE = (
    "Check arithmetic and bit layouts by running them (`python3 -c`), not in your "
    "reasoning: a long turn of reasoning is cut, costs minutes, and is no surer "
    "than the run. A run only checks a case; its expected values still come from "
    "the cited lines. The cited lines are right: do not write the code, or a "
    "version of it, to check them, for that version is what would be wrong. Where "
    "a row is shortened (`...`), write it out from the pattern it shows "
    "(`bytes(range(1, 255))`)."
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
    was red from the first task.
    """
    return _commit_only(root, [".beagle", ".gitignore"], ["pursuit: found — beagle setup"])


def _commit_only(root: Path, specs: list[str], message: list[str]) -> str | None:
    """Commit every change under `specs` and nothing else, one `-m` per item of
    `message`; None (also when nothing there changed), or why not.

    A pathspec commit leaves whatever else the user has staged or changed
    exactly as it was; a failed commit unstages only what this call staged.
    """
    pathspec = ["--", *specs]
    staged_now = ["git", "diff", "--cached", "--name-only", "--no-renames", *pathspec]
    rc, out = _run(staged_now, root, timeout=30.0)
    if rc != 0:
        return f"`git diff --cached` failed: {out}"
    before = set(out.splitlines())
    rc, out = _run(["git", "add", "-A", *pathspec], root, timeout=30.0)
    if rc != 0:
        return f"`git add` failed: {out}"
    rc, out = _run(staged_now, root, timeout=30.0)
    if rc != 0:
        return f"`git diff --cached` failed: {out}"
    staged = out.splitlines()
    if not staged:
        return None
    # Each path by name: `git commit -- <dir>` leaves a removed directory's
    # deletions staged rather than committed.
    paragraphs = [arg for para in message for arg in ("-m", para)]
    rc, out = _run(["git", "commit", "-q", *paragraphs, "--", *staged], root, timeout=60.0)
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
#: Seconds the command's `timeout` ends before the worker's bash timeout would (R39).
COMMAND_BASH_MARGIN = 10
#: What exit 124 means, said wherever a worker meets it (R30, R34, R39).
HANG_MEANING = (
    "the code under test likely loops (a loop that never advances), so run one case "
    "under a short `timeout` (e.g. `timeout 10`) to find where, rather than re-running "
    "the whole check."
)
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


def _command_bound(limit: str | None, timeout: float, bash: float | None = None) -> str:
    """The prefix a worker's own command runs under: half its memory cap, under its wall.

    Run R30: W4-W7 ran `timeout 540 python3 -m pytest …` inside their own capped
    scope; the runaway test took the worker down with it, and no report came
    back. A `systemd-run --user --scope` started by the worker is a scope of its
    own, so the command's memory is not the worker's and an over-cap command
    dies alone, exit 137, with the worker left to report it.

    Run R39: the bound was `timeout 540` while the worker's bash timeout was
    120 s, so a looping check reached W8 and W9 only as the bash tool's "timed
    out after 120 seconds", with an empty log, and W9 ran it 7 times. The bound
    sits COMMAND_BASH_MARGIN below `bash` (the worker's bash timeout, default
    `_worker_bash_timeout()`), so `timeout` ends it first: exit 124 and the log
    so far.
    """
    if bash is None:
        bash = _worker_bash_timeout()
    below_bash = bash - min(COMMAND_BASH_MARGIN, bash / 2)
    seconds = max(1, int(min(COMMAND_TIMEOUT, below_bash, timeout * COMMAND_TIMEOUT_SHARE)))
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


#: beagle 0.48's `next: <command>` line: the one move its output implies,
#: printed last (`_say_next`), on stderr after a refusal that names one.
_NEXT_LINE = re.compile(r"^next: (.+)$", re.MULTILINE)


def _beagle_next(out: str) -> str:
    """The move the last `next:` line in a beagle reply names, or ""."""
    moves = _NEXT_LINE.findall(out)
    return moves[-1].strip() if moves else ""


def _tau_next(move: str) -> str:
    """beagle's `next:` move as the tau tool call that makes it, as a "Next: …" line.

    The driver drives with tau's tools, not beagle's verbs: a verb pursuit_step
    runs is named as that call. A move no tool makes is passed on as beagle said it.
    """
    words = move.split()
    verb = words[2] if words[:2] == ["beagle", "pursuit"] and len(words) > 2 else ""
    task = words[3] if len(words) > 3 and _TASK_ID.fullmatch(words[3]) else ""
    if verb == "next" and len(words) == 3:
        return "Next: call pursuit_step with no arguments for the next task."
    if verb == "audit" and len(words) == 3:
        return "Next: call pursuit_step with no arguments; it runs the audit that is due."
    if verb == "open" and task:
        return f'Next: pursuit_step with task="{task}", which opens it.'
    if verb == "retry" and task:
        return f'Next: pursuit_step with task="{task}", which reworks it on its own check.'
    if verb == "spawn" and task:
        return (
            f'Next: pursuit_step with task="{task}", new_route=true and notes saying how '
            "the new route differs."
        )
    return f"Next, as beagle says: `{move}`."


def _relay_next(out: str, fallback: str) -> tuple[str, str]:
    """A beagle reply without its `next:` line, and the move it named as a tau call.

    `fallback`, the caller's own Next line, where the reply names no move.
    """
    move = _beagle_next(out)
    if not move:
        return out, fallback
    return _NEXT_LINE.sub("", out).strip(), _tau_next(move)


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _reference_key(name: str) -> str:
    return re.sub(r"[\W_]+", "", name).lower()


def _named_reference(source: str, root: Path) -> str | None:
    """`source` as naming what it names: itself when it carries a link or names
    a file in `root`'s references/ by name or stem; with the file's own name put
    in when a word of it, or the whole of it, spells one with other case or
    separators; None when it names none.

    F000 (q35 cobs): every source was references/ConsistentOverheadByteStuffing.txt
    for Consistent_Overhead_Byte_Stuffing.txt, and each joined its intent.
    """
    if _PROMPT_URL.search(source):
        return source
    try:
        files = [f for f in (root / REFERENCES_DIR).iterdir() if f.name != REFERENCES_INDEX]
    except OSError:
        return None
    if any(
        re.search(rf"(?i)(?<![\w-]){re.escape(word)}(?![\w-])", source)
        for f in files
        for word in {f.name, f.stem}
    ):
        return source
    names = {_reference_key(word): word for f in files for word in (f.stem, f.name)}
    if _reference_key(source) in names:
        return names[_reference_key(source)]
    for found in re.finditer(r"[\w./-]+", source):
        head, _, word = found.group().rpartition("/")
        if (key := _reference_key(word)) and key in names:
            named = f"{head}/{names[key]}" if head else names[key]
            return source[: found.start()] + named + source[found.end() :]
    return None


def _milestone_parts(
    value: Any, root: Path | None = None, notes: list[str] | None = None
) -> list[str]:
    """Milestone entries as `title::intent` strings; an entry given a `source`
    keeps it as the intent's last words, `Source: <ref>` (`_task_source`).

    Under a project `root`, a source that names no reference there and carries
    no link is what the part is for, and joins its intent (a note says so in
    `notes`). R124 (lfm24 wrenfold): every source described its part
    ("wrenfold.py with encode, decode, count functions implementing revision 3
    spec"), and T0002's cases were written from that.
    """
    if isinstance(value, (str, dict)):
        value = [value]
    if not isinstance(value, list):
        return []
    parts = []
    for item in value:
        if isinstance(item, dict):
            part = str(item.get("part") or item.get("title") or "").strip()
            source = " ".join(str(item.get("source") or "").split())
        else:
            part, source = str(item).strip(), ""
        if part and (not source or _NO_SOURCE.match(source)):
            part, source = _source_in_part(part, root)
        if part and source and not _NO_SOURCE.match(source):
            title, _, intent = part.partition("::")
            part = f"{title.strip()}::{f'{intent.strip()} ' if intent.strip() else ''}"
            named = source if root is None else _named_reference(source, root)
            if named:
                part += f"{SOURCE_LEAD} {named}"
            else:
                part += source
                if notes is not None:
                    notes.append(
                        f"Took the source of {title.strip()!r} as what it is for: a "
                        f"source names a file in {REFERENCES_DIR}/ or a link."
                    )
        parts.append(part)
    return [part for part in parts if part]


#: The words that lead a link written into a milestone's part ("..., based on <link>").
_LINK_LEAD = re.compile(r"[\s,;]*(?:\b(?:based on|according to|from|per|see)\s+)?$", re.I)


def _source_in_part(part: str, root: Path | None) -> tuple[str, str]:
    """A milestone `part` given no source, and the source it names in its own words:
    a link, taken out of them, or under `root` a references/ file named in them;
    "" when it names neither.

    F011, F012 (g26 cobs): every part ended "... based on <the request's link>"
    and none set a source, so no milestone kept Source:.
    """
    found = _PROMPT_URL.search(part)
    if found:
        link = found.group().rstrip(".,;:)")
        before = _LINK_LEAD.sub("", part[: found.start()])
        after = part[found.start() + len(link) :].lstrip(".,;:) ").strip()
        return " ".join(w for w in (before.strip(), after) if w), link
    if root is not None:
        for word in re.finditer(r"[\w./-]+", part):
            named = _named_reference(word.group().rstrip("."), root)
            if named:
                return part, named
    return part, ""


def _task_source(record: Mapping[str, Any]) -> str:
    """The reference a task's record names as its source (`_milestone_parts`), or ""."""
    found = _SOURCE_IN_INTENT.search(str(record.get("intent") or ""))
    source = found.group(1).strip() if found else ""
    return "" if _NO_SOURCE.match(source) else source


def _toml_string(text: str) -> str:
    # A JSON string is a valid TOML basic string: same quotes, same escapes.
    return json.dumps(text)


def _tree(root: Path) -> str:
    rc, out = _pursuit(["tree"], root)
    return out if rc == 0 else ""


#: The one sentence of planning guidance spec-tying needs: the rest is beagle's
#: (`pursuit rules 2e`), read by the worker that writes the cases.
SOURCE_SENTENCE = (
    "Name a source for a part whose behaviour a file in references/ or a link in the "
    "user's request states: "
    '{"part": "<title>::<what it is for>", "source": "<that file\'s name, or the link>"}.'
)

#: A milestone or plan part: the `title::intent` string, or that string with the
#: reference it is built from. Fixed per build, as every tool schema is.
MILESTONE_ITEM: dict[str, Any] = {
    "anyOf": [
        {"type": "string"},
        {
            "type": "object",
            "properties": {
                "part": {"type": "string", "description": "'<title>::<what it is for>'."},
                "source": {
                    "type": "string",
                    "description": (
                        "The file in references/ that states this part's behaviour, by "
                        "name (itc2008), optionally with the topic's words, or a link in "
                        "the user's request that states it, fetched first (R107). A "
                        "sub-agent writes its cases from it before the work."
                    ),
                },
            },
            "required": ["part"],
        },
    ]
}


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
                "checkable by someone else (a command that exits 0, a file that exists). "
                "Drafting them yourself, say what must pass and leave exact values, sizes, "
                "bounds and worked examples to the sources the workers read: a value "
                "written from memory can contradict them."
            ),
        },
        "milestones": {
            "type": "array",
            "items": MILESTONE_ITEM,
            "description": (
                "The parts of the goal you can already name, in order, each "
                "'<title>::<what it is for>'. Three to seven is typical. " + SOURCE_SENTENCE
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


#: How a leaf ends undone for good: beagle spawns a new route only from an open
#: or blocked task, so a leaf ended so stays undone unless a task holds its work.
_SEALING = ("infeasible", "abandoned", "superseded")


def _sealed(nodes: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Each container that can never be all-done, with the leaves that seal it.

    beagle's `_accountable_leaves` keeps a leaf that ended undone with no task
    holding its work (`sibling_of`, followed to the newest attempt), so every
    container above it stays undone for good: only the owner can re-scope or
    abandon it. q35 10-11: T0011 closed infeasible at 11:23 and sealed T0002,
    and 60 min of pursuit_plan parts under T0002 followed, none of which could
    make it done. A leaf dropped as a duplicate of a done task is left out, as
    `_unfinished` leaves it out.
    """
    by_id = {str(n.get("id")): n for n in nodes}
    after: dict[str, list[str]] = {}
    for n in nodes:
        if n.get("sibling_of"):
            after.setdefault(str(n.get("sibling_of")), []).append(str(n.get("id")))
    sealed: dict[str, list[str]] = {}
    for node in nodes:
        if node.get("container"):
            continue
        end, seen = str(node.get("id")), {str(node.get("id"))}
        while by_id[end].get("status") in (*_SEALING, "blocked") and after.get(end):
            end = max(after[end])
            if end in seen or end not in by_id:
                break
            seen.add(end)
        last = by_id.get(end, {})
        if last.get("container") or last.get("status") not in _SEALING:
            continue
        if last.get("status") == "abandoned":
            named = _TASK_ID.findall(str(last.get("reason") or ""))
            if any(by_id.get(t, {}).get("status") == "done" for t in named if t != end):
                continue
        up, walked = str(node.get("parent") or ""), set()
        while up and up not in walked and up in by_id:
            walked.add(up)
            if end not in sealed.setdefault(up, []):
                sealed[up].append(end)
            up = str(by_id[up].get("parent") or "")
    return sealed


#: What a sealed container's note ends on: the stop gate lets through the stop it offers.
SEALED_STOP = "Only the owner can re-scope or abandon"


def _sealed_text(
    container: str, leaves: list[str], nodes: list[dict[str, Any]], now: bool = False
) -> str:
    """Why `container` can never be all-done, and that the owner decides what next."""
    by_id = {str(n.get("id")): n for n in nodes}
    ended = ", ".join(f"{t} ({by_id.get(t, {}).get('status')})" for t in leaves)
    one = len(leaves) == 1
    return (
        f"{container} is {'now ' if now else ''}sealed: {ended} ended undone with no task holding "
        f"{'its' if one else 'their'} work, and beagle keeps {'it' if one else 'them'} "
        f"among {container}'s leaves, so {container} can never be all-done, nor can what "
        f"is above it or waits on it. No part planned under {container} changes that. "
        f"{SEALED_STOP} {container}: stop, and ask the user which."
    )


def _sealed_note(nodes: list[dict[str, Any]]) -> str:
    """The sealed containers' notes, the lowest of each chain only; "" when none is."""
    sealed = _sealed(nodes)
    by_id = {str(n.get("id")): n for n in nodes}
    lowest = [
        c
        for c, leaves in sealed.items()
        if any(str(by_id.get(t, {}).get("parent") or "") == c for t in leaves)
    ]
    return "\n".join(
        _sealed_text(c, [t for t in sealed[c] if by_id.get(t, {}).get("parent") == c], nodes)
        for c in lowest
    )


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
    if _lean():
        return None
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
                "is the goal's. Split it with pursuit_plan. If a done task's commit "
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
        source_notes: list[str] = []
        milestones = _milestone_parts(arguments.get("milestones"), root, source_notes)
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
        repairs = [*criteria_notes, *source_notes, *repairs]
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
            '\n[close]\nrequire = "witness"\n'
            # R0002: the lean arm runs no audit sub-agent, so beagle core's
            # cadence (an audit due every 16 closes refuses `open`) is off too.
            f"{LEAN_AUDIT_OFF if _lean() else ''}",
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
                f"\n\n{_goal_text(goal) or ''}"
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
            f"Founded the pursuit in {goal}, root task {root_task}.\n\n"
            f"{_goal_text(goal) or ''}\n\n{_tree(root)}\n\n"
            f"{noted}{DRIVER_STEERS_NOTE}\n\n"
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
            "items": MILESTONE_ITEM,
            "description": "Its steps, each '<title>::<what it is for>'. " + SOURCE_SENTENCE,
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

    R09: T0007 was split with its tests/ data file uncommitted, and T0009's commit
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
        f"Uncommitted in {task}'s scope: {named}. Give each to the part that writes it; "
        "otherwise it goes out in a later part's commit."
    )


def _commit_before_split(root: Path, task: str, scope: list[str], paths: list[str]) -> str:
    """Commit a split task's uncommitted work when its check last passed; the note to give.

    R12: test_comprehensive.py passed under T0007 and was left to the last
    part, so the workspace-clean gate stayed red for every part before it.
    Work whose check failed, or was never run, stays a note for the parts.
    """
    if _lean() or _LAST_CHECK_EXIT.get((str(root), task)) != 0:
        return _uncommitted_note(task, paths)
    said = _commit(task, SPLIT_WIP_TITLE, scope, root)
    left = [rel for rel in _changed_files(root) if _in_scope(rel, scope, root)]
    if left:
        return f"{said}\n\n{_uncommitted_note(task, left)}"
    return (
        f"{task}'s check passed at its last run, so its uncommitted work "
        f"({', '.join(paths[:8])}{', …' if len(paths) > 8 else ''}) was committed as "
        f"'{task}: {SPLIT_WIP_TITLE}' before the split: {said}"
    )


@dataclass(frozen=True)
class _SplitCarry:
    """The work a split committed for its parts: see `_split_carried`."""

    #: The task that was split, and the commit it opened on.
    parent: str = ""
    opened: str = ""
    #: The files its 'work in progress before split' commit added or changed.
    files: tuple[str, ...] = ()

    def base(self, rel: str, opened: str) -> str:
        """The commit `rel` counts as new against: the parent's open for a carried file."""
        return self.opened if os.path.normpath(rel) in self.files else opened

    def because(self, task: str) -> str:
        """The `--predates-because` for a witness in the carried files."""
        return (
            f"{self.parent}'s split committed this work as '{self.parent}: "
            f"{SPLIT_WIP_TITLE}' before {task} opened; it is {task}'s work, counted "
            f"from the commit {self.parent} opened on"
        )


def _split_carried(task: str, root: Path) -> _SplitCarry:
    """The work `_commit_before_split` committed for `task`, a part of the split task.

    q35 10-11: T0002's passing work was committed as 5f53adf before its split, so
    every part's check already passed at its open, and `_prove` had nothing new
    since the part opened to take away: 19 workers and 4 infeasible closes. The
    files that commit added or changed are the parts' work, counted from the
    commit the parent opened on, while no part has closed done and no later
    commit has changed them. Empty for any other task.
    """
    rc, out = _run(
        ["git", "log", "--format=%H %s", "--fixed-strings", f"--grep={SPLIT_WIP_TITLE}"],
        root,
        timeout=30.0,
    )
    commits = [line.partition(" ") for line in out.splitlines()] if rc == 0 else []
    if not commits:
        return _SplitCarry()
    nodes = _tree_nodes(root)
    parent = next((str(n.get("parent") or "") for n in nodes if n.get("id") == task), "")
    split = next(
        (sha for sha, _, subject in commits if subject == f"{parent}: {SPLIT_WIP_TITLE}"), ""
    )
    if not parent or not split:
        return _SplitCarry()
    if any(n.get("parent") == parent and n.get("status") == "done" for n in nodes):
        return _SplitCarry()
    opened = _opened_commit(parent, root)
    if not opened or opened == split:
        return _SplitCarry()
    since = set(
        _run(["git", "diff", "--name-only", split, "HEAD"], root, timeout=30.0)[1].splitlines()
    )
    files = [
        rel for rel in _commit_paths(split, root) if rel not in since and (root / rel).is_file()
    ]
    return _SplitCarry(parent, opened, tuple(os.path.normpath(rel) for rel in files))


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


def _steppable(ids: list[str], nodes: list[dict[str, Any]]) -> list[str]:
    """`ids` without the containers the tree shows, nor a task that waits on another.

    Run R28 listed open container T0012 as workable; the driver stepped it
    seven times in a row and the breaker stopped the run.
    """
    waits = _hard_waits(nodes)
    return [t for t in ids if not _is_container(t, nodes) and t not in waits]


def _live_title_clash(task: str, parts: list[str], nodes: list[dict[str, Any]]) -> str | None:
    """Why a plan may not add `parts`, one titled as a live task off `task`'s subtree is, or None.

    Run R22's driver planned five parts on the root that repeated pending
    tasks, and they then ranked against the tasks they repeated. Run R25's
    split of T0006 repeated pending T0003-T0005 the same way, off the root.
    A part may not take `task`'s own title either; its descendants' titles stay free.
    Ancestors of `task` and containers are left out: neither is a task to step.
    Titles are compared case-folded with whitespace normalized.
    """
    if _lean():
        return None
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
        source_notes: list[str] = []
        parts = _milestone_parts(arguments.get("parts"), root, source_notes)
        if not task or not parts:
            return _step_result("pursuit_plan: 'task' and 'parts' are both required.")
        parts, split_notes = _split_part_lines(parts)
        if not parts:
            return _step_result(f"pursuit_plan: nothing added — {split_notes[0]}")
        split_notes += source_notes
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
        # Read before the split, which leaves the task a container.
        scope, uncommitted = _uncommitted_in_scope(root, task)
        uncommitted_note = _uncommitted_note(task, uncommitted) if uncommitted else ""
        if len(parts) == 1:
            rc, out = _add_children(task, parts, root)
            # beagle says "a pending leaf" or, for one being worked, "a open
            # leaf": run R06's plan of one part on open T0002 came back raw.
            if rc != 0 and "leaf with work of its own" in out:
                return _step_result(one_step)
        else:
            if uncommitted:
                uncommitted_note = _commit_before_split(root, task, scope, uncommitted)
            rc, out = _pursuit(["split", task, *parts, *(["--ordered"] if ordered else [])], root)
            if rc != 0 and "already has children" in out:
                rc, out = _add_children(task, parts, root)
        if rc != 0:
            refused = f"pursuit_plan: beagle refused (exit {rc}):\n{out}"
            if uncommitted_note:
                refused += f"\n\n{uncommitted_note}"
            return _step_result(refused)
        _forget_task(root, task)
        notes = "".join(f"{note}\n\n" for note in split_notes)
        if uncommitted_note:
            notes += f"{uncommitted_note}\n\n"
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
                "Files this task writes, such as the known-answer cases from the reference. "
                "Nothing is locked: a later task may change them."
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
        "model": {
            "type": "string",
            "description": (
                "Tau model id for this task's sub-agent, when the project's model rules "
                "call for one. Omit for the project's pinned model, else the session's."
            ),
        },
        "provider": {
            "type": "string",
            "description": "Tau provider serving that model. Omit with model.",
        },
        "thinking": {
            "type": "string",
            "enum": list(WORKER_THINKING_LEVELS),
            "description": (
                "The sub-agent's thinking level; `default` is the catalog's, else the "
                "server's. Omit to inherit."
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
                f"{DEFAULT_DISPATCH_TIMEOUT:.0f}, {WALL_DESCRIPTION}."
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
      `python3 -m json.tool data.json`) and passes whatever it says;
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


def _module_names(rel: str) -> list[str]:
    """The dotted names `rel`, a .py file, may be imported as: each tail of its path."""
    parts = list(Path(rel).with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return [".".join(parts[i:]) for i in range(len(parts))]


def _judged_sources(entries: list[str], root: Path, check: str = "") -> tuple[list[str], list[str]]:
    """(source, helpers) among `entries`' non-test .py files.

    Run R31: a worker saved tests/casegen.py, a generator no test imported and the
    check did not name, beside its tests/ data file, and 51 calls were refused for
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
        # Run R09: scope src/, tests/ held a tests/ data file beside src/itc/*.py,
        # and a directory entry has neither suffix, so it is judged by its files.
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel.rstrip("/")))
    return entries


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


def _scope_holds_code_or_data(
    scope: list[str], root: Path, also: list[str] | None = None, tests_count: bool = True
) -> bool:
    """Whether `scope` (its directories walked) or `also` holds a .py file or test data.

    With `tests_count` false, a test .py is not code: only source counts.
    """
    entries = [rel.rstrip("/") for rel in [*scope, *(also or [])]]
    for rel in list(entries):
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel))
    return any(
        _is_test_data(rel) or (rel.endswith(".py") and (tests_count or not _is_test_path(rel)))
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
    if _scope_holds_code_or_data(scope, root, reads, tests_count=False):
        return None
    return (
        f"{reads[0]} is under tests/, so nothing can witness it; fold reading the "
        f"reference into the known-answers task, or abandon {task}: "
        f'pursuit_step task="{task}", abandon="folded into the known-answers task".'
    )


def _no_scope_problem(scope: list[str], root: Path) -> str | None:
    """Why a task may not open with no scope, or None.

    Run R17: T0002, T0008 and T0009 opened with scope [], so no worker on them
    was held to any path. With references/ fetched the pursuit is past founding,
    and every task it opens writes something nameable.
    """
    if scope or not (root / "references").is_dir():
        return None
    return (
        "no scope given, so its sub-agent would write anywhere. Pass scope=[...] "
        "naming the paths this task writes, and call pursuit_step again."
    )


def _data_task(scope: list[str], goal: Path, check: str) -> bool:
    """Whether a task writes known-answer data and its cases test, not the code.

    A scope's entries are judged with a directory judged by its files; a scope
    holding no data yet counts when its check names a cases or data test.
    """
    root = goal.parent.parent
    entries: list[str] = []
    for rel in scope:
        entries.append(rel)
        if (root / rel).is_dir():
            entries.extend(_scope_dir_files(root, rel.rstrip("/")))
    if any(rel.endswith(".py") and not _is_test_path(rel) for rel in entries):
        return False
    data = any(
        _is_test_path(rel.rstrip("/")) and Path(rel.rstrip("/")).suffix not in {"", ".py"}
        for rel in entries
    )
    return data or bool(re.search(r"test_\w*(case|data)", check))


#: Imports in a test that name no module of the project's.
_TEST_LIBRARIES = frozenset({"pytest", "_pytest", "hypothesis", "tests", "test", "conftest"})


def _module_of(rel: str) -> str:
    """The dotted module a source path under src/ or the root holds."""
    path = rel.removeprefix("src/").removesuffix(".py").removesuffix("/__init__")
    return path.replace("/", ".")


#: Suffixes of a data file under tests/ that a test reads, whose absence proves its
#: check (`prove --absent`).
TEST_DATA_SUFFIXES = frozenset({".json", ".toml", ".yaml", ".yml", ".csv"})


def _is_test_data(rel: str) -> bool:
    """Whether `rel` is a data file under tests/, which a check can be proved by taking away."""
    return Path(rel).suffix in TEST_DATA_SUFFIXES and _is_test_path(rel)


def _test_reads_file(test_path: Path, data_basename: str) -> bool:
    """Whether the test's code, not a docstring or comment, opens the data file.

    Run R14: test_cases.py held hand-written asserts and never opened
    the data file, so the locked known answers judged nothing. The read call
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


def _unanswered_case_note(root: Path) -> str:
    """The known-answers verdict's sentence for a case no reference line answers.

    q35 R52: it listed reference lines that "give a concrete result", and two were
    a table's example index and input ("1 | 00"); the driver read one as a result
    and a right case was made wrong. It names no lines, only where to search.
    """
    note = (
        f"If no line of {REFERENCES_DIR}/*.txt gives a case's result, no quote can source "
        "it: replace the case with one whose input and result the reference both gives, "
        "rather than quote a rule or prose line again."
    )
    return f"{note} To find lines that give a result, search with bash: `{_reference_search()}`."


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


def _python_c_code(argv: list[str]) -> str | None:
    """The code of a `python -c '...'` argv, or None for any other command."""
    if not Path(argv[0]).name.startswith("python") or "-c" not in argv[1:]:
        return None
    at = argv.index("-c") + 1
    return argv[at] if at < len(argv) else None


def _exit_call_name(func: ast.expr) -> str | None:
    """`SystemExit`, `exit`, `quit` or `sys.exit` when `func` names one, else None."""
    if isinstance(func, ast.Name) and func.id in ("SystemExit", "exit", "quit"):
        return func.id
    if (
        isinstance(func, ast.Attribute)
        and func.attr == "exit"
        and isinstance(func.value, ast.Name)
        and func.value.id == "sys"
    ):
        return "sys.exit"
    return None


def _is_bool_expr(node: ast.expr) -> bool:
    """Whether `node` is a `not`, a comparison, `bool(...)`, or `and`/`or` of those."""
    if isinstance(node, ast.BoolOp):
        return all(_is_bool_expr(value) for value in node.values)
    return (
        isinstance(node, ast.Compare)
        or (isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not))
        or (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "bool"
        )
    )


def _bool_exit(code: str | None) -> str | None:
    """The first `exit(<bool expression>)` call in Python `code`, unparsed, or None."""
    if code is None:
        return None
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and len(node.args) == 1 and not node.keywords:
            name = _exit_call_name(node.func)
            if name is not None and _is_bool_expr(node.args[0]):
                return f"{name}({ast.unparse(node.args[0])})"
    return None


def _inverted_exit_problem(command: str) -> str | None:
    """Why a `python -c` check's exit status is a bool expression, or None.

    Run R44: T0004 opened on `raise SystemExit(not bad and len(c)>=5)`. Python
    exits 1 for True and 0 for False, so a pass condition given as the exit
    status fails good work and passes bad; the open's run before any work saw
    exit 1, which a sound check also gives then. Which one an expression means
    cannot be told from the code, so the text says when the exit is right
    rather than that it is wrong. An int exit, or a call's result such as
    `sys.exit(main())`, is not judged.
    """
    call = _bash_find(command, lambda argv: _bool_exit(_python_c_code(argv)))
    if call is None:
        return None
    return (
        f"`{call}` exits 1, a failing check, when its expression is true, and 0 when "
        "it is false, so it is right only if the expression means a failure was found; "
        "one that means the work passed fails good work and passes bad. Make the exit "
        "explicit either way: `if <a failure is found>: raise SystemExit(1)`, or "
        "`raise SystemExit(0 if <it passes> else 1)`. Call pursuit_step again with that."
    )


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
        if _in_scope(rel, scope, root):
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
                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test")
            )
            or (isinstance(n, ast.ClassDef) and n.name.startswith("Test"))
        ]
        held = f"its tests are: {', '.join(tests[:5])}" if tests else "it holds no tests"
        return (
            f"done_when `{command}` names `{node_id}`, which is not in {rel}; {held}. "
            "No worker can add it, since it is outside the task's scope. Name a test that "
            "exists, or a test file in the task's scope, and call pursuit_step again with that."
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


def _imports_unwritten(
    command: str, scope: list[str], root: Path
) -> tuple[str, str, tuple[str, ...]] | None:
    """(test, module, via) when the check runs a test importing a module that does not
    exist and that no path in `scope` would create, or None. `via` holds the project
    test files, in order, through which `test` imports `module`; () when it imports
    `module` itself.

    Run R15 E9 amended the known-answers task's check to run tests/test_cases.py,
    which imports itc_clocks.itc that only a later task writes; no worker on the
    tests/ scope could pass it. A later part whose scope holds the module may bind
    the same test. Run R35: tests/test_case_data.py imported test_cases, which
    imported the unwritten module; a test_* import was skipped, so none of this saw it.
    """
    if not scope:
        return None
    for rel in _check_test_files(command, root):
        found = _unwritten_import(root / rel, scope, root, set())
        if found is not None:
            return rel, found[0], found[1]
    return None


def _sibling_test(name: str, test: Path, root: Path) -> Path | None:
    """The project test file an import of `name` in `test` names: a test_* module
    beside `test`, at the root or in a tests package; or None."""
    rel = name.replace(".", "/")
    if not rel.rsplit("/", 1)[-1].startswith("test_"):
        return None
    for base in (test.parent, root, root / "tests"):
        if (base / f"{rel}.py").is_file():
            return base / f"{rel}.py"
    return None


def _unwritten_import(
    test: Path, scope: list[str], root: Path, seen: set[Path]
) -> tuple[str, tuple[str, ...]] | None:
    """(module, via) for the first module `test` imports, itself or through the
    sibling tests in `via`, that does not exist and no path in `scope` creates."""
    seen.add(test.resolve())
    for names in _test_imports(test):
        siblings = [path for n in names if (path := _sibling_test(n, test, root)) is not None]
        if siblings or names[0].split(".")[0].startswith("test_"):
            for sibling in siblings:
                if sibling.resolve() in seen:
                    continue
                found = _unwritten_import(sibling, scope, root, seen)
                if found is not None:
                    return found[0], (sibling.relative_to(root).as_posix(), *found[1])
            continue
        if not any(_module_written(n, root, test.parent, scope) for n in names):
            return names[0], ()
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
    test, module = found[0], found[1]
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
    return f"\n\n{_import_chain_note(*found)}" if found is not None else ""


def _import_chain_note(test: str, module: str, via: tuple[str, ...]) -> str:
    """What a data test that imports unwritten `module`, itself or through `via`, must
    change.

    Run R35: tests/test_case_data.py imported test_cases, which imported the unwritten
    module; W8's direct import was refused and its `import test_cases` passed.
    """
    if not via:
        return (
            f"{test} imports {module}, which no path in this scope creates; a data test "
            "reads only the data file and imports none of the code: remove that import."
        )
    chain = "".join(f"{sibling}, which imports " for sibling in via)
    return (
        f"{test} imports {chain}{module}, which no path in this scope creates: a data "
        f"test imports no other test; copy what it needs into {test} or read the data "
        "file directly."
    )


def _import_line(test_path: Path, name: str) -> str:
    """The source line of the first import in `test_path` naming module `name` or a
    submodule of it, stripped; "" when the AST has none."""
    try:
        text = test_path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except (OSError, SyntaxError, ValueError):
        return ""
    lines = text.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names = [node.module]
        else:
            continue
        if any(n == name or n.startswith(f"{name}.") for n in names):
            return lines[node.lineno - 1].strip()
    return ""


def _data_test_unwritten_import(
    command: str, scope: list[str], root: Path
) -> tuple[str, str, str, str] | None:
    """(test, module, import line, data file) when, on a scope of data and tests, the
    check runs a scoped test that imports, itself or through a sibling test, a module
    neither the tree nor the installed packages provide and no scope path creates, and
    `_data_test_route` has no other data test to bind instead; or None.

    Run R41 T0005: tests/test_case_data.py imported the unwritten module, and the
    not-done result's Next offered a corrected done_when.
    """
    if not _only_data_and_tests(scope) or not (data := _scope_data(scope, root)):
        return None
    found = _imports_unwritten(command, scope, root)
    if found is None or not _in_scope(found[0], scope, root):
        return None
    if _data_test_route(command, scope, root) is not None:
        return None
    test, module, via = found
    imported = Path(via[0]).stem if via else module
    return test, module, _import_line(root / test, imported), data[0]


def _data_test_import_said(
    task: str, check: str, found: tuple[str, str, str, str]
) -> tuple[str, str]:
    """The not-done lead and Next for a data test that imports unwritten code."""
    test, module, line, data = found
    at = f" (`{line}`)" if line else ""
    return (
        f"{test} imports {module}{at}, which neither the project tree nor the installed "
        f"packages provide and no path in this scope creates, so the check fails for that "
        f"import: {test} is the data test: it loads {data} only and must import none of "
        "the code. The check is right; the import is the work: remove it, and check the "
        "data's own fields. The cases run against the code in the cases test, under the "
        "task that writes the code.",
        f'Next: pursuit_step with task="{task}" and notes saying {test} must import none '
        f"of the code: remove {f'`{line}`' if line else f'its import of {module}'} and every "
        f"use of {module}, and test only what {data} holds. Pass no done_when: `{check}` "
        "stays the check.",
    )


def _self_import(
    command: str, scope: list[str], root: Path | None
) -> tuple[str, str, tuple[str, ...]] | None:
    """(test, module, via) for a check whose data test imports unwritten code, or None."""
    found = _imports_unwritten(command, scope, root) if scope and root and command else None
    if found is None or _data_test(found[0], scope, root) != found[0]:
        return None
    return found


def _data_self_import(
    command: str, scope: list[str], root: Path | None
) -> tuple[str, str, tuple[str, ...]] | None:
    """`_self_import` for a scope of data and tests only, where the test is a data test."""
    if not (_scope_has_data(scope, root) and _only_data_and_tests(scope)):
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


def _known_answers_note(command: str, scope: list[str], root: Path) -> str:
    """The brief's proof note for a scope of data and tests: what the data test imports.

    Run R27 W3's brief held only `WITNESS_NOTE`, pointing at "the code they test", and
    W3 wrote `from cobs import …` into tests/test_case_data.py. Run R28 W3's brief said
    a test with `from src.interval_tree_clock import …`, a module on disk, imported
    none, and W3 deleted the import; so that is said only of a test whose AST imports
    no project module.
    """
    data = _scope_data(scope, root)[0]
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
        (t for t in runs if _test_reads_file(root / t, Path(data).name)),
        next((t for t in runs if _in_scope(t, scope, root)), runs[0] if runs else ""),
    ) or _data_test("", scope, root)
    proof = _tests_only_proof_note(command, scope, root)
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
    if not (_scope_has_data(scope, root) and _only_data_and_tests(scope)):
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


def _absent_test_kept_note(command: str, data_check: str, scope: list[str], root: Path) -> str:
    """The note on keeping `command` when `_absent_test_route`'s data test already passes."""
    route = _absent_test_route(command, scope, root)
    absent = route[0] if route is not None else []
    named = ", ".join(absent) or "the test it names that is not on disk yet"
    return (
        f"Kept done_when `{command}`: `{data_check}` alone already passes, before any "
        f"work, so {named}, in scope and not on disk yet, is the work; the check fails "
        "until it is written.\n\n"
    )


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
    if route is None or not (_scope_has_data(scope, root) and _only_data_and_tests(scope)):
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

    Run R21: T0005's check ran tests/test_case_data.py, which read a tests/ data file
    and imported nothing; the scope held only the test, so the data file's absence,
    the one proof such a test has, was out of reach. Found from the test's code (the
    file it opens, by `_test_reads_file`) and `TEST_DATA_SUFFIXES`; a bare name
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
            if named.suffix not in TEST_DATA_SUFFIXES or named.is_absolute():
                continue
            if not _test_reads_file(test, named.name):
                continue
            beside = (test.parent / named.name).relative_to(root).as_posix()
            data = named.as_posix() if len(named.parts) > 1 and (root / named).is_file() else beside
            if data not in found:
                found.append(data)
    return found


def _missing_data(command: str, scope: list[str], root: Path) -> list[str]:
    """The data files the check's tests read that `scope` does not hold."""
    return [rel for rel in _check_data_reads(command, root) if not _in_scope(rel, scope, root)]


def _tests_only_proof_note(command: str, scope: list[str], root: Path | None) -> str:
    """The proof note for a tests-only scope: the data file's absence where the scope
    or the check's tests hold one, else a defect in the module the test imports.

    Run R21 E76 said "mutate the module the test imports" of a test that imported
    none and read a tests/ data file, outside its scope.
    """
    reads = _check_data_reads(command, root) if root is not None and command else []
    if not _scope_has_data(scope, root) and not reads:
        return TESTS_ONLY_MUTATE_NOTE
    missing = [rel for rel in reads if not _in_scope(rel, scope, root)]
    if not missing:
        return TESTS_ONLY_PROOF_NOTE
    return (
        f"{TESTS_ONLY_PROOF_NOTE} The test this check runs reads {', '.join(missing)}, "
        f"which this scope does not hold: add it to the scope, "
        f"scope={json.dumps([*scope, *missing])}."
    )


def _joint_cases_route(command: str, scope: list[str], root: Path) -> str:
    """For a scope of tests only whose check runs a test importing a module that is not
    on disk: the route that writes that code and the test in one task; or "".

    q35 R59 L47-L53: T0003's scope held only tests/test_cases.py, which imports the
    unwritten itc. Told to mutate the module the test imports, or to name a new data
    test, it met prove's refusal of a WITNESS in a test file either way.
    """
    if not _only_data_and_tests(scope) or _scope_has_data(scope, root):
        return ""
    found = _imports_unwritten(command, scope, root)
    if found is None:
        return ""
    test, module = found[0], found[1]
    base = "src/" if (root / "src").is_dir() else ""
    scoped = json.dumps([test, f"{base}{module.split('.')[0]}/"])
    check = f'done_when="python3 -m pytest -q {test}"'
    write = f"Write {test} and the code it imports, `{module}`, in one task"
    return f"{write}: scope={scoped}, {check}."


def _data_test_imports_unwritten(data_check: str, scope: list[str], root: Path) -> str:
    """What the data test `data_check` runs must change when it imports unwritten code
    too, itself or through a sibling test; or "".

    Run R35 #10: the data test imported the cases test, which imported the unwritten
    module, and the data test was kept as the check that could pass.
    """
    found = _imports_unwritten(data_check, scope, root)
    return _import_chain_note(*found) if found is not None else ""


def _imports_unwritten_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check cannot pass on this scope because a test it runs imports unwritten
    code, naming the data-only test to bind instead; or None."""
    route = _data_test_route(command, scope, root)
    if route is None:
        return None
    test, module, data_check, needs = route
    neither = _data_test_imports_unwritten(data_check, scope, root)
    if neither:
        return (
            f"{test} fails with ImportError until a later task writes {module}, and no path "
            "in this scope creates it; neither it nor the data test can pass on this scope. "
            f"{neither} Then this task's check runs the data test only (`{data_check}`)."
            f"{_scope_note(needs, scope)} Call pursuit_step again with that, and that fix as "
            "notes."
        )
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

#: Setup acts that also open real work ('Create the clock type'): with one of
#: these, only a title naming beagle or the pursuit is setup.
_GENERIC_ACTS = frozenset({"create", "start"})


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
        # R118: 'Setup complete: beagle init written, pursuit founded …' named
        # the pursuit after its title only.
        names_setup = names_setup or (
            bool(words & _SETUP_ACTS - _GENERIC_ACTS)
            and bool(set(re.findall(r"[a-z]+", part.lower())) & _PURSUIT_NAMES)
        )
        if (words and words <= _SETUP_WORDS) or names_setup or ".beagle" in part:
            return (
                f"{title.strip()!r} is not part of the goal's work: pursuit_found is what "
                "sets the pursuit up, and it is done once it is founded. Leave it out. If "
                "the project itself needs a package layout, say so in the first part's "
                "intent, e.g. 'encoder::… in src/, with pyproject.toml'."
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
    if _lean():
        return None
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
        # R126 (g26 itc): 'Examine practical implementation patterns from <url>'
        # was kept as T0002, a study task, and took 22 of the 30 minutes.
        "examine",
        "inspect",
        "survey",
        "familiarize",
        "familiarise",
        "skim",
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
    """Whether milestone `part` already names the known answers or its cases."""
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
                "reads the reference in the task whose work needs it, and the design is part "
                "of the implementation, not a part of its own. Fold it into the part "
                "that uses it, and plan the parts that do the work."
            )
    return None


#: Words of a part that only lays the project out: run S05's 'Project
#: scaffolding' (pyproject.toml, package layout) was given the spec as its
#: source, so its cases had nothing to cite, and as a task it had nothing but an
#: import to check. R105's 'Environment setup' (uv, ruff, pytest), with no
#: source, had no check that could be shown to refuse.
_LAYOUT_WORDS = _SETUP_WORDS | frozenset(
    {
        "environment",
        "env",
        "dev",
        "development",
        "dependencies",
        "deps",
        "tools",
        "toolchain",
        "repository",
        "repo",
        "workspace",
        "scaffold",
        "scaffolding",
        "layout",
        "package",
        "packaging",
        "structure",
        "skeleton",
        "tooling",
        "pyproject",
        "initialization",
        "initialisation",
        "bootstrap",
        "bootstrapping",
    }
)
#: A step number ahead of a milestone's title: `1:`, `2.`, `3)`, `Step 2.`. R121's
#: '1: Project structure and setup — …' was read as the title '1'.
_STEP_NUMBER = re.compile(r"(?i)^\s*(?:step\s+)?\d+\s*[.:)]\s*")


def _layout_only_milestone(part: str) -> bool:
    """Whether milestone `part` only lays the project out, judged by its title.

    R123 (g26 cobs): 'Project initialization and environment setup.' stayed a
    task of its own and took 28 of the 30 minutes.
    """
    head = _STEP_NUMBER.sub("", _split_part(part)[0], count=1)
    title = re.split(r":| - | — ", head, maxsplit=1)[0]
    words = set(re.findall(r"[a-z]+", title.lower()))
    return bool(words) and words <= _LAYOUT_WORDS


def _fold_into_next(
    kept: list[str], only: Callable[[str], bool], kind: str, why: str
) -> tuple[list[str], list[str]]:
    """`kept` with each milestone `only` accepts folded into the next one's intent.

    Its text, less any source of its own, joins the following milestone's
    intent, or the one before it when none follows, ahead of that milestone's
    `Source:`, which must stay last (`_task_source`).
    """
    folded = list(kept)
    notes: list[str] = []
    index = 0
    while index < len(folded):
        part = folded[index]
        if len(folded) < 2 or not only(part):
            index += 1
            continue
        del folded[index]
        into = index if index < len(folded) else index - 1
        target = folded[into]
        # Split at '::' first: a part with no intent of its own is 'title::Source: x',
        # where the source follows '::' and not a space.
        title, _, intent = target.partition("::")
        cut = _SOURCE_IN_INTENT.search(intent)
        body, tail = (intent[: cut.start()], intent[cut.start() :]) if cut else (intent, "")
        own_title, _, own_intent = part.partition("::")
        own_intent = _SOURCE_IN_INTENT.sub("", own_intent).strip()
        text = f"{own_title.strip()}::{own_intent}" if own_intent else own_title.strip()
        merged = "; ".join(words for words in (body.strip(), text) if words)
        folded[into] = f"{title.rstrip()}::{merged}{tail}"
        notes.append(
            f"Folded the {kind} milestone {part.split(':', 1)[0].strip()!r} into "
            f"{target.split(':', 1)[0].strip()!r}: {why}"
        )
    return folded, notes


def _fold_design_milestones(kept: list[str]) -> tuple[list[str], list[str]]:
    """`kept` with each design-only milestone folded into the work after it.

    With known answers planned, a design milestone is part of the
    implementation.
    """
    return _fold_into_next(
        kept,
        _design_only_milestone,
        "design",
        "the design is part of the implementation, not a milestone of its own.",
    )


def _repair_milestones(milestones: list[str]) -> tuple[list[str], list[str]]:
    """`milestones` with what founding can fix fixed, and a note for each fix.

    A setup milestone and one that only re-runs a check are dropped, a
    design-only or layout-only milestone is folded into the next milestone's
    intent, a lone
    milestone that only reads the reference or chooses a design is retitled as
    the known answers, and an over-long title is cut at a word, its whole text
    moved after '::'. With
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
    # A milestone that only reads or designs is folded into the work after it:
    # the design is part of the implementation.
    kept, fold_notes = _fold_design_milestones(kept)
    notes.extend(fold_notes)
    kept, fold_notes = _fold_into_next(
        kept,
        _layout_only_milestone,
        "layout",
        "the files the code lives in are part of its first work, and a task that only "
        "lays them out has nothing to check.",
    )
    notes.extend(fold_notes)
    for index, part in enumerate(kept, 1):
        title, sep, intent = part.partition("::")
        title = title.strip()
        if len(kept) == 1 and _read_or_design_only(part):
            detail = f"{title} — {intent.strip()}" if sep and intent.strip() else title
            repaired.append(f"{KNOWN_ANSWERS_TITLE}::{detail}")
            notes.append(
                f"Milestone {index} {title!r} only reads the reference or chooses a "
                f"design, so it is now {KNOWN_ANSWERS_TITLE!r}, with its text after "
                "'::': a sub-agent reads the reference and writes its known answers "
                "as tests. The design is part of the implementation, not a milestone "
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


def _missing_program(program: str, root: Path) -> str:
    """Why a check's first word cannot be run in `root`, or "".

    R84: bound to `python -m pytest -q --co -q` where only python3 was on PATH,
    the check ran under systemd-run, which said "Failed to find executable
    python" and exited 1. That read as failing until the work was done, and two
    workers spent 32 minutes on a check no work could pass.
    """
    if "/" in program:
        path = Path(program) if Path(program).is_absolute() else root / program
        return "" if os.access(path, os.X_OK) else f"{program} is not a program here"
    if shutil.which(program):
        return ""
    near = [f"{program}3"] if shutil.which(f"{program}3") else []
    if os.access(root / ".venv" / "bin" / program, os.X_OK):
        near.append(f".venv/bin/{program}")
    if not near:
        return f"no `{program}` on PATH"
    return f"no `{program}` on PATH; {' and '.join(near)} {'are' if len(near) > 1 else 'is'}"


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
    missing = _missing_program(argv[0], root)
    if missing:
        return 127, f"the check could not start: {missing}"
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


def _absent_outside_scope(
    rc: int, output: str, scope: list[str] | None, root: Path | None
) -> list[str]:
    """The paths a pytest exit 4 found no file or directory at that are not on disk
    and outside `scope`: no worker on that scope may write them (run R40 class 4)."""
    if rc != 4 or not scope or root is None:
        return []
    found: list[str] = []
    for match in re.finditer(r"file or directory not found:\s*(\S+)", output):
        rel = _root_relative(match.group(1).split("::")[0].rstrip("/"), root)
        if rel is None:
            continue
        rel = os.path.normpath(rel)
        if rel not in found and not (root / rel).exists() and not _in_scope(rel, scope, root):
            found.append(rel)
    return found


def _absent_outside_scope_said(task: str, check: str, absent: list[str], scope: list[str]) -> str:
    """Why `check` cannot pass on `scope`: it exits 4 on `absent`, out of every worker's reach."""
    files = ", ".join(absent)
    return (
        f"`{check}` exits 4 on {files}, which is not on disk and outside {task}'s scope "
        f"({', '.join(scope)}). Writes outside the scope are refused, so no worker can "
        "write it, and the check cannot pass on this scope."
    )


def _check_broke(
    rc: int, output: str, scope: list[str] | None = None, root: Path | None = None
) -> str | None:
    """The first error line of a check run that could not run at all, or None.

    R13 bound `git diff --stat: x.md`, which exits 129 on the option before
    reading any file, and spent two workers on it. Exit 129 (git usage), 127
    (command not found), 2 or 64 with a `usage:` line, or a SyntaxError in an
    inline script mean no work can make the check pass; exit 1 is a check that
    fails, as it should before the work. Given the task's `scope` and `root`, so
    does pytest's exit 4 on a file not on disk and outside the scope (run R40
    class 4), and the line names that file and the scope.
    """
    absent = _absent_outside_scope(rc, output, scope, root)
    if absent and scope:
        return (
            f"file or directory not found: {', '.join(absent)}, which is not on disk and "
            f"outside the scope ({', '.join(scope)})"
        )
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
    "NEEDLE is text copied exactly from the file that occurs there only once, part of "
    "one line; the REPLACEMENT is the same text made wrong (a flipped condition, a "
    "wrong constant, a dropped step). The host puts it back and runs the check itself: "
    "a NEEDLE it cannot find once, or a defect the check misses, it tells you and asks "
    "for another.\n\n"
    "WITNESS: <path of the source file>\n"
    "NEEDLE:\n<exact text from the file>\n"
    "REPLACEMENT:\n<that text with the defect>\n"
    "END WITNESS"
)

#: Briefed to a worker on a task whose check an earlier step already made pass,
#: when only its WITNESS is still missing. R129 (g26 semver): the next worker
#: rewrote the passing module and regressed it. It must read, not rewrite.
WITNESS_PENDING_NOTE = (
    "An earlier sub-agent already made this task's check pass; its implementation "
    "is on disk and working. The only thing left is the WITNESS. Do NOT rewrite, "
    "refactor or otherwise change the implementation — leave it exactly as it is. "
    "Read it, then end your report with a WITNESS block below, naming one real "
    "defect (a NEEDLE that occurs there exactly once) in the module the check's "
    "test imports. If no test the check runs would catch that defect yet, add that "
    "one test case, and change nothing else."
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
#: The `--predates-because` for putting back a scope file's content at the open.
REVERSION_BECAUSE = (
    "the file was in the tree when this task opened, and an attempt at this task "
    "changed it; putting back its content at the open shows the check needs that change"
)
#: A scope file larger than this, now or at the open, is not put back by `prove`.
REVERSION_MAX_BYTES = 512 * 1024
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


#: A traceback frame pytest prints for a test module's import: `path:line: in <module>`
#: and, indented below it, the line that ran.
_MODULE_FRAME = re.compile(r"^(\S+\.py):(\d+): in <module>\n[ \t]+(\S.*)$", re.MULTILINE)
#: The exception line of a pytest error report: `E   ModuleNotFoundError: …`.
_ERROR_LINE = re.compile(r"^E\s+(\w+(?:Error|Exception)\b.*)$", re.MULTILINE)
#: Said whenever a data-and-tests task's own check fails at collection.
DATA_CHECK_IMPORT_DEFECT = (
    "The bound check must pass now; an ImportError from it is a defect, not the "
    "pre-implementation state."
)


def _collection_failure_lead(output: str, scope: list[str], root: Path) -> str:
    """The line a not-done result leads with when its check failed at collection,
    naming the import and file that broke it; else "".

    Run R35: every result led with a runner in tests/test_cases.py, which the
    check reached only through an import that failed before anything ran.
    """
    outcomes = _PYTEST_OUTCOME.findall(output)
    if not outcomes or any(kind != "ERROR" for kind, _ in outcomes):
        return ""
    if _IMPORT_FAILURE.search(output) is None and "ERROR collecting" not in output:
        return ""
    chain = []
    for path, line, code in _MODULE_FRAME.findall(output):
        rel = _root_relative(path, root)
        if rel is not None and (root / rel).is_file():
            chain.append(f"{rel}:{line} `{code.strip()}`")
    error = _ERROR_LINE.search(output)
    said = " → ".join([*chain, *([error.group(1).strip()] if error else [])])
    if not said:
        return ""
    where = (
        " Nothing in these files runs until that import succeeds: fix the import, not "
        "what would run after it."
        if chain
        else ""
    )
    defect = (
        f" {DATA_CHECK_IMPORT_DEFECT}"
        if _scope_has_data(scope, root) and _only_data_and_tests(scope)
        else ""
    )
    return f"The check fails at collection, before any test runs: {said}.{where}{defect}\n\n"


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
        if _in_scope(rel, scope, root) and (root / rel).is_file() and (runs is None or rel in runs)
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
        # Run R16: run_case only dispatched the data file's ops to the module, and
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
        f"{lead} Call pursuit_step task={json.dumps(task)}, "
        f"done_when={json.dumps(_suggested_check(done_when, root))}, "
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


def _pytest_selection(check: str) -> str:
    """The `-k` or `-m` selection a pytest check passes, as `-k 'expr'`, or ''.

    Only words after the pytest word count, so `python3 -m pytest` is no selection.
    """
    words = _check_words(check)
    start = next(
        (i + 1 for i, word in enumerate(words) if Path(word).name in ("pytest", "py.test")),
        None,
    )
    if start is None:
        return ""
    for i in range(start, len(words)):
        word = words[i]
        for flag in ("-k", "-m"):
            if word == flag and i + 1 < len(words):
                return f"{flag} {shlex.quote(words[i + 1])}"
            if word.startswith(flag) and len(word) > len(flag):
                return f"{flag} {shlex.quote(word[len(flag) :].removeprefix('='))}"
    return ""


def _selected_none(rc: int, output: str, check: str) -> str:
    """The selection of a pytest check that ran no test because the selection
    deselected every test it collected (exit 5 with an `N deselected` count), or ''."""
    if rc != 5 or not re.search(r"\b\d+ deselected\b", output):
        return ""
    return _pytest_selection(check)


#: A `-k` expression's words: parentheses, the boolean operators, and name parts.
_K_TOKEN = re.compile(r"\s*(\(|\)|[^\s()]+)")


def _k_matches_none(check: str, root: Path) -> str:
    """The `-k` selection of a pytest check that no test in the files it runs can
    match, read from their source, or '' when one may (or it cannot be told).

    pytest matches each name in the expression, case-blind, as a substring of a
    test's own name, its class's, its file's and its directories'; decorator names
    count too, so a marker or keyword match is never ruled out.
    """
    selection = _pytest_selection(check)
    if not selection.startswith("-k "):
        return ""
    expr = shlex.split(selection)[1]
    tokens = _K_TOKEN.findall(expr)
    if not tokens or any("[" in tok for tok in tokens):
        return ""
    items: list[set[str]] = []
    for rel in _check_test_files(check, root):
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            return ""
        base = {*Path(rel).parts, Path(rel).stem}
        for node in tree.body:
            funcs = ast.FunctionDef | ast.AsyncFunctionDef
            found: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, ast.ClassDef | None]] = (
                [(node, None)] if isinstance(node, funcs) else []
            )
            if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                found = [(sub, node) for sub in node.body if isinstance(sub, funcs)]
            for func, cls in found:
                if not func.name.startswith("test"):
                    continue
                marks = [
                    n.id if isinstance(n, ast.Name) else n.attr
                    for owner in (func, cls)
                    if owner is not None
                    for deco in owner.decorator_list
                    for n in ast.walk(deco)
                    if isinstance(n, ast.Name | ast.Attribute)
                ]
                items.append({func.name, *([cls.name] if cls else []), *base, *marks})
    if not items:
        return ""
    for names in items:
        folded = [name.lower() for name in names]
        parts = [
            tok
            if tok in ("(", ")", "and", "or", "not")
            else str(any(tok.lower() in name for name in folded))
            for tok in tokens
        ]
        try:
            if _truth(ast.parse(" ".join(parts), mode="eval").body):
                return ""
        except (SyntaxError, ValueError):
            return ""
    return selection


def _truth(node: ast.expr) -> bool:
    """The value of an expression of True, False, `and`, `or` and `not` only."""
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _truth(node.operand)
    if isinstance(node, ast.BoolOp):
        values = [_truth(value) for value in node.values]
        return all(values) if isinstance(node.op, ast.And) else any(values)
    raise ValueError(ast.dump(node))


def _without_selection(check: str, selection: str) -> str:
    """`check` with its `selection` (`-k 'expr'` or `-m 'expr'`) cut from its words,
    or '' when the selection is not one of its top-level words."""
    flag, expr = shlex.split(selection)
    try:
        words = shlex.split(check)
    except ValueError:
        return ""
    for i, word in enumerate(words):
        if word == flag and i + 1 < len(words) and words[i + 1] == expr:
            return shlex.join(words[:i] + words[i + 2 :])
        if word in (f"{flag}{expr}", f"{flag}={expr}"):
            return shlex.join(words[:i] + words[i + 1 :])
    return ""


def _suggested_check(check: str, root: Path) -> str:
    """`check` as a refusal echoes it in a call it suggests: without a `-k` that
    matches no test in the files it runs, when that can be cut from its words.

    Run R43: a scope refusal echoed `-k "test_cobs_impl"` back, the open bound it,
    and it deselected all five tests of the file.
    """
    selection = _k_matches_none(check, root)
    return (_without_selection(check, selection) if selection else "") or check


def _selected_none_refusal(check: str, selection: str, task: str) -> str:
    """Why an open refuses a check whose selection deselected every test it collected."""
    without = _without_selection(check, selection)
    call = (
        f" Without it: pursuit_step task={json.dumps(task)}, done_when={json.dumps(without)}."
        if without
        else ""
    )
    return (
        f"`{check}` exits 5 before any work because `{selection}` deselected every test "
        "it collected, so no test ran: it fails for its selection, not for want of "
        f"{task}'s work. Bind a check that runs the tests: without `{selection}`, or "
        f"with a selection naming a test the file defines.{call}"
    )


def _pytest_collected_none(rc: int, check: str, output: str = "") -> str | None:
    """The lead for a pytest check that exited 5 (no tests collected), or None.

    Run R17 showed T0009's `exit 5: no tests ran` raw, beside "Fix the work, not
    the check", to the driver and to three workers. Exit 5 is pytest's own code
    for an empty collection, so the test files the check names are not written yet;
    unless its `output` counts tests deselected: then its selection matched none
    (run R43 was told the file defined no test_ function when it defined five).
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
    selection = _selected_none(rc, output, check)
    if selection:
        return (
            f"pytest ran no test from {named}: it collected tests, and `{selection}` "
            "deselected every one. The check runs only a test that selection matches; "
            "with none, it runs nothing."
        )
    return (
        f"pytest collected no tests from {named}: it defines no test_ function; adding "
        "them is the work, not a different check."
    )


_COLLECT_ONLY = re.compile(r"(?<![\w-])--(?:collect-only|co)(?![\w-])")


def _amend_problem(check: str, bound: str) -> str | None:
    """Why `check` may not replace a task's bound check, judged before it runs.

    Run R17 #26 swapped T0008's check, which loaded a tests/ data file, for
    `pytest --collect-only -q tests/`, which passed before any work.
    """
    keep = (
        f" Keep the bound check `{bound}`: leave done_when out to keep it."
        if _keepable(bound)
        else ""
    )
    if _COLLECT_ONLY.search(check):
        return (
            f"`{check}` runs pytest --collect-only, which only imports the tests and runs "
            f"none, so it passes whatever the work does.{keep}"
        )
    return None


def _cwd_relative_data_lead(output: str, scope: list[str], root: Path) -> str:
    """The line a not-done result leads with when a test opened scoped data by a bare name.

    Run R15: tests/test_case_data.py ran `open("<data>.json")`; the check runs from
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


def _root_relative_scope(scope: list[str], root: Path) -> tuple[list[str], str | None]:
    """`scope` with absolute entries under `root` made root-relative, or why one is refused."""
    entries: list[str] = []
    for entry in scope:
        rel = _root_relative(entry, root)
        if rel is None:
            return scope, (
                f"pursuit_step: scope entry {entry} is outside the project root {root}. "
                f"Scope names paths in the project, relative to {root} "
                '(e.g. "src/module.py"); call pursuit_step again with those.'
            )
        entries.append(rel)
    return entries, None


def _in_scope(rel: str, scope: list[str], root: Path | None = None) -> bool:
    if not scope:
        return True
    if root is not None:
        scope = [e for e in (_root_relative(s, root) for s in scope) if e is not None]
    return any(rel == s.rstrip("/") or rel.startswith(s.rstrip("/") + "/") for s in scope)


def _scope_data(scope: list[str], root: Path | None = None) -> list[str]:
    """The data files `scope` names (a suffix other than .py) and, given `root`, the
    cases data files on disk under a directory entry.

    Run R44 T0002: the scope was ['tests/'], the cases data sat under it, and only
    file entries were counted, so the data test's unwritten import went unnamed.
    """
    found: list[str] = []
    for entry in scope:
        rel = entry.rstrip("/")
        if Path(rel).suffix not in {"", ".py"}:
            found.append(rel)
        elif root is not None and (root / rel).is_dir():
            for path in sorted((root / rel).rglob("*")):
                with contextlib.suppress(ValueError):
                    under = path.relative_to(root).as_posix()
                    if path.is_file() and _is_test_data(under) and under not in found:
                        found.append(under)
    return found


def _scope_has_data(scope: list[str], root: Path | None = None) -> bool:
    """Whether `scope` names a data file (a file with a suffix other than .py) or,
    given `root`, holds a cases data file under a directory entry."""
    return bool(_scope_data(scope, root))


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


def _attempts_past_limit(task: str, nodes: list[dict[str, Any]]) -> str:
    """`task`'s retry chain and how many attempts it holds against beagle's limit.

    q35 10-11: "is at beagle's limit of 3 attempts" was said of a chain of 4, and
    "holds 3 attempt(s), below beagle's limit of 3" of one of 3; beagle refuses a
    new route only once a chain holds more than the limit (`_at_spawn_limit`).
    """
    chain = sorted(_retry_chain(task, nodes))
    held = f"{len(chain)} attempt" + ("" if len(chain) == 1 else "s")
    named = f"retry chain ({', '.join(chain)}) holds {held}"
    if len(chain) > SPAWN_LIMIT:
        return f"{named}, past beagle's limit of {SPAWN_LIMIT}"
    return (
        f"{named}, and beagle refuses a new route only once a chain holds more than {SPAWN_LIMIT}"
    )


def _spawn_limit_offer(
    task: str, check: str, scope: list[str], nodes: list[dict[str, Any]], why: str = ""
) -> str:
    """What a result says for `task` at beagle's spawn limit: no new route, and the
    infeasible close to make instead, said to seal the parent (`_seal_warning`).

    _close_infeasible refuses a task that is not open, so a task the tree shows
    closed already (blocked, say) is offered the parent's re-plan alone. A pending
    one keeps the close: the tree was read before this step opened it.
    """
    attempts = _attempts_past_limit(task, nodes)
    replan = _replan_parent_call(task, nodes)
    node = next((n for n in nodes if str(n.get("id")) == task), {})
    status = str(node.get("status") or "")
    if status not in {"", "open", "pending"}:
        return f"{task} is {status}, and its {attempts}, so beagle refuses a new route " + (
            f"for it. Re-plan its parent instead: {replan}."
            if replan
            else "for it, and it has no parent to re-plan: stop and ask the user."
        )
    return (
        f"Its {attempts}, so beagle refuses a new route. Close it infeasible instead: "
        f"{_infeasible_call(task, check, scope, why)}. "
        + _seal_warning(task, str(node.get("parent") or ""))
    ).rstrip()


def _pending_route_said(task: str, done_when: str, scope: list[str], criteria: str) -> str:
    """What a spawn refused for a pending `task` says: a new route is for a route
    tried, so the call drops new_route and opens it.

    q35 10-11: T0012 was pending, and four new_route calls were each told to say
    in notes how the route differs, which no notes get past.
    """
    call = f"pursuit_step task={json.dumps(task)}"
    if criteria:
        call += f", criteria={json.dumps(criteria, ensure_ascii=False)}"
    if done_when:
        call += f", done_when={json.dumps(done_when)}"
    if scope:
        call += f", scope={json.dumps(scope)}"
    return (
        f"{task} is pending, never opened, so it has no route to replace and notes do not "
        f"change that. Drop new_route and open it with the same values: {call}."
    )


def _seal_warning(task: str, parent: str) -> str:
    """What an offer of `task`'s infeasible close says first: it seals `parent`.

    q35 10-11: the offer read as a normal exit, followed by a re-plan of the
    parent; T0011's close sealed T0002, and every part planned under it after
    was futile.
    """
    if not parent:
        return ""
    return (
        f"That close seals {parent}: {task} would end undone with no task holding its "
        f"work, and beagle still counts such a leaf in {parent}, so {parent} could never be "
        f"all-done, nor what waits on it, and no part planned under it would change "
        f"that; only the owner could then re-scope or abandon {parent}. If {parent}'s "
        "work still matters, stop instead, and ask the user."
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
    elif tests_only and _scope_has_data(scope, root):
        data = _scope_data(scope, root)[0]
        test = next(
            (t for t in tests if _test_reads_file(root / t, Path(data).name)),
            _data_test("", scope, root),
        )
        done_when, added = f"python3 -m pytest -q {test}", [test]
        notes = f"New route: {test} fails once {data} is taken away"
    elif tests_only:
        base = "src/" if (root / "src").is_dir() else ""
        for test in tests:
            found = _imported_modules(root, [test]) or [
                f"{base}{name.replace('.', '/')}.py" for name in _test_project_imports(root / test)
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
            and _scope_has_data(scope, root)
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
    #: A tests-only task had no WITNESS in the module its tests import, or taking
    #: a source away failed the check only on its import; named in `text`:
    #: another worker can give one, so the task is not unproven.
    ask_module: bool = False
    #: Proven only by taking away a source file: that shows the check needs the
    #: import, not that it tests the behaviour.
    by_absent_source: bool = False


def _opened_commit(task: str, root: Path, record: Any = None) -> str:
    """The commit `task` opened on: its record's, else the parent of its first
    commit, else HEAD; "" when git has none. `record` is `task`'s, when read."""
    if record is None:
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


def _check_scripts(check: str, root: Path) -> set[str]:
    """The files `check` runs as its own program: the script it gives Python or a
    shell, a file it runs by path, a .py it gives pytest; not the files it reads.

    q38fn 10-11 T0011: with tests/check_known_answers.py taken away, the check
    `python3 tests/check_known_answers.py` failed on the missing file alone.
    """
    try:
        tokens = [
            part
            for word in shlex.split(check)
            for part in (shlex.split(word) if " " in word and not word.startswith("-") else [word])
        ]
    except ValueError:
        return set()
    run = tokens[:1]
    for at, token in enumerate(tokens):
        name = Path(token).name
        if _PYTHON_NAME.fullmatch(name):
            run.append(_python_script(tokens[at + 1 :]) or "")
        elif name in _SHELLS:
            run += [arg for arg in tokens[at + 1 : at + 2] if not arg.startswith("-")]
    if any(Path(token).name in {"pytest", "py.test"} for token in tokens):
        run += [token for token in tokens if token.split("::")[0].endswith(".py")]
    found = (os.path.normpath(token.split("::")[0]) for token in run if token)
    return {
        rel
        for rel in found
        if not Path(rel).is_absolute() and ".." not in Path(rel).parts and (root / rel).is_file()
    }


def _check_reads(check: str, rel: str, root: Path) -> bool:
    """Whether `check` reads the file `rel`: its words name it, or a .py it runs opens it."""
    if not check:
        return False
    rel = os.path.normpath(rel)
    reach = [os.path.normpath(found) for found in _check_reach(check, root)]
    return rel in reach or any(
        found.endswith(".py") and _test_reads_file(root / found, Path(rel).name) for found in reach
    )


#: The `prove` flags whose next argument is a site the witness changes.
SITE_FLAGS = frozenset({"--absent", "--mutate"})

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


async def _run_prove(argv: list[str], root: Path, timeout: float) -> tuple[int, str]:
    """Run a `beagle pursuit prove` argv, in a scratch copy when beagle says so.

    beagle 0.48 refuses a prove in this checkout while another worker is live in
    the loop (a background dispatch's wait, `beagle loop tick --awaiting`): the
    defect put back would be read by that worker as its own failure. Its refusal
    ends `next: beagle pursuit prove <task> --isolated …`, and the prove is run
    again so, with `--isolated` added to `argv` for any later run of it.
    """
    rc, out = await asyncio.to_thread(_run, _capped(argv, _memory_max()), root, 2 * timeout + 120)
    if rc != 0 and "--isolated" not in argv and "--isolated" in _beagle_next(out).split():
        argv.append("--isolated")
        rc, out = await asyncio.to_thread(
            _run, _capped(argv, _memory_max()), root, 2 * timeout + 120
        )
    return rc, out


async def _prove(
    task: str,
    report: str,
    scope: list[str],
    root: Path,
    timeout: float,
) -> _Proof | None:
    """Ask `beagle pursuit prove` whether the passing check can refuse at all.

    A check that passes over a defect put back into the work is not about the
    work: run 11d closed two tasks on import-only checks. The worker names the
    defect (`WITNESS_NOTE`); a missing or misshapen one falls back to taking
    away the source files the task changed that were not in the tree when it
    opened, or with none, its data files. Last, each source file in scope that
    changed since the task opened is put back as the open held it, so a change
    an earlier, stopped attempt made is judged too. None
    when neither can be tried — no witness and no changed file — and the close
    decides.

    q38fn 10-11 T0011: the witness in a tests/ data file was refused as a test
    file, and the fallback took away tests/check_known_answers.py, the check's
    own script, so the check failed only on a missing file. The cases data the
    check reads is a site; a script the check runs is never taken away, and a
    witness in one under tests/ is refused (one elsewhere may be the program
    under test). A file the check only reads (`grep -q out tests/data.json`)
    is the work, and may be taken away.
    """
    attempts: list[list[str]] = []
    refused: list[str] = []
    witness = _witness(report)
    rc, out = _pursuit(["show", task], root)
    shown = _json_reply(out) if rc == 0 else None
    record = shown if isinstance(shown, dict) else {}
    check = str(record.get("done_when") or "").strip()
    scripts = _check_scripts(check, root)
    data_witness = (
        witness is not None and _is_test_data(witness[0]) and _check_reads(check, witness[0], root)
    )
    in_test = witness is not None and _is_test_path(witness[0]) and not data_witness
    modules = _imported_modules(root, scope) if _only_data_and_tests(scope) else []
    ask_module = bool(modules) and (witness is None or in_test)
    if ask_module:
        # Run R12: a tests-only task's witness in its test was refused, and it
        # had no source of its own to take away; the module it tests has one.
        where = f"{witness[0]}: the WITNESS is in a test file. " if witness else ""
        refused.append(
            f"{where}Give a WITNESS in {' or '.join(modules)}, the module the test imports: "
            "a NEEDLE there that the test must catch. Leave the test as it is."
        )
    elif in_test:
        # Run R04: W24's witness was in tests/test_case_data.py, and beagle
        # answered about the needle's count, not the check.
        refused.append(
            f"{witness[0]}: the WITNESS is in a test file; name a defect in the code the "
            "test runs, and leave the test as it is."
        )
    elif (
        witness is not None
        and os.path.normpath(witness[0]) in scripts
        and _in_tests_dir(witness[0])
    ):
        refused.append(
            f"{witness[0]}: the WITNESS is in the check's own script, `{check}`; changed, "
            "it makes the check fail whatever the work is, which proves nothing. Name a "
            "defect in what the script judges: the data it reads or the code it runs."
        )
    elif witness is not None:
        path, needle, replacement = witness
        attempts.append(["--mutate", path, "--needle", needle, "--replacement", replacement])
    mutated = attempts[-1] if witness is not None and attempts else None
    opened = _opened_commit(task, root, record or None)
    changed = _changed_files(root)
    # T0600: a worker that committed its work leaves git status clean; what
    # changed since the open is the task's work all the same.
    since = _run(["git", "diff", "--name-only", "--no-renames", opened, "--"], root, 30.0)
    committed = since[1].splitlines() if opened and since[0] == 0 else []
    committed = [rel for rel in committed if rel and Path(rel).parts[0] != ".beagle"]
    # q35 10-11: what the parent's split committed is this part's work.
    carried = _split_carried(task, root)
    changed = list(dict.fromkeys([*changed, *committed, *carried.files]))
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
        sources = [rel for rel in sources if not _in_commit(carried.base(rel, opened), rel, root)]
    sources = [rel for rel in sources if os.path.normpath(rel) not in scripts]
    if sources:
        attempts.append([arg for rel in sources for arg in ("--absent", rel)])
    # R95: a contract task's first worker hit the wall with contract/contract.json,
    # tracked before the task opened, edited so the check passed; the next
    # worker changed nothing and gave no WITNESS, and nothing was new to take
    # away. Putting back what changed since the open judges the task's change,
    # not only the last worker's.
    reversion = _open_reversion(opened, scope, root, carried, scripts)
    if reversion:
        attempts.append(reversion)
    still_passes = ""
    for how in attempts:
        argv = [BEAGLE_BIN, "pursuit", "prove", task, *how, "--check-timeout", f"{timeout:.0f}"]
        rc, out = await _run_prove(argv, root, timeout)
        sites = [
            os.path.normpath(how[at + 1]) for at, arg in enumerate(how[:-1]) if arg in SITE_FLAGS
        ]
        split_work = bool(sites) and set(sites) <= set(carried.files)
        if rc != 0 and "--predates-because" in out and ("--mutate" in how or split_work):
            # A task that adds tests for code an earlier task wrote: its
            # witness is a defect in that code, which beagle takes when said.
            # A part's witness in what its parent's split committed is its own.
            because = (
                carried.because(task)
                if split_work
                else REVERSION_BECAUSE
                if how is reversion
                else PREDATES_BECAUSE
            )
            argv += ["--predates-because", because]
            rc, out = await _run_prove(argv, root, timeout)
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
                # q35 R55: the check's test imports that code, so the next worker
                # can give that WITNESS on this check; no new route is needed.
                ask_module = True
                continue
            return _Proof(proven=True, text=tail, by_absent_source=by_absent_source)
        if verdicts.get(task) == "NOT PROVEN" and "STILL PASSES" in out:
            if how is mutated and (
                (not _in_scope(how[1], scope, root) and os.path.normpath(how[1]) not in changed)
                or os.path.normpath(how[1]) in {os.path.normpath(rel) for rel in sources}
            ):
                # q35 R54: W5's witness in cobs/__init__.py, outside T0005's scope
                # [pyproject.toml], still passed ruff, and that ended the attempts
                # before the absence of pyproject.toml, which would have proven.
                # R97: T0005's witness in src/semver/__init__.py, a file the task
                # wrote, still passed a file-existence check, and a second worker
                # was sent; taking that file away is tried next, and that proved.
                still_passes = tail
                continue
            # The check passed over the defect: a real answer, not one a
            # different witness should be asked to overturn.
            return _Proof(proven=False, text=tail, weak=True)
        refused.append(tail)
    if still_passes:
        return _Proof(proven=False, text=still_passes, weak=True)
    if ask_module:
        return _Proof(proven=False, text="\n\n".join(refused), ask_module=True)
    if not attempts and not refused:
        if not _requires_witness(root):
            return None
        return _Proof(
            proven=False,
            text="The worker gave no WITNESS block, and no source file in the task's "
            "scope has changed since it opened: none is new that could be taken away, "
            "and none was edited that could be put back as it was.",
        )
    return _Proof(proven=False, text="\n\n".join(refused))


def _open_reversion(
    opened: str, scope: list[str], root: Path, carried: _SplitCarry, scripts: set[str]
) -> list[str] | None:
    """`prove` arguments putting each source file in `scope` that changed since the
    task opened back as the open held it: the task's whole change, whichever
    attempt made it. None when no such file can be put back.

    A test, the check's own script, a file new since the open (taken away with
    `--absent` instead), and a binary or oversized file are left out.
    """
    if not opened:
        return None
    rc, out = _run(["git", "diff", "--name-only", "--no-renames", opened, "--"], root, 30.0)
    argv: list[str] = []
    for rel in out.splitlines() if rc == 0 else []:
        path = root / rel
        if (
            not rel
            or Path(rel).parts[0] == ".beagle"
            or _CACHE_DIRS & set(Path(rel).parts)
            or not _in_scope(rel, scope, root)
            or _is_test_path(rel)
            or os.path.normpath(rel) in scripts
            or not path.is_file()
        ):
            continue
        with contextlib.suppress(OSError):
            if path.stat().st_size > REVERSION_MAX_BYTES:
                continue
        was = _committed_bytes(root, carried.base(rel, opened), rel)
        if was is None or len(was) > REVERSION_MAX_BYTES:
            continue
        try:
            edit = _reversion_edit(path.read_text(encoding="utf-8"), was.decode("utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if edit is not None and "\0" not in edit[0]:
            argv += ["--mutate", rel, "--needle", edit[0], "--replacement", edit[1]]
    return argv or None


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
    opened" and "T0008 not opened": the spawn that superseded each was lost. It
    says `successor` was not opened only of an open refusal.
    """
    text = "".join(getattr(c, "text", "") for c in result.content)
    if spawned.strip() and spawned.strip() in text:
        return result
    if (
        f"pursuit_step: {successor} not opened — " not in text
        and "pursuit_step: `beagle pursuit open` refused" not in text
    ):
        # q35 R58 L25: T0007 opened, and its worker was killed at its wall.
        return _step_result(f"{predecessor} was superseded by {successor} (new route).\n\n{text}")
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


#: beagle's brief's aside on its Scope line, and what tau says instead. Run R40
#: class 4: W13 read the aside as leave to write outside the scope, which the
#: worker guard refuses.
_SCOPE_ASIDE = "(paths changed outside it are named at close)"
_SCOPE_REFUSED = "(writes outside it are refused)"


def _without_beagle_habits(brief: str, bound: str | None = None) -> str:
    """beagle's brief without the lines that tell a worker to run `beagle`.

    The worker guard refuses every `beagle` command. Run R06: W2 and W4 ran the
    "Working habits" line's `RUN_CONTAINED_FOREGROUND=1 beagle contain run heavy
    -- …` and were refused. That line is said again with a plain capped,
    redirected command; the standing-checks line (`beagle pursuit recheck`) is
    dropped, and the `beagle pursuit show` aside is cut. `bound` is the
    command's prefix, from `_command_bound` (by default for no memory cap and
    the default dispatch timeout). Run R39: the line says what exit 124 means.
    The Scope line says writes outside it are refused (`_SCOPE_REFUSED`).
    """
    if bound is None:
        bound = _command_bound(None, DEFAULT_DISPATCH_TIMEOUT)
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
                f'echo "exit $?"`), then read the tail of {log}. Exit 124 means the command '
                f"did not finish: {HANG_MEANING}{alone}{ending}"
            )
        elif "beagle pursuit recheck" in line:
            continue
        else:
            lines.append(_SHOW_ASIDE.sub("", line).replace(_SCOPE_ASIDE, _SCOPE_REFUSED))
    return "".join(lines)


#: The paths of a brief's Scope line, up to its aside.
_BRIEF_SCOPE_PATHS = re.compile(r"^Scope: .*?(?= \(|$)", re.M)


def _brief_in_scope(brief: str, scope: list[str]) -> str:
    """The brief with its Scope line naming `scope`, the paths the worker guard holds.

    q35 R52: the call's scope held cobs/__init__.py, and W8's brief named only the
    record's "Scope: tests/test_edge_cases.py (writes outside it are refused)".
    """
    return _BRIEF_SCOPE_PATHS.sub(lambda _: f"Scope: {' '.join(scope)}", brief)


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


#: What the auditing sub-agent is told beyond beagle's audit brief, which itself
#: says to change nothing and to end the closes on a SOUND or DEFECTS line.
AUDIT_NOTE = (
    "\n\nDo not run `beagle pursuit audit`: the session that sent you records what you report."
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
    pin = _dispatch_pin(REVIEWER_ROLE, root)
    model, provider = _worker_target(pin=pin)
    run = await _run_worker(
        brief + AUDIT_NOTE,
        root,
        model,
        provider,
        _worker_wall(root, model, provider),
        signal,
        thinking=_worker_thinking(model, provider, pin=pin),
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
    _forget_task(root, task)
    released = _release_waiters(task, why, root)
    freed = f"\nNo longer waiting on it: {', '.join(released)}." if released else ""
    _, then = _relay_next(out, "Next: call pursuit_step with no arguments for the next task.")
    return (
        f"{out.splitlines()[0] if out else task + ' abandoned'}{freed}\n\n{_tree(root)}\n\n{then}"
    )


#: An abandon that closes a task infeasible, with the evidence after the colon.
_INFEASIBLE = re.compile(r"(?is)^\s*infeasible\s*:\s*(.*)$")


def _open_pending_said(task: str, node: Mapping[str, Any]) -> str:
    """How an infeasible close refused for pending `task` says to open it.

    q35 10-11: T0024's open was refused at 12:17:31 as already passing, and at
    12:17:47 this said "Work it first: pursuit_step task=T0024", the same call.
    """
    bound = " ".join(str(node.get("done_when") or "").split())
    passing = f", so if its bound `{bound}` passes now, give another" if bound else ""
    return (
        f' Open it first with pursuit_step task="{task}" and a done_when that fails now: '
        f"an open on a check that already passes is refused{passing}. If a done task's "
        f'commit did its work, pursuit_step task="{task}", abandon="done by Tnnnn" and '
        "done_when, naming that task, closes it done on that commit instead."
    )


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
            + (_open_pending_said(task, node) if node.get("status") == "pending" else "")
        )
    if not _at_spawn_limit(task, nodes) and not _source_reruns_spent(task, root):
        # Run R40: a task the source judge alone held past its reruns is offered
        # this close, whatever its retry chain.
        return (
            f"pursuit_step: {task} not closed infeasible — its "
            f"{_attempts_past_limit(task, nodes)}, so a hard task is not yet shown "
            "infeasible. Call instead: "
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
    _forget_task(root, task)
    parent = str(node.get("parent") or "")
    # q35 10-11: this said to re-plan T0002 once T0011 closed, and the parts
    # planned under it could never make it done.
    closed = [{**n, "status": "infeasible"} if str(n.get("id")) == task else n for n in nodes]
    next_move = (
        _sealed_text(parent, [task], closed, now=True)
        if task in _sealed(closed).get(parent, [])
        else _relay_next(out, "Next: call pursuit_step with no arguments for the next task.")[1]
    )
    return (
        f"{out.splitlines()[0] if out else task + ' closed infeasible'}\n\n"
        f"{_tree(root)}\n\n{next_move}"
    )


#: Open tasks whose passing check `prove` could not show to refuse, by (project
#: root, task). A further step on the task runs no worker, whatever check or
#: scope it is sent with: run R04's driver got past a (check, scope) key by
#: changing the scope. A new route or a plan of the task clears it.
_UNPROVEN: set[tuple[str, str]] = set()

#: Tasks whose check passed in an earlier step but whose witness was not yet
#: accepted (ask_module), so the step ended before it could be witnessed in the
#: same worker. R129 (g26 semver): such a task's next step spawned a fresh
#: worker that rewrote the passing implementation and regressed it from 75/76 to
#: 27/76. The next worker on it is told the implementation passes and to add
#: only the WITNESS, not to rewrite it; the note is consumed when briefed.
_WITNESS_PENDING: set[tuple[str, str]] = set()

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


#: Output that names a failure: a traceback, an error or assertion, a failing test
#: or case, or a printed non-empty list.
_FAILURE_NAMED = re.compile(
    r"traceback|error|exception|assert|fail|mismatch|expected|missing|wrong|invalid|!="
    r"|\[\s*[^\]\s]",
    re.IGNORECASE,
)


def _fix_the_work(rc: int, output: str, check: str) -> str:
    """The retry note's last line for a check that failed with `rc` and `output`.

    Run R44: over "unsourced: []" from an inverted check, W9's brief said "Fix the
    work, not the check", and no work could have made it pass.
    """
    if rc == 124 or _pytest_collected_none(rc, check, output) or _FAILURE_NAMED.search(output):
        return "Fix the work, not the check."
    return (
        "The check fails, but its output names no failing case or test: read what the "
        "check tests. If the work already meets it, say so in your report, with the "
        "line of the check that fails it."
    )


def _last_failure_note(key: tuple[str, str], check: str) -> str:
    """The brief note for a step's first worker when the task's check last failed."""
    last = _LAST_CHECK_FAILURE.get(key)
    if last is None or not check or last[0] != check:
        return ""
    _, rc, tail = last
    no_tests = _pytest_collected_none(rc, check, tail)
    return (
        (f"\n\n{no_tests}" if no_tests else "")
        + f"\n\nThe check failed last step (exit {rc}). Its output ends:\n{tail}\n"
        + _fix_the_work(rc, tail, check)
    )


def _close_demand(text: str) -> str:
    """The demand of a result whose check passed but whose close kept the task open:
    the file and defect the close found, then its "the sub-agent must …" clause; else
    the reason after "the check passes, but".

    Run R35: only the clause after "the sub-agent must " reached the rerun, so
    W8 and W9 never heard that tests/test_cases.py defined no test function.
    """
    for para in text.split("\n\n"):
        _, passes, reason = para.partition("the check passes, but ")
        if not passes:
            continue
        if reason.startswith("the task "):
            reason = reason.partition(": ")[2] or reason
        found, must, demand = reason.partition("the sub-agent must ")
        if must and found.strip():
            return f"{found.strip()} {demand.strip()}"
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
#: The data file and cases the close's source judge named when it last kept the
#: task open, by (project root, task). Run R40: only that judge held T0002, and
#: the escalation offered a split by file, which cannot change a case.
_NOT_DONE_CASES: dict[tuple[str, str], tuple[str, tuple[str, ...]]] = {}
#: Tasks a not-done step left with their check failing, by (project root, task),
#: with the not-done count at the first such step since the check last passed.
_NOT_DONE_CHECK_FAILED: dict[tuple[str, str], int] = {}
#: Tasks whose `_NOT_DONE_CHECK_FAILED` record a later step's passing check
#: cleared, by (project root, task). Run R44: T0002's step-1 failure stood after
#: two passing steps, so the reruns keyed on a passing check were never offered.
_CHECK_FAILED_BEFORE: set[tuple[str, str]] = set()
#: Tasks that have had the one notes-only rerun a broken check earns past the cap
#: (see `_broken_check`), by (project root, task).
_BROKEN_RERUN_SPENT: set[tuple[str, str]] = set()

#: Not-done results after which a further step on the task dispatches no worker.
ESCALATE_AFTER = 3
#: Not-done results after which an escalation no longer offers a notes-only rerun
#: of a task only the close's own judge kept open.
JUDGE_NOTES_UNTIL = 2 * ESCALATE_AFTER
#: Notes-only reruns past JUDGE_NOTES_UNTIL left to a task only the close's source
#: judge kept open; after them, the escalation offers closing it or stopping.
SOURCE_JUDGE_RERUNS = 3
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
    check: str,
    task: str = "",
    nodes: list[dict[str, Any]] | None = None,
    done_by: str = "",
    *,
    rewritten_from: tuple[str, str] | None = None,
    scope: list[str] | None = None,
    unwitnessed: str = "",
) -> str:
    """Why a check that passes before any work is not bound.

    A part of a non-root container gets no abandon hint, which
    `_abandon_problem` would refuse: run R09's driver sent that refused call
    nine times. A done sibling closed on the same check is named instead.
    With `done_by`, a done task whose commit is in the scope's history, the
    done-by abandon is offered: run R14 was told to bind the goal's test,
    which was the same passing check. The offer names `scope`, the paths
    `_done_by` then takes. With `unwitnessed`, `_done_by_witness`'s refusal of
    that close, its way forward is offered in place of the done-by: runs R06,
    R09, R18 and R40 were offered a done-by close the witness rule refused.
    With `rewritten_from`, the command as sent and why it became `check`, the
    refusal names both: run R40 class 3 was told to put a new test in scope, which
    its call had done, four times, while the rewrite was said only in the route.
    """
    if rewritten_from is not None and rewritten_from[0].split() != check.split():
        sent, why = rewritten_from
        return f"`{sent}`, as sent, was rewritten to `{check}`: {why} " + _already_passes(
            check, task, nodes, done_by, scope=scope, unwitnessed=unwitnessed
        )
    if done_by and unwitnessed:
        return (
            f"`{check}` already passes, before any work, so it cannot tell this task's "
            f"work from none; {unwitnessed}"
        )
    if done_by:
        scoped = f" scope={json.dumps(scope)}" if scope else ""
        return (
            f"`{check}` already passes, before any work, so it cannot tell this task's "
            f"work from none. If {done_by}'s work already did this, call pursuit_step "
            f'task="{task}" abandon="done by {done_by}" done_when="{check}"{scoped}: it closes '
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
    if (
        container in roots
        and task in _founding_milestones(nodes)
        and _abandon_problem(task, "duplicate of Tnnnn", nodes) is not None
    ):
        # q35 R54 L37-L39: T0004, a founding milestone, was offered the duplicate
        # abandon, and `_abandon_problem` refused it: "it is a milestone".
        return text
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


async def _passes_without_own_work(
    check: str, scope: list[str], root: Path, carried: _SplitCarry | None = None
) -> bool:
    """Whether `check` still passes with the uncommitted files in `scope` put back as committed.

    Run R12: T0008's new route was refused as already passing, five times, when
    only its own uncommitted test made the check pass. q35 10-11: the files a
    split committed for its parts (`carried`) are put back as the split task
    opened on them.
    """
    carried = carried or _SplitCarry()
    own = [rel for rel in _changed_files(root) if scope and _in_scope(rel, scope, root)]
    own += [rel for rel in carried.files if scope and _in_scope(rel, scope, root)]
    own = list(dict.fromkeys(own))
    if not own:
        return True
    saved: dict[str, bytes | None] = {}
    try:
        for rel in own:
            path = root / rel
            saved[rel] = path.read_bytes() if path.is_file() else None
            head = subprocess.run(
                ["git", "show", f"{carried.base(rel, 'HEAD')}:{rel}"],
                cwd=root,
                capture_output=True,
                check=False,
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


async def _passes_only_by_uncommitted(
    check: str, scopes: list[list[str]], root: Path, carried: _SplitCarry | None = None
) -> bool:
    """Whether `check`, passing now, passes only because of uncommitted files in `scopes`.

    The task's own scope and its predecessor's: the close's witness takes those
    files away, so the close judges them. Run R18 refused T0005's open as
    "already passes" seven times, on W1's uncommitted known-answers files. A
    part's `carried` files, which its parent's split committed, count as its own.
    """
    combined = [entry for scope in scopes for entry in scope]
    if not combined:
        return False
    return not await _passes_without_own_work(check, combined, root, carried)


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


def _on_disk_note(check: str, task: str, carried: _SplitCarry | None = None) -> str:
    """The note on a check that passes only on uncommitted work in the task's scope,
    or on the work its parent's split committed for it (`carried`)."""
    if carried is not None and carried.files:
        return (
            f"`{check}` passes already, but only on uncommitted files in {task}'s scope or "
            f"on what '{carried.parent}: {SPLIT_WIP_TITLE}' committed for its parts, which "
            f"is {task}'s work: the close judges it (its witness takes those files away, "
            "and the check must then fail).\n\n"
        )
    return (
        f"`{check}` passes already, but only on uncommitted files in {task}'s scope: the "
        "work is on disk, and the close judges it (its witness takes those files away, "
        "and the check must then fail).\n\n"
    )


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
    is_open: bool = False,
) -> str | None:
    """What to say in place of "bind the data test" when that test already passes; or None.

    Run R18: told to bind `pytest tests/test_case_data.py`, which W1's uncommitted
    files made pass, the driver was refused as "already passes" for 14 minutes.
    Run R32: an open task was told to bind the check it was already bound to.
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
        opens = "its check is amended" if is_open and not same else "it opens"
        if is_open and same:
            opens = "it runs"
        opens += ", and the close judges the files on disk"
        return (
            f"Send pursuit_step task={json.dumps(task)}{rebind}: {opens}. {why}: {task} "
            f"closes on that work.{leave}"
        )
    # Run R42 class 2: only a pending task closes on abandon="done by …"; offered to
    # open T0007, it was refused five times.
    done_by = (
        ""
        if is_open
        else f"If a done task already did this work, call pursuit_step task={json.dumps(task)} "
        f'abandon="done by <that task>" done_when="{data_check}"; if '
    )
    # q35 R59 L49: for a scope of tests only, prove refuses a new data test's WITNESS too.
    joint = _joint_cases_route(f"pytest {shlex.quote(test)}", needs, root)
    return (
        f"{done_by or 'If '}work is left"
        + (
            f": {joint}"
            if joint
            else ", name a new data test file for it that fails now, put it in scope, and "
            "say in the notes what it should test."
        )
        + f" {test} imports {module}, which a later task writes, and the "
        f"data test `{data_check}` already passes on the committed tree, so neither check "
        f"can tell {task}'s work from none."
    )


async def _data_check_passes_committed(
    data_check: str, scopes: list[list[str]], root: Path
) -> bool:
    """Whether `data_check` passes on the committed tree, uncommitted work in `scopes`
    aside: binding it then closes on no work."""
    if (await _run_check(data_check, root, DEFAULT_CHECK_TIMEOUT))[0] != 0:
        return False
    return not await _passes_only_by_uncommitted(data_check, scopes, root)


def _own_test_import_note(command: str, scope: list[str], root: Path, task_text: str) -> str:
    """The worker note for a check whose own in-scope test imports, itself or through
    a sibling test, a module the tree and the installed packages do not provide and
    no scope path creates; or "". Also "" when `task_text`, the task's title and
    criteria, names that module: the import is then the work, not a stray.

    Run R42 class 2: tests/test_analysis_check.py, T0007's own test, gained an
    import of the unwritten module, and every step was refused before a worker ran.
    q35 R55: T0003's criteria required its cases test to import itc, and the note
    told its workers to remove `import itc`.
    """
    found = _imports_unwritten(command, scope, root)
    if found is None or not _in_scope(found[0], scope, root):
        return ""
    test, module, via = found
    if re.search(rf"(?<![\w.]){re.escape(module)}(?![\w])", task_text):
        return ""
    imported = Path(via[0]).stem if via else module
    line = _import_line(root / test, imported)
    named = f"`{line}`" if line else f"its import of {imported}"
    return (
        f"{test}, which this task's check runs, imports {module}, which neither the "
        "project tree nor the installed packages provide and no path in this scope "
        f"creates, so the check cannot pass. {test} checks this task's own files only: "
        f"remove {named} and every use of {imported}, and keep the tests of this task's "
        "own files."
    )


def _absent_check_file_problem(command: str, scope: list[str], root: Path) -> str | None:
    """Why a check runs a test file that is not on disk and `scope` does not hold, or None.

    Run R40 class 4: T0011, scope a tests/ data file, ran tests/test_cases_source.py,
    which was not on disk; pytest exited 4, and workers met 21 scope refusals writing
    it across three routes on the same scope. A test in scope and not on disk is the
    work, and is left alone.
    """
    if not scope:
        return None
    absent: list[str] = []
    for rel in _check_run_files(command, root):
        path = os.path.normpath(rel)
        if (
            path.endswith(".py")
            and _is_test_path(path)
            and path not in absent
            and not (root / path).exists()
            and _runs_test_file(command, rel)
            and not _in_scope(path, scope, root)
        ):
            absent.append(path)
    if not absent:
        return None
    files = ", ".join(absent)
    it = "it" if len(absent) == 1 else "them"
    return (
        f"done_when `{command}` runs {files}, which {'is' if len(absent) == 1 else 'are'} "
        f"not on disk and outside the scope ({', '.join(scope)}). Writes outside the scope "
        f"are refused, so no worker can write {it}, and the check fails on {it} whatever "
        f"the work does. If this task writes {files}, call pursuit_step again with the "
        f"same task, criteria and done_when, and scope={json.dumps([*scope, *absent])}; "
        "else name only test files that exist."
    )


async def _unwritten_check_problem(
    command: str,
    scope: list[str],
    task: str,
    root: Path,
    extra: list[str] | None = None,
    *,
    bound: str = "",
    is_open: bool = False,
) -> str | None:
    """`_imports_unwritten_problem`, unless the data test it prescribes already passes."""
    route = _data_test_route(command, scope, root)
    if route is None:
        return None
    on_disk = await _data_route_on_disk(task, route, root, extra, bound=bound, is_open=is_open)
    return on_disk or _imports_unwritten_problem(command, scope, root)


def _kept_data_check(done_when: str, scope: list[str], bound: str, root: Path) -> str | None:
    """The note for keeping the bound check when `done_when` runs a test importing
    unwritten code and the data test tau would propose instead is the bound check; or None.

    Run R32 #12: the notes that would have fixed the task were refused together
    with such a done_when.
    """
    if not _keepable(bound):
        return None
    route = _data_test_route(done_when, scope, root)
    if route is None or not _bound_is_data_check(bound, route[2], root):
        return None
    if _data_test_imports_unwritten(bound, scope, root):
        # Run R35 #10: the kept data test imported the code through a sibling test,
        # as unpassable as the done_when; `_imports_unwritten_problem` refuses both.
        return None
    test, module = route[0], route[1]
    return (
        f'Kept done_when="{bound}" (the data test); {test} imports {module}, which a '
        f"later task writes, so `{done_when}` is not bound.\n\n"
    )


def _keepable(bound: str) -> bool:
    """Whether a task's bound check is one its notes may run on, or a refusal may
    offer to keep: one valid command whose exit is not a bool expression.

    Run R44: E42's rewrite of T0004's inverted check was refused, and the notes
    ran on the inverted check.
    """
    return bool(bound) and _check_problem(bound) is None and _inverted_exit_problem(bound) is None


def _kept_bound_note(
    bound: str, notes: str, reason: str, scope: list[str], root: Path
) -> str | None:
    """The note for running `notes` against an open task's bound check when its
    rewritten done_when was rejected for `reason`; None when the call is refused,
    as it is without notes or when the bound check cannot pass on `scope` either.

    Audit 10: refusing the call dropped the driver's notes, and the step with them.
    """
    if not notes or not _keepable(bound):
        return None
    if _imports_unwritten(bound, scope, root) is not None:
        # Run R35 #10: a bound data test importing unwritten code fails whatever
        # the notes do; the refusal names the fix.
        return None
    return f"Kept the bound check `{bound}`; the new done_when was not taken: {reason}\n\n"


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

    Run R21 bound T0005, scope a tests/ data file, to T0006's tests/test_case_data.py;
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
    title = str(record.get("title") or "")
    if not check:
        return (
            f"{refused}it has no check: pass done_when, ONE command that exits 0 on "
            f"{done}'s work, and call again."
        )
    chained, prose = _and_chain(check)
    if prose is not None or chained is None:
        return f"{refused}{prose}"
    check = chained
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
    check_rc, check_out = await _run_check(check, root, DEFAULT_CHECK_TIMEOUT)
    if check_rc != 0:
        return (
            f"{refused}its check `{check}` does not pass now (exit {check_rc}), so the "
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
    named = f"{title}\n{record.get('criteria') or ''}\n{arguments.get('criteria') or ''}"
    witness, unwitnessed = _done_by_witness(
        task, done, check, paths, root, named, targets=not scope
    )
    if unwitnessed:
        return unwitnessed
    criteria = (
        str(arguments.get("criteria") or "").strip()
        or str(record.get("criteria") or "").strip()
        or f"`{check}` passes on {done}'s work"
    )
    # Run R28: beagle's rank gate refused the open of T0029, done by a commit,
    # because T0027, T0031 and T0032 ranked above it.
    over = f"closing as done by {done}: its commit {sha[:12]} already did this work"
    argv = ["open", task, "--criteria", criteria, "--done-when", check, "--over", over]
    if scope:
        argv += ["--scope", *scope]
    if witness:
        argv += ["--confirms", done]
    rc, opened = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    if rc != 0:
        refused, then = _relay_next(opened, "")
        return f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{refused}" + (
            f"\n\n{then}" if then else ""
        )
    if witness:
        argv = ["prove", task, *(a for rel in witness for a in ("--absent", rel))]
        argv += ["--check-timeout", f"{DEFAULT_CHECK_TIMEOUT:.0f}"]
        rc, proved = await _run_prove([BEAGLE_BIN, "pursuit", *argv], root, DEFAULT_CHECK_TIMEOUT)
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
    closed, then = _relay_next(
        closed, "Next: call pursuit_step with no arguments for the next task."
    )
    return f"{task} — {title}: closed done, {because}.\n\n{closed}\n\n{_tree(root)}\n\n{then}"


def _changes_done_work(
    task: str, done: str, title: str, record: Mapping[str, Any], nodes: list[dict[str, Any]]
) -> str:
    """How `task` is to change `done`'s work, by tau's own fix-route titles or the
    tree; "" when neither says so.

    Run R28: "Fix known answers" and "Known answers: fix <the data file>" closed
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


def _imported_at_top(rel: str, check: str, root: Path) -> bool:
    """Whether `rel`, a .py module, is imported at the top of a test `check` runs under
    pytest, so that taking it away fails only on the import (`_import_error_only`)."""
    if not rel.endswith(".py") or not any(
        Path(word).name in {"pytest", "py.test"} for word in re.split(r"[\s'\"]+", check)
    ):
        return False
    names = set(_module_names(rel))
    for test in _check_test_files(check, root):
        try:
            tree = ast.parse((root / test).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        for node in tree.body:
            if isinstance(node, ast.Import):
                imported = {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                imported = {node.module, *(f"{node.module}.{a.name}" for a in node.names)}
            else:
                continue
            if names & imported:
                return True
    return False


def _done_by_witness(
    task: str,
    done: str,
    check: str,
    paths: list[str],
    root: Path,
    named: str = "",
    lead: str = "",
    *,
    targets: bool = False,
) -> tuple[list[str], str]:
    """The files `done` committed in `paths` that can witness a done-by close of `task`,
    and, when the pursuit requires a witness and none can, `_done_by_unwitnessed`'s
    refusal ("" otherwise).

    `_done_by` refuses on it and `_already_passes` offers a done-by only where it
    gives no refusal: runs R06, R09, R18 and R40 were offered done-by closes this
    refused.
    """
    if not _requires_witness(root):
        return [], ""
    shas = _task_commits(done, root)
    committed = list(dict.fromkeys(rel for s in shas for rel in _commit_paths(s, root)))
    # q35 R54 L33-L35: T0003's cobs/__init__.py was offered as the witness, and the
    # test imports it at its top, so `_done_by`'s import-only rule refused the close.
    witness = [
        rel
        for rel in committed
        if _in_scope(rel, paths, root)
        and _can_witness(rel)
        and (root / rel).is_file()
        and not _imported_at_top(rel, check, root)
    ]
    if witness:
        return witness, ""
    return [], _done_by_unwitnessed(
        task, done, check, paths, committed, root, named, lead, targets=targets
    )


def _done_by_unwitnessed(
    task: str,
    done: str,
    check: str,
    paths: list[str],
    committed: list[str],
    root: Path,
    named: str = "",
    lead: str = "",
    *,
    targets: bool = False,
) -> str:
    """The up-front refusal of a done-by close the witness rule would refuse; `lead`,
    when given, stands for its opening "pursuit_step: T not closed done by D — ".

    Run R28: the offer widened eleven tasks' scope with a tests/ data file, T0002's
    data, and each then closed as done by T0002. A file outside the paths is
    offered only when the task's title or criteria (`named`) names it, or when
    the paths are the check's `targets`, no scope the call or record chose.
    """
    # q35 R53: the offered done-by named scope=["tests/", "itc/"]; the call sent
    # without it took the check's targets, and the refusal, offering only named
    # files, sent the driver to a new check rather than back to that scope.
    outside = [
        rel
        for rel in committed
        if not _in_scope(rel, paths, root)
        and _can_witness(rel)
        and (root / rel).is_file()
        and not _imported_at_top(rel, check, root)
        and (
            targets
            or rel in named
            or re.search(rf"(?<![\w./-]){re.escape(Path(rel).name)}\b", named)
        )
    ]
    said = (
        (lead or f"pursuit_step: {task} not closed done by {done} — ")
        + "this pursuit closes done only on a witnessed check, and no file "
        f"{done} committed in {', '.join(paths)} is a source or data file whose absence "
        f"could show the check refuses, so the close would refuse and leave {task} open. "
        "Nothing was opened."
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
    # q35 R54 L35: the pasted tail began mid-word, "n __init__.py is absent".
    cut = out[-CHECK_TAIL_CHARS:]
    tail = cut.split("\n", 1)[1] if len(cut) < len(out) and "\n" in cut else cut
    reason = f"done-by close not taken: {why}"[:500]
    argv = ["close", task, "--outcome", "blocked", "--reason", reason]
    if out.strip():
        argv += ["--body", out]
    argv += ["--spent", "0", "--spent-because", "no sub-agent ran: a done-by close"]
    rc, closed = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    _forget_task(root, task)
    if rc != 0:
        return (
            f"pursuit_step: {task} not closed done — {why}:\n{tail}\n\n"
            f"It is still open: closing it blocked exited {rc}:\n{closed}"
        )
    return (
        f"pursuit_step: {task} not closed done — {why}. It was closed blocked rather than "
        f"left open:\n{tail}\n\n{closed}\n\n{_tree(root)}\n\n"
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
    if _lean():
        return ""
    if arguments is None:
        return _escalation_options(
            task,
            count,
            f"pursuit_step: {task} not run: {count} steps on it have left it not done.",
            _MORE_SUBAGENTS,
        )
    demand = _judge_kept_open(task, root)
    if demand:
        return _judge_escalation(task, count, demand, root=root)
    failure = _broken_check(task, root)
    if failure:
        return _broken_check_escalation(task, count, failure)
    if record and _unchanged_route(task, arguments, record, root, data_test_passes, bound_fails):
        bound = " ".join(str(record.get("done_when") or "").split())
        said = (
            f"{count} steps on it have left it not done, on its bound check `{bound}` and "
            "its scope. The only new route left keeps both, and a new route that changes "
            "nothing gets the same result."
        )
        return _unchanged_route_escalation(task, count, record, said, root)
    lacks = _escalation_lacks(task, arguments, record, root, data_test_passes, bound_fails)
    # Run R16 E34 dropped the done_when line, and the driver resent without it.
    call = _working_call(task, arguments, record, root, data_test_passes, bound_fails)
    # Run R23 E34-E46: the breaker quotes only a result's first line, so the call
    # goes there, short enough to survive its quote, with notes elided if need be.
    lead = f"pursuit_step: {task} not run — call instead: "
    short = _working_call(task, arguments, record, root, data_test_passes, bound_fails, bare=True)
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _working_call(
            task,
            arguments,
            record,
            root,
            data_test_passes,
            bound_fails,
            bare=True,
            notes="…",
        )
    head = f"{lead}{short}\n{count} steps on it have left it not done."
    if lacks:
        head += "\n" + "\n".join(f"- {line}" for line in lacks)
    head += "\nThe call that works, whole: " + call
    return _escalation_options(task, count, head, _MORE_SUBAGENTS)


#: Why an escalated task gets no further sub-agent on its route, as it stands.
_MORE_SUBAGENTS = (
    "another sub-agent on it, however its scope or notes are put, would only add one more"
)
_JUDGE_ONLY = "its check passes each time, and only the close keeps it open"
#: The option an escalation gives to stop; the stop gate lets through a stop the
#: last pursuit tool result offered with it.
STOP_OPTION = "- stop, and tell the user what blocks it."


def _escalation_options(
    task: str, count: int, head: str, why: str, rerun: str | None = None, split: bool = True
) -> str:
    """An escalation's `head`, then why the task is escalated, then its options.

    `rerun`, given when a notes-only rerun is what the task has left, stands in
    for the new route with a rewritten done_when; "" offers neither. Run R37: the
    reason was inferred from `rerun`, so a task whose last check failed was told
    "its check passes each time". `split` False leaves the split out.
    """
    if rerun is None:
        rerun = (
            f'- pursuit_step task="{task}", new_route=true, with a rewritten done_when and '
            "notes saying what the new route does differently (the criteria stay);\n"
        )
    plan = (
        f'- pursuit_plan task="{task}" with two or more parts, to split it into smaller '
        "tasks (a plan of one part is refused: the task is already one step);\n"
        if split
        else ""
    )
    return (
        f"{head}\n{task} has had {count} steps without a pass, and {why}. Choose one:\n"
        f"{plan}{rerun}{STOP_OPTION}"
    )


def _judge_kept_open(task: str, root: Path | None) -> str:
    """The close judge's reason, when every not-done step on `task` since its check
    last failed passed it and only that judge kept the task open; else "".

    An unproven task gets "": its notes-only rerun runs no sub-agent. q35 10-11
    (11:19:02): the unproven refusal offered new_route=true, and this put "leave
    done_when and new_route out" and that rerun under it.
    """
    if root is None:
        return ""
    key = (str(root), task)
    if key in _UNPROVEN:
        return ""
    if key in _NOT_DONE_CHECK_FAILED or _LAST_CHECK_EXIT.get(key, 0) != 0:
        return ""
    return _NOT_DONE_DEMAND.get(key, "")


def _steps_passing(task: str, root: Path | None) -> str:
    """How the not-done steps on `task`, held by the close alone, did on its check."""
    if root is not None and (str(root), task) in _CHECK_FAILED_BEFORE:
        return "the last with its check passing"
    return "each with its check passing"


def _notes_only_call(task: str, notes: str) -> str:
    """The rerun of `task` with the bound check kept and `notes` saying what to fix."""
    return f"pursuit_step task={json.dumps(task)}, notes={json.dumps(notes, ensure_ascii=False)}"


def _source_judge_cases(task: str, root: Path | None) -> tuple[str, tuple[str, ...]] | None:
    """The data file and cases the close's source judge named, when only that judge
    kept `task` open and every not-done step on it since its check last failed
    passed it; else None."""
    if root is None or not _judge_kept_open(task, root):
        return None
    return _NOT_DONE_CASES.get((str(root), task))


def _source_reruns_spent(task: str, root: Path | None) -> bool:
    """Whether `task`, held by the close's source judge alone, has spent the
    SOURCE_JUDGE_RERUNS notes-only reruns it gets past JUDGE_NOTES_UNTIL."""
    if root is None or not _source_judge_cases(task, root):
        return False
    return _NOT_DONE.get((str(root), task), 0) >= JUDGE_NOTES_UNTIL + SOURCE_JUDGE_RERUNS


def _source_judge_escalation(
    task: str,
    count: int,
    root: Path,
    held: tuple[str, tuple[str, ...]],
    said: str = "",
    lead: str = "",
) -> str:
    """The escalation of a task only the close's source judge kept open: a notes-only
    rerun naming its cases and where to search, or stopping; once its
    SOURCE_JUDGE_RERUNS are spent, closing it infeasible on those cases, or stopping.

    Run R40: the escalation offered a split by file; its parts opened already
    passing, and no part could change a case, so the driver split and re-split.
    """
    data, cases = held
    one = len(cases) == 1
    listed = ("case " if one else "cases ") + ", ".join(cases)
    lead = (lead or f"pursuit_step: {task} not run — ") + "call instead: "
    if count >= JUDGE_NOTES_UNTIL + SOURCE_JUDGE_RERUNS:
        return _source_judge_spent(task, count, data, listed, said, lead, root)
    notes = (
        f"The close keeps {task} open on its cases' sources alone: {listed} in {data} "
        f"{'cites' if one else 'cite'} no line giving the expected result. Quote the line "
        f"that gives each result and make the expected value match it. "
        f"{_unanswered_case_note(root)}"
    )
    call = _notes_only_call(task, notes)
    short = call
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _notes_only_call(task, "…")
    head = f"{lead}{short}\n" + (f"{said}\n" if said else "")
    head += (
        f"{count} steps on it have left it not done, {_steps_passing(task, root)}: only "
        f"the close's source check keeps it open, on {listed}. A split by file cannot "
        "change a case, so none is offered; keep the bound check (leave done_when and "
        f"new_route out).\nThe call that works, whole: {call}"
    )
    rerun = f"- {call}, a sub-agent at those cases, with the bound check kept;\n"
    why = _last_check_said(task, root)
    return _escalation_options(task, count, head, why, rerun=rerun, split=False)


def _source_judge_spent(
    task: str, count: int, data: str, listed: str, said: str, lead: str, root: Path
) -> str:
    """The escalation of a task the source judge alone held through its
    SOURCE_JUDGE_RERUNS: no rerun and no split, but its infeasible close, or stopping."""
    why = f"no line of {REFERENCES_DIR}/*.txt gives the result of {listed} in {data}"
    close = _infeasible_call(task, "", [], why)
    short = close
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _infeasible_call(
            task, "", [], f"the references answer none of {data}'s unsourced cases"
        )
    head = f"{lead}{short}\n" + (f"{said}\n" if said else "")
    head += (
        f"The cases the references do not answer, {listed} in {data}, cannot close {task}: "
        f"{count} steps on it have left it not done, {_steps_passing(task, root)}, and its "
        f"{SOURCE_JUDGE_RERUNS} notes-only reruns past {JUDGE_NOTES_UNTIL} steps are spent. "
        "No rerun and no split is offered: a split by file cannot change a case. "
        f"{_seal_warning(task, 'its parent')}\n"
        f"The call that works, whole: {close}"
    )
    closing = f"- {close}, closing it infeasible on those cases;\n"
    why = _last_check_said(task, root)
    return _escalation_options(task, count, head, why, rerun=closing, split=False)


def _judge_escalation(
    task: str,
    count: int,
    demand: str,
    lead: str = "",
    root: Path | None = None,
    said: str = "",
) -> str:
    """The escalation of a task only the close's own judge kept open.

    Run R33 #13-#24: every not-done step had passed its check, yet the escalation
    asked for a new done_when, which the data-route rewrite put back to the bound
    one; no call passed both, and the driver resent one call 12 times. Run R36
    E57, E63: the not-done result and the not-workable refusal still said the next
    step runs no sub-agent, so they render this too, with `lead` in place of the
    refusal's "pursuit_step: <task> not run — ". A task only the source judge
    held gets `_source_judge_escalation` instead.
    """
    held = _source_judge_cases(task, root)
    if held and root is not None:
        return _source_judge_escalation(task, count, root, held, said=said, lead=lead)
    lead = lead or f"pursuit_step: {task} not run — "
    reason = demand.rstrip(".")
    why = _last_check_said(task, root)
    said = (f"\n{said}" if said else "") + (
        f"\n{count} steps on it have left it not done, {_steps_passing(task, root)}: the "
        f"close kept it open because {reason}. A new done_when would not change that, so "
        "keep the bound one (leave done_when and new_route out)."
    )
    if count >= JUDGE_NOTES_UNTIL:
        head = f"{lead}split it or stop.{said}"
        return _escalation_options(task, count, head, why, rerun="")
    call = _notes_only_call(task, reason)
    lead += "call instead: "
    short = call
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _notes_only_call(task, "…")
    head = f"{lead}{short}{said}\nThe call that works, whole: {call}"
    rerun = f"- {call}, a sub-agent at what the close refused, with the bound check kept;\n"
    return _escalation_options(task, count, head, why, rerun=rerun)


def _check_error_line(tail: str) -> str:
    """The first error line of a check's output tail, short; else its last line."""
    lines = [line.strip() for line in tail.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("E "):
            return line[1:].strip()[:CHECK_ERROR_LINE_CHARS]
    for line in lines:
        if re.search(r"\w(Error|Exception)\b", line):
            return line[:CHECK_ERROR_LINE_CHARS]
    return lines[-1][:CHECK_ERROR_LINE_CHARS] if lines else ""


#: How much of a failing check's first error line an escalation quotes.
CHECK_ERROR_LINE_CHARS = 120


def _last_error_line(key: tuple[str, str]) -> str:
    """The first error line of the last failing run of the check of the task at `key`."""
    failure = _LAST_CHECK_FAILURE.get(key)
    line = _check_error_line(failure[2]) if failure else ""
    return line or f"exit {_LAST_CHECK_EXIT.get(key)}"


def _last_check_said(task: str, root: Path | None) -> str:
    """What `task`'s last check did, as an escalation's reason: its first error line
    when it failed; else that only the close keeps the task open."""
    if root is None:
        return _JUDGE_ONLY
    key = (str(root), task)
    if _LAST_CHECK_EXIT.get(key, 0) != 0:
        return f"the last step's check failed: {_last_error_line(key)}"
    if key in _NOT_DONE_CHECK_FAILED or key in _CHECK_FAILED_BEFORE:
        return "its last check passed, and only the close keeps it open"
    return _JUDGE_ONLY


def _broken_check(task: str, root: Path | None) -> str:
    """The first error line of `task`'s check, when its last not-done step failed
    the check every earlier not-done step on it had passed, and the one rerun that
    earns is unspent; else "".

    Run R37: T0004's sixth step broke a data test five steps had passed (a
    cwd-relative path), the driver named the one-line fix, and the step cap
    refused every call that could carry it.
    """
    if root is None:
        return ""
    key = (str(root), task)
    count = _NOT_DONE.get(key, 0)
    if (
        count < 2
        or key in _BROKEN_RERUN_SPENT
        or key in _CHECK_FAILED_BEFORE
        or _NOT_DONE_CHECK_FAILED.get(key) != count
        or _LAST_CHECK_EXIT.get(key, 0) == 0
    ):
        return ""
    return _last_error_line(key)


def _broken_check_rerun(
    task: str, arguments: Mapping[str, Any], record: Mapping[str, Any], root: Path
) -> bool:
    """Whether a step on an escalated task is the notes-only rerun
    `_broken_check_escalation` offers: notes given, no new route, the bound check kept."""
    if not _broken_check(task, root):
        return False
    if arguments.get("new_route") is True or not str(arguments.get("notes") or "").strip():
        return False
    return _kept_bound(arguments, record, root)


def _broken_check_escalation(
    task: str, count: int, failure: str, said: str = "", lead: str = ""
) -> str:
    """The escalation of a task whose last step broke the check the steps before it
    passed: one notes-only rerun at `failure`, with the bound check, past the cap.
    `said`, given, says first why the refused call was refused."""
    lead = lead or f"pursuit_step: {task} not run — "
    call = _notes_only_call(
        task, f"The last step broke the check, which passed before: {failure}. Fix that."
    )
    lead += "call instead: "
    short = call
    if len(lead) + len(short) > ESCALATION_HEAD_CHARS:
        short = _notes_only_call(task, "…")
    head = f"{lead}{short}\n" + (f"{said}\n" if said else "")
    head += (
        f"{count} steps on it have left it not done; the last one failed its check, which "
        "every step before it had passed. That earns one notes-only rerun past the cap, "
        "with the bound check kept (leave done_when and new_route out); after it, the cap "
        f"stands.\nThe call that works, whole: {call}"
    )
    rerun = f"- {call}, once: a sub-agent at that failure, with the bound check kept;\n"
    return _escalation_options(
        task, count, head, f"the last step's check failed: {failure}", rerun=rerun
    )


def _judge_notes_rerun(
    task: str, arguments: Mapping[str, Any], record: Mapping[str, Any], root: Path
) -> bool:
    """Whether a step on an escalated task is the notes-only rerun `_judge_escalation`
    offers: notes given, no new route, and the bound check kept or put back. Past
    JUDGE_NOTES_UNTIL, only a task the source judge alone held still has it, until
    its SOURCE_JUDGE_RERUNS are spent; the escalation then refuses it."""
    if not _judge_kept_open(task, root):
        return False
    late = _NOT_DONE.get((str(root), task), 0) >= JUDGE_NOTES_UNTIL
    if late and (not _source_judge_cases(task, root) or _source_reruns_spent(task, root)):
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
            "This call has no new_route=true, so it asks for another sub-agent on the same route."
        )
    criteria = " ".join(str(arguments.get("criteria") or "").split())
    bound_criteria = " ".join(str(record.get("criteria") or "").split())
    if criteria and bound_criteria and criteria != bound_criteria:
        lacks.append(
            f"Its criteria differ from {task}'s: leave criteria out, since a new route keeps them."
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
                f'test only: done_when="{data_check}".{_scope_note(needs, scope)}'
            )
        elif done_when and not _keeps_bound_check(bound_check, scope, root, bound_fails):
            lacks.append(
                "Its done_when is the bound one: a new route needs a check a sub-agent on "
                "this scope can pass."
            )
    return lacks


def _working_route(
    task: str,
    arguments: Mapping[str, Any],
    record: Mapping[str, Any],
    root: Path | None,
    data_test_passes: bool = False,
    bound_fails: bool = False,
) -> tuple[str, list[str], list[str] | None]:
    """The done_when ("" when none is known) and scope of the new route an
    escalation offers, and the data files `_unproven_data_route` adds, or None."""
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
    return check, needs, unproven


def _unchanged_route(
    task: str,
    arguments: Mapping[str, Any],
    record: Mapping[str, Any],
    root: Path | None,
    data_test_passes: bool = False,
    bound_fails: bool = False,
) -> bool:
    """Whether the only new route an escalation could offer keeps the bound check
    and the bound scope, so it would change nothing.

    Run R35 E18, E26, E34 offered such a route three times; each spawned an heir
    with the same check and scope, and each heir was left not done the same way.
    q35 10-11 (11:19:02): an unproven data route adding no data file, the data
    already in scope, was offered as one that changes something.
    """
    bound_check = " ".join(str(record.get("done_when") or "").split())
    check, needs, unproven = _working_route(
        task, arguments, record, root, data_test_passes, bound_fails
    )
    return (
        bool(bound_check)
        and not unproven
        and check == bound_check
        and sorted(needs) == sorted(_strings(record.get("scope")))
    )


def _split_call(task: str, record: Mapping[str, Any]) -> str:
    """The pursuit_plan call splitting `task` one file of its scope per part, or ""
    when its scope has fewer than two files."""
    files = _strings(record.get("scope"))
    if len(files) < 2:
        return ""
    parts = [f"{rel}::the work in {rel}" for rel in files]
    return f"pursuit_plan task={json.dumps(task)}, parts={json.dumps(parts)}"


def _unchanged_route_escalation(
    task: str, count: int, record: Mapping[str, Any], said: str, root: Path | None
) -> str:
    """The escalation of a task whose only new route keeps its check and scope:
    `said` says why, then the split of its files one per part, or stopping; or,
    when its last step broke a passing check, the one rerun that earns; or, when
    only the close's judge held it, the notes-only rerun with that check kept.

    Run R44: T0002's check passed, and this offered only a split or a stop."""
    failure = _broken_check(task, root)
    if failure:
        return _broken_check_escalation(task, count, failure, said)
    demand = _judge_kept_open(task, root)
    if demand:
        return _judge_escalation(task, count, demand, root=root, said=said)
    split = _split_call(task, record)
    lead = f"pursuit_step: {task} not run — "
    if split and len(lead) + len("call instead: ") + len(split) <= ESCALATION_HEAD_CHARS:
        head = f"{lead}call instead: {split}"
    else:
        head = f"{lead}split it or stop."
    head += f"\n{said}"
    if split:
        head += f"\nThe call that works, whole: {split}"
    return _escalation_options(task, count, head, _last_check_said(task, root), rerun="")


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
    scope = _strings(arguments.get("scope")) or record_scope
    check, needs, unproven = _working_route(
        task, arguments, record, root, data_test_passes, bound_fails
    )
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
    return rc != 0 and _check_broke(rc, out, _strings(record.get("scope")), root) is None


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
    the tests/ data file, whose absence is the proof.
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


def _carry_not_done(root: Path, task: str, successor: str) -> None:
    """Give `successor`, a new route keeping `task`'s check and scope, what the step
    tool counts of `task` not done.

    Run R35: each such heir (T0002, T0005, T0006, T0007) started at no steps, so
    every new route bought three more sub-agents with nothing changed.
    """
    old, new = (str(root), task), (str(root), successor)
    if old in _NOT_DONE:
        _NOT_DONE[new] = _NOT_DONE[old]
    if old in _NOT_DONE_SCOPE:
        _NOT_DONE_SCOPE[new] = _NOT_DONE_SCOPE[old]
    if old in _NOT_DONE_DEMAND:
        _NOT_DONE_DEMAND[new] = _NOT_DONE_DEMAND[old]
    if old in _NOT_DONE_CASES:
        _NOT_DONE_CASES[new] = _NOT_DONE_CASES[old]
    if old in _LAST_CHECK_EXIT:
        _LAST_CHECK_EXIT[new] = _LAST_CHECK_EXIT[old]
    if old in _LAST_CHECK_FAILURE:
        _LAST_CHECK_FAILURE[new] = _LAST_CHECK_FAILURE[old]
    if old in _NOT_DONE_CHECK_FAILED:
        _NOT_DONE_CHECK_FAILED[new] = _NOT_DONE_CHECK_FAILED[old]
    if old in _BROKEN_RERUN_SPENT:
        _BROKEN_RERUN_SPENT.add(new)
    if old in _CHECK_FAILED_BEFORE:
        _CHECK_FAILED_BEFORE.add(new)


def _forget_task(root: Path, task: str) -> None:
    """Drop what the step tool remembers of `task`: closed, re-routed or planned."""
    key = (str(root), task)
    _UNPROVEN.discard(key)
    _WITNESS_PENDING.discard(key)
    _LAST_CHECK_EXIT.pop(key, None)
    _LAST_CHECK_FAILURE.pop(key, None)
    _NOT_DONE.pop(key, None)
    _NOT_DONE_SCOPE.pop(key, None)
    _NOT_DONE_DEMAND.pop(key, None)
    _NOT_DONE_CASES.pop(key, None)
    _NOT_DONE_CHECK_FAILED.pop(key, None)
    _CHECK_FAILED_BEFORE.discard(key)
    _BROKEN_RERUN_SPENT.discard(key)


def _killed_attempt_context(
    run: _WorkerRun,
    shown: str,
    verdict: tuple[int, str],
    check: str,
    root: Path,
    scope: list[str],
    reported: bool,
) -> str:
    """What a killed worker's step result keeps: the attempt before it, and the tree.

    Run R15's second worker was killed at the wall, and the result named only
    the timeout: the first worker's report and the check's output were dropped,
    so the driver went on believing the tests were unwritten.

    q35 R51: W5, killed at its step budget, had said "test is buggy, cannot make
    both pass"; only the next brief on T0003 held it, and the driver spent a
    3.6-min turn finding that again. The result shows the end of what it said.

    q35 R56: W3, the attempt before W4, was killed at its second cut-off with no
    report, and the result said "The attempt before it reported:".
    """
    parts: list[str] = []
    if shown:
        ended = "reported" if reported else "ended without a report"
        parts.append(f"The attempt before it {ended}:\n{shown}")
        if check and verdict[1]:
            parts.append(
                f"`{check}` exit {verdict[0]} after that attempt:\n{verdict[1][-CHECK_TAIL_CHARS:]}"
            )
    kind, said = run.said_last
    if said:
        tail = said[-KILLED_WORDS_CHARS:]
        cut = "[...] " if len(tail) < len(said) else ""
        parts.append(f"What it said last (its {kind}, the end of it):\n{cut}{tail}")
    if run.transcript is not None:
        changes = _scope_changes(root, scope)
        if changes:
            parts.append("In the tree now:\n" + "\n".join(changes))
    return "".join(f"{part}\n\n" for part in parts)


def _not_done(
    root: Path,
    task: str,
    scope: list[str],
    text: str,
    *,
    ran: bool = True,
    cases: tuple[str, list[str]] | None = None,
) -> AgentToolResult:
    """Count a result that left `task` not done, and return it.

    Only a result where a sub-agent ran counts toward ESCALATE_AFTER: run R23
    counted two refusals that ran nothing, and escalated after one worker run.
    `cases`, given by the close's source judge, is its data file and the cases
    it named.
    """
    key = (str(root), task)
    count = _NOT_DONE.get(key, 0) + (1 if ran else 0)
    if ran:
        _NOT_DONE[key] = count
    if scope:
        _NOT_DONE_SCOPE[key] = tuple(scope)
    if ran and _LAST_CHECK_EXIT.get(key, 0) == 0 and key in _NOT_DONE_CHECK_FAILED:
        del _NOT_DONE_CHECK_FAILED[key]
        _CHECK_FAILED_BEFORE.add(key)
    demand = _close_demand(text)
    if demand:
        _NOT_DONE_DEMAND[key] = demand
        if cases:
            _NOT_DONE_CASES[key] = (cases[0], tuple(cases[1]))
        else:
            _NOT_DONE_CASES.pop(key, None)
    elif ran:
        _NOT_DONE_DEMAND.pop(key, None)
        _NOT_DONE_CASES.pop(key, None)
        if _LAST_CHECK_EXIT.get(key, 0) != 0:
            _NOT_DONE_CHECK_FAILED.setdefault(key, count)
    if count >= ESCALATE_AFTER and not _lean():
        text += "\n\n" + _still_open_escalation(task, count, root)
    elif count >= DRIVER_READS_UNTIL and scope:
        text += (
            f"\n\nThe files in {task}'s scope are the sub-agent's while it is open: "
            "reading them yourself is refused. Say what to fix in the step's notes, "
            f'or give it a new route (pursuit_step task="{task}", new_route=true).'
        )
    return _step_result(text)


def _still_open_escalation(task: str, count: int, root: Path) -> str:
    """What a not-done result, and a refusal pointing at `task`, say once `count`
    steps have left it not done: the notes-only rerun when only the close's judge
    kept it open, else that the next step runs no sub-agent."""
    if _lean():
        return ""
    demand = _judge_kept_open(task, root)
    if demand:
        return _judge_escalation(task, count, demand, lead=f"{task} is still open — ", root=root)
    failure = _broken_check(task, root)
    if failure:
        return _broken_check_escalation(task, count, failure, lead=f"{task} is still open — ")
    return _escalation(task, count).replace(
        f"pursuit_step: {task} not run: ", "The next step on it runs no sub-agent: ", 1
    )


def _held_scope(target: Path, root: Path) -> tuple[str, str, int, Path] | None:
    """The open task, its scope entry, not-done count and project root as the step
    tool keys it, holding `target` from the driver."""
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
                    return task, entry, count, Path(where)
                continue
            path = _resolved(root / text)
            if target == path or path in target.parents:
                return task, entry, count, Path(where)
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
    if root is None or _lean():
        return ""
    said = ""
    for t in workable:
        count = _NOT_DONE.get((str(root), t), 0)
        if count >= ESCALATE_AFTER:
            if _judge_kept_open(t, root) or _broken_check(t, root):
                said += "\n" + _still_open_escalation(t, count, root)
                continue
            shown = _shown(t, root)
            if _unchanged_route(t, {}, shown, root):
                split = _split_call(t, shown)
                said += (
                    f"\n{t} has had {count} steps on its bound check and scope, and a new "
                    "route that changes nothing gets the same result: "
                    + (f"split it, {split}, or stop." if split else "split it or stop.")
                )
                continue
            call = _working_call(t, {}, shown, root)
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
            "arguments."
        )
    return (
        f"{task} is not a task to work now. Workable now: {listed}. Call pursuit_step "
        "with no arguments."
    )


def _cases_scope(done_when: str, root: Path) -> list[str]:
    """Where a spec-tied task's cases worker may write: the test paths its check
    names, so every case file is one the check runs. None when it names none: the
    check runs no cases, and the task is not opened on it (S02)."""
    return [
        rel
        for rel in _check_run_files(done_when, root)
        if _is_test_path(rel) or Path(rel).name in ("tests", "test")
    ]


#: Where a case's expected values come from. Run R100: of 17 cases, every one
#: that copied the cited line's bytes was right; the three that worked bytes out
#: (63 with its end marker dropped, the first values of the three- and five-byte
#: forms) were wrong, and the code worker, held to them, edited the pinned cases
#: and left the task unprovable. Interim, until `pursuit rules 2e` says it
#: (dev-notes/beagle-0.48/upstream-asks.md, 10).
CASES_VALUES_NOTE = (
    "Assert only what the cited lines say. Where they give the output, copy it "
    "exactly. Where they give a rule or a bound with no output, assert the rule "
    "(which form, how many bytes, that it is refused, that it round-trips), not "
    "an output you work out: a value you compute is a value you may get wrong, "
    "and the code is held to it."
)


#: How a case's marker reads, for the cases worker. Run S03: q35 took rule 2e's
#: `fork-seed` for part of the cite, wrote the cite where the name goes, then a
#: `cite=` with no name, and spent a 19-minute worker on the guessing.
CASES_MARKER_NOTE = (
    "Above each case put one marker line, `# beagle-case: NAME cite={ref}:LINE#HASH "
    "kind=KIND op=FUNCTION`. NAME is a short name you give the case, unique in the "
    "file (`zero-is-one-byte`); LINE#HASH is the anchor `beagle refs find` printed, "
    "or LINE#HASH-LINE#HASH for a passage; KIND is example, invalid, limit or gap; "
    "FUNCTION is the function the case calls."
)


def _cases_brief(
    task: str,
    title: str,
    source: str,
    criteria: str,
    done_when: str,
    scope: list[str],
    cases_scope: list[str],
) -> str:
    """The cases worker's brief: beagle's `pursuit rules 2e` is the policy, the
    dry run of the task's own open is the stop; tau fills in the task, the
    criteria and the check, the worker the cites and the case files."""
    dry = ["beagle", "pursuit", "open", task, "--criteria", criteria, "--done-when", done_when]
    if scope:
        dry += ["--scope", *scope]
    dry_run = " ".join(shlex.quote(word) for word in dry)
    return (
        f"You write the cases for {task} ({title}) from the source {source} in "
        f"{REFERENCES_DIR}/. A later sub-agent writes the code: write only the tests.\n\n"
        "Run `beagle pursuit rules 2e` first and do what it says. Find the source's "
        "lines with `beagle refs find WORDS` and `beagle refs show NAME`.\n\n"
        f"The task: {criteria}\n"
        f"Write the cases in {', '.join(cases_scope)}, which its check runs: `{done_when}`\n\n"
        + CASES_VALUES_NOTE
        + "\n\n"
        + CASES_MARKER_NOTE.format(ref=Path(source).stem)
        + "\n\n"
        "You are done when this passes, with your cites and case files added:\n"
        f"  {dry_run} --cites REF:ANCHOR ... --cases FILE ... --dry-run\n"
        "It passes while the tests fail: the code is not written yet, so the case file "
        "fails to import it, and that is the failure expected. Import the code as the "
        "check will and do not stub it: a stub hides the code from the tests. Its --scope is "
        f"the code's, for the later sub-agent; you write only in {', '.join(cases_scope)}. "
        "End with a report naming the case files and the cites.\n\n"
        + NO_BEAGLE_NOTE
        + " You may also run that `beagle pursuit open ... --dry-run`."
        + "\n\n"
        + _turn_cap_note(CASES_WORK_IT_OUT_NOTE)
    )


#: A `beagle-case:` line whose first word is a cite where the id goes, with no
#: `cite=`: run S03's cases worker wrote all 17 of its markers so.
_CITE_AS_CASE_ID = re.compile(
    r"^(?P<pre>.*beagle-case:\s*)(?P<cite>[\w.-]+:\d+#[0-9a-f]+(?:-\d+#[0-9a-f]+)?)(?P<rest>.*)$"
)
#: A `beagle-case:` line with no name, its first word already a `key=value`:
#: S03's second cases worker, told "no cite=", moved to `beagle-case: cite=…`.
_CASE_WITHOUT_ID = re.compile(r"^(?P<pre>.*beagle-case:\s*)(?P<rest>\w+=.*)$")


def _case_name(fields: str, index: int) -> str:
    """A name for an unnamed case: its `op=` (or `case`) and its line number."""
    op = re.search(r"\bop=(\S+)", fields)
    return f"{op.group(1) if op else 'case'}-{index + 1}"


def _repair_case_markers(root: Path, cases_scope: list[str]) -> list[str]:
    """Name each `beagle-case:` line in `cases_scope` that has no name: one with
    its cite where the name goes (`_CITE_AS_CASE_ID`) also gets its `cite=`, one
    whose first word is a `key=value` (`_CASE_WITHOUT_ID`) gets only the name.
    The case files changed, for the step's result.

    Run S03: the cases worker's 17 cases were sound but every marker read
    `# beagle-case: wrenfold-r3:25#019 kind=example op=encode_single`; none tied,
    and the whole round of cases was sent again, 6 min of a 30 min run.
    """
    repaired: list[str] = []
    for rel in _changed_files(root):
        if not _in_scope(rel, cases_scope, root) or not (root / rel).is_file():
            continue
        try:
            lines = (root / rel).read_text().splitlines(keepends=True)
        except (OSError, UnicodeDecodeError):
            continue
        changed = False
        for n, line in enumerate(lines):
            body = line.rstrip("\r\n")
            ending = line[len(body) :]
            as_id, no_id = _CITE_AS_CASE_ID.match(body), _CASE_WITHOUT_ID.match(body)
            if as_id is not None and "cite=" not in body:
                case = _case_name(as_id["rest"], n)
                lines[n] = f"{as_id['pre']}{case} cite={as_id['cite']}{as_id['rest']}{ending}"
            elif no_id is not None:
                lines[n] = f"{no_id['pre']}{_case_name(no_id['rest'], n)} {no_id['rest']}{ending}"
            else:
                continue
            changed = True
        if changed:
            (root / rel).write_text("".join(lines))
            repaired.append(rel)
    return repaired


_SHOWN_ANCHOR = re.compile(r"^(\d+)#([0-9a-f]+)\|", re.MULTILINE)


def _line_anchor(name: str, line: int, root: Path) -> str | None:
    """The anchor `beagle refs show` gives line `line` of reference `name`, or None."""
    rc, out = _run(
        [BEAGLE_BIN, "refs", "show", name, "--from", str(line), "--to", str(line)], root, 30.0
    )
    shown = {int(n): anchor for n, anchor in _SHOWN_ANCHOR.findall(out)} if rc == 0 else {}
    return shown.get(line)


def _reanchor_cites(root: Path, files: list[str], cites: list[str]) -> dict[str, str]:
    """Each of `cites` whose anchors are not those of the lines it names, mapped to
    the cite with beagle's anchors for those lines, rewritten so in the case files.

    Run R109 (lfm24): every marker carried the anchor #0b7 beside the right line
    numbers; `open` refused 146#0b7 as line 136's anchor, and three cases
    workers in a row left it so. A worker points at a line; a short anchor
    that fits another line is chance, so the line decides.

    Unless that line, with that anchor, is in another reference: R130 (lfm24
    itc) cited itc2008:48#015, the line `refs find` had shown it in
    interval-tree-clocks, and by the line alone it became the paper's blank
    line 48. A line and its anchor together name that other reference.
    """
    fixed: dict[str, str] = {}
    known: dict[tuple[str, int], str | None] = {}

    def anchor_of(name: str, number: int) -> str | None:
        if (name, number) not in known:
            known[(name, number)] = _line_anchor(name, number, root)
        return known[(name, number)]

    others = sorted(
        {
            path.stem
            for path in (root / REFERENCES_DIR).glob("*")
            if path.is_file() and path.stem != "index"
        }
    )
    for cite in cites:
        name, sep, anchors = cite.partition(":")
        if not sep:
            continue
        parts = re.findall(r"(\d+)#([0-9a-f]+)", anchors)
        wrong = [(n, a) for n, a in parts if anchor_of(name, int(n)) not in (None, a)]
        if not wrong:
            continue
        holders = [
            other
            for other in others
            if other != name and all(anchor_of(other, int(n)) == a for n, a in parts)
        ]
        if len(holders) == 1:
            fixed[cite] = f"{holders[0]}:{anchors}"
            continue
        new = anchors
        for number, anchor in wrong:
            new = re.sub(rf"\b{number}#{anchor}\b", f"{number}#{anchor_of(name, int(number))}", new)
        fixed[cite] = f"{name}:{new}"
    if fixed:
        for rel in files:
            path = root / rel
            text = path.read_text()
            changed = re.sub(
                r"(cite=)(\S+)", lambda m: m.group(1) + fixed.get(m.group(2), m.group(2)), text
            )
            if changed != text:
                path.write_text(changed)
    return fixed


def _marker_ties(root: Path, cases_scope: list[str]) -> tuple[list[str], list[str]]:
    """The case files a cases worker left (changed files in `cases_scope` whose
    new lines carry a `beagle-case:` marker) and the `cite=`s of those markers.

    Interim, until beagle reads the ties from the markers itself
    (dev-notes/beagle-0.48/upstream-asks.md, 3).
    """
    files: list[str] = []
    cites: list[str] = []
    candidates = _changed_files(root)
    if _run(["git", "rev-parse", "--is-inside-work-tree"], root, 30.0)[0] != 0:
        # No history to tell this worker's lines from older ones: every file there.
        candidates = [
            path.relative_to(root).as_posix()
            for entry in cases_scope
            for path in sorted([root / entry, *(root / entry).rglob("*")])
            if path.is_file()
        ]
    for rel in candidates:
        if not _in_scope(rel, cases_scope, root) or not (root / rel).is_file():
            continue
        rc, diff = _run(["git", "diff", "-U0", "HEAD", "--", rel], root, 30.0)
        if rc == 0 and diff:
            lines = [line[1:] for line in diff.splitlines() if line.startswith("+")]
        else:
            try:
                lines = (root / rel).read_text(errors="replace").splitlines()
            except OSError:
                continue
        found = [m.group(1) for line in lines if (m := _CASE_CITE.search(line))]
        if found:
            files.append(rel)
            cites.extend(cite for cite in found if cite not in cites)
    return files, cites


#: The code worker's brief on a task with cases. Run R100: the T0002 code worker
#: corrected three cases that read the source wrong, in the pinned file; the
#: close refused the changed check and the task never closed, though its code
#: passed every hidden test. `pursuit rules 2e`: "A case that reads the source
#: wrong is a finding and an `amend`, never a quiet edit"; tau makes the amend
#: from the worker's quotes (`_settle_case_edits`).
CASES_PINNED_NOTE = (
    "The cases in {files} were written from the source before this work, and the "
    "check runs them as they are: write the code to them, not them to the code. If "
    "a case reads the source wrong, correct only that case, and end your report with "
    'one line per case you changed: `CASE <id>: "<the source\'s words>"`, the id from '
    "its `beagle-case:` line and words copied from the lines its cite= names that "
    "show the case was wrong. A case changed with no such line, or with words its "
    "cited lines do not hold, is put back as it was."
)

_CASE_MARKER = re.compile(r"beagle-case:\s*(\S+)")
_CASE_LINE = re.compile(r"^\s*[`*]*CASE\s+([^\s:`]+)\s*:\s*(.+?)\s*$", re.MULTILINE)
_QUOTE_CLOSE = {'"': '"', "`": "`", "\u201c": "\u201d"}


def _case_key(case: str) -> str:
    """`case` as a CASE line may name it: the marker's id or its test's name, so
    `test_sixty_three_two_byte` and `sixty-three-two-byte` are one case."""
    key = case.strip().casefold().replace("_", "-")
    return key.removeprefix("test-")


def _case_quotes(report: str) -> dict[str, str]:
    """The words of each `CASE <id>: "<words>"` line in `report`, by `_case_key`.
    Run S06: q35 named the case by its test and put its reason after the quote, so
    a quoted line keeps only its first quoted span."""
    quotes: dict[str, str] = {}
    for case, words in _CASE_LINE.findall(report):
        words = words.strip()
        close = _QUOTE_CLOSE.get(words[:1])
        end = words.find(close, 1) if close else -1
        if end > 1:
            words = words[1:end]
        quotes[_case_key(case)] = words.strip().strip("`\"'\u201c\u201d")
    return quotes


def _case_blocks(text: str) -> tuple[str, dict[str, tuple[str, str]]]:
    """`text` split at its `beagle-case:` lines: what comes before the first, and
    each case's id with its cite and its lines up to the next marker."""
    preamble: list[str] = []
    blocks: dict[str, tuple[str, list[str]]] = {}
    current: list[str] = preamble
    for line in text.splitlines():
        marker = _CASE_MARKER.search(line)
        if marker is not None:
            cite = _CASE_CITE.search(line)
            current = [line]
            blocks[marker.group(1)] = (cite.group(1) if cite else "", current)
        else:
            current.append(line)
    return "\n".join(preamble).strip(), {
        case: (cite, "\n".join(lines).strip()) for case, (cite, lines) in blocks.items()
    }


CITE_CONTEXT_LINES = 4


def _cited_text(cite: str, root: Path) -> str:
    """The lines `cite` (`name:12#ab3` or `name:12#ab3-15#c01`) names in references/,
    with the rest of their paragraph, up to CITE_CONTEXT_LINES either side. Run S06:
    a cite names one line, and the sentence that line ends began two lines above."""
    name, _, anchors = cite.partition(":")
    numbers = [int(n) for n in re.findall(r"(\d+)#", anchors)]
    if not numbers:
        return ""
    path = root / REFERENCES_DIR / (name if name.endswith(".txt") else f"{name}.txt")
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return ""
    start = first = numbers[0] - 1
    end = last = numbers[-1]
    while start > 0 and first - start < CITE_CONTEXT_LINES and lines[start - 1].strip():
        start -= 1
    while end < len(lines) and end - last < CITE_CONTEXT_LINES and lines[end].strip():
        end += 1
    return "\n".join(lines[start:end])


def _squeezed(text: str) -> str:
    return " ".join(text.replace("\u2212", "-").split()).casefold()


def _loose(text: str) -> str:
    """`text` squeezed, without the spacing around brackets and commas: the paper's
    `(i1 , i2 )` is a worker's `(i1, i2)`."""
    return re.sub(r"\s*([()\[\]{},])\s*", r"\1", _squeezed(text))


_QUOTED_SPAN = re.compile(r"`([^`\n]+)`|\"([^\"\n]+)\"|\u201c([^\u201d\n]+)\u201d")
QUOTED_SPAN_MIN = 8  # shorter spans (`0`, `fork`) are held by any source


def _case_source_words(
    report: str, case: str, test_names: list[str], cite: str, kind: str, root: Path
) -> str:
    """The source words `report` gives for changing `case`, or "": its CASE line's
    words, else a quoted span on a report line naming the case or its test, held by
    the case's cited paragraph; a `kind=gap` case, which says the source is silent,
    is answered by words anywhere in references/.

    Run R110 (q35): two code workers corrected gap cases that the paper's
    `split(0) = (0, 0)` and `sum(0, i) = i` contradict, quoting them in backticks
    beside the test's name, and put the case's docstring in the CASE line.
    """
    keys = {_case_key(case), *(_case_key(name) for name in test_names)}
    candidates = [words for key, words in _case_quotes(report).items() if key in keys]
    for line in report.splitlines():
        if _CASE_LINE.match(line):
            continue
        named = re.sub(r"(?<![\w-])test-", "", line.casefold().replace("_", "-"))
        if not any(re.search(rf"(?<![\w-]){re.escape(key)}(?![\w-])", named) for key in keys):
            continue
        for span in _QUOTED_SPAN.finditer(line):
            words = next(group for group in span.groups() if group).strip()
            if len(_loose(words)) >= QUOTED_SPAN_MIN:
                candidates.append(words)
    if kind == "gap":
        source = "\n".join(
            path.read_text(errors="replace")
            for path in sorted((root / REFERENCES_DIR).glob("*.txt"))
        )
    else:
        source = _cited_text(cite, root)
    held = _loose(source)
    return next((words for words in candidates if words and _loose(words) in held), "")


def _pinned_text(rel: str, sha: str, root: Path) -> str | None:
    """The text of `rel` whose sha256 is `sha`, from its recent history, or None."""
    rc, out = _run(["git", "log", "--format=%H", "-n", "40", "--", rel], root, 30.0)
    for commit in out.split() if rc == 0 else []:
        shown = subprocess.run(
            ["git", "show", f"{commit}:{rel}"], cwd=root, capture_output=True, check=False
        )
        if shown.returncode == 0 and hashlib.sha256(shown.stdout).hexdigest() == sha:
            return shown.stdout.decode(errors="replace")
    return None


def _settle_case_edits(task: str, report: str, root: Path) -> str:
    """Settle a code worker's edits to `task`'s pinned cases, before its check runs.

    Each changed case needs a `CASE <id>: "<words>"` line in `report` whose words
    the case's cited lines hold: then the check is re-pinned by `pursuit amend`,
    with those lines as the reason. Otherwise the file is put back as pinned. What
    happened, for the step's result, or "" when no case file changed.
    """
    rc, out = _pursuit(["show", task], root)
    record = _json_reply(out) if rc == 0 else None
    if not isinstance(record, dict) or not _strings(record.get("cases")):
        return ""
    pins = dict(
        (path, sha)
        for sha, _, path in (line.partition("  ") for line in _strings(record.get("check_files")))
    )
    quotes = _case_quotes(report)
    changed: dict[str, tuple[str, str]] = {}
    for rel in _strings(record.get("cases")):
        sha = pins.get(rel)
        try:
            now = (root / rel).read_bytes()
        except OSError:
            continue
        if sha is None or hashlib.sha256(now).hexdigest() == sha:
            continue
        old = _pinned_text(rel, sha, root)
        if old is None:
            continue
        changed[rel] = (old, now.decode(errors="replace"))
    if not changed:
        return ""
    why: list[str] = []
    reasons: list[str] = []
    for rel, (old, new) in changed.items():
        old_pre, old_cases = _case_blocks(old)
        new_pre, new_cases = _case_blocks(new)
        if old_pre != new_pre:
            why.append(f"{rel}: the lines before its first case changed")
        for case in sorted(set(old_cases) | set(new_cases)):
            if old_cases.get(case) == new_cases.get(case):
                continue
            cite = (new_cases.get(case) or old_cases[case])[0]
            blocks = [b[1] for b in (old_cases.get(case), new_cases.get(case)) if b]
            kind = next(iter(re.findall(r"\bkind=(\S+)", blocks[0])), "")
            names = re.findall(r"def\s+(test_\w+)", "\n".join(blocks))
            words = quotes.get(_case_key(case), "")
            held = _case_source_words(report, case, names, cite, kind, root)
            if held:
                reasons.append(f'{case}: "{held}"')
            elif not words:
                why.append(f'case {case} changed with no `CASE {case}: "<words>"` line')
            else:
                why.append(f'case {case}: its cited lines ({cite}) do not hold "{words}"')
    files = ", ".join(changed)
    if not why:
        reason = (
            "cases read the source wrong; corrected by the code worker from " + "; ".join(reasons)
        )[:900]
        done_when = str(record.get("done_when") or "")
        amend_rc, amended = _pursuit(
            ["amend", task, "--done-when", done_when, "--reason", reason], root
        )
        if amend_rc == 0:
            return (
                f"The sub-agent corrected case(s) in {files} from the source "
                f"({'; '.join(reasons)}); the check is re-pinned on the record by "
                "`pursuit amend`, with those words as the reason."
            )
        why.append(f"`pursuit amend` refused: {amended.strip()[-300:]}")
    for rel, (old, _new) in changed.items():
        (root / rel).write_text(old)
    return (
        f"The sub-agent changed the pinned cases in {files}, so they are put back as "
        f"pinned: {'; '.join(why)}. A case changes only with a "
        '`CASE <id>: "<the source\'s words>"` line in the report, words its cited lines hold.'
    )


# --------------------------------------------------------------------------- #
# attempts: each check run of a task kept as a commit, ranked by its figure
# --------------------------------------------------------------------------- #

#: Where each check run of a task is kept, as a commit of its scope and case
#: files: `refs/tau/attempts/<task>/<n>`. R129 (g26 semver) went 8/8 → 4/8 of
#: its cases and R131 (q35 cobs) 19/21 → 4/21, each on a later worker's
#: rewrite, and nothing held the better tree to compare or go back to.
ATTEMPT_REFS = "refs/tau/attempts"
#: The identity attempt commits are made under, so they need no git config.
ATTEMPT_IDENTITY = {
    "GIT_AUTHOR_NAME": "tau",
    "GIT_AUTHOR_EMAIL": "tau@localhost",
    "GIT_COMMITTER_NAME": "tau",
    "GIT_COMMITTER_EMAIL": "tau@localhost",
}
_ATTEMPT_TASK = re.compile(r"[A-Za-z0-9][\w.-]*")
_ATTEMPT_TRAILER = re.compile(r"^Tau-Attempt-([\w-]+): ?(.*)$", re.MULTILINE)

#: A word on an output line that says the case it names failed: pytest's
#: FAILED/ERROR, cargo's `... FAILED` and `panicked`, TAP's `not ok`, and the
#: crosses jest and mocha print.
_CASE_FAILED_WORD = re.compile("fail|error|not ok|panicked|[✗×✕✘]", re.I)
#: The test a `beagle-case:` marker heads: `def`/`fn`/`func`/`function NAME`,
#: or a `test("…")`/`it("…")` call.
_CASE_TEST_NAME = re.compile(
    r"\b(?:def|fn|func|function)\s+([A-Za-z_]\w*)"
    r"|\b(?:test|it)\s*\(\s*[\"'`]([^\"'`\n]+)[\"'`]"
)


def _marked_cases(root: Path, case_files: list[str]) -> list[tuple[str, str]]:
    """Each `beagle-case:` marker in `case_files`: its id and the name of the test
    defined below it ("" when none is found)."""
    found: list[tuple[str, str]] = []
    for rel in case_files:
        try:
            text = (root / rel).read_text(errors="replace")
        except OSError:
            continue
        for case, (_cite, block) in _case_blocks(text)[1].items():
            named = _CASE_TEST_NAME.search(block)
            found.append((case, next((g for g in named.groups() if g), "") if named else ""))
    return found


def _failing_cases(output: str, cases: list[tuple[str, str]]) -> list[str]:
    """The ids of `cases` that `output` names, by id or test name, on a line with a
    failure word: `FAILED tests/t.py::test_x`, `test x ... FAILED`, `✕ x`,
    `not ok 3 - x`."""
    lines = [
        re.sub(r"(?<![\w-])test-", "", line.casefold().replace("_", "-"))
        for line in output.splitlines()
        if _CASE_FAILED_WORD.search(line)
    ]
    failing: list[str] = []
    for case, name in cases:
        keys = {_case_key(case), *([_case_key(name)] if name else [])} - {""}
        patterns = [re.compile(rf"(?<![\w-]){re.escape(key)}(?![\w-])") for key in keys]
        if any(p.search(line) for p in patterns for line in lines):
            failing.append(case)
    return failing


def _attempt_figure(rc: int, output: str, cases: list[tuple[str, str]]) -> int:
    """How far a check run got: on exit 0 every marked case (1 when the task marks
    none); else the marked cases its output does not name as failing, and 0 when it
    names none of them failing, since then it did not say which ran.

    Run R131: the check failed at 19/21 and at 4/21, so exit codes alone cannot
    rank the two trees; the case names in the runner's output can, in any language.
    """
    if rc == 0:
        return len(cases) or 1
    failing = _failing_cases(output, cases)
    return len(cases) - len(failing) if failing else 0


@dataclass(frozen=True)
class _Attempt:
    """One kept check run of a task: its ref, number and what the check said."""

    n: int
    ref: str
    exit: int
    figure: int
    total: int
    check: str = ""
    cases: str = ""
    by: str = ""

    @property
    def rank(self) -> tuple[bool, int, int]:
        """A passing check beats a failing one, then the higher figure; ties go to
        the latest."""
        return (self.exit == 0, self.figure, self.n)


def _git_out(
    args: list[str], root: Path, env: Mapping[str, str] | None = None, timeout: float = 30.0
) -> tuple[int, bytes]:
    """Run `git args` in `root` for its stdout bytes, failing soft (rc 1 on any error)."""
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            env=dict(env) if env is not None else None,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return 1, b""
    return proc.returncode, proc.stdout


def _squeezed_line(text: str) -> str:
    return " ".join(text.split())


def _cases_digest(root: Path, case_files: list[str]) -> str:
    """A short hash of the case files' text: figures count only against the same cases."""
    digest = hashlib.sha256()
    for rel in sorted(case_files):
        digest.update(rel.encode() + b"\0")
        with contextlib.suppress(OSError):
            digest.update((root / rel).read_bytes())
    return digest.hexdigest()[:16]


def _attempts(root: Path, task: str, check: str = "", cases: str = "") -> list[_Attempt]:
    """`task`'s kept attempts, oldest first: only those of `check` and of the case
    files hashed `cases`, when given."""
    if not _ATTEMPT_TASK.fullmatch(task):
        return []
    fmt = "--format=%(refname)%1f%(contents)%1e"
    rc, out = _git_out(["for-each-ref", fmt, f"{ATTEMPT_REFS}/{task}/"], root)
    found: list[_Attempt] = []
    for entry in out.decode(errors="replace").split("\x1e") if rc == 0 else []:
        ref, _, message = entry.strip().partition("\x1f")
        fields = dict(_ATTEMPT_TRAILER.findall(message))
        try:
            attempt = _Attempt(
                n=int(ref.rpartition("/")[2]),
                ref=ref,
                exit=int(fields["Exit"]),
                figure=int(fields["Figure"]),
                total=int(fields.get("Total", "0")),
                check=fields.get("Check", ""),
                cases=fields.get("Cases", ""),
                by=fields.get("By", ""),
            )
        except (KeyError, ValueError):
            continue
        if check and attempt.check != _squeezed_line(check):
            continue
        if cases and attempt.cases != cases:
            continue
        found.append(attempt)
    return sorted(found, key=lambda a: a.n)


def _attempt_paths(scope: list[str] | tuple[str, ...], case_files: list[str]) -> list[str]:
    """The paths an attempt keeps: the task's scope and its case files, each once."""
    paths: list[str] = []
    for path in [*scope, *case_files]:
        if path and not os.path.isabs(path) and path not in paths:
            paths.append(path)
    return paths


def _record_attempt(
    root: Path,
    task: str,
    scope: list[str] | tuple[str, ...],
    case_files: list[str],
    check: str,
    verdict: tuple[int, str],
    by: str,
) -> _Attempt | None:
    """Keep the tree's `scope` and case files as `task`'s next attempt, with the
    check's exit and figure as trailers; None when nothing could be kept.

    The commit is built in a scratch index, from HEAD with these paths added, so
    the work tree and the real index are left as they are: the worker's view of
    its files does not change, only a ref is added.
    """
    paths = _attempt_paths(scope, case_files)
    if not paths or not check or not _ATTEMPT_TASK.fullmatch(task):
        return None
    if _git_out(["rev-parse", "--git-dir"], root)[0] != 0:
        return None
    rc, head = _git_out(["rev-parse", "--verify", "-q", "HEAD^{commit}"], root)
    parent = head.decode().strip() if rc == 0 else ""
    cases = _marked_cases(root, case_files)
    figure = _attempt_figure(verdict[0], verdict[1], cases)
    digest = _cases_digest(root, case_files)
    with tempfile.TemporaryDirectory(prefix="tau-attempt-") as scratch:
        env = {**os.environ, **ATTEMPT_IDENTITY, "GIT_INDEX_FILE": str(Path(scratch) / "index")}
        if parent and _git_out(["read-tree", parent], root, env)[0] != 0:
            return None
        for path in paths:
            # A path neither on disk nor in HEAD has nothing to add; the rest still go.
            _git_out(["add", "-A", "--", path], root, env, timeout=120.0)
        rc, tree = _git_out(["write-tree"], root, env)
        if rc != 0:
            return None
        message = (
            f"tau attempt of {task}: exit {verdict[0]}, figure {figure}\n\n"
            f"Tau-Attempt-Task: {task}\n"
            f"Tau-Attempt-Exit: {verdict[0]}\n"
            f"Tau-Attempt-Figure: {figure}\n"
            f"Tau-Attempt-Total: {len(cases)}\n"
            f"Tau-Attempt-Cases: {digest}\n"
            f"Tau-Attempt-By: {by}\n"
            f"Tau-Attempt-Check: {_squeezed_line(check)}\n"
        )
        argv = ["commit-tree", tree.decode().strip(), *(["-p", parent] if parent else [])]
        rc, sha = _git_out([*argv, "-m", message], root, env)
        if rc != 0:
            return None
    commit = sha.decode().strip()
    for _ in range(3):
        n = max((a.n for a in _attempts(root, task)), default=0) + 1
        ref = f"{ATTEMPT_REFS}/{task}/{n}"
        # An empty old value creates the ref only if no one else has.
        if _git_out(["update-ref", ref, commit, ""], root)[0] == 0:
            squeezed = _squeezed_line(check)
            return _Attempt(n, ref, verdict[0], figure, len(cases), squeezed, digest, by)
    return None


def _best_attempt(attempts: list[_Attempt]) -> _Attempt | None:
    return max(attempts, key=lambda a: a.rank, default=None)


def _attempt_said(attempt: _Attempt) -> str:
    """What `attempt`'s check run reached, as the note says it."""
    if not attempt.total and attempt.exit == 0:
        return "passed the check"
    if not attempt.total:
        return f"failed the check (exit {attempt.exit})"
    if attempt.exit == 0:
        return f"passed all {attempt.total} cases"
    return f"passed {attempt.figure} of {attempt.total} cases"


def _attempt_now(attempt: _Attempt) -> str:
    """What the tree as it is reaches, after "this tree"."""
    if not attempt.total:
        return "passes it" if attempt.exit == 0 else f"fails it (exit {attempt.exit})"
    if attempt.exit == 0:
        return f"passes all {attempt.total}"
    return f"passes {attempt.figure}"


def _attempt_note(
    task: str, latest: _Attempt, attempts: list[_Attempt], scope: list[str] | tuple[str, ...]
) -> str:
    """What the model is told when `latest` ranks below the best of `attempts`: the
    best one's ref and figure, and the git commands that show and take back what
    changed since; "" when `latest` is the best.

    R131 (q35 cobs): the last worker's rewrite took T0002 from 19 of 21 cases to 4,
    and the step ended there. The commit and the diff keep what a worse attempt got
    right, which a whole restore would throw away (R132).
    """
    best = _best_attempt(attempts)
    if best is None or best.n == latest.n or best.rank <= latest.rank:
        return ""
    where = " ".join(shlex.quote(path) for path in scope) or "."
    return (
        f"{task}: attempt {best.n} (`{best.ref}`) {_attempt_said(best)}; this tree "
        f"{_attempt_now(latest)}. `git diff {best.ref} -- {where}` shows what changed "
        "since. Keep what helped and put back what broke; "
        f"`git checkout {best.ref} -- <path>` puts one file back."
    )


def _restore_attempt(
    root: Path,
    best: _Attempt,
    latest: _Attempt,
    scope: list[str] | tuple[str, ...],
    case_files: list[str],
) -> list[str]:
    """Put the files in `scope` back as `best` kept them, where `latest` differs, and
    return the paths put back. The case files are left as `_settle_case_edits`
    settled them, and the index is not touched: the files are written, not checked
    out."""
    paths = [path for path in scope if path and not os.path.isabs(path)]
    if not paths:
        return []
    argv = ["diff", "--name-only", "--no-renames", "--relative", "-z", best.ref, latest.ref]
    rc, out = _git_out([*argv, "--", *paths], root)
    if rc != 0:
        return []
    pinned = {os.path.normpath(rel) for rel in case_files}
    restored: list[str] = []
    for rel in filter(None, out.decode(errors="surrogateescape").split("\0")):
        if os.path.normpath(rel) in pinned:
            continue
        rc, entry = _git_out(["ls-tree", "-z", best.ref, "--", rel], root)
        if rc != 0:
            continue
        target = root / rel
        meta = entry.decode(errors="surrogateescape").rstrip("\0").partition("\t")[0]
        try:
            if not meta:
                if target.is_file() or target.is_symlink():
                    target.unlink()
                    restored.append(rel)
                continue
            mode, kind, sha = meta.split()
            if kind != "blob":
                continue
            rc, blob = _git_out(["cat-file", "blob", sha], root)
            if rc != 0:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_symlink():
                target.unlink()
            if mode == "120000":
                target.symlink_to(blob.decode(errors="surrogateescape"))
            else:
                target.write_bytes(blob)
                if mode == "100755":
                    target.chmod(target.stat().st_mode | 0o111)
            restored.append(rel)
        except (OSError, ValueError):
            continue
    return restored


async def _write_cases(
    task: str,
    title: str,
    source: str,
    criteria: str,
    done_when: str,
    scope: list[str],
    arguments: Mapping[str, Any],
    root: Path,
    signal: Any = None,
) -> tuple[list[str], list[str], int | None, str] | str:
    """Run a spec-tied task's cases worker: its case files, their cites, the
    tokens it spent and a note of the cites it re-anchored, or the step's reply
    when the task cannot open on them.

    One cases worker per pursuit_step call; what it wrote stays on disk, so the
    next call's worker corrects it rather than starting over.
    """
    cases_scope = _cases_scope(done_when, root)
    if not cases_scope:
        # Run S02: a `python3 -c` of asserts the driver worked out itself, six of
        # ten wrong against the spec; the cases copied them, and the check never
        # ran the case files.
        return (
            f"pursuit_step: {task} not opened — its source is {source}, so its check "
            f"runs the cases a sub-agent writes from that, and done_when names no test "
            f"file: `{done_when}`\n\nMake done_when the project's test command over the "
            "file the cases go in, e.g. `python3 -m pytest -q tests/test_<part>.py`, with "
            "no expected values in it: the cases read them from the source. Call "
            f'pursuit_step with task="{task}" again.'
        )
    bad_thinking = _bad_thinking(arguments.get("thinking"))
    if bad_thinking:
        return f"pursuit_step: {task} not run — {bad_thinking}"
    source, unfetched = await asyncio.to_thread(_fetched_source, source, root)
    if unfetched:
        return (
            f"pursuit_step: {task} not opened — its source {source} could not be "
            f"fetched, so there is nothing to write its cases from: {unfetched}\n\n"
            f"Fetch it with `beagle refs fetch <url>` (a copy of the page, or a "
            f'mirror), then call pursuit_step with task="{task}" again.'
        )
    # dispatch.toml has no cases role: the executor's pin and the step's choices.
    pin = _dispatch_pin(EXECUTOR_ROLE, root)
    model, provider = _worker_target(arguments.get("model"), arguments.get("provider"), pin)
    thinking = _worker_thinking(model, provider, arguments.get("thinking"), pin)
    timeout = _worker_timeout(arguments.get("timeout"), _worker_wall(root, model, provider))[0]
    brief = _cases_brief(task, title, source, criteria, done_when, scope, cases_scope)
    run = await _run_worker(
        brief, root, model, provider, timeout, signal, task, cases_scope, thinking, CASES_ROLE
    )
    said = f"\n\nIts report:\n{_capped_report(run)}" if run.report else ""
    if run.problem is not None:
        return (
            f"pursuit_step: {task} not opened — the sub-agent writing its cases from "
            f"{source} did not finish: {run.problem}{said}\n\nCall pursuit_step with "
            f'task="{task}" again to have them written.'
        )
    _repair_case_markers(root, cases_scope)
    files, cites = _marker_ties(root, cases_scope)
    spent, reanchored = run.spent, {}
    # R114 (g26) and R115 (lfm24): workers ended without the dry run their brief
    # names, and the open refused them 5-12 min in; the next call's worker read
    # the source again. The host runs it, and the same session mends the cases.
    for mends in range(CASES_DRY_RUN_MENDS + 1):
        if not files:
            break
        moved = _reanchor_cites(root, files, cites)
        reanchored.update(moved)
        cites = [moved.get(cite, cite) for cite in cites]
        refused = _cases_dry_run_refusal(task, criteria, done_when, scope, files, cites, root)
        if refused is None:
            break
        if mends == CASES_DRY_RUN_MENDS or run.transcript is None:
            rc, said_open = refused
            relayed, then = _relay_next(said_open, "")
            return (
                f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{relayed}\n\n"
                f"{task} is not opened. The cases written from {source} stay in "
                f"{', '.join(files)}; the next pursuit_step for {task} has them corrected."
                + (f"\n\n{then}" if then else "")
            )
        brief = _cases_mend_brief(refused[1], cases_scope)
        wall = min(timeout, CASES_MEND_SECONDS)
        run = await _run_worker(
            brief,
            root,
            model,
            provider,
            wall,
            signal,
            task,
            cases_scope,
            thinking,
            CASES_ROLE,
            resume=run.transcript.stem,
        )
        spent = max(spent or 0, run.spent or 0) or None
        if run.problem is not None:
            said = f"\n\nIts report:\n{_capped_report(run)}" if run.report else ""
            return (
                f"pursuit_step: {task} not opened — the sub-agent mending its cases from "
                f"{source} after beagle refused them did not finish: {run.problem}{said}"
                f'\n\nCall pursuit_step with task="{task}" again to have them written.'
            )
        _repair_case_markers(root, cases_scope)
        files, cites = _marker_ties(root, cases_scope)
    if not files:
        return (
            f"pursuit_step: {task} not opened — the sub-agent writing its cases from "
            f"{source} left no test in {', '.join(cases_scope)} with a `beagle-case:` "
            "marker of the form `# beagle-case: <id> cite=<ref>:<anchor> kind=<kind> "
            f"op=<op>`, so there is nothing to tie the task to.{said}\n\nCall pursuit_step "
            f'with task="{task}" again to have them written, or with a done_when that '
            "names the test file the cases go in."
        )
    note = "".join(
        (
            f"Re-anchored the cite {old} to {new}: the anchor of the line it names.\n"
            if old.partition(":")[0] == new.partition(":")[0]
            else f"Moved the cite {old} to {new}: that line, with that anchor, is in "
            f"{new.partition(':')[0]}.\n"
        )
        for old, new in reanchored.items()
    )
    return files, cites, spent, note


#: How many times a refused cases dry run goes back to the worker that wrote them.
CASES_DRY_RUN_MENDS = 2
#: The wall of a cases worker resumed to mend its cases: its source is in context.
CASES_MEND_SECONDS = 300.0
#: A dry run's refusal that is the cases' to mend, not the task's.
_CASES_REFUSAL = re.compile(r"\bcases?\b|beagle-case|\bcites?\b|\bop=")


def _cases_dry_run_refusal(
    task: str,
    criteria: str,
    done_when: str,
    scope: list[str],
    files: list[str],
    cites: list[str],
    root: Path,
) -> tuple[int, str] | None:
    """beagle's exit and words when the task's open, dry run, refuses its cases."""
    argv = ["open", task, "--criteria", criteria, "--done-when", done_when]
    if scope:
        argv += ["--scope", *scope]
    argv += ["--cites", *cites, "--cases", *files, "--dry-run"]
    rc, said = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
    return (rc, said) if rc != 0 and _CASES_REFUSAL.search(said) else None


def _cases_mend_brief(refusal: str, cases_scope: list[str]) -> str:
    """The next prompt of a cases worker whose open, dry run, beagle refused."""
    return (
        "You ended, and the host ran the dry run of the task's open on your cases. "
        f"beagle refused it:\n\n{refusal.strip()}\n\nMend the cases in "
        f"{', '.join(cases_scope)} so it passes, reading the source lines again with "
        "`beagle refs show` where a case needs them; write nowhere else. Run the dry "
        "run again yourself, then end with a report naming the case files and the cites."
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
    #: This call's dispatch.toml pin, once a worker is about to be chosen.
    pinned: list[_DispatchPin] = []
    #: This call's worker wall (`_worker_wall`), once its model is chosen.
    walls: list[float] = []

    async def _execute(
        tool_call_id: str,
        arguments: Mapping[str, Any],
        signal: ToolCancellationToken | None = None,
        on_update: ToolUpdateCallback | None = None,
    ) -> AgentToolResult:
        del tool_call_id
        step_started = _step_clock()
        root, goal = _project_root()
        if goal is None:
            return _step_result("pursuit_step: no pursuit here yet; call pursuit_found first.")
        if _strings(arguments.get("scope")):
            scope, outside = _root_relative_scope(_strings(arguments.get("scope")), root)
            if outside is not None:
                return _step_result(outside)
            arguments = {**arguments, "scope": scope}
        if _strings(arguments.get("locks")):
            kept_lead.append(LOCKS_NOTE)
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
            # here with the root stalled and four milestones abandoned. q35
            # 10-11: under a sealed T0002, pursuit_plan was no way on.
            sealed = _sealed_note(nodes)
            after = (
                "The pursuit is NOT done: these tasks are not done, and nothing took "
                "their work on:\n" + "\n".join(left) + "\n\nDo not tell the user it is "
                "done. "
                + (
                    sealed
                    or "A task that waits on another starts once that one is done. Add "
                    "missing work with pursuit_plan, or give a task a new route with "
                    'pursuit_step task="<id>", new_route=true and notes.'
                )
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
            if done_by is not None and task not in roots and not _lean():
                return _step_result(
                    await _done_by(task, done_by.group(1).upper(), arguments, nodes, root)
                )
            refused = _abandon_problem(task, abandon, nodes)
            if refused is not None:
                return _step_result(refused)
            return _step_result(_abandon(task, abandon, root, goal))
        if ready.get("audit_due") and not _lean():
            return _step_result(await _audit(root, signal, on_update))
        workable = list(dict.fromkeys(open_ids + ready_ids))
        if (
            task
            and not _TASK_ID.fullmatch(task)
            and len(workable) == 1
            and not any(str(n.get("id")) == task for n in nodes)
        ):
            # R106 (lfm24): criteria, done_when and scope right, the task's
            # description in `task`; told to call with no arguments, it lost
            # them. With one task workable, that is the task.
            notes = str(arguments.get("notes") or "").strip()
            arguments = {**arguments, "task": workable[0], "notes": f"{task}\n\n{notes}".strip()}
            kept_lead.append(
                f"Took the task described as {workable[0]}, the one task workable now; "
                f'its description went into the notes. Name it as task="{workable[0]}".\n\n'
            )
            task = workable[0]
            stepped[:] = [task]
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
        probed: dict[str, tuple[int, str]] = {}

        async def probe(command: str) -> tuple[int, str]:
            # One run per offered command in a call, whichever refusal asks.
            if command not in probed:
                probed[command] = await _run_check(command, root, DEFAULT_CHECK_TIMEOUT)
            return probed[command]

        hang = ""
        drop_import = ""
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
                f'Took done_when="{done_when}" as {task}\'s new route without new_route=true: '
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
                if (
                    criteria
                    and old_criteria
                    and " ".join(criteria.split()) != " ".join(old_criteria.split())
                ):
                    # Run R36 #24, #28, #29: refused here for the criteria alone, ahead
                    # of the same-route check below, and the driver sent them again.
                    notes = f"{notes}\n\nCriteria sent with this route: {criteria}"
                    taken = (
                        f"Criteria kept from {task}; yours went into the notes: a new "
                        "route changes how the work is done or checked, not what it is "
                        f"for, so it keeps {old_criteria!r}. If the end itself is wrong, "
                        "that is the user's to change: ask them.\n\n"
                    ) + taken
                    criteria = old_criteria
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
                # The criteria are the bound task's here: other ones went into the notes.
                same_route = " ".join((done_when or old_check).split()) == " ".join(
                    old_check.split()
                ) and sorted(route_scope) == sorted(_strings(record.get("scope")))
                tried = _NOT_DONE.get((str(root), task), 0)
                if same_route and tried >= ESCALATE_AFTER and not _lean():
                    # Run R35 #8, #12, #16: each such route spawned an heir that
                    # was left not done the same way.
                    return _step_result(
                        _unchanged_route_escalation(
                            task,
                            tried,
                            record,
                            f"No new route for {task}: its done_when `{old_check}`, scope and "
                            f"criteria are {task}'s own, and {tried} steps on them have left "
                            "it not done, and a new route that changes nothing gets the same "
                            "result.",
                            root,
                        )
                    )

                async def route_passing(command: str) -> str | None:
                    # The rehearsal's refusal below, for an offered command.
                    passed = (await probe(command))[0] == 0
                    if not passed or await _passes_only_by_uncommitted(
                        command, [route_scope], root, _split_carried(task, root)
                    ):
                        return None
                    return _already_passes(command, task, _tree_nodes(root))

                scoped = (
                    _scope_problem(route_scope, task, nodes, root)
                    or _sibling_owned_check_problem(
                        done_when or old_check, route_scope, task, nodes, root
                    )
                    or _import_scope_problem(done_when or old_check, route_scope, root)
                    or _inverted_exit_problem(done_when or old_check)
                    or _absent_check_file_problem(done_when or old_check, route_scope, root)
                    or _pytest_node_missing_problem(done_when or old_check, route_scope, root)
                    or _pytest_node_import_only_problem(done_when or old_check, route_scope, root)
                ) or await _unwritten_check_problem(
                    done_when or old_check,
                    route_scope,
                    task,
                    root,
                    _strings(record.get("scope")),
                    bound=old_check,
                    is_open=status == "open",
                )
                if scoped is not None:
                    return _step_result(f"pursuit_step: no new route for {task} — {scoped}")
                new_check = done_when or old_check
                rehearsed = await _run_check(new_check, root, DEFAULT_CHECK_TIMEOUT)
                outside = _absent_outside_scope(rehearsed[0], rehearsed[1], route_scope, root)
                if outside:
                    # Run R40 class 4: T0013 and T0014 kept T0011's scope, which could
                    # not hold the test its check ran.
                    return _step_result(
                        f"pursuit_step: no new route for {task} — "
                        + _absent_outside_scope_said(task, new_check, outside, route_scope)
                        + f" Send the call again with scope={json.dumps([*route_scope, *outside])}."
                    )
                if rehearsed[0] != 0 and _check_stopped(new_check, root) is not None:
                    # Run R30 #22: a -9 here fell through to the open, which ran the
                    # check to the cap a second time.
                    killed_run = rehearsed
                if (
                    rehearsed[0] == 0
                    and not _lean()
                    and not (
                        await _passes_only_by_uncommitted(
                            new_check, [route_scope], root, _split_carried(task, root)
                        )
                    )
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
                            else _pending_route_said(task, done_when, scope, criteria)
                            if status == "pending"
                            else "Say more specifically in notes how this route differs."
                        )
                    )
                route = f"{taken}{spawned}\n\n"
                spawns[:] = [(task, successor, spawned)]
                if same_route:
                    _carry_not_done(root, task, successor)
                # q35 R51: W5's last words were kept for T0003's next brief, and the
                # new route to T0007 dropped them; the successor's first brief has them.
                kept_progress = _KILLED_PROGRESS.pop((str(_resolved(root)), task), None)
                if kept_progress:
                    _KILLED_PROGRESS[(str(_resolved(root)), successor)] = kept_progress
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
            and not _lean()
            and not _judge_notes_rerun(task, arguments, record, root)
        ):
            if _broken_check_rerun(task, arguments, record, root):
                # Run R37: the step that broke a passing check earns one rerun at it.
                _BROKEN_RERUN_SPENT.add((str(root), task))
            else:
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
        # T0601: a task with a source has its cases written before it opens.
        source = _task_source(record)
        cases_spent: int | None = None
        case_files: list[str] = []
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
                    + (
                        f"\nIts source is {source}: first another sub-agent writes its "
                        "cases from that as tests, in the test file done_when runs. Write "
                        "no expected values in done_when: the cases read them from the source."
                        if source
                        else ""
                    )
                )
            chained, prose = _and_chain(done_when)
            if prose is not None or chained is None:
                return _step_result(f"pursuit_step: {task} not opened — {prose}")
            route += _bound_note(done_when, chained)
            done_when = chained
            # R112 (lfm24) and R114 (g26): a call with no scope, and one scoped
            # into references/, each ran a cases worker for 5-6 min and was
            # refused only then; a scope judged on its own costs the driver seconds.
            if source:
                carried_scope = scope or _predecessor_scope(record, root)
                wrong_scope = _no_scope_problem(carried_scope, root) or _scope_problem(
                    carried_scope, task, nodes, root
                )
                if wrong_scope is not None:
                    return _step_result(f"pursuit_step: {task} not opened — {wrong_scope}")
            if source:
                cased = await _write_cases(
                    task, title, source, criteria, done_when, scope, arguments, root, signal
                )
                if isinstance(cased, str):
                    return _step_result(cased)
                case_files, case_cites, cases_spent, reanchored = cased
                route += f"{reanchored}\n" if reanchored else ""
                # R108 (g26): T0002's scope held only its test file, and the
                # data-test route that refused it made a second cases worker
                # and left the code worker no file to write. The cases import
                # the code this task writes, so its scope holds that code.
                unwritten = _imports_unwritten(done_when, scope, root)
                if unwritten is not None:
                    _test, module, _via = unwritten
                    top = f"{'src/' if (root / 'src').is_dir() else ''}{module.split('.')[0]}"
                    scope = [*scope, f"{top}.py", f"{top}/"]
                    route += (
                        f"Added {top}.py and {top}/ to {task}'s scope: its cases import "
                        f"`{module}`, the code this task writes.\n\n"
                    )
            rewritten_from: tuple[str, str] | None = None
            # A spec-tied task's check runs its cases as they are: no data-test rewrite.
            data_only = None if source else _data_only_bind(done_when, scope, root)
            if data_only is not None:
                data_check, data_scope, data_note = data_only
                probe = await _run_check(data_check, root, DEFAULT_CHECK_TIMEOUT)
                if probe[0] == 0 and not await _passes_only_by_uncommitted(
                    data_check,
                    [data_scope, _predecessor_scope(record, root)],
                    root,
                    _split_carried(task, root),
                ):
                    # Run R40 class 3: the data test alone already passed, so the
                    # rewrite was refused as no work, four times; the absent test
                    # in scope is the work, and it fails until written.
                    route += _absent_test_kept_note(done_when, data_check, scope, root)
                else:
                    # Run R24 #4: the cases test, not yet written, later imported a
                    # module no path in this scope could hold.
                    if probe[0] != 0 and _check_stopped(data_check, root) is not None:
                        killed_run = probe
                    why = data_note.removeprefix(f"Bound the data test only: `{data_check}`.")
                    rewritten_from = (done_when, " ".join(why.split()))
                    done_when, scope = data_check, data_scope
                    route += data_note
            if not scope and record.get("sibling_of"):
                # Run R18 #56: T0008, spawned with no scope, was refused "no scope given".
                scope = _predecessor_scope(record, root)

            def passing_refusal(
                command: str,
                scope: list[str],
                rewritten_from: tuple[str, str] | None = None,
            ) -> str:
                """The pre-run's refusal of `command`, which passes before any work."""
                now = _tree_nodes(root)
                # The paths `_done_by` takes for the offered call, which names `scope`.
                chosen = scope or _strings(record.get("scope"))
                paths = chosen or _check_targets(command, root)
                done_by = _done_task_in_log(paths, task, now, root)
                named = f"{title}\n{record.get('criteria') or ''}\n{criteria}"
                refused_lead = f"a close done by {done_by} would be refused: "
                _, unwitnessed = (
                    _done_by_witness(
                        task, done_by, command, paths, root, named, refused_lead, targets=not chosen
                    )
                    if done_by
                    else ([], "")
                )
                return _already_passes(
                    command,
                    task,
                    now,
                    done_by,
                    rewritten_from=rewritten_from,
                    scope=scope,
                    unwitnessed=unwitnessed,
                )

            async def open_passing(command: str, scope: list[str]) -> str | None:
                # The pre-run's refusal below, for an offered command.
                if (await probe(command))[0] != 0 or await _passes_only_by_uncommitted(
                    command,
                    [scope, _predecessor_scope(record, root)],
                    root,
                    _split_carried(task, root),
                ):
                    return None
                return passing_refusal(command, scope)

            async def scope_refusal(scope: list[str]) -> str | None:
                return (
                    _no_scope_problem(scope, root)
                    or _scope_problem(scope, task, nodes, root)
                    or _sibling_owned_check_problem(done_when, scope, task, nodes, root)
                    or _doc_only_check_problem(done_when, scope, task, root)
                    or _import_scope_problem(done_when, scope, root)
                    or _inverted_exit_problem(done_when)
                    or _absent_check_file_problem(done_when, scope, root)
                    or _pytest_node_missing_problem(done_when, scope, root)
                    or _pytest_node_import_only_problem(done_when, scope, root)
                ) or await _unwritten_check_problem(
                    done_when,
                    scope,
                    task,
                    root,
                    _predecessor_scope(record, root),
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
            split_work = _split_carried(task, root)
            if pre_rc == 0 and await _passes_only_by_uncommitted(
                done_when, [scope, _predecessor_scope(record, root)], root, split_work
            ):
                route += _on_disk_note(done_when, task, split_work)
                passed_on_disk = (pre_rc, pre_out)
            elif pre_rc == 0 and not _lean():
                return _step_result(
                    f"pursuit_step: {task} not opened — "
                    + passing_refusal(done_when, scope, rewritten_from)
                )
            broke = _check_broke(pre_rc, pre_out, scope, root)
            if broke is not None:
                return _step_result(
                    f"pursuit_step: {task} not opened — the check could not run: `{broke}` "
                    f"(exit {pre_rc}). Correct the command and call pursuit_step again."
                )
            unselected = _selected_none(pre_rc, pre_out, done_when)
            if unselected:
                # Run R43: a -k that matched none of the file's five tests exited 5
                # and was taken as failing now.
                return _step_result(
                    f"pursuit_step: {task} not opened — "
                    + _selected_none_refusal(done_when, unselected, task)
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
            if case_files:
                argv += ["--cites", *case_cites, "--cases", *case_files]
            budget = str(arguments.get("budget") or "").strip()
            if budget:
                argv += ["--budget", budget]
            rc, opened = _pursuit(argv, root, timeout=DEFAULT_CHECK_TIMEOUT + 60)
            ranked = _RANKED_BELOW.search(opened) if rc != 0 else None
            if ranked is not None and (first := _TASK_ID.search(ranked.group(1))):
                # q35 R58 L63: beagle's remedy is `--over "<why>"`, which this
                # tool cannot pass.
                return _step_result(
                    f"pursuit_step: {task} not opened — it ranks below {ranked.group(1)}. "
                    f'Send {first.group()} first, with pursuit_step task="{first.group()}".'
                )
            if rc != 0:
                refused, then = _relay_next(opened, "")
                return _step_result(
                    f"pursuit_step: `beagle pursuit open` refused (exit {rc}):\n{refused}"
                    + (
                        f"\n\n{task} is not opened. The cases written from {source} stay "
                        f"in {', '.join(case_files)}; the next pursuit_step for {task} has "
                        "them corrected."
                        if case_files
                        else ""
                    )
                    + (f"\n\n{then}" if then else "")
                )
            if case_files:
                # beagle pins the cases by hash at the open; commit them as the
                # task's first work, so the code worker starts from them.
                subject = f"{task}: cases from {source}"
                argv = ["commit", task, *case_files, "--subject", subject, "--no-claims"]
                if _pursuit(argv, root)[0] != 0:
                    unsaved = _commit_only(root, case_files, [subject])
                    if unsaved:
                        route += f"The cases are not committed: {unsaved}\n\n"
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
            before = route
            own_scope = scope or _strings(record.get("scope"))
            rejected: tuple[str, str] | None = None
            chained, prose = _and_chain(done_when)
            if prose is not None or chained is None:
                advice = ""
                if prose is not None and "has a bare" in prose and _keepable(bound_check):
                    # Run R17 #23-#25 were told to name a new test in scope; the
                    # bound check was one valid command all along.
                    advice = (
                        f" The bound check `{bound_check}` stands: it is one valid "
                        "command; leave done_when out to keep it."
                    )
                rejected = (f"{prose}", advice)
            else:
                route += _bound_note(done_when, chained)
                done_when = chained
                problem = (
                    _amend_problem(done_when, bound_check)
                    or _inverted_exit_problem(done_when)
                    or _sibling_owned_check_problem(done_when, own_scope, task, nodes, root)
                    or _absent_check_file_problem(done_when, own_scope, root)
                    or _pytest_node_missing_problem(done_when, own_scope, root)
                    or _pytest_node_import_only_problem(done_when, own_scope, root)
                    or await _unwritten_check_problem(
                        done_when,
                        own_scope,
                        task,
                        root,
                        _predecessor_scope(record, root),
                        bound=bound_check,
                        is_open=True,
                    )
                )
                if problem is not None:
                    rejected = (problem, "")
                else:
                    pre_rc, pre_out = await _run_check(done_when, root, DEFAULT_CHECK_TIMEOUT)
                    if pre_rc == 0 and await _passes_only_by_uncommitted(
                        done_when,
                        [own_scope, _predecessor_scope(record, root)],
                        root,
                        _split_carried(task, root),
                    ):
                        # Run R18: the T0151 refusal had the open's blind spot.
                        route += _on_disk_note(done_when, task)
                        # q35 R57: and the amend's worker got no witness note.
                        passed_on_disk = (pre_rc, pre_out)
                    elif pre_rc == 0 and not _lean():
                        keep = (
                            f" Keep the bound check `{bound_check}`: leave done_when out to "
                            "keep it."
                            if _keepable(bound_check)
                            else ""
                        )
                        rejected = (
                            f"`{done_when}` already passes before any work, so it would "
                            f"close {task} on no work.",
                            keep,
                        )
                    broke = (
                        _check_broke(pre_rc, pre_out, own_scope, root) if rejected is None else None
                    )
                    if broke is not None:
                        rejected = (
                            f"the check could not run: `{broke}` (exit {pre_rc}).",
                            " Correct the command and call pursuit_step again.",
                        )
                    elif rejected is None and (
                        unselected := _selected_none(pre_rc, pre_out, done_when)
                    ):
                        rejected = (_selected_none_refusal(done_when, unselected, task), "")
            if rejected is not None:
                reason, advice = rejected
                kept_note = _kept_bound_note(bound_check, notes, reason, own_scope, root)
                if kept_note is None:
                    inverted = _inverted_exit_problem(bound_check) if bound_check else None
                    if inverted is not None:
                        advice += (
                            f" The bound check `{bound_check}` cannot judge the work either: "
                            + inverted
                        )
                    return _step_result(
                        f"pursuit_step: {task}'s check not changed — {reason}{advice}"
                    )
                # Audit 10: each rejection dropped the driver's notes on an open
                # task; the bound check stays and they run, as `_kept_data_check`'s do.
                route = before + kept_note
                done_when = bound_check
            else:
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
                _WITNESS_PENDING.discard((str(root), task))
                _LAST_CHECK_EXIT.pop((str(root), task), None)
                _LAST_CHECK_FAILURE.pop((str(root), task), None)
                # q35 R57: the old check's close demand is not the new check's.
                _NOT_DONE_DEMAND.pop((str(root), task), None)
                kept = _strings(record.get("scope"))
                route += (
                    f"{task}'s check is now `{done_when}`, run on scope {json.dumps(own_scope)}"
                )
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
            # Run R42 class 2: the data test passed on the committed tree, so binding it
            # judged no work, and the import in the check's own test was never dropped.
            own_import = _own_test_import_note(
                bound_check,
                scope or _strings(record.get("scope")),
                root,
                f"{title}\n{record.get('criteria') or ''}\n{criteria}",
            )
            if own_import and await _data_check_passes_committed(
                data_check, [data_route[3], _predecessor_scope(record, root)], root
            ):
                drop_import = own_import
            else:
                on_disk = await _data_route_on_disk(
                    task,
                    data_route,
                    root,
                    _predecessor_scope(record, root),
                    bound=bound_check,
                    is_open=True,
                )
                if on_disk is not None:
                    return _step_result(f"pursuit_step: {task} not run — {on_disk}")
                return _step_result(
                    f"pursuit_step: {task} not run — its bound check `{bound_check}` cannot "
                    f"pass: {problem}"
                    f' Sent as pursuit_step task="{task}", done_when="{data_check}", it is '
                    "taken as this task's new route."
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
        if scope and {os.path.normpath(e) for e in scope} != {
            os.path.normpath(e) for e in _strings(record.get("scope"))
        }:
            # q35 R52: the guard held W8 to the call's scope; its brief named the record's.
            brief = _brief_in_scope(brief, scope)
        references = _references_brief(
            root,
            _data_task(scope or _strings(record.get("scope")), goal, check),
        )
        if references:
            brief = f"{brief}\n\n{references}"
        brief += _last_close_note((str(root), task))
        if _strings(record.get("cases")):
            brief += "\n\n" + CASES_PINNED_NOTE.format(
                files=", ".join(_strings(record.get("cases")))
            )
        briefed_scope = scope or _strings(record.get("scope"))
        if check and _scope_has_data(briefed_scope, root) and _only_data_and_tests(briefed_scope):
            # Run R35: workers took the data check's ImportError for the goal.
            brief += f"\n\n{DATA_CHECK_IMPORT_DEFECT}"
        if notes:
            brief = f"{brief}\n\nFrom the driver (who has not read the reference):\n{notes}"
        if drop_import:
            brief = f"{brief}\n\n{drop_import}"
        if hang:
            brief = f"{brief}\n\n{hang.rstrip()}"
        brief += "\n\n" + NO_BEAGLE_NOTE + "\n\n" + _turn_cap_note()
        try:
            attempts = max(1, int(arguments.get("attempts") or DEFAULT_STEP_ATTEMPTS))
        except (TypeError, ValueError):
            attempts = DEFAULT_STEP_ATTEMPTS
        check_timeout = float(record.get("check_timeout") or DEFAULT_CHECK_TIMEOUT)

        spent: int | None = cases_spent
        report = shown = ended = ""
        verdict: tuple[int, str] = (1, "")
        bad_thinking = _bad_thinking(arguments.get("thinking"))
        if bad_thinking:
            return _step_result(f"pursuit_step: {task} not run — {bad_thinking}")
        pin = _dispatch_pin(EXECUTOR_ROLE, root)
        pinned[:] = [pin]
        model, provider = _worker_target(arguments.get("model"), arguments.get("provider"), pin)
        thinking = _worker_thinking(model, provider, arguments.get("thinking"), pin)
        walls[:] = [_worker_wall(root, model, provider)]
        timeout = _worker_timeout(arguments.get("timeout"), walls[0])[0]
        retry_note = _last_failure_note((str(root), task), check) if status == "open" else ""
        progress_key = (str(_resolved(root)), task)
        retry_note = _KILLED_PROGRESS.get(progress_key, "") + retry_note
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
            elif tests_only and _scope_has_data(scope, root):
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
                f"scope ({', '.join(scope) or 'none'}). Another sub-agent on this route "
                "would change nothing. "
                + how
                + ". Its notes say what the new route does differently.",
                ran=False,
            )
        if not (tests_only and _scope_has_data(scope, root)):
            brief += "\n\n" + WITNESS_NOTE
        elif not (_fixes_known_answers(title) and _check_imports_code(check, root)):
            # Run R28: a fix task's check ran a test importing code, and the note
            # told W3 it imported none.
            brief += "\n\n" + _known_answers_note(check, scope, root)
        if (str(root), task) in _WITNESS_PENDING:
            # R129 (g26 semver): an earlier step made the check pass but ended
            # before the witness was accepted; this worker adds only the witness.
            _WITNESS_PENDING.discard((str(root), task))
            brief += "\n\n" + WITNESS_PENDING_NOTE
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
                proof = await _prove(task, "", scope, root, check_timeout)
        elif passed_on_disk is not None and check == done_when and not _judge_kept_open(task, root):
            # Run R20: T0007's check passed at open on T0003's leftovers, and W11
            # passed at turn 2 and spent 29 more: the work was done; prove and close.
            # q35 R57: not a new route the close judge held: it proved, was held
            # again with no worker, and its notes reached no one.
            verdict = passed_on_disk
            _note_check_run(unproven_key, check, verdict)
            proof = await _prove(task, "", scope, root, check_timeout)
            if proof is not None and (not proof.proven or proof.by_absent_source):
                if proof.proven:
                    proof = _Proof(proven=False, text=proof.text)
                attempts = 1
                retry_note = "\n\n" + ON_DISK_WITNESS_NOTE
        worker_ran = False
        _KILLED_PROGRESS.pop(progress_key, None)
        unreported: list[tuple[int, _WorkerRun, list[str]]] = []
        reported: tuple[int, str] | None = None
        # Run R39: one step is bounded by one budget, not a full timeout per attempt.
        step_budget = timeout * STEP_BUDGET_FACTOR
        budget_spent = ""
        # R117 (g26): a worker copied its 280-char NEEDLE in its reasoning for 10
        # min, since a refused witness cost a new worker; the same session mends it.
        resume = ""
        for attempt in range(1, attempts + 1):
            if verdict[0] == 0 and (proof is None or proof.proven):
                break
            attempt_timeout = timeout
            if attempt > 1:
                left = step_budget - (_step_clock() - step_started)
                if left < min(STEP_ATTEMPT_FLOOR, timeout):
                    budget_spent = (
                        f"This step's time is spent ({attempt - 1} of {attempts} sub-agent "
                        f"attempts ran in its {step_budget:.0f}s budget), so the task "
                        + ("stays blocked" if retrying else "stays open")
                        + f': call pursuit_step with task="{task}" again, with notes '
                        "saying what to fix.\n\n"
                    )
                    break
                attempt_timeout = min(timeout, left)
            if on_update is not None:
                with contextlib.suppress(Exception):
                    on_update(_step_result(f"{task}: sub-agent attempt {attempt} of {attempts}"))
            run = await _run_worker(
                retry_note.strip() if resume else brief + retry_note,
                root,
                model,
                provider,
                attempt_timeout,
                signal,
                task,
                scope,
                thinking=thinking,
                resume=resume,
            )
            resume = ""
            worker_ran = True
            if run.spent is not None:
                spent = (spent or 0) + run.spent
            if run.problem is not None:
                return _not_done(
                    root,
                    task,
                    scope,
                    _implementation_in_tests_lead(root, scope, check)
                    + f"pursuit_step: {task} stays open — {run.problem}\n\n"
                    + _killed_attempt_context(
                        run, shown, verdict, check, root, scope, ended == "reported back"
                    )
                    + f'Call pursuit_step with task="{task}" to send it again.',
                )
            if run.unreported:
                unreported.append((attempt, run, _scope_changes(root, scope)))
            report, shown = run.report, _capped_report(run)
            if report.strip() and not report.startswith(NO_REPORT):
                reported = (attempt, shown)
            elif reported is not None:
                # q35 R52: W7 left no report, and the step result showed its stub,
                # not W6's report that cobs/__init__.py was outside the scope.
                shown = (
                    f"(attempt {attempt} left no report; attempt {reported[0]}'s follows)\n\n"
                    + reported[1]
                )
            # Run R17: W4, W9 and W11 claimed files they never wrote.
            missing = _report_missing_paths(report, root)
            if missing:
                shown = f"{shown}\n\n{missing.rstrip()}"
            helpers_left = _helpers_left_in_scope(root, scope, check)
            if helpers_left:
                shown = f"{shown}\n\n{helpers_left.rstrip()}"
            settled = _settle_case_edits(task, report, root)
            if settled:
                shown = f"{shown}\n\n{settled}"
            if not check:
                verdict = (0, "")
                break
            verdict = await _run_check(check, root, check_timeout)
            _note_check_run(unproven_key, check, verdict)
            # q35 R53: W4 was killed at its second cut-off and wrote no report, and
            # W5's brief said "An earlier attempt reported back".
            ended = (
                "ended without a report"
                if run.unreported or (run.stop_reason == "length" and CUT_OFF_ENDED in report)
                else "reported back"
            )
            if verdict[0] == 0:
                proof = await _prove(task, report, scope, root, check_timeout)
                if proof is None or proof.proven:
                    break
                if not proof.weak and not proof.ask_module:
                    # No defect could be put back: run R02 sent a second worker
                    # after every such verdict, and six identical steps more.
                    _UNPROVEN.add(unproven_key)
                    break
                # q35 R54: W6 was told to make the tests catch the defect, and
                # T0005's scope [pyproject.toml] held no test; its check ran none.
                tests_in_scope = any(
                    _in_scope(test, scope, root) for test in _check_test_files(check, root)
                )
                retry_note = (
                    f"\n\nAn earlier attempt {ended} and the check passes, but `prove` "
                    "could not show the check catches a defect in the work:\n"
                    f"{proof.text}\n"
                    + (
                        "The check passed with the defect put back, so it does not test "
                        "what this task built. Make the task's tests catch such a defect "
                        "(in the test file, not by changing the check), then give a new "
                        "WITNESS block."
                        if proof.weak and tests_in_scope
                        else "The check passed with the defect put back, so it does not "
                        "catch that defect, and no test the check runs is in this task's "
                        f"scope ({', '.join(scope)}): write none. Give a new WITNESS block "
                        "whose NEEDLE is in a file in that scope, a defect the check must "
                        "catch."
                        if proof.weak
                        else "Give that WITNESS block; its NEEDLE must occur exactly once "
                        "in that module."
                        if proof.ask_module
                        else "Give a WITNESS block whose NEEDLE occurs exactly once in a "
                        "source file you changed (not a test)."
                    )
                )
                if run.transcript is not None and not run.unreported:
                    resume = run.transcript.stem
                continue
            retry_note = (
                f"\n\nAn earlier attempt {ended}, but the check still fails (exit "
                f"{verdict[0]}). Its output ends:\n{verdict[1][-CHECK_TAIL_CHARS:]}\n"
            )
            cannot_pass = _data_test_route(check, scope, root)
            if cannot_pass is not None:
                # Run R16 sent W4, W6, W8, W10 and W12 after this was already known.
                break
            if _absent_outside_scope(verdict[0], verdict[1], scope, root):
                # Run R40 class 4: W9-W13 met 21 scope refusals on the file it ran.
                break
            if verdict[0] == 124:
                # Run R39: told only "the check timed out after 60s", W9 re-ran the hang.
                retry_note += f"Exit 124 means the check did not finish: {HANG_MEANING} "
            retry_note = _self_import_note(check, scope, root) + retry_note
            no_tests = _pytest_collected_none(verdict[0], check, verdict[1])
            if no_tests is not None:
                retry_note = f"\n\n{no_tests}" + retry_note
            retry_note += _fix_the_work(verdict[0], verdict[1], check)
            if missing:
                retry_note += "\n\n" + missing.rstrip()
            # q35 R58: W2's cut-off kill note was briefed as its notes. A cut-off
            # kill's notes are what it wrote before the note, if anything.
            cut_off = run.stop_reason == "length" and CUT_OFF_ENDED in report
            notes = (run.last_words if cut_off else report).strip()
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
        if budget_spent:
            attempt -= 1
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
            no_tests = _pytest_collected_none(verdict[0], check, verdict[1])
            if no_tests is not None:
                if_line = ""
            unpassable = ""
            outside = _absent_outside_scope(verdict[0], verdict[1], scope, root)
            if outside:
                # Run R40 class 4: nothing named why every worker on T0011 failed.
                if_line = ""
                unpassable = (
                    _absent_outside_scope_said(task, check, outside, scope)
                    + f" Give it a new route whose scope holds it: pursuit_step "
                    f"task={json.dumps(task)}, new_route=true, "
                    f"scope={json.dumps([*scope, *outside])}, notes saying to write "
                    f"{', '.join(outside)}.\n\n"
                )
            on_disk = (
                await _data_route_on_disk(
                    task,
                    cannot_pass,
                    root,
                    bound=check,
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
            collection = _collection_failure_lead(verdict[1], scope, root)
            self_imported = _data_test_unwritten_import(check, scope, root)
            if self_imported is not None:
                # Run R41 T0005: told to pass a corrected done_when, the driver
                # weakened the check instead of having the import dropped.
                import_lead, next_step = _data_test_import_said(task, check, self_imported)
                unpassable = f"{import_lead}\n\n"
            else:
                next_step = (
                    f'Next: pursuit_step with task="{task}" and notes saying what to fix. '
                    + (
                        f"{if_line}If this route is wrong: "
                        + _spawn_limit_offer(task, check, scope, fresh)
                        if _at_spawn_limit(task, fresh := _tree_nodes(root))
                        else f"{if_line}If this route is wrong, pursuit_step with "
                        f'task="{task}", new_route=true and notes saying what to do instead.'
                    )
                )
            return _not_done(
                root,
                task,
                scope,
                budget_spent
                + (f"{no_tests}\n\n" if no_tests else "")
                + unpassable
                + _cwd_relative_data_lead(verdict[1], scope, root)
                + collection
                + f"{route}{task} — {title}: the check still fails after {attempt} "
                f"sub-agent run(s), so the task {state}.\n\n`{check}` exit {verdict[0]}:\n"
                f"{verdict[1][-CHECK_TAIL_CHARS:]}\n\n"
                + ("" if collection else _implementation_in_tests_lead(root, scope, check))
                + _unreported_runs(unreported, attempt)
                + f"Last report:\n{shown}\n\n"
                + next_step,
            )
        if proof is not None and not proof.proven:
            state = "stays blocked" if retrying else "stays open"
            if proof_note == TESTS_ONLY_MUTATE_NOTE:
                # q35 R59 L47: no module the test imports is on disk to mutate.
                proof_note = _joint_cases_route(check, scope, root) or proof_note
            # The new route the Next offers keeps this check only where the route's
            # open would not refuse it as already passing: one rule for both.
            keeps = (
                tests_only
                and missing_data
                and await _passes_only_by_uncommitted(
                    check, [[*scope, *missing_data]], root, _split_carried(task, root)
                )
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
            if proof.ask_module:
                # R129: the check passes and a witness is obtainable in the
                # module; the next worker adds only that, leaving the work alone.
                _WITNESS_PENDING.add((str(root), task))
            return _not_done(
                root,
                task,
                scope,
                f"{budget_spent}{route}{task} — {title}: the check passes, but "
                f"{why}; the task "
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
                    and not _scope_holds_code_or_data(scope, root)
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
                        if tests_only and missing_data
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
                f"{route}{task} — {title}: the check passes, but the task {state}: "
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
            # R116: beagle shows this body to the tasks that wait on this one, and
            # T0003's worker took T0002's witness for its own; prove recorded it.
            shown_on = _WITNESS.sub("", report).strip()
            body = (unrun_note + shown_on)[:CLOSE_BODY_CHARS] or "-"
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
        superseded = _SUPERSEDED_REPORT_NOTE if rc == 0 and _report_claims_failure(shown) else ""
        # T0602: beagle's `next:` names the move after this close, as a tau call.
        closed, then = _relay_next(
            closed, "Next: call pursuit_step with no arguments for the next task."
        )
        return _step_result(
            f"{route}{task} — {title}: {state}.\n\n{committed}\n\n{closed}\n\n"
            f"{unrun_note}"
            f"{superseded}Sub-agent report:\n{shown}\n\n{then}"
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
        pinned.clear()
        walls.clear()
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
        if walls:
            result = _with_note(result, _worker_timeout(arguments.get("timeout"), walls[0])[1])
        if pinned and pinned[0].rules:
            # After the result: run R23's breaker quotes only a result's first line.
            text = "".join(getattr(c, "text", "") for c in result.content)
            result = _step_result(text + _rules_note(pinned[0], "pursuit_step"))
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
    The refusal names the pursuit_step call for the task beagle offers, so a
    refused driver is one turn from it. `BEAGLE_TAU_DRIVER_EDITS=1` lets it edit.
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
        if refused is not None:
            call = (
                f"{refused[0]} was last refused on a killed check, and the same call is "
                f"refused again; call {refused[1]}"
            )
        elif task := _offered_task(store.parent):
            call = f"Call pursuit_step with task={task}, with what you meant to change in its notes"
        else:
            call = (
                "Call pursuit_step with no arguments: it shows the next ready task; then call "
                "it with that task, with what you meant to change in its notes"
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
    {
        "next", "brief", "show", "status", "view", "tree", "findings", "rules",
        "review-check", "coverage",
    }
)  # fmt: skip


def _worker_beagle_read(argv: list[str]) -> str | None:
    """`argv` itself if it is a beagle read a worker sent on a task may run, or None.

    beagle 0.48 gives a spec-tied task's worker its reads: `refs find` and `refs
    show` print the numbered reference lines a cite copies, `pursuit rules
    [section]` the step's rules, and `pursuit coverage <ref>` the reference's
    lines no done task cites. None of them writes, and neither does the cases
    worker's `pursuit open … --dry-run` (`_cases_dry_run`).
    """
    if not _named(argv, "beagle"):
        return None
    if _cases_dry_run(argv):
        return " ".join(argv)
    words = [arg for arg in argv[1:] if not arg.startswith("-")]
    if words[:2] in (["refs", "find"], ["refs", "show"]):
        return " ".join(argv)
    if words[:2] in (["pursuit", "rules"], ["pursuit", "coverage"]):
        return " ".join(argv)
    return None


def _cases_dry_run(argv: list[str]) -> bool:
    """Whether `argv` is `beagle pursuit open … --dry-run` in a cases worker.

    A dry run makes every refusal and runs the check, binding nothing: the
    cases worker's stop condition (`_cases_brief`). Every other worker, and
    every open that binds, stays the parent's.
    """
    words = argv[1 : argv.index("--")] if "--" in argv else argv[1:]
    return (
        os.environ.get(WORKER_ROLE_ENV, "") == CASES_ROLE
        and _pursuit_verb(argv) == "open"
        and "--dry-run" in words
    )


def _refs_read_call(command: str) -> bool:
    """Whether a bash command only prints reference lines with `beagle refs find`
    or `beagle refs show`, after at most a `cd`, piped at most into filters
    such as head: the anchored read of a reference, as a search of it counts.
    """

    def refs(argv: list[str]) -> str | None:
        words = [arg for arg in argv[1:] if not arg.startswith("-")]
        return _worker_beagle_read(argv) if words[:1] == ["refs"] else None

    def other(argv: list[str]) -> str | None:
        if refs(argv) or _named(argv, "cd") or Path(argv[0]).name in _SEARCH_FILTERS:
            return None
        return argv[0]

    command = _QUIET_REDIRECT.sub(" ", command)
    return _bash_find(command, refs) is not None and _bash_find(command, other) is None


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


def _ruff_over_tree(command: str, cwd: Path, root: Path) -> str | None:
    """The `ruff` rewrite in `command` over the whole tree, not named files, or None.

    Run R14: W5 ran `uv run ruff format .` and `ruff check --fix .`, which
    rewrote the locked tests. Refused: no path, or the project root.
    Named files pass; the scope guard holds those.
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
        return None

    return _bash_find(command, match)


#: Why a worker is kept from beagle and its store.
NO_BEAGLE_REASON = (
    "the brief already holds what the task needs; do the task. A worker does not "
    "inspect .beagle/ or run beagle, beyond the reads `beagle refs find|show`, `beagle "
    "pursuit rules [section]` and `beagle pursuit coverage <ref>`: the session that "
    "sent you does that."
)
#: What a worker is told in its brief, to the same end.
NO_BEAGLE_NOTE = (
    "Do not inspect .beagle/ or run beagle, apart from `beagle doctor`, any beagle "
    "command's `--help`, and the reads `beagle refs find|show`, `beagle pursuit rules "
    "[section]` and `beagle pursuit coverage <ref>`."
)
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


def _beagle_help_or_doctor(argv: list[str]) -> bool:
    """Whether `argv` is a beagle command that only prints: `-h`/`--help` anywhere
    before a `--` (argparse prints the help and exits before any verb acts), or
    `beagle doctor`. S01: a worker was refused a beagle verb's `--help` and
    `beagle doctor`."""
    words = argv[1 : argv.index("--")] if "--" in argv else argv[1:]
    if "-h" in words or "--help" in words:
        return True
    verbs = [arg for arg in words if not arg.startswith("-")]
    return verbs[:1] == ["doctor"]


def _substituted(command: str) -> list[str]:
    """The commands `$(...)` and backticks run inside `command`, quoted or not.

    shlex keeps `"$(beagle pursuit close T1)"` one word, and a backtick in the
    word it touches, so an allowed `beagle` call could carry another unseen.
    """
    found: list[str] = []
    at = 0
    while at < len(command):
        if command.startswith("$(", at):
            depth, end = 1, at + 2
            while end < len(command) and depth:
                depth += {"(": 1, ")": -1}.get(command[end], 0)
                end += 1
            found.append(command[at + 2 : end - 1 if not depth else end])
            at += 2
        elif command[at] == "`":
            end = command.find("`", at + 1)
            found.append(command[at + 1 : end if end != -1 else len(command)])
            at = end + 1 if end != -1 else len(command)
        else:
            at += 1
    return found


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
        if argv[0] in ("eval", "xargs"):  # the command they run is in their words
            named = [at for at, arg in enumerate(argv) if Path(arg).name == "beagle"]
            if argv[0] == "eval":
                return _bash_find(" ".join(argv[1:]), match)
            return match(argv[named[0] :]) if named else None
        if _named(argv, "beagle"):
            if _beagle_help_or_doctor(argv) or _worker_beagle_read(argv):
                return None
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
    for inner in _substituted(command):
        found = _bash_find(inner, match)
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


def _read_path(
    tool: str, args: Mapping[str, Any], cwd: Path, hit: Callable[[Path], bool]
) -> str | None:
    """The path a read or a reading command names for which `hit` holds, or None."""

    def held(word: str) -> bool:
        try:
            return hit(cwd / Path(word).expanduser())
        except RuntimeError:  # `~user` with no such user
            return False

    if tool == "read":
        raw = str(args.get("path") or "")
        return raw if raw.strip() and held(raw) else None
    if tool != "bash":
        return None

    def match(argv: list[str]) -> str | None:
        if Path(argv[0]).name not in _READERS:
            return None
        return next((a for a in argv[1:] if a and not a.startswith("-") and held(a)), None)

    return _bash_find(str(args.get("command", "")), match)


def _sibling_read(tool: str, args: Mapping[str, Any], cwd: Path, root: Path) -> str | None:
    """The path a read or a reading command names beside the project, or None."""
    return _read_path(tool, args, cwd, lambda path: _beside(path, root))


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


def _task_record(goal: Path, task: str) -> dict[str, Any]:
    """The task's record in the pursuit's tree, or {}."""
    try:
        text = (goal.parent / "tree" / f"{task}.md").read_text(encoding="utf-8")
        return tomllib.loads(text.split("+++")[1])
    except (OSError, IndexError, ValueError):
        return {}


def _task_check(goal: Path, task: str) -> str:
    """The task's bound `done_when`, read from its record in the pursuit's tree; or ""."""
    return str(_task_record(goal, task).get("done_when") or "")


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


def _reads_needed(path: Path) -> tuple[int, int] | None:
    """A file's line count and the reads one pass through it takes, or None."""
    try:
        count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return None
    return count, max(1, -(-count // WINDOW_LINES))


_GREPS = frozenset({"grep", "egrep", "fgrep", "rg"})
_GREP_VALUES = frozenset({"-e", "-f", "-m", "-A", "-B", "-C", "--regexp", "--file", "--max-count"})
_FILTER_VALUES = frozenset({"-n", "-c", "-d", "-f", "-k", "-t"})
_SEARCH_FILTERS = frozenset({"head", "tail", "sort", "uniq", "wc", "cut", "nl"})
_QUIET_REDIRECT = re.compile(r"\s2>(?:&1|\s*/dev/null)")
_SED_PRINT = re.compile(r"(?:\d+|\$)(?:,(?:\d+|\$))?p|/[^/]*/p")


def _searched_files(program: str, args: list[str], piped: bool) -> list[str] | None:
    """The files one command of a reference search reads, or None if it is not
    a search: grep or rg, tilth with --scope, `sed -n '<lines>p'`, or, fed by a
    pipe, a filter such as head."""
    if program in _GREPS:
        positional = _positional(args, _GREP_VALUES)
        patterned = any(a.split("=")[0] in ("-e", "-f", "--regexp", "--file") for a in args)
        return positional if patterned else positional[1:]
    if program == "tilth":
        scoped = [value for flag, value in itertools.pairwise(args) if flag == "--scope"]
        return scoped + [a.removeprefix("--scope=") for a in args if a.startswith("--scope=")]
    if program == "sed":
        positional = _positional(args)
        if "-n" not in args or _sed_in_place_files(args) or not positional:
            return None
        return positional[1:] if _SED_PRINT.fullmatch(positional[0]) else None
    if piped and program in _SEARCH_FILTERS:
        return _positional(args, _FILTER_VALUES)
    return None


def _reference_search_call(command: str, cwd: Path, root: Path) -> bool:
    """Whether a bash command only searches the references: grep, rg, tilth or
    `sed -n '<lines>p'` over paths under references/, piped at most into filters
    such as head.

    q35 R51: the read guard's refusal offered `grep -n ... references/*.txt`, and
    the bash guard then refused W2's four greps and W3's two searches of it.
    """
    tokens = _shell_tokens(_QUIET_REDIRECT.sub(" ", command))
    if not tokens:
        return False
    references = root / REFERENCES_DIR
    segments: list[tuple[str, list[str]]] = []
    separator, words = ";", []
    for token in [*tokens, ";"]:
        if token in ("|", "&&", "||", ";"):
            if words:
                segments.append((separator, words))
            elif token != ";":
                return False
            separator, words = token, []
        elif _is_operator(token):
            return False
        else:
            words.append(token)
    for separator, (program, *args) in segments:
        piped = separator == "|"
        files = _searched_files(program, args, piped)
        if files is None or not (files or piped):
            return False
        for name in files:
            path = _own_path(cwd / Path(name).expanduser(), root)
            if path != references and references not in path.parents:
                return False
    return bool(segments)


def _reference_window(
    arguments: Mapping[str, Any], cwd: Path, root: Path
) -> tuple[Path, int, int] | None:
    """The reference window a ranged read asks for, (file, first line, limit), or None.

    A read of a file under references/ with an explicit limit of at most
    WINDOW_LINES is a window; a read without one pages the file whole (R40).
    """
    path = arguments.get("path")
    if not isinstance(path, str) or not path:
        return None
    first, limit = read_request(arguments)
    if limit is None or limit > WINDOW_LINES:
        return None
    target = _own_path(cwd / Path(path).expanduser(), root)
    if root / REFERENCES_DIR not in target.parents:
        return None
    return target, first, limit


def _free_reference_call(
    tool: str,
    arguments: Mapping[str, Any],
    command: str,
    cwd: Path,
    windows: set[tuple[Path, int, int]],
) -> str | None:
    """What a call that the nothing-written refusals do not count is: "read" for
    the first read of a reference window, "search" for a search confined to the
    references; else None. The window is recorded as read.

    q35 R51: a known-answers brief asks for ranged reads and searches of the
    references, and W1-W3 were refused them at 15-25 of 30 calls although they
    read each window once. The guards were built for 9Bs re-reading the same
    windows (R33, R34, R40), and a second read of a window is not free.
    """
    goal = _find_goal(cwd) if tool in ("read", "bash") else None
    if goal is None:
        return None
    root = _resolved(goal.parent.parent)
    if tool == "bash":
        if command and (_reference_search_call(command, cwd, root) or _refs_read_call(command)):
            return "search"
        return None
    window = _reference_window(arguments, cwd, root)
    if window is None or window in windows:
        return None
    windows.add(window)
    return "read"


def _reread_refusal(
    tool: str,
    arguments: Mapping[str, Any],
    cwd: Path,
    scope: tuple[str, ...],
    calls: int,
    reads: dict[Path, int] | None = None,
) -> str | None:
    """Why a worker's read is refused once half its calls went with nothing written, or None.

    Run R33: W3 and W7 spent their calls re-reading references in short windows
    and wrote their file at the last call, or never ran the check. A read of a
    file in the scope passes while its reads fit one pass through the file and a
    quarter of the cap: a write may need it, and a file too long to page within
    the cap is queried instead. `reads` counts each file's reads so far. Run
    R34: W9 paged the in-scope 4048-line tests/ data file 27 times and wrote nothing.
    Run R40: workers re-read whole references 6-20 times; a refused read of one
    offers the search that finds the line instead.
    """
    if _lean():
        return None
    cap = _worker_max_turns()
    if tool != "read":
        return None
    path = arguments.get("path")
    goal = _find_goal(cwd)
    if not isinstance(path, str) or not path or goal is None:
        return None
    root = _resolved(goal.parent.parent)
    target = _own_path(cwd / Path(path).expanduser(), root)
    seen = 1
    if reads is not None:
        seen = reads[target] = reads.get(target, 0) + 1
    if calls <= cap // 2:
        return None
    if (target == root or root in target.parents) and _scope_hit(target, root, scope) is not None:
        size = _reads_needed(target)
        budget = max(1, cap // 4)
        if size is None or seen <= min(size[1], budget):
            return None
        count, needed = size
        paging = (
            f"that one pass reads in {needed} at {WINDOW_LINES} lines per read"
            if needed <= budget
            else f"that takes {needed} reads at {WINDOW_LINES} lines per read, more than "
            f"the {budget} a file gets under a cap of {cap}"
        )
        return (
            f"refusing to read {path} again: this is read {seen} of a {count}-line file "
            f"{paging}, and "
            f"{calls - 1} of {cap} calls are used with nothing written. Query it instead, "
            "e.g. `python3 -c` over the file for the case or line you need, and write "
            f"{', '.join(scope)} now."
        )
    # No scope names references/ (`_scope_problem`), so its reads land here.
    if root / REFERENCES_DIR in target.parents:
        return (
            f"refusing to read {path}: {calls - 1} of {cap} calls used and nothing written. "
            f"Search the references instead with bash, `{_reference_search()}`, for the "
            f"line that gives the value you need, then write {', '.join(scope)} now."
        )
    return (
        f"refusing to read {path}: {calls - 1} of {cap} calls used and nothing written. "
        f"Write {', '.join(scope)} now; re-read only what a write needs."
    )


def _idle_bash_refusal(
    command: str, goal: Path, task: str, scope: tuple[str, ...], calls: int
) -> str | None:
    """Why a bash command that writes nothing in scope is refused late, or None.

    Past three-quarters of the cap with nothing written, only the task's check
    runs. Run R34: W7's ~12 encoder trials and W8's analysis scripts wrote no
    file and ran into the cap. Fails open when the task has no bound check.
    """
    if _lean():
        return None
    cap = _worker_max_turns()
    if calls <= cap * 3 // 4:
        return None
    check = " ".join(_task_check(goal, task).split())
    if not check or check in " ".join(command.split()):
        return None
    return (
        f"refusing to run this command: {calls - 1} of {cap} calls used and nothing "
        f"written, and a command that is not the check changes nothing in the scope. "
        f"Write {', '.join(scope)} now with `write` or `edit`, then run the check: {check}"
    )


def _task_log(root: Path, task: str) -> Path | None:
    """The one file under .git/beagle/ a worker sent on `task` may write: the log
    beagle's brief redirects its runs to (`_brief_scratch`), or None with no task."""
    return root / ".git" / "beagle" / "logs" / f"{task}.log" if task else None


def _store_write_refusal(rel: Path, root: Path, log: Path | None) -> str:
    """Why a worker may not write `rel` under .git/beagle/.

    Run R35: W15-W17 wrote .git/beagle/logs/T0006.result.md, .git/beagle/T0006.md
    and .git/beagle/{finding,memory,obligations,pursuit,findings}/T0006.md to
    record a close the driver runs.
    """
    own = (
        f" The one file there that is yours is {log.relative_to(root)}, the log your "
        "runs are redirected to."
        if log is not None
        else ""
    )
    return (
        f"refusing to write {rel}: beagle's store under .git/beagle/ is the driver's, "
        "and so is the close. Put your result in your report." + own
    )


def make_worker_scope_guard() -> Any:
    """Build the `tool_call` guard that keeps a worker's writes inside its task's scope.

    The scope was recorded and not enforced: in run R02 a worker wrote
    `tests/` over .gitignore with two turns left, and the next three steps went
    to repairing it. A worker sent with a scope (`BEAGLE_TAU_WORKER_SCOPE`) may
    write in it, outside the project (/tmp), in beagle's store (the record guard
    has that) and the task's log, `.git/beagle/logs/<task>.log`; nothing else
    under `.git/beagle/` (run R35). A known-answers task's worker writes no new
    source outside tests/ (run R36). A link in the project is
    judged by its own path, and one an inline script makes may not point out
    of the project. A worker with no scope is not held. Any worker sent on a
    task is kept from reading the trees beside its project. A path refused
    again in the session is told how often, and to write in the scope or end
    the turn with its report (mining: 210 of 400 scope refusals repeated one).
    Fails open.
    """

    cut_offs = 0
    calls = 0
    wrote = False
    reads: dict[Path, int] = {}
    windows: set[tuple[Path, int, int]] = set()
    offered = False
    refusals: dict[Path, int] = {}

    async def guard(event: Any, context: ExtensionContext) -> ToolCallHookResult | None:
        nonlocal cut_offs, calls, wrote, offered
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
                ruff = _ruff_over_tree(command, cwd, root)
                if ruff is not None:
                    files = ", ".join(sent[1]) if sent is not None else "the files you changed"
                    return ToolCallHookResult(
                        block=True, reason=f"refusing {ruff}. Name the files instead: {files}."
                    )
            if sent is None:
                return None
            task, scope = sent
            known = _only_data_and_tests(list(scope))
            free = _free_reference_call(event.tool_name, arguments, command, cwd, windows)
            uncounted = free is not None and known
            if uncounted:
                calls -= 1  # q35 R51: not counted toward the nothing-written refusals
            reread = (
                None
                if wrote or uncounted
                else _reread_refusal(event.tool_name, arguments, cwd, scope, calls, reads)
            )
            if reread is not None:
                offered = offered or _reference_search() in reread
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
            searched = free == "search" and (uncounted or offered)
            idle = bool(command) and not wrote and sent_on_task and not searched
            goal = _find_goal(cwd) if targets or idle else None
            if goal is None:
                return None
            root = _resolved(goal.parent.parent)
            allowed = [_resolved(goal.parent)]
            store = root / ".git" / "beagle"
            log = _task_log(root, os.environ.get(WORKER_TASK_ENV, "").strip())
            in_store = False
            hits = 0
            for target in targets:
                target = _own_path(target, root)
                if target != root and root not in target.parents:
                    continue  # outside the project: /tmp, /dev/null
                if target == log:
                    continue
                if target == store or store in target.parents:
                    in_store = True
                    break
                if any(target == a or a in target.parents for a in allowed):
                    continue
                if _CACHE_DIRS & set(target.parts):
                    continue
                if _scope_hit(target, root, scope) is None:
                    break
                hits += 1
            else:
                refused = _link_out(links, root)
                if idle and hits == 0 and refused is None:
                    late = _idle_bash_refusal(command, goal, task, scope, calls)
                    if late is not None:
                        return ToolCallHookResult(block=True, reason=late)
                wrote = wrote or (hits > 0 and refused is None)
                return refused
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        rel = target.relative_to(root) if target != root else target
        if in_store:
            return ToolCallHookResult(block=True, reason=_store_write_refusal(rel, root, log))
        source = (
            # Run R09: refused src/, W4 wrote the library to tests/itc/ instead.
            " The implementation does not go under tests/ either: it is a later "
            "task's work, so report it instead."
            if rel.suffix == ".py" and not _is_test_path(rel.as_posix())
            else ""
        )
        scopes = ", ".join(scope)
        refusals[rel] = refusals.get(rel, 0) + 1
        times = refusals[rel]
        again = (
            # Run R21: W5 was refused itc/__init__.py and itc/clock.py 12 times, to the breaker.
            f"refusing to write {rel}: it is outside {task}'s scope ({scopes}), refused "
            f"again, {times} times now. No write outside the scope will be taken: write "
            f"only under {scopes}, or end the turn now with your report"
            if times > 1
            else ""
        )
        if _scratch_like(rel):
            if again:
                return ToolCallHookResult(
                    block=True,
                    reason=f"{again} naming {rel} as follow-up. Scratch files go in /tmp.",
                )
            return ToolCallHookResult(
                block=True,
                reason=(
                    f"refusing to write {rel}: it is outside {task}'s scope "
                    f"({scopes}); name it in your report as follow-up. Scratch "
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
        if again:
            named = f" naming {rel} as needed." if needed != "." else "."
            return ToolCallHookResult(block=True, reason=f"{again}{named}{imported}{source}")
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing to write {rel}: it is outside {task}'s scope "
                f"({scopes}). Work written outside {task}'s scope is not its work "
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

                # S01: `--help` prints and exits, whatever verb it follows.
                def write(argv: list[str]) -> str | None:
                    if _beagle_help_or_doctor(argv) or _cases_dry_run(argv):
                        return None
                    return _pursuit_write_verb(argv)

                verb = next(
                    (
                        found
                        for each in (command, *_substituted(command))
                        if (found := _bash_find(each, write)) is not None
                    ),
                    None,
                )
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
    "close": "pursuit_step, which closes a task on its check",
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
    "next": ("pursuit_step with no arguments, which picks the ready task and says what to send"),
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


#: How many tasks a close steer names as ones its task may be dropped as a repeat of.
_DROP_TAKERS = 5
_SENTENCE_BREAK = re.compile(r"(?<=\.)\s+(?=[A-Z])")


def _close_argv(argv: list[str]) -> str | None:
    """A `beagle pursuit close` argv's task and why to drop it, as JSON, or None."""
    if _steered_verb(argv) != "close" or "close" not in argv:
        return None
    task, values = "", {"--abandon": "", "--reason": "", "--outcome": ""}
    args = iter(argv[argv.index("close") + 1 :])
    for arg in args:
        name, eq, value = arg.partition("=")
        if name in values:
            values[name] = value if eq else next(args, "")
        elif not task and _TASK_ID.fullmatch(arg):
            task = arg
    why = values["--abandon"] or (values["--reason"] if values["--outcome"] == "abandoned" else "")
    return json.dumps([task, why.strip()])


def _close_drop(command: str, root: Path) -> str:
    """How the driver may drop the task of a `beagle pursuit close` it was refused.

    Runs R06, R08, R22, R26 and R28 closed a founding milestone from bash, were
    told to drop it with abandon='<why>', and had every why refused: a milestone
    is the goal's. So the tree decides: a drop is offered only where
    `_abandon_problem` takes it, and otherwise what its refusal says to do.
    """
    found = _bash_find(command, _close_argv)
    task, why = json.loads(found) if found else ("", "")
    nodes = _tree_nodes(root) if task else []
    ids = [str(n.get("id")) for n in nodes]
    if task not in ids:
        return ABANDON_HINT
    call = f'pursuit_step task="{task}"'
    plain = why and not _DONE_BY.match(why) and not _INFEASIBLE.match(why)
    if plain and _abandon_problem(task, why, nodes) is None:
        return f"To drop {task} for that reason, call {call}, abandon={json.dumps(why)}."
    others = [t for t in ids if t != task]
    takers = [t for t in others if _abandon_problem(task, f"duplicate of {t}", nodes) is None]
    if takers:
        named = ", ".join(takers[:_DROP_TAKERS])
        if len(takers) > _DROP_TAKERS:
            named += f" and {len(takers) - _DROP_TAKERS} more"
        return (
            f'To drop {task} as a repeat, call {call}, abandon="duplicate of Tnnnn", '
            f"naming as Tnnnn the task that holds its work, one of: {named}."
        )
    status = {str(n.get("id")): n.get("status") for n in nodes}
    live = [t for t in others if status.get(t) in ("done", "open")]
    refusal = _abandon_problem(task, f"duplicate of {(live or others or [''])[0]}", nodes) or ""
    body = refusal.split(" not abandoned — ", 1)[-1]
    kept = [s for s in _SENTENCE_BREAK.split(body) if "abandon=" not in s]
    return f"{task} is not one to drop: {' '.join(kept)}"


def _amend_argv(argv: list[str]) -> str | None:
    """The task a `beagle pursuit amend` argv names, or None."""
    if _steered_verb(argv) != "amend" or "amend" not in argv:
        return None
    rest = argv[argv.index("amend") + 1 :]
    return next((arg for arg in rest if _TASK_ID.fullmatch(arg)), "")


def _amend_steer(command: str, root: Path) -> str:
    """Where a `beagle pursuit amend` run from bash goes, for the task it names.

    q35 10-11: ten bash amends of container T0002 were each sent to "pursuit_step
    on the open task", which refuses a container as not a task to work.
    """
    task = _bash_find(command, _amend_argv) or ""
    node = next((n for n in _tree_nodes(root) if str(n.get("id")) == task), None)
    if node is None or node.get("status") == "open" and not node.get("container"):
        return f"use {_STEERED_VERBS['amend']}."
    call = f"pursuit_step task={json.dumps(task)}"
    if node.get("container"):
        return (
            f"{task} is a container, and pursuit_step does not take one. What it is for "
            "is the user's to change: stop and ask them. A part's check changes with "
            f"{call.replace(task, 'Tnnnn')} and the new done_when, on an open part."
        )
    status = str(node.get("status") or "")
    if status == "pending":
        return (
            f"{task} is pending, and its check is bound when it opens: {call} with the "
            "new done_when opens it on that check once it is ready (pursuit_step with "
            "no arguments hands out the ready one)."
        )
    if status == "blocked":
        return f"{task} is blocked: {call}, new_route=true, the new done_when and notes."
    return (
        f"{task} is {status or 'not in the tree'}, and no pursuit tool changes a closed "
        "task: if its record is wrong, tell the user."
    )


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
            command = str((event.arguments or {}).get("command", ""))
            verb = _bash_find(command, _steered_verb)
            goal = _find_goal(Path(context.cwd)) if verb is not None else None
            if verb is None or goal is None:
                return None
        except Exception:  # noqa: BLE001 - fail open, never block on a guard bug
            return None
        drop = ""
        use = f"use {_STEERED_VERBS[verb]}."
        if verb == "amend":
            # A tree it cannot read gets the plain steer.
            with contextlib.suppress(Exception):
                use = _amend_steer(command, goal.parent.parent)
        if verb == "close":
            try:
                drop = f" {_close_drop(command, goal.parent.parent)}"
            except Exception:  # noqa: BLE001 - a tree it cannot read gets the plain offer
                drop = f" {ABANDON_HINT}"
        return ToolCallHookResult(
            block=True,
            reason=(
                f"refusing `beagle pursuit {verb}` from bash: {use} "
                f"The tool runs it with the checks around it that the bare verb skips.{drop}"
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
            task, entry, count, where = held
            refused = (
                f"refusing to read {target} from the driving session: it is in the "
                f"scope of {task} ({entry}), which {count} steps have left not done, "
                "and debugging its work is the sub-agent's."
            )
            # Run R37 E16: past the cap, this pointed at a notes step and a new
            # route that the step guard refused alike; the escalation's own options.
            escalated = _escalated_calls([task], where) if count >= ESCALATE_AFTER else ""
            if escalated:
                return ToolCallHookResult(block=True, reason=f"{refused}{escalated}")
            return ToolCallHookResult(
                block=True,
                reason=(
                    f"{refused} Say what to fix in pursuit_step's notes "
                    f'(task="{task}"), or give it a new route: pursuit_step task="{task}", '
                    "new_route=true, with a rewritten done_when and notes saying what to "
                    "do differently."
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


#: What beagle keeps under `.beagle/` as its record of the pursuit. Only beagle
#: and this extension write them; the `*.toml` beside them is configuration, and
#: editable.
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
    _record_session_model(context)
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
    "references or design the solution first: `pursuit_step` sub-agents read the "
    "references as each task needs them. The design is part of the implementation, "
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


def _note_founded(goal: Path) -> None:
    """Count founding's result as this session's state note.

    It carries the goal, criteria and tree, so the next run's start sends no
    second one. Run 10 founded mid-session and kept only the not-yet-founded
    orientation; the system prompt now says how to work a founded pursuit
    from load, and this result and the note after each compaction say which.
    """
    del goal
    _STATE_NOTED.add(_STARTED_SESSION or "")


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


def _pursuit_state(root: Path, goal: Path) -> str:
    """Where the pursuit stands, from beagle and the goal file.

    The goal and criteria, `beagle pursuit tree`, the ready (or open) tasks,
    and the last `pursuit_step` result on each of them.
    """
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
    last = ""
    for task in ready_ids + open_ids:
        if task in _LAST_STEP_RESULT:
            last += f"\n\nLast pursuit_step on {task} said:\n{_LAST_STEP_RESULT[task]}"
    sealed = _sealed_note(nodes)
    parts = [
        _goal_text(goal),
        _tree(root),
        f"{now} Next: call pursuit_step with no arguments. "
        + (
            f"{sealed}{last}"
            if sealed
            else f"Work no task covers goes in with pursuit_plan; this session does not "
            f"do it itself.{last}"
        ),
    ]
    return "\n\n".join(part for part in parts if part)


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
        tau.send_custom_message(
            "The conversation was just compacted. Where the pursuit stands, from beagle "
            f"itself (trust this over the summary):\n\n{_pursuit_state(root, goal)}",
            custom_type="beagle",
            deliver_as="steer",
        )

    return note


def make_state_at_session_start(tau: ExtensionAPI) -> Any:
    """At a session's first run, tell the driver where the pursuit stands.

    The state used to be a system prompt section, which a pursuit founded
    mid-session had to swap in, re-prefilling the whole context. As a message
    after the user's request it changes no prefix. Only the host's session
    gets it, once: founding's result and the note after a compaction carry
    the same state later.
    """

    async def note(event: Any, context: ExtensionContext) -> None:
        del event
        session = context.session_id or ""
        if session in _STATE_NOTED or session != (_STARTED_SESSION or ""):
            return
        root, goal = _project_root()
        if goal is None:
            return
        _STATE_NOTED.add(session)
        state = await asyncio.to_thread(_pursuit_state, root, goal)
        report = (
            f"\n\nAt session start, `beagle hook loop-report` said:\n\n{_LOOP_REPORT}"
            if _LOOP_REPORT
            else ""
        )
        tau.send_custom_message(
            f"Where the pursuit stands as this session starts, from beagle:\n\n{state}{report}",
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

    Run R38: setup call 6 was `agent`, whose sub-agent ran 57 minutes outside
    the pursuit, with no scope, check or time limit. Before founding, `agent`
    is refused whatever the count, and does not spend it.
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
        if event.tool_name == "agent":
            return ToolCallHookResult(
                block=True,
                reason=(
                    "refusing agent: the pursuit is not founded, and a sub-agent started "
                    "now works outside it, with no scope, no check and no time limit. "
                    "Reading the references and writing the known answers is "
                    "pursuit_step's first milestone. Call pursuit_found now (again, "
                    "fixing what its refusal named, if it was refused)."
                ),
            )
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
    for segment in re.split(r"&&|\|\||[;|\n]", _strip_heredocs(command)):
        try:
            words = shlex.split(segment)
        except ValueError:
            words = segment.split()
        # Run R22: `touch` and `ln -sf /dev/null` into `.beagle/locked/` went through.
        if any(".beagle" in target for target in _command_targets(words, Path.cwd())):
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
#: Whether the last pursuit tool result in this run offered STOP_OPTION.
_STOP_OFFERED = False
#: Driver turns in a row that ended at the output limit without acting.
_CUTS_IN_A_ROW = 0


def _reset_stop_gate(event: Any, context: ExtensionContext) -> None:
    global _STOP_GATE_SENT, _STOP_OFFERED, _CUTS_IN_A_ROW
    del event, context
    _STOP_GATE_SENT = 0
    _STOP_OFFERED = False
    _CUTS_IN_A_ROW = 0


def _tau_nudges_cut(message: Any) -> bool:
    """Whether tau sends its own follow-up to `message`, a turn cut off at the limit.

    Counts the cut-offs in a row as the session does
    (`CodingSession._continue_after_output_limit`): a turn that acts starts
    over, and a time cut is allowed more nudges than an output-limit one.
    """
    global _CUTS_IN_A_ROW
    if getattr(message, "stop_reason", None) != "length" or getattr(message, "tool_calls", None):
        _CUTS_IN_A_ROW = 0
        return False
    _CUTS_IN_A_ROW += 1
    cuts = {getattr(d, "type", None) for d in getattr(message, "diagnostics", None) or ()}
    in_a_row = (
        MAX_TIME_CUT_CONTINUATIONS
        if REASONING_TIME_CUT in cuts and REASONING_LOOP_CUT not in cuts
        else MAX_OUTPUT_LIMIT_CONTINUATIONS
    )
    return in_a_row >= _CUTS_IN_A_ROW


def _note_stop_offer(results: Any) -> None:
    """Remember whether the last pursuit tool result of a turn offered a stop."""
    global _STOP_OFFERED
    for result in reversed(list(results or ())):
        if str(getattr(result, "tool_name", "")).startswith("pursuit_"):
            text = "".join(
                str(getattr(part, "text", "") or "") for part in getattr(result, "content", ())
            )
            _STOP_OFFERED = STOP_OPTION in text or SEALED_STOP in text
            return


def make_stop_gate(tau: ExtensionAPI) -> Any:
    """Build the driver's `turn_end` gate: no stop while the pursuit is unfinished.

    Run R02's driver ended a `tau -p` run with "complete" while the root was
    stalled, and nothing objected: the Stop hooks do not run in print mode. A
    turn that ends with no tool call is the run's last unless something is
    queued, so this queues a follow-up naming what is not done, as the
    session's output-limit nudge does; the loop sends it in print mode too.
    At most `MAX_STOP_GATE_FOLLOWUPS` a run, then the stop is let through.

    Run R44: an escalation offered T0002's driver a stop, the driver took it,
    and this refused it. A stop the last pursuit tool result offered goes through.

    Run R127 (lfm24, cobs): after founding, three driver turns in a row
    reasoned out COBS to the output limit; tau nudged the first two and let
    the third end the run at 12 of 30 min. A cut-off tau still nudges is left
    to it; the one past its nudges is a stop like any other. Replayed with
    its 48k tokens of cut reasoning, that turn's follow-up drew a pursuit
    call in 7 of 7 samples.
    """

    async def gate(event: Any, context: ExtensionContext) -> None:
        global _STOP_GATE_SENT, _FOUND_AWAITS_USER, _STOP_OFFERED
        message = getattr(event, "message", None)
        if getattr(message, "tool_calls", None):
            _note_stop_offer(getattr(event, "tool_results", None))
        if (
            getattr(message, "role", None) != "assistant"
            or _tau_nudges_cut(message)
            or getattr(message, "tool_calls", None)
            or getattr(message, "stop_reason", None) in ("error", "aborted")
            or _STOP_GATE_SENT >= MAX_STOP_GATE_FOLLOWUPS
            or _STOP_OFFERED
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
        sealed = _sealed_note(nodes)
        if sealed:
            # q35 10-11: this said to add the missing work with pursuit_plan at
            # 11:56 and 12:18, under a T0002 that T0011's close had sealed at 11:23.
            _STOP_OFFERED = True
            tau.send_user_message(
                "[beagle] The pursuit is not done, and part of it cannot be done without "
                "the owner. Not done, and nothing took their work on:\n"
                + "\n".join(left)
                + f"\n\n{sealed}\n\nCall pursuit_step with no arguments only for work "
                "that is not under a sealed task and does not wait on one; if there is "
                "none, stop and ask the user."
            )
            return
        # Run R37: both follow-ups said to call pursuit_step, which the step cap
        # refused for T0004; a task at the cap gets its escalation's options.
        root = goal.parent.parent
        open_ids = [
            str(n.get("id"))
            for n in nodes
            if not n.get("container") and n.get("status") not in ("done", "abandoned")
        ]
        escalated = await asyncio.to_thread(_escalated_calls, open_ids, root)
        tau.send_user_message(
            "[beagle] The pursuit is not done, so this is not the place to stop. Not "
            "done, and nothing took their work on:\n"
            + "\n".join(left)
            + (f"\n\nAt the step cap:{escalated}" if escalated else "")
            + "\n\nCall "
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
true`, then end the turn exactly as the driver says for a dispatched worker, \
with `pursuit_wakeup` as its wakeup. The worker's completion arrives as a \
`<task-notification>` message that starts your next turn, an errored run's \
too: release its wait as the driver says, read the full report with \
`get_subagent_result` if the notification is truncated, and run the close. \
Claude Code's `SendMessage` to a running worker is `steer_subagent`; \
`get_subagent_result` with `wait: true` blocks on one. Parallel independent \
tasks may each get a background agent.
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
returns the worker's report within the same turn, so declare no wait for \
it; run the close straight after.
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
    "tests/data.json is removed). That test reads only the data file, opened beside "
    "it: `Path(__file__).with_name('data.json')`, not `open('data.json')`, which "
    "looks in the working directory."
)

#: Said instead of TESTS_ONLY_PROOF_NOTE when the scope holds no data file. Run
#: R12: that note pointed T0008 at a tests/ data file, another task's locked file.
TESTS_ONLY_MUTATE_NOTE = (
    "This scope holds only tests, so mutate the module the test imports: a WITNESS "
    "in that module, a NEEDLE there that the test must catch."
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


def _goal_text(goal_file: Path) -> str | None:
    """The goal's statement and criteria from `pursuit.toml`, or None if unreadable.

    Read straight from the goal file rather than shelling out to `beagle`, so
    loading never depends on `beagle` being on PATH or paying a subprocess at
    setup. The counts and ready set live behind `/pursuit-view` and
    `beagle pursuit next`; this is the part the driver must not lose.
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
    lines = [f"This project is a **pursuit**: {statement.strip()}"]
    if isinstance(criteria, list) and criteria:
        lines += ["", "Acceptance criteria (the user's; do not edit them to fit the work):"]
        lines += [f"  - {str(c).strip()}" for c in criteria if str(c).strip()]
    return "\n".join(lines)


def _worker_section(goal_file: Path) -> str | None:
    """A worker's orientation: the goal and criteria, then how to take on its task.

    A worker's session starts after founding and ends with its task, so the
    goal can sit in its system prompt: it never changes there.
    """
    goal = _goal_text(goal_file)
    if goal is None:
        return None
    return "\n".join(
        [
            goal,
            "",
            "You are a sub-agent doing one task of it; your brief says which.",
            "",
            PIECE_BY_PIECE_NOTE,
            GIT_IDENTITY_NOTE,
        ]
    )


#: How the driver works a founded pursuit. In the system prompt from load,
#: whether or not the pursuit is founded yet, so founding changes no prefix.
DRIVER_PROCEDURE = [
    "How to work a founded pursuit — this session steers, sub-agents do the work:",
    "1. `pursuit_step` with no arguments shows the next ready task.",
    "2. `pursuit_step` again with that task, its `criteria`, a `done_when` (one "
    "command, no shell operators, that exits 0 only when the task is done, such as "
    "`python3 -m pytest -q tests/test_x.py`), and its `scope`: a sub-agent does the "
    "work, the check runs, and the task closes when it passes.",
    "3. Repeat until nothing is ready. A task too big for one sub-agent: split it "
    "into steps with `pursuit_plan` first.",
    "Do not edit project files in this session; put what you want changed in the step's `notes`.",
    DRIVER_STEERS_NOTE,
    GIT_IDENTITY_NOTE,
    "",
    # No slash commands here: run 11c's driver read `/pursuit-run` in this
    # line as something to run, and ran it through bash.
    "For the rarer moves — spawning another route, binding a container's check, "
    "gates — call the `pursuit_driver` tool.",
]


def _founded_section() -> str:
    """The driver's orientation in a project founded before load."""
    return "\n".join(
        [
            "This project is a beagle pursuit. Its goal, criteria and tasks come from "
            "beagle in this conversation: at the start of each session and after each "
            "compaction. Its goal file (`pursuit.toml` in `.beagle`) is the user's; never edit it.",
            "",
            *DRIVER_PROCEDURE,
        ]
    )


def _unfounded_section(root: Path) -> str | None:
    """Orientation for a project with no pursuit at load, or None with no driver.

    Without it a model asked to set beagle up gets no frame at all until the
    goal file exists — and the setup skill, written for Claude Code, has it
    hunt for a CLI shim and look for a `/pursuit` it cannot type. It also
    says how to work a founded pursuit: founding mid-session leaves it in
    place, and it stays true.
    """
    if _driver_file(PURSUIT_COMMAND) is None:
        return None
    lines = ["Until this project is a beagle pursuit (no `pursuit.toml` in `.beagle` yet):"]
    if (root / BIN_REL).exists():
        lines.append(
            f"- `beagle` on PATH is already this checkout's CLI ({root / BIN_REL}); skip "
            "the setup skill's step that links it. Never link or run a `beagle` from "
            "`~/.claude/plugins/cache/...`: that is another release, with other commands."
        )
    lines += [
        "- Found it first. Asked to set beagle up and build something, call "
        "`pursuit_found` as your first move, before you read any reference or design "
        "anything: `pursuit_step` sub-agents read the references as each task needs "
        "them; the design is part of the implementation, not a milestone of its own. "
        "Your part is to steer, a few "
        "steps at a time.",
        "- Pass `pursuit_found` the user's goal, their acceptance criteria and the "
        "milestones you can already name. The goal and the criteria are the user's: use "
        "their words. If they gave none, ask, unless they told you to decide yourself "
        "('use your judgement', 'without further discussion'). Then draft the criteria "
        "from their request and set `user_delegated`.",
        "- It runs `git init` if the project is not a repository yet.",
        "- A reference the work needs (a URL, a paper) goes in a step's notes, or is "
        "saved inside the project; a sub-agent cannot see your context.",
        "- `beagle init` places templates; read one when you need it, not all of them.",
        "",
        "Once `pursuit_found` has founded it, its result says where the pursuit stands.",
        "",
        *DRIVER_PROCEDURE,
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
    global _SEEN_CWD, _PLUGIN_ROOT, _LAYOUT, _DRIVERS_DIR, _ENDED_RUN_NOTE, _LOOP_REPORT
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
                    on_founded=_note_founded, interactive=lambda: tau.context.has_ui
                ),
                prompt_snippet="Found a pursuit: goal, criteria, milestones.",
                prompt_guidelines=(
                    "The pursuit's goal and criteria are the user's: use their words, and set "
                    "user_confirmed only when they gave or approved them. When they told you "
                    "to decide the details yourself, draft the criteria from their request "
                    "and set user_delegated instead of asking. Then say what must pass and "
                    "leave exact values, sizes, bounds and worked examples to the sources the "
                    "workers read: a value written from memory can contradict them.",
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
    if _is_worker():
        # q35 R59 W10: before the bash hooks, so a worker's `git commit` gets this
        # refusal, not commit-claims advice naming verbs a worker is refused.
        tau.on("tool_call", make_worker_pursuit_guard())
    tau.on("tool_call", make_bash_hooks())
    if _is_worker():
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
        tau.on("agent_start", make_state_at_session_start(tau))
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
    if goal is not None and _is_worker():
        section = _worker_section(goal)
        if section:
            tau.add_prompt_section("Beagle pursuit", section)
    elif goal is not None:
        # Before loop-report, so it does not tell this session to stand
        # down for a driver that has ended.
        _ENDED_RUN_NOTE = _retire_gone_driver(goal.parent.parent)
        if _ENDED_RUN_NOTE is not None:
            tau.on("session_start", _notify_retired_once())
        # loop-report is the SessionStart hook: what a run left in flight, and
        # the driver's core while one is. It rides with each session's first
        # state note.
        _LOOP_REPORT = _session_start_report("loop-report", goal.parent.parent)
        tau.add_prompt_section("Beagle", _founded_section())
    elif _PLUGIN_ROOT is not None and not _is_worker():
        section = _unfounded_section(_PLUGIN_ROOT)
        if section:
            tau.add_prompt_section("Beagle", section)
