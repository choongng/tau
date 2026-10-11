# ITC and COBS runs R21–R44: summary

Twenty-four unattended runs, from 2026-10-04 to 2026-10-10. R21–R35 cycle
mimo-v2.6-9b-q4 and qwen3.5-9b-q4-mtp-thinking-coding over two prompts,
`~/tautest/itc_prompt.txt` (interval tree clocks) and
`~/tautest/cobs_prompt.txt` (consistent overhead byte stuffing), each in
Python through a beagle pursuit. From R36 the cycle adds gemma4-12b-q4. After
each run, tau was fixed from the trace. Each run's notes are in `RNN.md`. The
baselines (plain tau, no pursuit) are in `B01.md`–`B03.md` and `baselines.md`.
The trace-mining findings over R01–R44 and B01–B03 are in `mining.md`, and
beagle-side items are in `upstream.md`. The previous block is
`summary-R11-R20.md`.

The owner authorized R21–R40 on 2026-10-04 and later extended the series to
R50. On 2026-10-10 the owner stopped new runs: R45–R50 were dropped in favour
of mining the traces already on disk (`mining.md`, T0394–T0412).

## Headline lessons

1. No run completed: none passed every hidden test. The best was R34 (qwen,
   cobs) at 7/44, below R12's 12/42 in the previous block. Six of 24 runs passed
   any test: five qwen runs and one gemma run. mimo passed none in 11 runs.
2. The grade came from cobs. Five of 12 cobs runs passed some test (R22, R30,
   R34, R39, R43), against one of 12 itc runs (R24, 3/42). On itc, the prompt
   R11–R20 also ran, the best fell from 12/42 to 3/42.
3. Known answers decided the run. Of the 9 runs that closed a known-answers or
   reference task (R22, R27, R28, R30, R33, R34, R39, R42, R43), 5 passed a
   test. Of the 15 that did not, only R24 did (`mining.md`, Known answers). The
   cases the workers wrote were often their own, not the reference's results, in
   every model and both prompts (R32, R34, R40, R41, R43, R44). tau tightened
   the close one shape at a time, but cannot make a small worker transcribe the
   right answers.
4. The driver's refusal loops ended, and the output limit took their place.
   The breaker ended 7 runs, R23–R33, and none after (`mining.md`, point 2).
   With driver thinking on from R36, runs instead lost time to reasoning that
   filled the 8192-token output limit (R36, R38), and with worker thinking on
   from R41, workers lost it the same way (R41, R43, R44). Thinking changed
   how runs failed, not the grade: 4 of 15 thinking-off runs scored (16
   points), and 2 of 9 thinking-on runs (9 points).
5. Mining found one cross-cutting tau defect: an offer that the next refusal
   turns down (T0402). It was fixed at every offer site in T0405–T0410, and
   the bool-exit refusal in T0412, on 2026-10-10 after R44 ended. No run has
   met those fixes.
6. The baselines split by model. Plain tau scored B02 (mimo, itc) 5/42,
   above every mimo pursuit run in this block (all 0). For qwen cobs and gemma
   cobs, plain tau scored 0/44 (B01, B03), below the pursuit's best (R34 7/44,
   R39 4/44).

## Runs

Driver and worker thinking are as recorded in each run's meta.json
(`driver_thinking`, `worker_thinking`); where a field is absent the table says
off. Min is process minutes (exit.json end minus meta.json start). R38's
session holds only 1.1 min of events, but its process ran to the cap. The sha
is the tau commit the run used. Grades are `passed/total` from grade.json.

| Run | Model | Prompt | Driver | Workers | tau sha | Min | Grader | How it ended |
|---|---|---|---|---|---|---|---|---|
| R21 | mimo | itc | off | off | 352c288 | 60.0 | 0/42 | Cap. 0 of 7 done; T0005 (cases.json, split from known answers) still open; no implementation |
| R22 | qwen | cobs | off | off | 3e6a92f | 56.0 | 3/44 | OOM kill (exit 143): an encoder that never passed a zero byte grew a test run to the 8G cap; 1 of 21 done |
| R23 | mimo | cobs | off | off | 0eab6c1 | 13.3 | 0/44 | Breaker. An absolute scope hid a passing notes task's file from prove; 0 of 5 done |
| R24 | qwen | itc | off | off | 31b5ff9 | 60.0 | 3/42 | Cap. 0 of 20 done; passing known-answers work held open as misplaced implementation |
| R25 | mimo | itc | off | off | 7251a99 | 60.0 | 0/42 | Cap. 0 of 10 done; the first known-answers task did not fit one 30-call worker |
| R26 | qwen | cobs | off | off | 7a23ce9 | 34.0 | 0/44 | Breaker. 0 of 14 done; a passing data task held open, then no offered call could be followed at beagle's attempt limit |
| R27 | mimo | cobs | off | off | 36f5db8 | 60.0 | 0/44 | Cap. 1 of 8 done (the reference task); an invented frame size became a check |
| R28 | qwen | itc | off | off | da70942 | 38.9 | 0/42 | Breaker. 13 of 40 done (known-answers, test and verify tasks); lock, title-clash and container refusals looped; the module is not an ITC |
| R29 | mimo | itc | off | off | 573a8ba | 7.4 | 0/42 | Breaker. 0 of 7 done; Cases first refused the known-answers task itself |
| R30 | qwen | cobs | off | off | eb39f78 | 60.0 | 3/44 | Cap. 1 of 7 done (known answers); a check killed at the memory cap was read as "cannot run" |
| R31 | mimo | cobs | off | off | 3dd92ec | 27.1 | 0/44 | Breaker. 0 of 3 done; an oracle-with-code refusal on a helper script, resent to the stop |
| R32 | qwen | itc | off | off | ee85665 | 2.8 | 0/42 | Breaker. 0 of 5 done; the data-route refusal proposed the check already bound |
| R33 | mimo | itc | off | off | 1bd98f5 | 40.3 | 0/42 | Breaker. 1 of 6 done (reading notes); one call resent twelve times |
| R34 | qwen | cobs | off | off | 515feb3 | 60.0 | 7/44 | Cap. 1 of 12 done (known answers); locked files kept in the code task's scope; cobs.py uncommitted |
| R35 | mimo | cobs | off | off | 0980278 | 60.0 | 0/44 | Cap. 0 of 7 done; workers wrote under .git/beagle/ and broke cases.json |
| R36 | gemma | itc | medium | off | 037df4f | 49.5 | 0/42 | Finished: the 7th output-limit cut-off, a driver reasoning loop, ended tau -p; 0 of 4 done |
| R37 | qwen | cobs | medium | off | e2f3da5 | 20.2 | 0/44 | Finished after the driver's third stop; the step cap refused a failure it could name; 0 of 4 done |
| R38 | mimo | itc | medium | off | 114f605 | 60.0 | 0/42 | Cap. Never founded: a pre-founding agent call held 57 of the 60 minutes |
| R39 | gemma | cobs | medium | off | d4deb2d | 60.0 | 4/44 | Cap mid-worker. Known answers closed with a cases test that copied the data test; 1 of 5 done |
| R40 | qwen | itc | medium | off | dc8c3f9 | 26.8 | 0/42 | Finished by itself; never left known answers (unsourced cases); 0 of 16 done |
| R41 | mimo | cobs | medium | medium | 7ac432d | 60.0 | 0/44 | Cap mid-worker. Worker reasoning filled the output limit before any call; 0 of 5 done |
| R42 | gemma | itc | medium | medium | 284198d | 60.0 | 0/42 | Cap. 2 of 8 done; the cases lock fired on an analysis task, then two refused calls alternated |
| R43 | qwen | cobs | medium | medium | b8c6772 | 60.0 | 5/44 | Cap, W14 killed. 1 of 5 done; a locked cases test with a guarded import passed without the code |
| R44 | mimo | itc | medium | medium | e870feb | 60.0 | 0/42 | Cap, W9 killed. Known answers held by the source rule; an inverted python -c check; the implementation task never opened |

Worker thinking "off" means beagle dispatched workers with `--thinking off`.
gemma's workers reasoned anyway in R36 (62,550 chars), because gemma opens a
thought channel on its own (R36.md:196, R36.md:199). From R41, launch.sh
dispatches workers at the driver's level (itc-harness `eaa83cb`, T0362). From
R42, a step whose worker was cut off reasoning retries thinking-off
(`b30996a4`), so some R42–R44 workers ran off (R44.md:5).

On thinking before R36: tau's git log records that a provider without
`thinking_parameter` drops every thinking level, and the qwen-chat-template
format then sends `enable_thinking: false` (`66382dc1`, 2026-10-08). That
commit names krang's qwen3.8. `baselines.md` (Confounds) says bane's 9B
models had the same gap until the 2026-10-08 catalog fix. No RNN.md for R21–R35
says so. It does not change this table: R21–R35 sent no driver thinking at all
(their meta.json has no `driver_thinking`; R36.md:109 calls them thinking
off), and R36 onward ran on 2026-10-09 and later, after the fix. R40.md:144
confirms the fixed catalog sends the level.

Baselines, plain `tau -p --no-extensions` on the prompt without its beagle
lines, same cap and memory limit:

| Run | Model | Prompt | Driver | tau sha | Min | Grader | How it ended |
|---|---|---|---|---|---|---|---|
| B01 | qwen | cobs | medium | 1fad2d1 | 35.0 | 0/44 | Stopped on its own. Never read the reference; its scheme is not COBS (0xFF delimiter); rewrote its tests to match its code |
| B02 | mimo | itc | medium | ad8fbd7 | 60.0 | 5/42 | Cap, mid `pytest -x` loop. Read both references first; real id and event trees, but split and join wrong |
| B03 | gemma | cobs | medium | 41a1fa2 | 6.5 | 0/44 | One unrun 66-line draft, then "done" with 53.5 min unused; scheme not COBS |

No baseline committed anything. `baselines.md` sets each beside the pursuit
runs of the same model and prompt.

## By model and prompt

Recomputed from grade.json and meta.json; the same numbers as
`python3 ~/tautest/itc-harness/progress.py`. Completed means every hidden test
passed.

| Model | Prompt | Runs | Completed | Any-pass | Best | Run ids | Baseline |
|---|---|---|---|---|---|---|---|
| gemma | cobs | 1 | 0 | 1 | 4/44 | R39 | B03 0/44 |
| gemma | itc | 2 | 0 | 0 | 0/42 | R36, R42 | none |
| mimo | cobs | 5 | 0 | 0 | 0/44 | R23, R27, R31, R35, R41 | none |
| mimo | itc | 6 | 0 | 0 | 0/42 | R21, R25, R29, R33, R38, R44 | B02 5/42 |
| qwen | cobs | 6 | 0 | 4 | 7/44 | R22, R26, R30, R34, R37, R43 | B01 0/44 |
| qwen | itc | 4 | 0 | 1 | 3/42 | R24, R28, R32, R40 | none |

By thinking:

| Runs | Driver | Workers | Runs | Any-pass | Points | Best | Breaker stops |
|---|---|---|---|---|---|---|---|
| R21–R35 | off | off | 15 | 4 | 16 | 7/44 | 7 |
| R36–R40 | medium | off | 5 | 1 | 4 | 4/44 | 0 |
| R41–R44 | medium | medium | 4 | 1 | 5 | 5/44 | 0 |

Each tau sha met one run, so these rows mix thinking with tau version, model
and prompt. Within qwen cobs, the cell with the most runs, thinking off gave 3,
0, 3 and 7 (R22, R26, R30, R34) and thinking on gave 0 and 5 (R37, R43).

## Recurring failure classes

Only classes seen in two or more runs of R21–R44 are listed. Evidence is
`RNN.md:line`, pointing at the failure-class heading in that run's notes.
Fixes are tau commits unless marked. Every RNN.md class marked prompt- and
model-independent says so on its own line under the heading.

### Known answers that do not hold the reference's answers
Runs: R24, R30, R32, R33, R34, R35, R36, R37, R39, R40, R41, R43, R44
Evidence: R30.md:187, R32.md:169, R33.md:154, R34.md:156, R34.md:202,
R35.md:132, R36.md:188, R37.md:105, R39.md:198, R40.md:161, R40.md:189,
R41.md:163, R43.md:147, R43.md:175, R44.md:144, R44.md:172
Status: the close was tightened one shape at a time. A source must hold the
case's result, not its input (`bff8eda5`, R34). The read judge counts
`with … as` handles (`7c564c92`, R33). A data test that imports the code
through a sibling test is followed (`f46f6c16`, R35). Each changed result field
must be quoted (`a0c00b15`, R36). The unsourced verdict points at the lines
holding each case's value (`dcaa2f43`, R37). A cases test that copies the data
test does not close (`ad321fe4`, R39). Result lines are found by structure, so
hex runs and table rows count across prompts (`1f4f1dce`, R40). A cases test
that passes without the code it imports is held (`2a82449c`, R43). A nested
result is judged whole (`a5eeb2bb`, R44). The workers' invented values are the
model's part, and are deferred: `mining.md` proposes a stronger model for this
one task.
Carried across: all three models and both prompts. Each new close rule met a
new evasion in the next run of a different model.

### Checks that no worker can pass, or that pass without the code
Runs: R21, R24, R25, R26, R28, R40, R41, R42, R43, R44
Evidence: R21.md:94, R24.md:82, R25.md:103, R26.md:118, R28.md:161,
R40.md:182, R41.md:150, R42.md:145, R43.md:154, R44.md:137, R44.md:158
Status: fixed for each shape seen. A check may not run a test a waiting
sibling writes (`9f575cd8`, R21). A module under tests/ is refused a scope
(`4208560d`, R24). A resent check keeps the data-only bind (`9cbfd89f`, R25).
The rebind never proposes the bound check (`383841f8`, R26). A pytest
import-only check is refused (`cd010aec`, R28). A check that runs an absent
file outside scope is refused (`9f6ef116`, R40). The not-done result names a
data test's unwritten import (`22271c7d`, R41), also on a directory scope
(`373a374f`, R44). An open task's own test that imports unwritten code is run
to drop it (`3988a77d`, R42). An open whose selection deselects every test is
refused (`134f7fd6`, R43). A python -c check whose exit is a bool expression is
refused (`8b3241fb`, T0392), and on amend and new route too (`37d5eca4`,
T0412). That refusal parses only python -c, not a heredoc or a script.
Carried across: all three models and both prompts.

### Offers that the next refusal turns down
Runs: R21, R22, R26, R28, R32, R33, R36, R37, R40, R42, R43, R44
Evidence: R21.md:99, R22.md:106, R26.md:128, R28.md:109, R32.md:131,
R33.md:160, R36.md:158, R37.md:95, R40.md:168, R42.md:145, R43.md:168,
R44.md:151
Status: fixed per run first: `a5e56969` (R21), `1be30e06` (R22), `b85586b5`
and `160d19fb` (R26), `438d88ed` (R28), `ec5b4363` (R32), `9cdf6150` (R33),
`8c6b8288` (R36), `39d1650b` (R37), `bb9e3974` (R40), `808f1a9a` (R43) and
`d31878cc` (R44). Mining then found 139 offered-then-refused rows, all driver
(`mining.md`, T0402), and fixed every offer site so that it renders only a
call its refuser accepts: `2088f9b7`, `696970f7`, `66b1cc7c`, `bca1b457`,
`45b8572c` and `d6c81b3b` (T0405–T0410). Each has a test that feeds the offered
call back to its refuser. One beagle-side cause, `open --help` on `--over`, is
on ~/beagle branch mining-fixes-2026-10-10 (`518aa89`). None of the T0405–T0410
fixes has met a run.
Carried across: mimo, qwen and gemma, both prompts. The escalation shape
(R33, R36, R37, R40) recurred across three models after each local fix.

### The driver resends refused calls, edits files or runs tests itself
Runs: R21, R22, R23, R25, R28, R29, R30, R31, R32, R33, R40, R41, R43, R44
Evidence: R21.md:125, R22.md:101, R22.md:126, R23.md:89, R25.md:123,
R28.md:167, R29.md:124, R30.md:177, R31.md:161, R31.md:187, R32.md:157,
R33.md:183, R40.md:202, R41.md:169, R43.md:181, R44.md:178
Status: partly fixed. The edit guard reads `bash -c` behind env words
(`30cb8475`, R22). The breaker quotes the sentence of a refusal that holds its
call (`5d8da031`, R23; `bcabadad`, R32). Mining replayed 132 driver bash
writes against today's guard and closed two gaps, heredocs inside `bash -c`
and `touch`/`ln` into `.beagle/locked/` (`62c11bb1`, T0404). The driver
running the tests itself (18 runs) and the repeat-guard rows before each
breaker stop are deferred (`mining.md`, ranks 1 and 6). The breaker ended R23,
R26, R28, R29, R31, R32 and R33, all thinking-off mimo and qwen runs; the
thinking-on drivers R40, R41, R43 and R44 churned but were not stopped.
Carried across: all three models. Resending to the breaker was mimo's and
qwen's with thinking off; with thinking on, the drivers wrote tests and checks
themselves (R43, R44).

### Workers spend their turns on the wrong work
Runs: R25, R27, R31, R33, R34, R35, R40, R42
Evidence: R25.md:113, R27.md:111, R31.md:176, R33.md:166, R33.md:178,
R34.md:183, R35.md:150, R35.md:168, R40.md:196, R42.md:172
Capped workers (scorecard.json): 82 of 131 in R21–R35, 14 of 32 in R36–R40,
8 of 37 in R41–R44.
Status: partly fixed. The brief states the call cap and each reference's read
cost (`f9e3ac74`, R25). Workers stop re-reading past half the call cap with
nothing written (`2221617e`, R33), and paging and idle bash count toward that
(`038d1493`, R34). Workers may write only their task's log under .git/beagle
(`b1cbab4b`, R35). A repeated scope refusal gives the count and sends the
worker to report (`2d1bd0cf`, T0403, 13 runs R21–R44). The idle and re-read
guards are deferred as model behaviour (`mining.md`, point 6).
Carried across: all three models and both prompts. The caps fell once workers
thought (R41–R44), but the reasoning cut-offs below took that time instead.

### Output-limit cut-offs and reasoning loops
Runs: R27, R31, R33, R36, R38, R41, R42, R43, R44
Evidence: R27.md:86, R31.md:152, R33.md:172, R36.md:138, R36.md:195,
R38.md:85, R41.md:143, R42.md:159, R43.md:161, R44.md:172
Status: partly fixed. A cut-off call gets a character budget and counts as a
length stop (`1f72eb39`, R27); cut-off advice keeps generator scripts out of
scope (`c394a5ba`, R31). Looping reasoning is cut early and nudged thinking
off (`c9a62a95`, R36); a queued nudge blocks another, and tau says when it
cannot build the thinking-off provider (`361c0536`, `588ad070`, R38). A
cut-off step retries its next worker thinking-off (`b30996a4`, R41). A
loop-cut nudge keeps the session's thinking, so the prefix cache holds
(`45968678`, R42). The kill note says what filled the turns (`fe63d587`, R43).
Worker length endings are deferred (`mining.md`, rank 16).
Carried across: thinking-off runs had at most one driver length stop
(R36.md:109). With thinking on, it reached gemma (R36), mimo (R38, R41, R44)
and qwen (R43), on both prompts.

### Tool calls cut off, written as text, or carrying template tokens
Runs: R21, R36, R37, R38, R39, R40, R44
Evidence: R21.md:115, R36.md:179, R36.md:201, R37.md:112, R38.md:78,
R39.md:156, R39.md:191, R40.md:215, R44.md:165
Status: fixed for the forms seen. The guard explains a cut-off call
(`9989dac8`, R21). Arguments carrying chat-template tokens are refused
(`8d71fb84`, R36), and a leaked tail is cut where the call can run without it
(`0b242e0d`, R39). A reply that writes a tool call as text gets a bounded
follow-up (`f0876d09`, R37), also without its opening tag (`faf061f5`, R44). A
cut-off call says so instead of "path must be a string" (`fd37b7c7`, R38), and
a missing argument is named (`abc47437`, R39).
Carried across: all three models. Each model family leaks its own template
tokens, and the fixes key on the token forms, not the task (R37.md:116).

### Checks and tests that hang or reach the memory cap
Runs: R22, R30, R34, R39
Evidence: R22.md:81, R22.md:86, R30.md:147, R30.md:164, R34.md:177,
R39.md:170, R39.md:184
Status: fixed for the paths seen. beagle subprocesses run capped in their own
group (`79e65525`, R22). A check killed on the chain's own code opens as a hang
to find (`4f1aad55`, R30), and worker test commands are bounded below the
worker cap (`53f7a4a1`, R30). Worker bash defaults to 120 s (`038d1493`, R34),
and the brief's command is bound below it (`86445034`, R39). One pursuit_step
is bounded by one step budget across attempts (`29380a00`, R39).
Carried across: cobs only, qwen and gemma. An encoder that never advances past
a zero byte (R22, R30) turns every test run into a hang.

### Domain mis-grounding: invented constants, APIs and representations
Runs: R27, R28, R30, R39, R43, R44
Evidence: R27.md:81, R28.md:172, R30.md:182, R39.md:211, R43.md:175,
R44.md:172
Status: model; deferred. R27's founding invented a ceil(len/10) frame size,
R28's a non-ITC API, R30's encoder never advanced past a zero, R39's driver
worked COBS out wrongly and put it in every brief, R43's workers could not get
decode right, and R44's workers invented a representation. Known answers taken
from the reference are the only lever tau has here, which is the first class.
Carried across: all three models and both prompts.

## What carried across

Prompts. cobs gave more passes than itc: 5 of 12 runs against 1 of 12. The COBS
reference gives worked examples as hex rows, which the result-line rule reads by
structure since `1f4f1dce`. The ITC paper defines its operations by rules with
few worked results, so the source verdict asked for result lines it does not
have (R40.md:161), and the workers quoted rules instead (R44.md:172). The tau
classes above were marked prompt- and model-independent in each RNN.md, and
every class except the hang class reached both prompts. The hangs were
cobs-only, because a COBS encoder can loop on a zero byte.

Models. qwen passed some test in 5 of 10 runs, gemma in 1 of 3, mimo in 0 of
11. mimo's runs ended on refusal loops with thinking off (R23, R29, R31, R33),
then on cut-offs and a pre-founding sub-agent call with thinking on (R38, R41,
R44). gemma brought new failure shapes, such as template tokens in arguments
and reasoning loops (R36), that later showed up in mimo (R38) and qwen (R43).
The fixes for those keyed on token forms and stop reasons, and they held when
the class reached the next model: no tool-call class recurred in the same form.

Thinking. R21–R35 ran with driver and workers thinking off, R36–R40 with the
driver at medium, and R41–R44 with workers at medium too. Breaker stops ended
with thinking-off drivers (none after R33). The thinking-on drivers instead
filled the output limit (R36, R38), and thinking-on workers did the same (R41:
358,318 reasoning chars; R44: 6 cut-offs, 986 s). Capped workers fell from 82 of
131 (R21–R35) to 8 of 37 (R41–R44), but no grade rose: the best thinking-on run
(R43, 5/44) is below R34 (7/44, thinking off). Every sha met one run, so
thinking is mixed with tau version here. `baselines.md` proposed one run with
thinking-off workers to separate them, and that run was not made.

Known answers. This is the finding from `mining.md` that holds across all
three axes. Runs that closed a known-answers or reference task passed a test 9
times in 13 over R01–R44; runs that did not, 3 times in 31. Within R21–R44 it
is 5 of 9 against 1 of 15 (R24). `mining.md` puts five of the runs here that
left it open on the worker side (R21, R24, R35, R41, R44): the workers had the
time and did not produce cases that pass. The split is correlation, and R27,
R28, R33 and R42 closed it and still scored 0. `mining.md` proposes giving
that one task's worker a stronger model, across a sub-agent boundary so the
driver's prefix cache is untouched, and an offline test of it on R44's or
R41's brief. Neither has been run.

Baselines. For mimo, the pursuit has not bought grade: B02 scored 5/42 with no
structure, and the six mimo itc runs here scored 0. For qwen cobs and gemma
cobs, the pursuit aimed the model at the reference (B01 never read it) and kept
it working (B03 quit at 6.5 min). In every cell the ceiling, 4–7 of 42–44, is
far below complete, with or without the pursuit.

## Compared with R11–R20

| | R11–R20 | R21–R44 |
|---|---|---|
| Runs | 10 (itc; mimo, qwen) | 24 (itc, cobs; mimo, qwen, gemma) |
| Runs founded | 9 of 10 | 23 of 24 (R38 never founded) |
| Runs that scored | 4 (R12, R14, R17, R20) | 6 (R22, R24, R30, R34, R39, R43) |
| Best grade | 12/42 (R12) | 7/44 (R34); itc 3/42 (R24) |
| Total grade points | 28 | 25 |
| Closed a known-answers or reference task | 3 (R12, R14, R20) | 9 |
| Median session minutes | 25.8 | 50.5 |
| Ended by the breaker | 8 | 7 (R23–R33) |

R11–R20 lost runs in the oracle and the locks: known answers that judged
nothing, or locked checks nothing could pass. That class carried into this
block. Unpassable checks kept coming back in new shapes (R40–R44), and beside
them the content of the known answers became the main failure: cases the
workers invented. Founding stayed solved except R38, where the failure was an
`agent` call before founding. The breaker, which ended 8 of 10 runs in R11–R20,
ended 7 of 24 here and none of the last 11. Runs got longer (median 50.5 min
against 25.8) and itc grades fell. The longer runs were spent in known answers,
not in implementation.

## What changed in tau

The fix tasks are T0200–T0392 under T0176 (`beagle pursuit tree --under
T0176`), and T0402–T0412 from mining. Each run's header names the fixes that
were new to it. Dates are commit dates.

- Known answers and the close (2026-10-04 to 10-10): `645ded1b` (R22: the
  data lock carries the cases test), `bc1ddbb8` (R26: a proven known-answers
  task closes done), `578593b3` (R27: the brief says the data test imports no
  code), `7c564c92` (R33), `bff8eda5` (R34), `f46f6c16` (R35), `a0c00b15` and
  `3a42717c` (R36), `dcaa2f43` (R37), `ad321fe4` (R39), `fd1aa18e`,
  `1f4f1dce`, `bb9e3974`, `c0e7dc62` (R40), `30f13b47` (worked example in the
  brief, T0364), `25414919` (R42), `2a82449c`, `808f1a9a` (R43), `a5eeb2bb`
  (R44).
- Checks at open (10-04 to 10-10): `9f575cd8` (R21), `4208560d` (R24),
  `9cbfd89f` (R25), `383841f8` (R26), `cd010aec` (R28), `9f6ef116` (R40),
  `22271c7d` (R41), `3988a77d` (R42), `134f7fd6` (R43), `373a374f` and
  `8b3241fb` (R44), `37d5eca4` (T0412).
- Offers, escalations and exits (10-04 to 10-10): `a5e56969` (R21), `1be30e06`
  (R22), `b85586b5`, `160d19fb` (R26), `438d88ed`, `db37e782` (R28), `ec5b4363`
  (R32), `9cdf6150` (R33), `7af91db5` (R35), `07f60cc2`, `8c6b8288` (R36),
  `39d1650b` (R37), `d31878cc` (R44), then T0405–T0410: `2088f9b7`, `696970f7`,
  `66b1cc7c`, `bca1b457`, `45b8572c`, `d6c81b3b`.
- Driver guards and the breaker: `30cb8475` (R22), `5d8da031` (R23),
  `bcabadad` (R32), `700e6865` (R38: the found-first gate refuses `agent`),
  `d0978b70` (T0365: the edit refusal names pursuit_step), `62c11bb1` (T0404).
- Workers: `f9e3ac74` (R25), `2221617e` (R33), `038d1493` (R34), `b1cbab4b`
  (R35), `4c8c8ac5` (how to search references, T0363), `2d1bd0cf` (T0403).
- Output limit and thinking: `1f72eb39` (R27), `c394a5ba` (R31), `c9a62a95`
  (R36), `361c0536`, `588ad070` (R38), `b30996a4` (R41), `45968678` (R42),
  `fe63d587` (R43). Between R35 and R36: `66382dc1` (warn when a provider
  drops thinking levels). In the harness: `eaa83cb` (workers at the driver's
  thinking level, from R41).
- Tool calls: `9989dac8` (R21), `8d71fb84` (R36), `f0876d09` (R37),
  `fd37b7c7` (R38), `0b242e0d`, `abc47437` (R39), `faf061f5` (R44).
- Hangs: `79e65525` (R22), `4f1aad55`, `53f7a4a1` (R30), `86445034`,
  `29380a00` (R39).
- Context: `6b60ab80` and `4fe27c04` (R26: compaction keeps at most half the
  threshold and bounds its summary).

The R21–R35 fixes landed on 2026-10-04 and 10-05. The runs paused from 10-06
to 10-08, while tau took TUI work, an upstream merge (`24405796`) and the
thinking warning. The R36–R40 fixes landed on 10-09 and the R41–R44 fixes on
10-10. The mining fixes (`faf061f5` to `37d5eca4`) landed on 10-10 between
16:08 and 19:51, after R44 had ended.

## Still open

- No run completed, and the best grade (7/44) is below the previous block's
  12/42. Nothing yet checks the implementation's shape against the reference.
- The known answers are the model's. Every close rule above judges how a case
  quotes the reference; none can make a worker copy the right result. The
  stronger-model idea in `mining.md` needs per-task model choice: launch.sh
  picks one model per run, and beagle's dispatch has one role.
- Untested by any run: T0405–T0410, T0412, `62c11bb1`, `2d1bd0cf`,
  `d31878cc` and `faf061f5`.
- Deferred in `mining.md`: the repeat guard rows before each breaker stop, the
  driver running tests itself, worker idle and re-read guards, output-limit
  endings, and workers that end on a tool use with no report.
- The bool-exit refusal parses only python -c checks (T0392).
- Thinking is still mixed with tau version. No run separated worker thinking
  from the workflow, and no baseline was rerun on a newer tau.
- Upstream: beagle reports no attempt count for a retry chain (`upstream.md`,
  R26). The tau-subagents fix for a child session's provider config is a
  local commit, not pushed (`upstream.md`, R38). The `--over` help fix is on a
  ~/beagle branch (`518aa89`).

## Next

Runs are stopped, so the next steps are offline.

1. Run the offline known-answers test from `mining.md`: give R44's T0002 brief,
   or R41's, once to a stronger model in a copy of its repo, and grade its
   tests/cases.json with the run's hidden test. That tests the one lever this
   block points at.
2. If runs resume, start with one mimo itc run on today's tau. Score it
   against B02's 5/42, and on whether the T0405–T0410 offers hold.
3. Add per-task model choice to beagle's dispatch, so known answers can use a
   different worker without touching the driver's prefix cache.
4. Rerun one baseline on today's tau, to tell a gain in the tool from a gain
   in the pursuit.
