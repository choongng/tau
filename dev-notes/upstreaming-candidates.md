# Upstreaming candidates: tau and tau-subagents vs upstream

As of 2026-10-11. This lists what our `choong-dev` branches change against
upstream, grouped by area, with the commits behind each change, as a basis for
planning what to send upstream. Nothing has gone upstream yet; both branches
are pushed only to the private `urd` remote.

| Repo | Upstream | Fork point | Ahead |
|---|---|---|---|
| `~/tautest/tau` | huggingface/tau | `c41aacf7` (10-06, still upstream HEAD) | 1040 commits |
| `~/tau-subagents` | rian-dolphin/tau-subagents | `f2a8b4b` (09-15, still upstream HEAD) | 22 commits |

The tau commit count overstates the change. Most of those commits are
`.beagle/` pursuit state (log, tree, checks) and `dev-notes/`. The code change
is:

- `src/`: 30 files, +2852 / −326, across about 85 commits.
- `examples/` and `tests/`: +43.9k lines, almost all of it the beagle
  extension (`examples/extensions/beagle.py`) and its test file.

The commit lists come from `git log`; the descriptions come from commit
messages and diffs, not a line-by-line review.

## Upstream branches so far

Each is cut from `c41aacf7`. It holds only the feature's end state, with
comments rewritten so they don't cite our run IDs.

| Branch | Items | Commits | State (10-12) |
|---|---|---|---|
| `upstream/tui-stream-cpu` | §6 streaming CPU | 3 | On urd. |
| `upstream/accurate-failures` | §4 clearer argument errors and cancel between turns | `947c660f`, `eb5756af` | Local only: urd push blocked (no authorized SSH key in agent). Adds a user-cancel loop test; both loop tests fail on upstream. The breaker-dependent session test was dropped, and the tool tests were folded into `test_coding_tools.py`. |
| `upstream/thinking-level-warning` | §5 thinking-level warning | `638a7832` | Local only, as above. |
| `upstream/bash-timeout` | §3 default timeout and `TAU_BASH_TIMEOUT_SECONDS` (not `d434f101`) | `8f69a297` | Local only, as above. Also updates `reference/tools.md`, which still said "No default". |

All three new branches pass `pytest` (about 2065 passed, 3 skipped),
`ruff check`, `ruff format --check` and `mypy`.

## Cross-cutting notes for planning

These apply to most of the items below.

- **Send end states, not histories.** Several areas went through versions
  that were later reversed. Each upstream PR should be built from the current
  code, not by cherry-picking the commit chain:
  - Output-limit nudge: `c9a62a95` and `361c0536` turned thinking off for the
    nudge, `588ad070` warned when that was impossible, then `45968678` and
    `88f99810` (10-11) removed all of it. The nudge now keeps the session's
    thinking level.
  - TUI layout: about 25 commits on 10-07 and 10-08 adjust padding and
    columns, several undoing earlier ones (`cdc1c67e` "restore the left
    inset…").
- **Core changes inside beagle-labelled commits.** These commits are labelled
  "beagle" but change tau core:
  - `2f7f9f38` adds `report_at_max_turns` to the agent loop
    (`tau_agent/loop.py`) and the print-mode `--max-turns` flag (`cli.py`).
  - `e6e0b9a7` adds `WORKSPACE_CHANGING_TOOLS` to the repeat breaker.
  - `85b38a3e` makes the repeat breaker quote the earlier result.
  - `038d1493` adds the `TAU_BASH_TIMEOUT_SECONDS` override (`tools.py`).
- **A beagle tool name is hard-coded in core.**
  `src/tau_coding/session.py:228`:
  `WORKSPACE_CHANGING_TOOLS = frozenset({"pursuit_step", "write", "edit"})`.
  Before upstreaming, this needs to be generalized, for example as a
  tool-level flag or an extension API.
- **Internal references in comments.** The `src/` diff has 15 added lines, and
  the core tests 26, that cite our run IDs (R08, R36, "Run 11c"), beagle task
  IDs or `dev-notes/itc-runs/`. Upstream readers can't see those runs, so each
  comment needs to state the failure it guards against in its own words.
- **Evidence base.** Most of the guards in §4 were found in small-model local
  runs (gemma, mimo, qwen on llama.cpp). The changes are meant to hold across
  models (see `hardening-intent` in memory), but each PR should describe the
  failure in general terms and, where we have one, give a frontier-model case
  too.
- **Prefix-cache principle.** As of 10-11, nothing on choong-dev changes the
  system prompt or the thinking level mid-session. That is a useful framing
  for upstream: guards steer with messages or refusals, never by editing the
  prefix.
- **Dependencies between repos.** Some tau-subagents changes behave better on
  our tau (see the tau-subagents section). Upstreaming tau first is the
  simpler order.

## tau: core changes (`src/`)

### 1. Extension API (added for beagle)

| Change | Commits | Notes |
|---|---|---|
| `tau.register_skill_dir()`: an extension supplies a directory of skills | `e739546c` | Self-contained, with docs (`data/docs/extensions.md`) and tests. A good first PR. |
| `tau.add_compaction_instructions()`: an extension tells the compaction summarizer what to focus on | `b0cc38a4` | Small (+66). |
| `set_prompt_section()`: an extension changes its prompt section mid-session | `90fd84b6` | **Drop.** It has had no caller since `718f0051` (10-11), and it works against the prefix-cache principle. Could be removed from choong-dev as well. |

### 2. Compaction and context (`session.py`, `context_window.py`)

| Change | Commits |
|---|---|
| Automatic compaction waits for the start of the next turn | `8e110ec6` |
| Compaction can run between turns of a long run; `max_tokens` is passed through to the provider | `9fe56363` |
| Summaries stay current and quote an open question word for word | `b21c5032` |
| The recent context kept after compaction scales with the threshold | `8ae07850` |
| The kept tail is cut until the context is at most half the threshold | `6b60ab80` |
| The summary gets a bounded budget and is held to it | `4fe27c04` |

Notes:
- These build on each other and probably go up as one or two PRs.
- `9fe56363` combines two unrelated changes. The `max_tokens` pass-through
  could be its own PR.

### 3. Tool output and the bash tool (`tools.py`, `tool_buffers.py`)

| Change | Commits |
|---|---|
| Model-issued bash commands get a default timeout | `d87cda84` |
| `TAU_BASH_TIMEOUT_SECONDS` overrides that default for one session | `038d1493` (core part only) |
| The bash tool runs under `bash` instead of `/bin/sh` | `d434f101` |
| Oversized tool results are written to a buffer file beside the session file | `aa0987b9` |
| Long bash output goes through the same buffer | `acb61acf` |
| A cut-off read lists the file's def/class lines | `7b0656fb` |
| A cut-off read names the line range shown and the next offset; an explicit limit fills the character window | `779903b0` |
| A bash command that runs one of the session's own tools is refused | `f25597a3` |

Notes:
- `d434f101` changes user-visible behaviour (the shell) and has a docs change
  in `reference/configuration.md`. Upstream may want this to be configurable.

### 4. Guards against bad agent behaviour (`session.py`, `loop.py`, `tools.py`)

These were mostly found in the R-series small-model runs.

| Guard | Commits | Notes |
|---|---|---|
| **Repeat breaker.** An identical repeated call is refused, and so is one that keeps returning the same result; a run that keeps repeating is stopped. | `e277e065`, `0e67c983`, `90aaf2c5`, `bcabadad`, `a6693cc4`, plus the core parts of `e6e0b9a7` and `85b38a3e` | Generalize `WORKSPACE_CHANGING_TOOLS` first (see above). The refusal quotes the earlier result. |
| **Output limit.** A turn that hit the output limit before acting is continued with a nudge, bounded at 2 in a row and 6 per run. | `a3831c2b`; end state after `88f99810` | The nudge keeps the session's thinking level. Send only the end state (see above). |
| **Looping reasoning** is cut early and handled like an output-limit cut-off. | `c9a62a95` (detector), `45968678` | The detector's thresholds were tuned on gemma traces (R36) and tested against varied long reasoning. Upstream will want to know its false-positive rate. |
| **Chat-template tokens in arguments.** A tool call whose arguments carry template tokens is refused; a leaked template tail is cut when the call can run without it. | `8d71fb84`, `0b242e0d`, `7f582765` | The patterns are tied to specific chat templates. |
| **Tool calls written as text** get a bounded follow-up, including a call missing its opening tag. | `f0876d09`, `faf061f5` | |
| **Clearer argument errors.** Cut-off arguments are reported as cut off, not as `path must be a string`; a missing string argument is named. | `fd37b7c7`, `abc47437` | Low risk, and useful for any model. A good early PR. |
| **Cancel between turns** sends no further request and ends the run as aborted, with the stopping call's reason. | `cc8dfd5d` (`tau_agent/loop.py`) | Agent-loop change. Small. |
| **Turn budget.** `report_at_max_turns` warns the model 2 turns ahead, then makes one last request with no tools so the run ends with a report. Print mode gets `--max-turns`. | core part of `2f7f9f38` | Generic, though it currently sits in a beagle commit. |

### 5. Providers (`provider_config.py`, `openai_compatible.py`, `request_gate.py`, `prompt_cache.py`)

| Change | Commits |
|---|---|
| OpenAI-compatible providers can opt in to llama.cpp prompt caching (`cache_prompt`, `id_slot_count`) | `94d08ee6` |
| Prompt-cache misses are reported on providers that normally cache | `af8b5a98` |
| An opt-in per-provider concurrency limit (`max_concurrent_requests`) queues extra requests | `d4ae2395` |
| tau warns when a model offers thinking levels tau never sends | `66382dc1` |

Notes:
- All four are opt-in or diagnostic only, and each has docs in
  `guides/providers-and-models.md`. These are good standalone PRs.

### 6. TUI (`tui/app.py`, `tui/widgets.py`, `tui/config.py`)

| Change | Commits | Notes |
|---|---|---|
| Ctrl+B toggles the sidebar | `c38b8797`, `b1cda13d` | Conflicts with tmux's default prefix; the docs mention this. |
| Ctrl+J is the default newline key | `25a9c8eb` | Changes a default, so it needs upstream agreement. |
| PgUp/PgDn page the transcript while the prompt has focus | `0f712c4e`, `df158481` | |
| Down after an Up-recall returns to an empty prompt | `1693b3b8` | |
| Streaming CPU: streamed text is merged into at most about 10 appends a second; full GC runs when the agent settles; 80 transcript items stay mounted instead of 200 | `fd0bd79d`, `c98b5f6b`, `da73b977` | **In progress:** branch `upstream/tui-stream-cpu` (on urd, off `c41aacf7`, 10-11). Measured there with `stream_probe.py`: CPU 58–60% → 16%, p99 stall 107–161 ms → 8–9 ms. Write-up in `dev-notes/tui-stream-cpu/`. |
| Hidden thinking is a status line, not scrollback rows | `4fe85228`, `b217f3ef`, `0cc57a2d`, `34259e15` | |
| Borders and layout: solid borders, column alignment, padding, tool-row grouping | `16074431`, `2f7d0bb2`, `91a4862a`, about 25 commits on 10-07 and 10-08, `0d76b22d`, `1e571060`, `d9906d88` | Mostly a matter of taste. Squash into one end-state PR, if it goes up at all. |

### 7. Smaller changes

| Change | Commits |
|---|---|
| The PyPI update notice is skipped for direct-URL installs | `bb96d6df` |
| Persisted user messages record their delivery mode and source | `a5ede4c9` |
| Formatting and type fixes after the upstream merge | `aed36081`, `ac73e1c6` (not upstream material) |

## tau: the beagle extension (`examples/extensions/beagle.py`)

The extension ports the beagle Claude Code plugin onto tau's extension hooks.
At about 18k lines with its tests, it probably belongs with beagle, not in
tau's `examples/`. If so, the upstream work for tau is the extension APIs it
needs (§1), not the extension itself.

What it does:
- **Skills and commands.** It loads every beagle skill through a merged
  `CLAUDE_PLUGIN_ROOT`, adds `/pursuit` and the `pursuit_driver` tool, and
  puts the checkout's own `beagle` first on `PATH`.
- **Workers.** `pursuit_dispatch` runs a worker as a nested `tau -p`
  step-executor. It also writes beagle's agent definitions into
  `~/.tau/agents/`, so tau-subagents can run them as background workers.
- **Steering tools.** `pursuit_found`, `pursuit_plan` and `pursuit_step`
  guide a small model through a pursuit without the full driver text, which
  runs to tens of thousands of tokens.
- **Guards:**
  - `pursuit.toml` can't be edited after founding.
  - No history rewrites: `reset --hard`, `rebase`, force-push and similar.
  - The driver can't write into a busy worker's task scope.
  - The driver may edit only `.beagle/`.
- **Worker limits.** A turn cap, a 120 s bash timeout, a guard against workers
  that never write, and a fallback report. Thinking is off by default and has
  been passed on from the driver since R41.
- **Pursuit state as messages** (since `718f0051`, 10-11):
  - The driver's system prompt holds only the fixed procedure.
  - The goal, criteria and task tree arrive as messages: in the
    `pursuit_found` result, at the first run of each host session (with
    `beagle hook loop-report` output), and after each compaction.
  - Workers keep the goal in their system prompt.
- **Other.** It bridges beagle's hooks and stops runs whose driver session has
  ended.

Beagle-side fixes waiting to go upstream are tracked separately: `~/beagle`,
branch `mining-fixes-2026-10-10`.

## tau-subagents (22 commits, 34 files, +7486 / −175)

### Liveness and visibility

| Change | Commits |
|---|---|
| `stop_subagent` tool; the strip shows whether a running agent is alive | `267fd48` |
| Running agents report a phase, shown in results and the UI | `810715f` |
| `get_subagent_result` can list an agent's last tool calls | `2f20251` |
| Transcript entries are written when a tool starts, stamped with the event time | `4177572` |
| The parent is told when a background agent has gone quiet | `9d1e1d4` |

### Making sure results arrive

| Change | Commits |
|---|---|
| An agent that ends with an empty message is asked once for a report | `ae21b0e` |
| A stopped or cancelled run keeps its partial result | `c18e113` |
| A finished agent's notice reaches a busy parent at its next turn | `f4c4676` |
| A child at its turn limit is told how many turns it has left; the status is renamed to `turn_limit` | `fc51344`, `5a6856d` |

Note: the rename in `5a6856d` changes a status value that callers may match
on.

### Starting agents and long runs

| Change | Commits | Notes |
|---|---|---|
| Provider, model and credentials are checked before a spawn is reported | `5c18795` | |
| Subagents can compact, so long tasks outlive their context window | `25c24ed` | Works on upstream tau. Its between-turns test skips unless tau compacts between turns (our `9fe56363`). |
| Child sessions get the parent's runtime provider config | `0236dfe` | **Re-evaluate.** Its stated reason was to let tau build the thinking-off twin for output-limit nudges, which `88f99810` removed. Keep it only if something else needs the config in children, such as the thinking-level warning or `cache_prompt`. It also sets a private field (`session._runtime_provider_config`), which upstream would want as a public API. |

### Background jobs (new)

| Change | Commits |
|---|---|
| Design: a tee'd spawn and an on-disk registry | `e6a018c` |
| A job is recorded as files on disk, so it outlives the session that started it | `b06085f` |
| A job's log is its stdout; it is supervised until it writes `done.json` | `5410205` |
| A watcher on the job registry tells the parent when a job ends | `7d4ae32` |
| `--detach` returns once the job starts | `d6dd24a` |
| The model gets a `jobs` tool, and there is a `/jobs` command | `a9541c5` |
| Docs: which clock a deadline uses | `7f77d92` |

Note: this adds a `tau-job` console script (`pyproject.toml`). It is the
largest new feature here, so it is worth asking the upstream maintainer before
writing the PR.

### UI

| Change | Commits |
|---|---|
| The strip's cursor is drawn only while navigating | `6e5ff66` |
| Strip navigation starts on the row on screen | `fd0efdb` |

## Not covered here

- The `review-fixes`, `review-fixes-core` and `review-fixes-bridge` branches
  (worktrees in `~/wt/`) have no commits beyond choong-dev.
- `choong-dev-pre-rebase-2026-09-27` is a pre-rebase snapshot whose commits
  are on choong-dev under new hashes.
- Neither of the 10-11 changes (`88f99810`, `718f0051`) has been measured in a
  run yet.
