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
  (`/campaign-run`, `/pursue`, …).
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

`beagle-campaign` is script-bearing but out of scope regardless, so the common
case stays simple.

## Hooks mapping (optional Tier-2 shim, not required for skills)

Beagle's `.claude/settings.json` wires:

| Claude hook (`matcher`)          | Command                       | Closest Tau extension seam                     |
|----------------------------------|-------------------------------|-----------------------------------------------|
| `SessionStart` (`startup\|resume`) | `beagle hook cadence-report`  | `tau.on("session_start", …)` shell out        |
| `PreToolUse` (`Bash`)            | `beagle hook commit-trailer`  | `tau.on("tool_call", …)` filter `bash`         |
| `Stop`                           | `beagle hook close-out`/`cadence` | `tau.on("turn_end", …)` (approximate)      |

Sketch (add to the same extension if you want hook parity for the parts that map):

```python
import subprocess
from tau_coding.extensions import ToolCallHookResult  # for PreToolUse rewrites


def _run(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=False)


def setup(tau: ExtensionAPI) -> None:
    # ... register_skill_dir(...) from above ...

    tau.on("session_start", lambda e, c: _run("beagle hook cadence-report"))
    tau.on("turn_end", lambda e, c: (_run("beagle hook close-out"),
                                     _run("beagle hook cadence")))

    def _commit_trailer(event, context):
        if event.tool_name == "bash":
            _run("beagle hook commit-trailer")
        return None  # ToolCallHookResult: set block/arguments to interfere

    tau.on("tool_call", _commit_trailer)
```

Be clear-eyed: this is a **translation layer, not lossless loading**. Tau's
`turn_end` approximates Claude's `Stop` (which can force continuation); Tau's
`tool_call` hook can block/rewrite but the payloads differ. Hooks are independent
of the skill seam — install skills first, add hooks only if you miss them.

## Out of scope (and why)

- **Slash commands** (`commands/*.md`, e.g. `/campaign-run`). Tau has no Claude
  command loader. To expose them you would `tau.register_command(name, handler)`
  by hand and shell out to `beagle`, or read the `.md` as a prompt. Not automatic.
- **Sub-agents + MCP** (`agents/*.md` with `mcp__tilth__*`; campaign
  worker/verifier dispatch). Tau's `tau_agent`/`tau_coding` have **no** `Task`/
  sub-agent tool and **no** MCP client. The campaign half of beagle cannot run
  until those host features exist in Tau core; `beagle doctor` will keep flagging
  `tilth` until then. `register_skill_dir` does not and cannot shim this.

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
