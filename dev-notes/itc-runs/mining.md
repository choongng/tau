# Mining R01-R44 and B01-B03 (T0394-T0399)

The owner stopped new runs on 2026-10-10. These scripts in
~/tautest/itc-harness/mine/ read every driver and worker session of R01-R44 and
B01-B03 and turn them into ranked findings, each judged against today's tau
(choong-dev, be6c1c6d) and ~/beagle (choong-dev).

## How to rerun

From ~/tautest/itc-harness, Python 3 stdlib only, about 3 s in all:

```sh
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out $OUT/events.jsonl
python3 mine/refusals.py --events $OUT/events.jsonl --out $OUT/refusals.json --rows $OUT/refused.jsonl
python3 mine/contradictions.py --events $OUT/events.jsonl --refused $OUT/refused.jsonl --kinds $OUT/refusals.json --out $OUT/contra.json
python3 mine/indicators.py --events $OUT/events.jsonl --refused $OUT/refused.jsonl --kinds $OUT/refusals.json --out $OUT/ind.json
python3 mine/findings.py --kinds $OUT/refusals.json --contradictions $OUT/contra.json --indicators $OUT/ind.json \
  --dispositions mine/dispositions.json --out $OUT/findings.json --table $OUT/table.md
python3 -m pytest -q mine/
```

- events.py: one normalized row per session line.
- refusals.py: catalogs refused results into kinds, each tied to the source line that writes it today. 2268 rows, 172 kinds, 168 live.
- contradictions.py: offered-then-refused (139, all driver), alternating (76) and repeated (184).
- indicators.py: time, workers, stops, driver work, sinks and recovery. It now also lists `unrecovered_lines`, so findings can cite trace lines.
- findings.py: applies the fixed rules in its docstring (pairs seen 2+ times; 5+ repeated stretches; 3+ alternating stretches; 10+ unrecovered driver rows; every non-reported worker outcome; every abnormal stop by cause and role; driver edits and test runs outside the baselines; 60 s+ sinks by role and tool). Ids come from class and kind ids, never from rank. findings.py warns about a finding with no disposition and about a disposition that matches no finding.
- dispositions.json: hand-written and keyed by finding id. `same_as` shares one entry's disposition.

When a disposition changes, edit dispositions.json, rerun, and paste the new table below.

## Findings

Ranked by runs reached, then models, then count, then whether it stops a run.
Generated, verbatim:

| rank | id | class | count | runs | models | live | disposition | title |
|---:|---|---|---:|---|---|---|---|---|
| 1 | `unrecovered:c23264dad9` | unrecovered | 199 | 24: B01…R42 | gemma/mimo/qwen | yes | deferred | 199 of 238 driver rows unrecovered: «Not run: this `Q` call ran N times in the last N calls with the same res… |
| 2 | `driver_work:edit` | driver_work | 180 | 22: R01…R44 | mimo/qwen | yes | task T0404 | the driver wrote or edited files itself ({'write': 28, 'redirect': 94, 'edit': 22, 'in_place': 21, 'open_w': … |
| 3 | `repeated:c23264dad9` | repeated | 42 | 21: R09…R42 | gemma/mimo/qwen | yes | deferred | repeated ×286 rows: «Not run: this `Q` call ran N times in the last N calls with the same result each time, a… |
| 4 | `stop:breaker/driver` | stop | 20 | 20: R03…R33 | mimo/qwen | yes | not_a_bug | driver stopped by breaker (0 went on after it; reasons {'error': 12, 'aborted': 8}) |
| 5 | `unrecovered:59291e85e9` | unrecovered | 20 | 20: R03…R33 | mimo/qwen | yes | not_a_bug | 20 of 20 driver rows unrecovered: «Not run, and the run is stopped: N tool calls in a row were refused.» |
| 6 | `driver_work:test` | driver_work | 62 | 18: R04…R44 | gemma/mimo/qwen | yes | deferred | the driver ran the tests itself ({'test': 62}) |
| 7 | `stop:length/worker` | stop | 47 | 18: R01…R44 | gemma/mimo/qwen | yes | not_a_bug | worker stopped by length (36 went on after it; reasons {'length': 47}) |
| 8 | `worker_outcome:no_report/raw_call` | worker_outcome | 34 | 15: R02…R44 | mimo/qwen | no | fixed faf061f5 | worker ended no_report (raw_call): last stop L67: stopReason=stop, 204 chars, 0 call(s) |
| 9 | `repeated:fba65173cb` | repeated | 22 | 13: R21…R44 | mimo/qwen | yes | task T0403 | repeated ×101 rows: «Tool call blocked: refusing to write P: it is outside T#'s scope (P).» |
| 10 | `worker_outcome:capped/tool_result` | worker_outcome | 10 | 10: R04…R44 | gemma/mimo/qwen | yes | not_a_bug | worker ended capped (tool_result): last stop L32: stopReason=toolUse, 0 chars, 1 call(s) |
| 11 | `repeated:30cf569817` | repeated | 30 | 9: R04…R20 | mimo/qwen | yes | task T0403 | repeated ×165 rows: «Tool call blocked: refusing to write P: it is outside T#'s scope (P); name it in your re… |
| 12 | `stop:length/driver` | stop | 44 | 8: B01…R42 | gemma/mimo/qwen | yes | not_a_bug | driver stopped by length (43 went on after it; reasons {'length': 44}) |
| 13 | `stop:breaker/worker` | stop | 14 | 7: R09…R42 | gemma/mimo | yes | not_a_bug | worker stopped by breaker (0 went on after it; reasons {'error': 3, 'aborted': 11}) |
| 14 | `repeated:a9d4253fcf` | repeated | 12 | 7: R16…R44 | mimo/qwen | yes | deferred | repeated ×78 rows: «Tool call blocked: refusing to run `Q`: the brief already holds what the task needs; do t… |
| 15 | `alternating:5c7fa72947~a9d4253fcf` | alternating | 7 | 6: R16…R44 | mimo/qwen | yes | deferred | alternating ×54 rows: «Tool call blocked: refusing to read P: the brief already holds what the task needs; do… |
| 16 | `worker_outcome:length/length_stop` | worker_outcome | 11 | 5: R13…R44 | gemma/mimo/qwen | yes | deferred | worker ended length (length_stop): last stop L67: stopReason=length, 28921 chars, 0 call(s) |
| 17 | `worker_outcome:breaker/aborted` | worker_outcome | 11 | 5: R21…R42 | gemma/mimo | yes | not_a_bug | worker ended breaker (aborted): last stop L62: stopReason=aborted, 0 chars, 0 call(s), error 'Not run, and th… |
| 18 | `worker_outcome:no_report/ended_on_tool_use` | worker_outcome | 8 | 5: R22…R41 | mimo/qwen | yes | deferred | worker ended no_report (ended_on_tool_use): last stop L37: stopReason=toolUse, 30 chars, 1 call(s) |
| 19 | `unrecovered:349b62dd47` | unrecovered | 11 | 4: R06, R09, R18, R40 | mimo/qwen | yes | task T0402 | 11 of 31 driver rows unrecovered: «pursuit_step: T# not opened — `Q` already passes, before any work, so it c… |
| 20 | `repeated:9290e1e36a` | repeated | 8 | 4: R06, R08, R09, R15 | mimo/qwen | yes | deferred | repeated ×33 rows: «Tool call blocked: refusing to run `Q`: the brief has everything; do the task.» |
| 21 | `worker_outcome:timeout/tool_result` | worker_outcome | 6 | 4: R01, R15, R21, R39 | gemma/mimo | yes | not_a_bug | worker ended timeout (tool_result): last stop L96: stopReason=toolUse, 0 chars, 1 call(s) |
| 22 | `alternating:c23264dad9~fba65173cb` | alternating | 4 | 4: R21, R23, R24, R25 | mimo/qwen | yes | task T0403 | alternating ×24 rows: «Not run: this `Q` call ran N times in the last N calls with the same result each time,… |
| 23 | `unrecovered:7c5c3a3012` | unrecovered | 12 | 3: R06, R12, R15 | mimo/qwen | yes | not_a_bug | 12 of 17 driver rows unrecovered: «pursuit_step: T# not run: N steps on it have left it not done, and another… |
| 24 | `repeated:8f66e037e3` | repeated | 5 | 3: R35, R40, R44 | mimo/qwen | yes | deferred | repeated ×30 rows: «Tool call blocked: refusing to run this command: N of N calls used and nothing written, a… |
| 25 | `alternating:30cf569817~c23264dad9` | alternating | 4 | 3: R09, R12, R15 | mimo/qwen | yes | task T0403 | alternating ×39 rows: «Tool call blocked: refusing to write P: it is outside T#'s scope (P); name it in your … |
| 26 | `offered_then_refused:9513435cfa>16decd7096` | offered_then_refused | 8 | 3: R06, R22, R28 | qwen | yes | task T0402 | offered by «Tool call blocked: refusing `Q` from bash: use pursuit_step, which closes a task on its check; to… |
| 27 | `offered_then_refused:9513435cfa>6d1383189f` | offered_then_refused | 3 | 3: R08, R22, R26 | qwen | yes | task T0402 | offered by «Tool call blocked: refusing `Q` from bash: use pursuit_step, which closes a task on its check; to… |
| 28 | `unrecovered:00c2703ea8` | unrecovered | 21 | 2: R21, R28 | mimo/qwen | no | fixed 438d88ed | 21 of 27 driver rows unrecovered: «T# is not a task to work now: it is a container of T#, …, done when its pa… |
| 29 | `time_sink:worker/bash` | time_sink | 8 | 2: R34, R39 | gemma/qwen | no | fixed 86445034 | worker bash calls of 60s+ with no worker inside: [600, 120, 120, 120, 120, 120, 120, 120] s (8 timed out) |
| 30 | `alternating:06a23045d9~9290e1e36a` | alternating | 3 | 2: R06, R15 | mimo/qwen | yes | deferred | alternating ×20 rows: «Tool call blocked: refusing to read P: the brief has everything; do the task.» / «Tool… |
| 31 | `unrecovered:7fdeddcb23` | unrecovered | 10 | 2: R03, R07 | mimo | yes | deferred | 10 of 10 driver rows unrecovered: «pursuit_found: nothing written — 'Q' is not part of the goal's work: pursu… |
| 32 | `alternating:30cf569817~a9d4253fcf` | alternating | 3 | 2: R16, R20 | qwen | yes | task T0403 | alternating ×17 rows: «Tool call blocked: refusing to write P: it is outside T#'s scope (P); name it in your … |
| 33 | `time_sink:driver/pursuit_step` | time_sink | 3 | 2: R22, R30 | qwen | no | fixed 4f1aad55 | driver pursuit_step calls of 60s+ with no worker inside: [557, 278, 132] s (0 timed out) |
| 34 | `worker_outcome:breaker/error` | worker_outcome | 3 | 2: R09, R17 | mimo | no | fixed cc8dfd5d | worker ended breaker (error): last stop L58: stopReason=error, 0 chars, 0 call(s), error 'Provider stream end… |
| 35 | `offered_then_refused:fa3aafba9a>7913202752` | offered_then_refused | 2 | 2: R12, R20 | qwen | yes | not_a_bug | offered by «Tool call blocked: refusing to read P from the driving session: it is in the scope of T# (P), whi… |
| 36 | `offered_then_refused:a3d88158cf>nudge:pursuit_not_done` | offered_then_refused | 2 | 2: R37, R40 | qwen | no | fixed d31878cc | offered by «pursuit_step: T# not run — split it or stop. No new route for T#: its done_when `Q`, scope and cr… |
| 37 | `offered_then_refused:fa3aafba9a>a3d88158cf` | offered_then_refused | 2 | 2: R37, R40 | qwen | yes | not_a_bug | offered by «Tool call blocked: refusing to read P from the driving session: it is in the scope of T# (P), whi… |
| 38 | `worker_outcome:timeout/cut_call` | worker_outcome | 2 | 2: R27, R33 | mimo | yes | deferred | worker ended timeout (cut_call): last stop L29: stopReason=toolUse, 0 chars, 1 call(s) |
| 39 | `unrecovered:4891205280` | unrecovered | 46 | 1: R31 | mimo | no | fixed 3a708abf | 46 of 52 driver rows unrecovered: «pursuit_step: T# not run — scope holds known-answer data (P) and the code … |
| 40 | `unrecovered:c04fb59c0d` | unrecovered | 19 | 1: R18 | qwen | yes | deferred | 19 of 21 driver rows unrecovered: «pursuit_step: T# not opened — P fails with ImportError until a later task … |
| 41 | `offered_then_refused:ef06d83f7a>d9265791df` | offered_then_refused | 17 | 1: R28 | qwen | no | fixed 438d88ed | offered by «pursuit_step: T# not opened — P is locked as the known answers (T#): a worker's change to it is p… |
| 42 | `offered_then_refused:ef06d83f7a>42b649b070` | offered_then_refused | 16 | 1: R28 | qwen | no | fixed 438d88ed | offered by «pursuit_step: T# not opened — P is locked as the known answers (T#): a worker's change to it is p… |
| 43 | `unrecovered:d4ccc98bf7` | unrecovered | 13 | 1: R26 | qwen | yes | task T0402 | 13 of 13 driver rows unrecovered: «pursuit_step: `Q` refused: beagle: this intent has already been attempted … |
| 44 | `offered_then_refused:42b649b070>00c2703ea8` | offered_then_refused | 10 | 1: R28 | qwen | no | fixed 438d88ed | offered by «pursuit_plan: nothing added — part 'Q' has the title of T# (pending), which is still to be done.»… |
| 45 | `unrecovered:ef06d83f7a` | unrecovered | 10 | 1: R28 | qwen | no | fixed db37e782 | 10 of 66 driver rows unrecovered: «pursuit_step: T# not opened — P is locked as the known answers (T#): a wor… |
| 46 | `repeated:42b649b070` | repeated | 6 | 1: R28 | qwen | no | fixed 438d88ed | repeated ×23 rows: «pursuit_plan: nothing added — part 'Q' has the title of T# (pending), which is still to b… |
| 47 | `repeated:d9265791df` | repeated | 5 | 1: R28 | qwen | no | fixed 438d88ed | repeated ×20 rows: «pursuit_plan: nothing added — part 'Q' has the title of T#, the task being split.» |
| 48 | `repeated:ef06d83f7a` | repeated | 5 | 1: R28 | qwen | no | fixed db37e782 | repeated ×25 rows: «pursuit_step: T# not opened — P is locked as the known answers (T#): a worker's change to… |
| 49 | `alternating:42b649b070~c23264dad9` | alternating | 3 | 1: R28 | qwen | no | fixed 438d88ed | alternating ×13 rows: «pursuit_plan: nothing added — part 'Q' has the title of T# (pending), which is still t… |
| 50 | `offered_then_refused:0370db2c56>ef06d83f7a` | offered_then_refused | 3 | 1: R28 | qwen | no | fixed db37e782 | offered by «pursuit_plan: nothing added — T# is already one step, so one part does not break it down: a plan … |
| 51 | `offered_then_refused:7f9a877e94>d4ccc98bf7` | offered_then_refused | 3 | 1: R26 | qwen | yes | task T0402 | offered by «pursuit_step: T# not opened — Cases first: Scope names new source P, and no locked test imports i… |
| 52 | `offered_then_refused:349b62dd47>ea2e98ac3f` | offered_then_refused | 2 | 1: R28 | qwen | yes | task T0402 | offered by «pursuit_step: T# not opened — `Q` already passes, before any work, so it cannot tell this task's … |
| 53 | `offered_then_refused:d9a572c630>0370db2c56` | offered_then_refused | 2 | 1: R29 | mimo | yes | not_a_bug | offered by «pursuit_step: T# not opened — Cases first: open the known-answers milestone before the code; its … |
| 54 | `offered_then_refused:ea2e98ac3f>f4043165b7` | offered_then_refused | 2 | 1: R28 | qwen | yes | task T0402 | offered by «pursuit_step: T# not closed done by T# — this pursuit closes done only on a witnessed check, and … |
| 55 | `offered_then_refused:ef06d83f7a>619d1748bb` | offered_then_refused | 2 | 1: R28 | qwen | yes | not_a_bug | offered by «pursuit_step: T# not opened — P is locked as the known answers (T#): a worker's change to it is p… |
| 56 | `offered_then_refused:49ef5a6664>cc17f4c660` | offered_then_refused | 2 | 1: R43 | qwen | yes | task T0402 | offered by «Tool call blocked: refusing to change P from the driving session: in a pursuit the work, and its … |
| 57 | `offered_then_refused:a22ae99e29>c23264dad9` | offered_then_refused | 2 | 1: R42 | gemma | no | fixed 3988a77d | offered by «pursuit_step: T# not run — If a done task already did this work, call pursuit_step task="Q" aband… |
| 58 | `offered_then_refused:a22ae99e29>ce68b4ec23` | offered_then_refused | 2 | 1: R42 | gemma | no | fixed 3988a77d | offered by «pursuit_step: T# not run — If a done task already did this work, call pursuit_step task="Q" aband… |
| 59 | `offered_then_refused:c23264dad9>a22ae99e29` | offered_then_refused | 2 | 1: R42 | gemma | no | fixed 3988a77d | offered by «Not run: this `Q` call ran N times in the last N calls with the same result each time, and would … |
| 60 | `offered_then_refused:cc17f4c660>349b62dd47` | offered_then_refused | 2 | 1: R43 | qwen | yes | task T0402 | offered by «pursuit_step: T# not opened — the scope holds X, which the locked P judges, but done_when runs no… |
| 61 | `time_sink:driver/agent` | time_sink | 1 | 1: R11 | mimo | no | fixed 700e6865 | driver agent calls of 60s+ with no worker inside: [88] s (0 timed out) |
| 62 | `worker_outcome:capped/user_message` | worker_outcome | 1 | 1: R25 | mimo | yes | not_a_bug | worker ended capped (user_message): last stop L66: stopReason=toolUse, 248 chars, 1 call(s) |
| 63 | `worker_outcome:length/cut_call` | worker_outcome | 1 | 1: R41 | mimo | yes | deferred | worker ended length (cut_call): last stop L18: stopReason=toolUse, 50 chars, 1 call(s) |

### What the ranking says

1. **Offers the next refusal turns down (T0402).** Here an offer and the refuser of the call it offers disagree about the state. Today's code still does it in three places:
   - The bash `close` steer (`_STEERED_VERBS`, beagle.py:15511) offers `abandon=` to any task. `_abandon_problem` (beagle.py:3430, 3449) refuses that for a milestone or a non-duplicate.
   - `_already_passes` (beagle.py:10921) offers `abandon="done by X"` whenever it has an X. `_done_by` and `_done_by_unwitnessed` then refuse it (R28, and R42 L53 once).
   - Smaller cases: the open rank gate (R28), beagle's spawn attempt limit (R26), and held()'s "run the locked test" offer, which `_already_passes` then refuses (R43).

   The fix: render an offer only if the call passes the refusers now.
2. **The repeat guard and the breaker are symptoms.**
   - Rank 1, `unrecovered:c23264dad9`, is the 7 guard rows before each breaker stop.
   - All 34 breaker stops follow 8+ refusals. That is the designed end, so `not_a_bug`.
   - 15 of them (R03-R18) surfaced as provider stream errors. That surfacing was fixed by cc8dfd5d.
   - No driver breaker stop happened after R33.
3. **Driver bash writes (T0404).** These were replayed on 2026-10-10. Each driver bash call shaped like a write in the pursuit runs, 132 in all, was put through today's `_driver_bash_change` and `_bash_writes_dot_beagle` with its full command from the session file. 76 are refused today, and most of the rest write /tmp, which is allowed, or only read. Two gaps are still live:
   - `_bash_write_targets` finds no target in a `bash -c '…'` script that holds a heredoc. Examples: R28 L142, and R22 L158-L194 behind a `BEAGLE_TAU_DRIVER_EDITS=1` prefix. `bash -c 'echo x > f'` is caught.
   - `_bash_writes_dot_beagle` misses `touch` and `ln -sf /dev/null` into `.beagle/locked/` (R22 L190, L210; R28 L842). This was the driver trying to get around the locked known answers.
4. **Worker out-of-scope writes (T0403).** This is 52 stretches in 22 runs. The refusal (beagle.py:1208) never says what the worker can write instead.
5. **Fixed since the run that showed them, each pinned by a test:**
   - The stop gate refused the stop the step cap offered (d31878cc).
   - Done-by was offered to an open task (3988a77d).
   - R28's fix-route title clashes (438d88ed, db37e782).
   - R31's 49-call oracle-with-code loop (3a708abf).
   - Text tool calls (f0876d09, faf061f5).
   - R30's sinks. **Traced:** L49's 557 s is a new_route rehearsal plus the open path rerunning the same check. Both grew to the 4G cap and were SIGKILLed after about 4.6 min (R30.md:94, :148). L99's 278 s is the same check once more. 4f1aad55 no longer reruns a killed rehearsal. Neither call had a worker inside.
6. **Deferred:**
   - The worker idle and re-read guards, and output-limit endings. These are model behaviour that the opportunity below would test.
   - `ended_on_tool_use` workers. These need the dispatch result joined to name a cause.
   - R18's and R03/R07's refusals. These have not come back since, but no test replays them.

### A gap in the check, amended

As first bound, T0399's check required two things that cannot both hold. Every offered-then-refused pair seen twice had to be a finding. Every kind in such a finding also had to be a refusals.py kind. But a refused stop's second kind is the stop gate's nudge (`nudge:pursuit_not_done`), which is a user message, not a tool result in the catalog. The check was amended to exempt `nudge:` kinds from the catalog lookup only, so `offered_then_refused:a3d88158cf>nudge:pursuit_not_done` (R37, R40) stands as a finding. Its disposition is fixed, by d31878cc.

## Known answers

These are the owner's numbers from the run trees (.beagle/tree/T*.md under ~/itc.rNN and ~/cobs.rNN). This task carries them; it did not re-derive them.

- R03, R05, R07, R11 and R38 never founded.
- 13 runs closed a known-answers or reference task done: R08, R12, R14, R20, R22, R27, R28, R30, R33, R34, R39, R42 and R43. **9 of those 13 passed some hidden test.**
- The other 31 did not close one, and **3 of them passed any test** (R09, R17, R24).
- 19 runs ended with the reading or known-answers task still open:
  - **Worker-side** (about 43-54 worker-minutes, run to the cap): R04, R21, R24, R35, R41, R44. Here the workers had the time and did not produce cases that pass.
  - **Driver-side** (refusal loops to the breaker, few worker-minutes): R06, R18, R29, R31, R32. R31 is the "scope holds known-answer data" loop ×49 (`unrecovered:4891205280`, fixed by 3a708abf).
  - In between: R02, R13, R15, R16, R23, R36, R37 and R40.

**The opportunity, for the owner to weigh:** give that one task's worker a stronger model.
- The dispatch is already a sub-agent boundary, so the driver's prefix cache is untouched.
- beagle locks the cases file after that task, so cheaper workers are then judged against better known answers.
- Choosing a model per task needs dispatch support, and none exists today:
  - launch.sh picks one model per run (launch.sh:33-35).
  - beagle's dispatch config has one role, `ROLES = ("executor",)` (beagle dispatch.py:56), with no per-task key.

**Caveats:**
- The 9/13 vs 3/31 split is correlation: runs that closed the task may also differ in model, prompt and tau version.
- R27, R28, R33 and R42 closed known answers and still scored 0.
- The best grade of all is 12/42.
- **Proposed offline test, not run** (the owner stopped runs): give one stuck run's known-answers brief (for example R44 T0002, or R41) once to a stronger model in a copy of its repo, then grade its tests/cases.json with the run's hidden test.
