---
title: "Beagle Plugin Integration with Tau"
---

This note is a tutorial **and** a reference for running the `beagle` Claude Code
marketplace plugin inside Tau using the `tau.register_skill_dir(...)` extension
API. Read the core design note first:
[`extension-skill-dir-registration.md`](./architecture/extension-skill-dir-registration.md),
and the user-facing API doc:
`website/content/guides/extensions.md` → "Skill directories".

## TL;DR

`beagle` ships ~28 Agent Skills in the exact directory layout Tau's skill loader
already understands (`<plugin>/skills/<skill>/SKILL.md`). One extension that
calls `tau.register_skill_dir(...)` per plugin makes every skill available in Tau
with no copying or symlinking, and no edits to the plugin. Scripts inside a few
skills reference `${CLAUDE_PLUGIN_ROOT}`; set that one env var and they resolve
too. Slash commands, the Claude `hooks` block, sub-agents, and MCP are **not**
covered by this seam — see "Out of scope".

## What beagle is

Beagle is a Claude Code *marketplace* repo (`choongng/beagle`), not a single
plugin. `.claude-plugin/marketplace.json` lists three plugins:

| Plugin             | Skills | Has scripts via `${CLAUDE_PLUGIN_ROOT}` | Needs sub-agents/MCP |
|--------------------|:------:|:---------------------------------------:|:--------------------:|
| `beagle-dev`       |  15    | yes (context-audit, tilth-usage, …)     | no                   |
| `beagle-reference` |  2     | no                                      | no                   |
| `beagle-campaign`  |  11    | yes                                     | **yes** (`tilth`, workers/verifiers) |

Every skill is a directory containing `SKILL.md` (the Agent Skills spec), which
is exactly what Tau scans for. Beagle also ships things Tau has no host feature
for:

- `plugins/*/agents/*.md` — portable sub-agent definitions (`scout`,
  `step-executor`, `campaign-*`) with `mcp__tilth__*` tool grants.
- `plugins/beagle-campaign/commands/*.md` — Claude slash commands
  (`/campaign-run`, `/pursuit`, `/pursuit-run`, …).
- `.claude/settings.json` — Claude `hooks` (`Stop`, `PreToolUse`, `SessionStart`).
- A `beagle`/`tilth` CLI, put on `PATH` by the repo's `setup.sh`.

The skill-directory seam covers the **skills** half cleanly. Everything else is
either a separate translation layer (hooks, commands) or genuinely unsupported
(sub-agents, MCP). Be honest with yourself about which half you are installing.

## The seam you are using

`tau.register_skill_dir(path)` adds a directory of skills discovered directly
from disk. Its contract (recap of the design note):

- `path` must be a **skills directory**: its subdirectories each hold `SKILL.md`.
- Contributed skills load at the **lowest precedence** — a skill in `~/.tau/skills/`
  or the project's `.tau/skills/` always wins over a same-named beagle skill.
- The directory must exist when `setup()` runs; a missing/non-directory path is a
  warning diagnostic and is skipped.
- Contributions are de-duplicated by resolved path and **source-owned**: failed
  setup, `/reload`, and runtime retirement drop them.
- Skills surface in the `<available_skills>` system-prompt index and `/skill:<name>`
  on the next load or `/reload`.

## Tutorial: beagle-dev + beagle-reference

This gets the two plugins that Tau can actually run fully working. `beagle-campaign`
is deliberately excluded (it needs a sub-agent/Task tool and an MCP client that Tau
does not have — see "Out of scope").

### 1. Clone beagle and install its CLI

```bash
git clone git@github.com:choongng/beagle ~/beagle
bash ~/beagle/setup.sh          # links `beagle` + `tilth` shims onto PATH
command -v beagle tilth         # sanity check
```

`setup.sh` only puts the CLI on `PATH`; the skills themselves need no install —
Tau reads them straight from the checkout.

### 2. Write the Tau extension

Create `~/.tau/extensions/beagle.py`:

```python
"""Load Beagle's engineering-practice skills into Tau (no campaign machinery)."""

import os
from pathlib import Path

from tau_coding.extensions import ExtensionAPI

BEAGLE = Path.home() / "beagle"
SCRIPT_PLUGIN = "beagle-dev"  # plugin whose skills reference ${CLAUDE_PLUGIN_ROOT}
LOAD = ("beagle-dev", "beagle-reference")


def setup(tau: ExtensionAPI) -> None:
    for plugin in LOAD:
        skills = BEAGLE / "plugins" / plugin / "skills"
        if skills.is_dir():
            tau.register_skill_dir(skills)

    # Several beagle-dev skills run helper scripts with an absolute path built
    # from ${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/... . The bash tool spawns
    # subprocesses that inherit this process env, so exporting it here makes
    # those script paths resolve for the loaded plugin.
    root = BEAGLE / "plugins" / SCRIPT_PLUGIN
    os.environ.setdefault("CLAUDE_PLUGIN_ROOT", str(root))
```

Load it one-off during development with `tau -e ~/.tau/extensions/beagle.py`, or
leave it in `~/.tau/extensions/` to load by default.

### 3. (Alternative) set the env var from config instead of code

If you prefer not to mutate the process env from the extension, set the shell
prefix that is prepended to every bash command via `~/.tau/settings.json`:

```json
{
  "shellCommandPrefix": "export CLAUDE_PLUGIN_ROOT=\"$HOME/beagle/plugins/beagle-dev\";"
}
```

Use **one** of the two approaches, not both. The config route is global to all
Tau sessions; the `os.environ` route is scoped to whichever extensions are loaded.

### 4. Verify

```python
# from an interactive tau session
# - /skill:<TAB> autocompletes beagle-dev skills (context-audit, tilth-usage, …)
# - the system prompt <available_skills> block lists them
```

Programmatic check (matches the tests in this repo):

```bash
cd ~/tau          # a Tau checkout with the extension feature
uv run python - <<'PY'
from pathlib import Path
from tau_coding import CodingSession, CodingSessionConfig  # + provider/storage wiring
# See tests/test_extensions.py::test_session_loads_skills_from_extension_skill_dir
# for a complete runnable config with FakeProvider.
PY
```

Invoke a skill with `/skill:context-audit` (or let the model reach it via the
index). A script-backed skill like `tilth-usage` runs
`${CLAUDE_PLUGIN_ROOT}/skills/tilth-usage/...` — with step 2/3 in place it resolves.

## The `${CLAUDE_PLUGIN_ROOT}` nuance (multi-plugin)

Claude Code sets `CLAUDE_PLUGIN_ROOT` **per plugin** at skill-invocation time.
Tau has no such per-skill env, and `CLAUDE_PLUGIN_ROOT` is a single shell
variable. Beagle skills only ever reference their **own** plugin's tree as
`${CLAUDE_PLUGIN_ROOT}/skills/<their-own-name>/…`, so:

- Loading `beagle-dev` (+ script-free `beagle-reference`) with
  `CLAUDE_PLUGIN_ROOT=~/beagle/plugins/beagle-dev` is correct: every script path
  in a beagle-dev skill resolves, and beagle-reference skills use no scripts.
- Loading **two script-bearing plugins together with one env var is not**
  correct — one of them would resolve scripts against the wrong root. Options:
  1. Load one script-bearing plugin at a time (recommended).
  2. Build a merged `skills/` view (symlink each skill dir under one root) and
     point `CLAUDE_PLUGIN_ROOT` at that root — this is exactly what the pre-seam
     symlink sweep did, at the cost of the seam's "no copying" property.

For the skills-only tutorial above, option 1 keeps things simple. The pursuit
example extension (next section) needs campaign skills beside beagle-dev ones,
so it takes option 2.

## Pursuit mode: `examples/extensions/beagle.py`

The example extension goes past skills to run beagle's **pursuit** mode (one
goal, a task tree grown by doing the work, a `done_when` bound before each task)
in Tau. Symlink it into `~/.tau/extensions/` so dispatched workers load it too.

What it adds, and how each piece maps to what Claude Code provides:

| Claude Code | Tau stand-in in the example | Notes |
|---|---|---|
| One `${CLAUDE_PLUGIN_ROOT}` per plugin | One merged root at `$TAU_HOME/beagle-plugin/` (`skills/`, `commands/`, `agents/`, `bin/` as symlinks) | Plugins are read from beagle's `.claude-plugin/marketplace.json` (else a scan of `plugins/*/.claude-plugin/plugin.json`); every skill of every plugin is linked, the first in manifest order winning a clash. Only stale *symlinks* are pruned. `BEAGLE_ROOT` overrides `~/beagle`. |
| `/pursuit`, `/pursuit-run` slash commands | `tau.register_command` injecting the command text as a turn, in the same `<skill>` block `/skill:<name>` sends | `${CLAUDE_PLUGIN_ROOT}` is spelled out; the user's input follows the block; `/pursuit-run`'s body opens with a short host mapping. |
| (the model reaching a slash command) | `pursuit_driver` tool (`command`: `pursuit` / `pursuit-run`, `args`) | Returns the same driver text as the command, in-turn, so a user asking in prose gets the driver rather than a guessed shell command. Not registered in workers. |
| Task tool + `beagle-dev:*` agents, `run_in_background` | [tau-subagents](https://github.com/rian-dolphin/tau-subagents)' `agent` tool, with beagle's agents written as agent types `~/.tau/agents/beagle-dev:<agent>.md` | Needs tau-subagents installed. Completion arrives as a `<task-notification>` follow-up that starts the next turn; the driver uses the `--awaiting` tick as in Claude Code. |
| `SendMessage` to a running agent / `TaskOutput` | tau-subagents' `steer_subagent` / `get_subagent_result` (`wait: true` blocks) | |
| (fallback without tau-subagents) | `pursuit_dispatch`: a nested `tau -p --append-system-prompt step-executor.md` | Synchronous; its report returns in the same turn, so no `--awaiting` tick. |
| `ScheduleWakeup` | `pursuit_wakeup` (arm / replace / `stop`) | In-process timer; interactive TUI only (refused in print mode, which the driver treats as a stopping condition). Firing re-expands `/pursuit-run`. |
| `CLAUDE_CODE_SESSION_ID` / `CLAUDE_PID` | Tau session id exported at `session_start`; `CLAUDE_PID` removed; each session's pid recorded under `$TAU_HOME/state/beagle-drivers/` | beagle only trusts a pid named claude/node, so without one it judges liveness by the run's own promises. The bridge judges it instead: see *A driver that has ended* below. |
| `Stop` hooks `loop-guard`, `close-out`, `cadence` | `agent_settled` → `beagle hook NAME` | `loop-guard` in any pursuit; the others when installed in the project's `.claude/settings.json`, under the entry's timeout. Skipped for aborted/errored runs, runs cut off at the output limit (`length`), and print mode. Objections from one settle join into one more turn; the next settle passes `stop_hook_active` to all of them. |
| `PreToolUse` hooks `commit-claims`, `commit-trailer` | bash `tool_call` → `beagle hook NAME` | Only commands containing `commit`; `commit-claims` in a pursuit, `commit-trailer` when installed. |
| `SessionStart` hooks `loop-report`, `cadence-report` | Prompt sections at load ("Beagle pursuit", "Beagle cadences"; "Beagle" in a project with no `.beagle/pursuit.toml`) | `cadence-report` when installed. Extensions load before the session binds, so this (and goal discovery) uses the process cwd. |
| `SessionStart` `tilth-load`, `PreToolUse` `transcript-guard` | Not bridged | One note at session start if installed: tilth-load names Claude Code's ToolSearch, and transcript-guard needs a transcript path Tau does not give extensions. |
| (host identity) | `BEAGLE_HOST=tau` in every subprocess's env | For beagle to tell Tau from Claude Code, whose `CLAUDE_*` variables the bridge borrows. beagle 0.36 does not read it yet. |
| (none: one agent per tree) | Scope guard on the driver's `edit`/`write`/writing `bash` | While the recorded driver session waits on a worker (`loop tick --awaiting`, inside its lease), writes into an open task's `scope` are refused. Subagent sessions pass. `stop_subagent` during such a wait gets a reminder to clear it, since a cancelled run sends no notification. |

### Finding the loop from a cold start

A model asked to "set up beagle and pursue X" in a fresh project has three
ways to go wrong, all seen in one small-model trace (2026-10-01): it re-links
a `beagle` CLI that was already on `PATH` to a path that does not exist, it
types `/pursuit` into bash, and it reads every template `beagle init` placed.
The bridge closes each:

- **`beagle` on PATH.** The checkout's `bin/beagle` shim is linked into the
  merged root and `$TAU_HOME/beagle-plugin/bin` is put first on `PATH`, so the
  CLI always matches the skills loaded beside it and needs no setup step.
  A checkout without the shim leaves `PATH` alone.
- **`pursuit_driver`.** The tool hands the model `/pursuit` or `/pursuit-run`
  without the user typing it. Its guidelines say the goal and criteria are the
  user's and are read back before `.beagle/pursuit.toml` is written.
- **The "Beagle" prompt section.** In an unfounded project it says the CLI is
  already on `PATH` (never link one from `~/.claude/plugins/cache`), that a
  pursuit is founded through `pursuit_driver`, and to read a template only
  when it is needed.

A runaway turn that hits the output limit stops with `length`; the Stop hooks
skip it, since a close-out objection would only push an overfull context
further. Cap a small model's response in `~/.tau/catalog.toml`
(`[providers.model_metadata."<model>"] max_tokens = …`) so one turn cannot
fill its window.

Hooks are invoked as bare `beagle hook NAME` with the project root as cwd —
beagle's fast path ignores `--root` — and a JSON payload on stdin. Every bridge
fails open. Workers get `BEAGLE_TAU_WORKER=1`: they keep the parent's session
id and register no wakeup, `/pursuit-run` or loop-guard.

### Known gaps versus Claude Code

Background sub-agents come from the separate
[tau-subagents](https://github.com/rian-dolphin/tau-subagents) extension, the
project's reference sub-agent extension (see
`architecture/phase-21-extensions.md`), not from Tau core or this example:

```bash
git clone https://github.com/rian-dolphin/tau-subagents ~/tau-subagents
ln -s ~/tau-subagents ~/.tau/extensions/tau-subagents
```

On every load the beagle extension translates each `beagle-dev` agent
(`step-executor`, `scout`) into `~/.tau/agents/beagle-dev:<agent>.md`, the
location tau-subagents reads (`BEAGLE_TAU_AGENTS_DIR` overrides it). Claude
tool grants map onto Tau's (`Read`→`read`, `Edit`→`edit`, `Write`→`write`,
`Bash`/`Grep`/`Glob`→`bash`); MCP grants and the Claude `model:` alias are
dropped, so the sub-agent inherits the session model. Only files carrying
`generated_by: beagle-tau-extension` are rewritten or pruned; a hand-written
type of the same name wins. `/pursuit-run`'s host note tells the driver to
dispatch through `agent` with `run_in_background: true` when that tool exists,
and to fall back to `pursuit_dispatch` otherwise.

Sub-agents run in-process and load extensions too, so this extension runs
inside each one. That is safe: a child never emits `session_start` (only hosts
call `emit_pending_session_start`), so it never re-exports
`CLAUDE_CODE_SESSION_ID`, and it has no UI, so `loop-guard` and
`pursuit_wakeup` stay inert in it. `commit-claims` and the ground-truth guard
stay live, which is the point.

Remaining gaps versus Claude Code:

- **Print mode cannot wait.** A background worker still running when a
  `tau -p` turn ends is lost with the process, like a wakeup. Use foreground
  `agent` calls there; `/pursuit-run` itself stops at the refused wakeup.
- **No MCP.** `mcp__tilth__*` grants do nothing; tilth is CLI-only.
- **A run does not outlive its driver session.** Workers and the wakeup die
  with the session (see below), so the run is stopped at the next session
  start and `/pursuit-run` starts a new one. Wakeups are not persisted.
- **Two installed hooks are not bridged.** `tilth-load` and
  `transcript-guard` (see the table). `beagle hooks install` is how the others
  are switched on under Tau too.
- **A worker cancelled from the UI leaves its wait standing** until the
  lease runs out: tau-subagents sends no notification for a cancelled run.
- **Campaign agents are not translated.** Only `beagle-dev` agents become
  types; campaign mode is being retired.

tau-subagents 0.2.0's own test suite shows drift against current Tau (its fake
providers lack the `session_id` keyword, its fake TUI session lacks newer
attributes, and project-trust gating hides untrusted project skills from its
skill-index tests); a live background and foreground run against this checkout
works.

### A driver that has ended

Workers do not outlive the Tau session that spawned them: tau-subagents
cancels them at every `session_shutdown` (quit, `/new`, `/resume`, a branch,
`/reload`), and a crash or a closed terminal takes them down with the
process. The wakeup goes the same way. So once its driver session has ended,
a run has nothing left that will come back for it. beagle cannot tell that
under Tau (it has no pid it trusts), and would tell a new session to stand
down, and a resumed one that its dead worker still holds the task, until the
wait's lease ran out.

The bridge closes that gap itself:

- Every non-worker session writes `$TAU_HOME/state/beagle-drivers/<session
  id>.json` with its pid and the pid's start time, and marks it `ended` at
  `session_shutdown`.
- At load, and at every `session_start`, a run whose `driver_session` has
  such a record that is ended, or whose process is gone, is stopped with
  `beagle loop stop --reason` naming the session and what it was awaiting.
  Load does this before `loop-report`, so the report does not say to stand
  down. A session with no record (a Claude Code session, say) is left to
  beagle.
- The user gets a warning, and the next `/pursuit-run` turn starts with a
  note: the run was stopped, and a task it left open may hold a cancelled
  worker's partial work — uncommitted changes in its scope, a `tau-agent-*`
  branch, and its transcript under `~/.tau/subagents/*/<session>/tasks/` —
  to read before redoing the task. The driver then treats that task as one
  a previous session left open: finish it, or close it abandoned.

Some work is lost this way: whatever the worker had not written to disk. That
is the trade for workers that never outlive the session driving them.

### Testing it

`tests/test_beagle_example_extension.py` loads the real extension through
`ExtensionRuntime` against a fake beagle checkout and a fake `beagle` script
that logs each hook call. For a live check, in a pursuit project:

```bash
echo '{"hook_event_name":"SessionStart"}' | beagle hook loop-report
tau          # then /pursuit-view, /pursuit-run
```

## Hooks mapping

The example extension bridges beagle's hooks itself (see the table under the
pursuit section): Tau never reads `.claude/settings.json`, but the extension
reads which hooks `beagle hooks install` wrote there and runs them on Tau's
seams — Stop on `agent_settled`, SessionStart at load, Bash PreToolUse on
`tool_call`. It is a translation layer, not lossless loading: a Tau
`agent_settled` stands in for Claude's `Stop`, and the payloads carry only the
fields the hooks read.

## Out of scope (and why)

- **Slash commands** (`commands/*.md`, e.g. `/campaign-run`). Tau has no Claude
  command loader. Each must be registered by hand with
  `tau.register_command(name, handler)`, as the pursuit example does for
  `/pursuit` and `/pursuit-run`. Not automatic.
- **Sub-agents + MCP** (`agents/*.md` with `mcp__tilth__*`; campaign
  worker/verifier dispatch). Tau core has **no** `Task`/sub-agent tool and
  **no** MCP client. The pursuit example approximates one blocking
  step-executor with a nested `tau -p`; campaign mode's worker/verifier pairs
  remain out of reach, and `beagle doctor` will keep flagging `tilth`.

## Design reference (as it applies to beagle)

- **Precedence** — beagle skills are lowest; drop your own override in
  `~/.tau/skills/<name>/SKILL.md` to shadow one without touching the plugin.
- **Ownership** — registering the same dir twice (or from two extensions) collapses
  to one entry; if the extension's `setup()` raises, its skill dirs roll back.
- **Ordering** — project extensions load before resources, so a *project-local*
  beagle extension's `register_skill_dir` is seen in the same snapshot;
  non-project extensions load before the trust decision.
- **Lifecycle** — `/reload` re-runs `setup()` (re-registers), retirement clears.
  Resume/new/branch route through `CodingSession.load`, so contributed skills are
  present there too.
- **Diagnostics** — a missing beagle path (e.g. wrong `BEAGLE` root) shows up as an
  extension-load warning, not a crash.

## Gotchas

- `register_skill_dir` points at a **skills directory** (`…/<plugin>/skills`), not a
  single skill dir and not the plugin root. Pointing at the plugin root loads
  nothing (its children have no `SKILL.md`).
- Beagle skill **names** are unique within beagle, but could collide with your own
  skills or another plugin — precedence (above) decides the winner, and a diagnostic
  names the override.
- Set the CLI up (`setup.sh`) *before* relying on script-backed skills; the skill
  seam does not install `beagle`/`tilth`.
- The `os.environ.setdefault(...)` trick only works because the bash tool spawns
  subprocesses that inherit the process env; if that ever changes, use the
  `shellCommandPrefix` route instead.

## How it's tested

The seam itself is covered in this repo by:

- `tests/test_skills.py` — `extra_skill_dirs` load / precedence / override
  diagnostic / collapsing.
- `tests/test_extensions.py` — registration, missing-path diagnostic,
  de-duplication, failed-setup rollback, retire cleanup, and a `CodingSession`
  integration + reload test (`test_session_loads_skills_from_extension_skill_dir`,
  `test_session_reload_keeps_extension_skill_dir`).

Use `test_session_loads_skills_from_extension_skill_dir` as the template for a
deterministic fake-provider test of any real plugin integration you add.
