# ITC run harness

Lives outside this repo, at `~/tautest/itc-harness` (its own git repo), so
nothing in it reaches tau's tree or the model's `~/itc`.

## Launch a run

    ~/tautest/itc-harness/launch.sh [--dry-run] RNN mimo|qwen

- `mimo` → `mimo-v2.6-9b-q4`, `qwen` → `qwen3.5-9b-q4-mtp-thinking-coding`.
- Moves the current `~/itc` aside to `~/itc.<previous run id, lowercased>`
  (e.g. `~/itc.r01`), found as the newest `runs/R*/` with a `meta.json`. With
  no earlier run recorded it uses `~/itc.run11e` if that name is free, else
  `~/itc.run-prev-<timestamp>`. It refuses if the target exists, or if
  `runs/RNN/meta.json` already exists.
- Creates an empty `~/itc` and puts nothing in it. Run metadata goes to
  `runs/RNN/` in the harness instead.
- Runs `tau -p --provider bane --model <model> "<itc_prompt.txt, byte for byte>"`
  from `~/itc`, with git identity and `BEAGLE_TAU_DISPATCH_*` in the env.
  The command runs under `systemd-run --user --scope --unit itc-RNN -p MemoryMax=8G -p MemorySwapMax=0`
  and `timeout -k 30 3600`.
- Runs in the foreground. Background it yourself, and stop it early with
  `systemctl --user stop itc-RNN.scope`.
- `--dry-run` prints the planned move and the full command, and changes nothing.

Files in `runs/RNN/`:

- `meta.json`: model, start time (epoch), launch command, unit, tau git sha
  and dirty-file count, `beagle --version`, and the path `~/itc` was moved to.
  After exit it also holds `session`: the newest
  `~/.tau/sessions/home-itc-*/*.jsonl` modified since the start.
- `stdout.log`: tau's stdout and stderr.
- `exit.json`: `exit_code`, `end`, and `capped`, which is true on exit code
  124 or 137, the codes `timeout` uses.

## Grade the result

    python3 ~/tautest/itc-harness/grade.py --adapter runs/RNN/adapter.py [--json]

The run's code is not graded directly. Write a small per-run adapter that maps
the model's API onto `seed()`, `fork(s) -> (a, b)`, `event(s)`, `join(a, b)`,
`leq(a, b) -> bool` and `canon(s) -> (id, ev)`. `canon` returns the normalised
stamp as nested tuples: ids `0 | 1 | (l, r)`, events `n | (n, l, r)`. Set
`MISSING = {"op", ...}` for ops the run never implemented. The cases that need
those ops then fail instead of crashing the grader. Use
`adapters/reference.py` as a template.

The suite has 42 cases in these categories:

| category | what it covers |
|---|---|
| paper | Examples from the paper and blog |
| norm | Normalisation and fill |
| leq | `leq` |
| join | Join laws |
| trace-canon | 10 cases × 20 seeded random fork/event/join traces. After every op, `canon` is compared with `itc_ref.py`. |
| trace-causal | The same kind of traces. `leq` on every pair is checked against ground-truth causal history (sets of event ids). An implementation that grows events differently but validly still scores on these cases. |

How the grader contains the code it runs:

- It caps itself with `setrlimit`: 2 GiB address space and 300 s CPU.
- Each case has a 5 s `SIGALRM` timeout.
- An op that hangs once is not called again.
- Every exception counts as a failure, `SystemExit` included.
- The graded code's stdout is sent to stderr.

The grader exits 0 only if every case passes. `adapters/broken_join.py`, a
join that keeps only the left side's events, must score failing.
`itc_ref.py` is the reference implementation.

## Score the trace

    python3 ~/tautest/itc-harness/scorecard.py --session <session.jsonl> --repo ~/itc \
        [--exit-json runs/RNN/exit.json] [--json]

The scorecard reads the repo through `beagle pursuit status --json` and
`beagle pursuit tree --json` with cwd set to the repo, plus `git log` and
`git status`. It writes nothing.

| field | meaning |
|---|---|
| `model` | |
| `founded` | Whether `pursuit_found` succeeded |
| `found_attempts` | `pursuit_found` calls up to and including the first success |
| `tasks_done` | |
| `tasks_abandoned` | |
| `tasks_stalled` | Blocked tasks plus containers whose subtree is `stalled` |
| `witnessed` | `closed_proven/closed_on_command` |
| `commits` | Commits that touch anything outside `.beagle/` |
| `record_commits` | Commits that touch only `.beagle/` |
| `uncommitted_files` | Files outside `.beagle/` left uncommitted |
| `breaker_refusals` | Tool results counted by kind: `repeat` (*Not run: this \`X\` call ran…*), `tool_as_command`, `stop` (*Not run, and the run is stopped*), `guard` (*Tool call blocked:*) |
| `length_stops` | |
| `compactions` | |
| `ended` | One of `capped`, `breaker`, `error`, `finished`, decided in that order |
| `wall_minutes` | First to last session timestamp |
| `tool_calls` | Total and per tool |
| `pursuit_steps` | `pursuit_step` outcomes, classified from beagle's wording |
| `worker_timeouts` | |
| `turns` | |
| `stop_reasons` | |
| `last_error` | |
| `gate_debt` | |

## Session format notes

- One JSON object per line. Each line has `type`: `session_info` (has `cwd`),
  `model_change` (`model`, `provider`), `thinking_level_change`, `message`,
  `custom_message` or `compaction` (has `summary` and `tokens_before`).
- Line `timestamp` values are float epoch seconds. The `message.timestamp`
  values nested inside are epoch milliseconds.
- In a `message`, `message.role` is `user`, `assistant` or `toolResult`.
  - An assistant message's `content` holds `thinking`, `text` and `toolCall`
    blocks. A `toolCall` block has `name` and `arguments`. The message also
    has `stopReason` (`toolUse`, `stop`, `length`, `error` or `aborted`),
    `errorMessage`, `usage` and `timing`.
  - A tool result has `toolName`, `isError` and `content` (a list of
    `{type: text}` blocks).
- The text of a beagle `custom_message` is in the top-level `content` field,
  not under `message`. For example, the post-compaction state note begins
  "The conversation was just compacted".
- A breaker refusal still appears as a `toolCall` followed by a `toolResult`
  with `isError` true, so `tool_calls` counts it.
- When the breaker stops a run, an empty assistant message usually follows,
  with `stopReason: error` and "Provider stream ended without a terminal
  event". `ended` reports `breaker` for that case, not `error`.
