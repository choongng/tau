# What fang does to make 9B models work, and what tau could take

T0018. Survey of `~/fang` (coach/player harness, 954 commits) for 9B tuning
that could fix the ITC failure modes. Read-only; nothing in fang was run.

## The framing first: fang never asks a 9B model to think alone

Fang's whole design is a split. A small, fast **player** executes. A large
**coach** (`qwen3.8-flash-next-iq4`, thinking at `medium`) sets direction,
checks, and decides when the work is done
(/home/choong/fang/doc/engineering-brief.md lines 13-35, 143-175). The 9B
model was only ever measured **in the player seat**, as
`qwen3.5-9b-q4-mtp-instruct-general`: the *instruct* variant, with thinking off
(/home/choong/fang/doc/scale-screen.md lines 26 and 53). I found no fang
result for a 9B model driving a task on its own.

Even with the coach, the 9B player did not hold up on multi-part work. On the
six-task bundle, `relay_9b_h10` passed 0 of 3 runs. In run 1 the player's
context overflowed (33,082 prompt tokens against 32,768). In runs 2 and 3 the
coach called the goal done with four tasks never started
(/home/choong/fang/doc/scale-screen.md line 82; commit `00840036`). Single
tasks passed. Most of fang's later work is about cost, not about 9B
competence. So fang has fewer 9B-specific techniques than "significant
tuning" suggests. About half of what follows is general small-model hygiene
that fang measured on its 1.2B, 4B and 9B players.

Fang's prompt-only fixes also failed to change behaviour. In round 2, the
coach was told to cross-check against an oracle and to order patches rather
than rewrites. Neither instruction showed up in the runs (both arms are
marked "not testing", /home/choong/fang/notes/bundle6-hypotheses-r2/results.md).
Tau found the same with 9B: only hard refusals change what the model does.
Every idea below is ranked with that in mind.

Ranked by expected value against the ITC failures.

### 1. Run the executing 9B with thinking off; put the thinking somewhere else

**What fang does.** The player seat is a non-thinking instruct model at
`reasoning_effort = "none"`
(/home/choong/fang/doc/engineering-brief.md line 901;
/home/choong/fang/coachplayer/default_config.toml line 46). The 9B runs used
the `-instruct-general` build, not a thinking build
(/home/choong/fang/doc/scale-screen.md line 53). Deciding what to do, which
is the reasoning-heavy part, belongs to the coach. Fang also found that
`reasoning_effort` `low`/`xhigh` inject text at the top of the system prompt
and break the prefix cache. Only `none` (an empty `<think></think>` at the
tail) is safe to switch per request
(/home/choong/fang/doc/engineering-brief.md lines 349-354, 925).

**Tau today.** Workers inherit the session's thinking level, with no per-role
override. The worker command line has `--provider`/`--model` and no
`--thinking` (examples/extensions/beagle.py, the worker `cmd` near line
1267). Tau has the primitives: `--thinking` in src/tau_coding/cli.py line
226 and `include_reasoning_effort_none` in src/tau_coding/provider_config.py
line 1788. Tau's ITC runs use `qwen3.5-9b-q4-mtp-thinking-coding`, which is
the variant that spirals. `DRIVER_STEERS_NOTE` records "30K characters of
reasoning, then nothing, in every ITC trial" (examples/extensions/beagle.py
line 4485).

**Where it lands.** In the worker spawn in examples/extensions/beagle.py, add
a `BEAGLE_TAU_DISPATCH_THINKING` (next to `BEAGLE_TAU_DISPATCH_MODEL`) that
passes `--thinking off`. Also send `reasoning_effort: "none"` for llama.cpp
through src/tau_coding/provider_config.py. Then run a trial with the instruct
build of the same 9B as worker.

**Value: high, cheap.** This goes straight at the top failure (output cap hit
with no tool call). The risk is that an ITC piece really does need reasoning
(idea 2 says where that reasoning should go). Try it as a one-variable arm.

### 2. A stronger model sets direction and judges done; the 9B executes

**What fang does.** This is the relay. The coach writes the direction in
prose, then calls an argument-free `player_handoff`. The player gets a
bounded window. The coach checks with a read-only `Check` tool and calls
`Complete` (/home/choong/fang/coachplayer/relay.py lines 1-120, 765-860). The
coach is barred from `Bash`/`Write`/`Edit` (`COACH_WITHHELD_TOOLS`, relay.py
line 748), so it cannot do the work itself. Its `Check` refuses commands that
write (`CHECK_WRITES`, relay.py line 1119).

**Tau today.** The pieces are there, pointed the other way. Tau's driver
already only steers (`DRIVER_STEERS_NOTE`, driver edit guard commit
`7053ea5`). `BEAGLE_TAU_DISPATCH_MODEL` (examples/extensions/beagle.py line
197) lets workers run a *different* model from the driver. Nothing yet puts
the stronger model in the driver seat, or uses it for the one step that reads
the ITC paper.

**Where it lands.** This is configuration first, not code. Run the driver on
a stronger model and keep 9B workers via `BEAGLE_TAU_DISPATCH_MODEL`. Or keep
a 9B driver and add a per-step `model` for the "read the reference / write
the cases" milestone (the `model` argument already exists on the dispatch
tool, examples/extensions/beagle.py line 1387). Provider wiring is in
src/tau_coding/provider_runtime.py.

**Value: high for misreading the problem** (ITC vs interval trees) and for
weak done_when checks, since the strong seat writes them. It changes the
experiment ("9B does it"), so it is a decision for the user, not a fix to
slip in. Fang's own numbers say a 9B executor with a strong director passes
single tasks and fails long bundles.

### 3. Bound the executor in turns and hand back with a note, not a wall-clock kill

**What fang does.** The player runs at most `HANDBACK_AFTER_PLAYER_TURNS`
turns (5, then 10, then 20; relay.py line 485). When those are used up, the
harness writes `NOTE_AFTER_TURN_COUNT`: "The turns for carrying out this
direction are used up. Back to setting direction: check what was done against
what success looks like..." (relay.py line 905). The player also has an
argument-free `ran_into_trouble` tool to hand back early (relay.py lines
837-860, 972). Fang measured how the windows end: 82% hand back because the
counter expires, and `ran_into_trouble` fired 0 times in 30 runs (relay.py
lines 495-509). A small model does not ask for help. The counter is what
stops it.

**Tau today.** A worker is stopped only by `DEFAULT_DISPATCH_TIMEOUT = 900.0`
seconds (examples/extensions/beagle.py line 191). A worker that overruns its
scope reaches the timeout and returns nothing usable. `PIECE_BY_PIECE_NOTE`
asks it to "Stay inside your task" (line 4517), but that is prompt-only.

**Where it lands.** Add a turn cap to the agent loop that ends the run with a
final "turns used up: say what is done and what is left" user turn, so the
worker's last message is a report. The run-loop bound goes in
src/tau_agent/loop.py, and the per-session setting in src/tau_coding/session.py
(beside `MAX_OUTPUT_LIMIT_CONTINUATIONS`). The worker spawn
(examples/extensions/beagle.py) sets it from the task's budget.

**Value: high for "workers overrun scope, then time out".** A worker that
returns partial work and a report gives the driver something to close or
re-split. A timeout leaves only a dead container.

### 4. Correct malformed tool-call JSON with the model's own string, bounded at three

**What fang does.** When a call's arguments are not valid JSON, the tool
result names the tool and quotes back up to 400 characters of what arrived.
It says the call was not made and asks for "one complete JSON object"
(`malformed_arguments_error`, /home/choong/fang/coachplayer/loop.py lines
916-960). When llama.cpp's server rejects the completion itself, a `user`
correction is sent instead. After 3 such corrections in a row
(`UNPARSED_ARGUMENTS_CORRECTIONS`, loop.py line 964), the seat is told the
cause and the fix: "A multi-line command -- a heredoc or a pasted script --
is what fails to parse: keep a command on one line (`python3 -c '...'`)"
(`COACH_CORRECTIONS_SPENT`, relay.py line 576). Before that change, the coach
resent the same heredoc about 110 times (Q1017, same docstring).

**Tau today.** Unparseable arguments are kept as `{"_raw_arguments": ...}`
(src/tau_ai/openai_compatible.py line 731). Nothing in src/tau_agent or
src/tau_coding reads that key, so the model presumably gets a generic
missing-argument error. Unverified: I did not run a malformed call to see
the exact text.

**Where it lands.** Check for `_raw_arguments` before executing the tool, in
src/tau_agent/loop.py, and return fang's three-part result. Count consecutive
failures in src/tau_coding/session.py, next to the `REPEATED_CALL_*`
counters.

**Value: medium.** It targets the heredoc/bash-bypass pattern when it shows
up as broken JSON. The trace would show whether ITC runs hit
`_raw_arguments` at all. Check that before building this.

### 5. Gate "done" on a fresh green check, and give the checker an oracle

**What fang does.** `Complete` is refused for three reasons: `no_check`,
`red` (the last `Check` exited nonzero), or `stale` (the player wrote after
the last green `Check`) (`COMPLETE_GATE_REASONS`, relay.py lines 1040-1080).
This came from a run where the coach called Complete without re-running a
check that had aborted early
(/home/choong/fang/notes/bundle6-hypotheses-r2/hypotheses.md, H2).
Separately, `ORACLE_CHECK_NOTE` asks for randomized inputs compared against an
independent oracle. It also says to hand back "that failing input and the
oracle's expected value, not code" (relay.py line 1081).

**Tau today.** It already has the gate, in a stronger form. pursuit_step's
done close runs the check itself, and work is committed only on a proven
check (commits `6ce2507`, `0f601cd`). `dd75c37` refuses checks that pass
before the work exists. `CASES_FIRST_NOTE` plus `locks` make reference cases
before code (examples/extensions/beagle.py line 4497).

**Where it lands.** The gate needs nothing. The oracle half would be a
property-test task for ITC: fork/join round-trip, event strictly increases,
join is the least upper bound, normalisation is idempotent. It runs under
`locks` beside `tests/cases.json` and goes in `CASES_FIRST_NOTE`. One more
gate is worth adding in the beagle bridge. When the driver abandons a task,
run that task's check first and refuse the abandon if it passes. This is the
"abandoning tasks whose checks already pass" failure, and it is the same
"done is what the check says" rule turned around.

**Value: medium.** The close gate is already there. Property tests help
against "tests rewritten to fit the code", because locked properties cannot
be fitted. Fang's prompt-only oracle arm never fired, so property tests only
help if they come from a locked task, not from a note.

### 6. Do not send temperature 0; use the server's anti-repetition sampling

**What fang does.** Fang used to send `temperature 0` on every request. On
llama.cpp that turns the sampler chain into argmax, so the server's
`presence_penalty 1.5` never applied. The "rung-7 doom loop" was the result.
After the fix, sampling is left to the server defaults: player
`temp 0.7 / top_p 0.8 / presence_penalty 1.5`, coach `1.0 / 0.95`
(commit `75801ff6`, /home/choong/fang/coachplayer/llm.py).

**Tau today.** Already handled. No tau source sends `temperature`, `top_p`
or `presence_penalty` (grep over src/ finds none), so the bane server's
defaults apply. What is left is server-side, outside tau: confirm the
llama.cpp preset for the 9B models has Qwen's recommended presence penalty.
If tau ever starts servers itself, that goes in
src/tau_coding/extensions/builtins/llama_cpp/service.py.

**Value: low-medium.** It may help with repeated identical calls, which tau's
refusal (src/tau_coding/session.py `REPEATED_CALL_LIMIT`, line 197) already
handles.

### 7. A prose-only turn gets one nudge, not an end

**What fang does.** When a player turn calls no tool, the harness answers
with `NOTE_AFTER_PLAYER_PROSE`: "That reply called no tool, so nothing ran...
take the next step toward success with a tool, or call ran_into_trouble". Only
a second prose-only turn in a row ends the window
(`PLAYER_PROSE_ONLY_TURNS = 2`, relay.py lines 529-566, 879). Measured: 22 of
27 prose handbacks came on the window's *first* reply, often an
announcement ("Carrying out: ...") that the nudge turned into work.

**Tau today.** A worker turn with no tool call ends the run. Tau continues
only after an output-limit cut (`MAX_OUTPUT_LIMIT_CONTINUATIONS`,
src/tau_coding/session.py line 203).

**Where it lands.** For worker sessions only, in src/tau_coding/session.py,
next to the output-limit continuation: if a run ends on text with no tool
call and the task's check has not passed, send the nudge once.

**Value: low-medium.** It helps workers that announce a plan and stop. Check
the ITC worker traces for that ending first.

### Already in tau, or not worth taking

- **Normalised repeat detection** (`REPEAT_WINDOW_N = 8`, whitespace and case
  folded, /home/choong/fang/coachplayer/loop.py lines 193, 311). Tau's version
  is stronger: it refuses a call that keeps returning the same result, and
  stops the run after 8 refusals (src/tau_coding/session.py lines 195-202).
- **Buffered tool output with handles.** Fang's small players could not copy
  an opaque `buf_<hex>` handle at first: 0 of 3, later 1/3 to 2/3 once a
  prompt rule and a list of live handles were added (commit `39dfd7d7`). Tau
  already avoids the problem by making the handle a file path
  (src/tau_coding/tool_buffers.py line 10).
- **Coach-only tripwires, the veto gate, credits**
  (/home/choong/fang/doc/engineering-brief.md sections 5 and 7). These save
  coach calls in a two-model setup. They do nothing for a single-model run.
- **Short player prompt with rules** ("one tool per step", "Keep every reply
  short. No preamble", /home/choong/fang/coachplayer/player.py line 72). Fang
  never measured its effect, and tau's experience says prompt rules alone do
  not move a 9B model.

## Unverified

- What text a tau tool returns for `{"_raw_arguments": ...}` (idea 4).
- Whether the bane llama.cpp preset for the two 9B models sets a presence
  penalty (idea 6).
- Whether an instruct (non-thinking) build of either 9B model is served on
  bane (idea 1).
