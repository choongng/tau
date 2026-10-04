# ITC runs R11–R20: summary

Ten more unattended runs, on 2026-10-03 and 2026-10-04. Like R01–R10, they
alternate mimo-v2.6-9b-q4 (odd runs) and qwen3.5-9b-q4-mtp-thinking-coding
(even runs). Each one used tau + beagle on `~/tautest/itc_prompt.txt`
(interval tree clocks in Python). After each run, tau was fixed from the
trace. Each run's notes are in `RNN.md`. The first ten runs are summarised in
`summary.md`, the harness is described in `harness.md`, beagle-side items are
in `upstream.md`, and the ideas from fang are in `fang-ideas.md`.

## Headline lessons

1. **Founding is no longer the main killer.** R11 never founded (11
   `pursuit_found` calls, refused for want of `user_delegated` in print mode).
   T0107 inferred delegation from the prompt, and every run from R12 on
   founded on the first call. R19 then lost the run to a founding leftover: a
   "Found the pursuit" milestone that became the only ready task.
2. **The failure has moved to the oracle and the locks.** Cases-first now
   holds by structure: known answers are written first and then locked. But
   the locked cases test was often weak, unread or unpassable. R14's never
   read cases.json. R15's and R16's could not pass until a later task's module
   existed. R20's named three cases that were not in the data, and used
   `.event` both as a method and as an int. Once such a test is locked, every
   implementation task is bound to it and nothing can close.
3. **A refusal still has to carry the one move the model can make.** R13
   (bare `&&`), R14 and R18 (refusals that pointed at each other) and R19
   (a `.beagle/` refusal that never said "abandon this setup task") all ended
   with the driver resending one refused call until the breaker stopped it.
   Each of these was fixed by making the refusal name the exit, not by
   refusing harder.
4. **Workers run to the cap when the check cannot pass.** 64 of 84 workers
   hit the 31-turn cap. R20's notes trace this to the checks, not the budget:
   the one worker there on a passable check finished in 24 turns
   (R20.md:68). On test-only scopes, workers spent their turns trying to write
   the implementation anyway (R16, R17, R18), or built it in /tmp (R20).
5. **The correctness ceiling moved, but not far.** R12 scored 12/42 against
   R08's 5/42. No run built the paper's event tree. R12's event component is a
   plain int, R17's `event` returns only a max, and R20 has a flat ClockId and
   an int counter. The passes come from seed, fork-of-seed, norm and join
   cases that a simple structure meets by accident.

## Runs

Minutes are `wall_minutes` from each run's scorecard. The sha is the tau
commit the run used. Grades are out of 42, as recorded on each run's
`grader:` line.

| Run | Model | tau sha | Min | Grader | How it ended |
|---|---|---|---|---|---|
| R11 | mimo | bb28fab | 3.4 | 0/42 | Breaker stop. 11 `pursuit_found` calls without `user_delegated` in print mode; never founded, no worker |
| R12 | qwen | 674f0d0 | 33.2 | 12/42 | Breaker stop. 4 of 9 tasks done; a tests-only task with a passing check had no exit, and the driver tried to `sed` its status |
| R13 | mimo | 3ea4015 | 11.3 | 0/42 | Breaker stop. T0002 opened on a check exiting 129; every rebind refused for a bare `&&`/`<<`, resent until the stop |
| R14 | qwen | 39aff5d | 12.3 | 5/42 | Breaker stop. 4 of 9 done; the locked cases test never read cases.json, and T0009 met contradictory refusals |
| R15 | mimo | 55a2b7a | 36.0 | 0/42 | Breaker stop. 0 of 2 done; the known-answers check ran a test that could not pass yet; 11 resends without `new_route` |
| R16 | qwen | cf4ca14 | 33.6 | 0/42 | Breaker stop. 0 of 11 done; an unpassable known-answers check, 9 of 12 workers capped |
| R17 | mimo | 1bd68d8 | 55.1 | 6/42 | One-hour cap. 1 of 10 done (T0008, itc/itc.py under a collect-only check); T0009's rework uncommitted |
| R18 | qwen | f176ecd | 18.4 | 0/42 | Breaker stop (reported as a provider error). 0 of 8 done; 74 steps, 50 not opened, in a known-answers refusal cycle |
| R19 | mimo | 424a779 | 2.7 | 0/42 | Breaker stop. A "Found the pursuit" milestone was the only ready task, and its `.beagle/` check was refused; no task opened |
| R20 | qwen | d796f11 | 59.9 | 5/42 | One-hour cap. 2 of 11 done; a wrong cases test was locked at minute 12, and every implementation task failed against it |

qwen did better this time. It scored in three of its five runs (R12 12, R14 5,
R20 5), and mimo in one of five (R17 6). qwen also did more work per run: 59
workers against mimo's 25, and 343 driver tool calls against 127. mimo's
three shortest runs (R11 3.4, R13 11.3, R19 2.7 min) all ended on one refused
call resent to the breaker, before any implementation task opened. That is
the same brittleness to refusals that R03, R05 and R07 showed. The one mimo
score (R17) came from the longest mimo run. As before, each sha met only one
model, so the comparison mixes models *and* tau versions.

## Recurring failure classes

Only classes seen in two or more runs are listed. Evidence is `RNN.md:line`,
pointing at the failure-class heading or the header line in that run's
notes.

### Founding and first-task refusals that a 9B resends
Runs: R11, R13, R19
Evidence: R11.md:78, R13.md:108, R13.md:166, R19.md:63, R19.md:67
Status: fixed for the shapes seen. T0107 (print-mode delegation inferred),
T0118 (refuse a check that cannot run), T0119 (bare operators get a move),
T0165 (drop a "Found the pursuit" milestone), T0166 (a setup task's refusal
says to abandon it). T0165 and T0166 have not met that shape in a run.
R19's notes show that setup detection is still a word list: it missed
"found".

### Known answers and cases-first: weak or unread cases tests, unpassable locked checks, refusal cycles
Runs: R12, R14, R15, R16, R17, R18, R20
Evidence: R12.md:267, R14.md:120, R14.md:147, R15.md:117, R15.md:150, R16.md:127, R16.md:151, R17.md:130, R17.md:158, R18.md:125, R18.md:165, R20.md:76, R20.md:84
Status: partly fixed. Each run found a new shape. R12 had cases-first as
advice only (T0113). In R14 the locked test never read the data (T0123), and
there was no exit for an already-passing part (T0124). In R15 and R16 the
check imported unwritten code (T0132, T0140). In R17 an amend dropped the
data, and a close went through with the lock missing (T0151, T0152). In R18
the refusals formed a closed cycle (T0159, T0160, T0161). In R20 a test was
locked unchecked against the data, and there was no route to fix a locked
test (T0170, T0171, T0174). The R20 fixes have not met a model.

### Workers hit the 31-turn cap, and write the implementation under test-only scopes
Runs: R12, R13, R14, R15, R16, R17, R18, R20
Evidence: R12.md:358, R13.md:154, R14.md:247, R15.md:309, R16.md:195, R16.md:270, R17.md:216, R18.md:204, R20.md:88, R20.md:96
Capped workers per run: R12 5/11, R13 1/2, R14 4/6, R15 4/6, R16 9/12,
R17 15/17, R18 4/4, R20 22/26.
Status: partly fixed. T0136 keeps reports that hit a wall or end in a raw
tool call. T0137 and T0146 stop workers reading `.beagle/` and re-reading the
references. T0142 carries a capped report into the not-done result. T0150
refuses an open with no scope. T0153 checks a report's file claims against
the disk. T0172 stops the scope refusal pointing project work at /tmp.
R20's notes keep the cap as it is (R20.md:96). The loops follow from
unpassable checks, so the known-answers fixes are the real lever.

### The driver resends refused calls or edits files itself
Runs: R12, R13, R14, R15, R18, R19, R20
Evidence: R12.md:349, R13.md:166, R14.md:261, R15.md:150, R18.md:196, R19.md:75, R20.md:96
Status: model. The guards held every time: R12's `sed -i status=done`,
R19's `.beagle/` and `.gitignore` writes, and R20's edit of cases.json were
all refused. Tau's part is to give each refusal an exit the model can take
(T0119, T0133, T0166, T0171).

### The breaker ends most runs
Runs: R11, R12, R13, R14, R15, R16, R18, R19 (8 of 10; R17 and R20 hit the
one-hour cap)
Evidence: R11.md:3, R12.md:3, R13.md:3, R14.md:3, R15.md:3, R16.md:3, R18.md:3, R18.md:184, R19.md:3
Status: working as designed. The breaker is how a run with no exit ends. In
R18 it was reported as a provider error. T0162 made the stop end the run as
aborted, with the breaker's reason, and R19 confirmed that. The breaker
counts are a symptom of the refusal classes above.

### Domain mis-grounding: event as an int, a generic interval tree
Runs: R12, R14, R16, R17, R20
Evidence: R12.md:5, R12.md:267, R14.md:233, R16.md:255, R17.md:5, R20.md:5
Status: open. R12 built a generic CS `IntervalTree` with `event: int`. R14's
driver designed a generic interval tree. R16's founding invented an API the
references do not have. R17's `event(i, e)` returns only `max(e)`. R20's class
has a flat ClockId and an int counter. T0115 makes cases quote the
references, and R15's 32 cases did quote the paper. But no locked test has
yet bound the event tree's shape.

### The worker scope guard misses a write path
Runs: R12, R16
Evidence: R12.md:301, R16.md:233
Status: fixed for the paths seen. T0111 covers `os.system`/subprocess, and
T0143 covers symlinks. As in R01–R10, the guard is a list of known write
paths, not a sandbox.

## Compared with R01–R10

| | R01–R10 | R11–R20 |
|---|---|---|
| Runs founded | 7 of 10 | 9 of 10 (R12–R20 all on the first call) |
| Runs that scored | 2 (R08, R09) | 4 (R12, R14, R17, R20) |
| Best grade | 5/42 | 12/42 |
| Total grade points | 9 | 28 |
| Median minutes | 21.6 | 25.8 |
| Ended by the breaker | 5 | 8 |

In R01–R10 founding and setup were the main killer: five runs (R01, R03, R05,
R07, R10) never got a worker to write ITC code. From R12 on, founding
succeeded on the first call every time. Only R19 lost its run to a founding
leftover. The runs now get to the work and die in the oracle and lock layer
instead: known answers that judge nothing, or locked checks that nothing can
pass. Tree liveness was the R01–R10 deadlock class. It shows up again here as
known-answers refusals with no exit (R12, R14, R18). The driver leaving the
step loop did less harm: the seat and edit guards held in every run, and the
off-loop attempts were refused rather than done.

## What changed in tau

The fix tasks are T0107–T0175 under T0090 (`beagle pursuit tree --under
T0090`). Each run's sha above marks where it cut in.

- **Founding** (R11, R15, R17, R19): T0107 (print mode infers
  `user_delegated`), T0135 (founding milestones are known answers, not
  read-and-design), T0155 (founding docs milestone and split locks), T0165
  (drop a "Found the pursuit" milestone), T0166 (a setup task's `.beagle/`
  refusal says to abandon it), T0167 (fold a design milestone into the next),
  T0175 (test that the fold keeps R17's docs milestone).
- **Checks and refusals the driver can act on** (R13, R14, R15, R16, R17):
  T0118 (refuse a check that cannot run), T0119 (bare-operator checks get a
  move), T0120 (refuse deliverables under references/), T0126 (refuse
  construct-and-call checks), T0133 (the escalation names what the call
  lacks), T0145 (check judge: `uv run python`, pytest in strings), T0147
  (quote check strips a leading label), T0154 (pytest exit 5 explained).
- **Exits for stuck tasks** (R12, R14, R15, R16, R18, R20): T0110 (prove a
  tests-only task by mutating the module its tests import), T0112 (split
  commits passing uncommitted work first), T0124 (done-by route for a part an
  earlier commit made pass), T0134 and T0144 (plan parts split, long titles
  cut), T0141 (cases-first order on plans, waits named), T0160 (data-test
  resend amends an open task), T0173 (open closes without a worker when
  uncommitted work already passes).
- **Known answers and locks** (R12, R14, R15, R16, R17, R18, R20): T0113
  (no new source module before a known-answers test imports it), T0115 (case
  sources quote references/), T0123 (a locked cases test must read the cases
  file), T0125 (locked tests are restored even if the lock store is
  rewritten), T0127 (tests for unguarded clauses of T0118, T0123, T0124),
  T0132 and T0140 (an unpassable known-answers check is refused, before and
  after the test exists), T0151 (an amend keeps the check on the data), T0152
  (close refuses a missing lock), T0156 (R15 cases fixture covers all 32
  cases), T0159 (known-answers open/amend accepts a pass on its own
  uncommitted work), T0161 (no abandon of known answers as a duplicate of a
  superseded task), T0170 (close checks the cases test against the data
  before locking), T0171 (a locked file cannot sit in a task's scope; a
  "Known answers: fix" route), T0174 (only that step may change a locked
  file).
- **Workers** (R12, R15, R16, R17, R20): T0111 (scope guard catches
  `os.system`/subprocess), T0136 (reports survive walls and raw tool calls),
  T0137 (no reading `.beagle/` or re-reading references), T0142 (case-runner
  wording, capped report in the not-done result), T0143 (symlinks out of
  scope), T0146 (read guard and report gaps from audit 7), T0150 (open
  without scope refused; known-answers scope named), T0153 (report path
  claims checked against disk), T0172 (scope refusal no longer points
  project work to /tmp).
- **Harness and run plumbing**: T0091 and T0105 (run checks assert the
  launch facts; R10's Actions name files), T0128 (scored.sh asserts the
  model), T0129 (`_changed_files` dropped a filename's first character),
  T0162 (a breaker stop ends as aborted, not as a provider error).

## Still open

- **Untested by any run:** the R20 fixes T0170–T0175 (cases test checked
  against the data before locking, no locked file in scope plus a
  known-answers fix route, only that route changes a lock, no /tmp pointer,
  close without a worker on an uncommitted pass, the design-fold test). The
  R19 fixes T0165–T0167 ran in R20, but had nothing to act on (R20.md:54).
  Each passed its own check. None has met a 9B model in the shape it fixes.
- **The correctness ceiling is still 12/42.** No run built the event tree.
  trace-canon and trace-causal scored 0/10 each in R12 and R14. A locked
  cases test can still be shallow, as long as it reads `expected` and names
  real cases. Nothing yet checks the implementation's shape against the
  paper.
- **Each known-answers shape was fixed one at a time.** Seven runs found
  seven shapes. There is still no general rule that a locked check must be
  passable by some task in reach, or that every open task has a legal exit.
- **Setup detection is a word list** (R19 missed "found").
- **Scope guarding is a list of write paths**, not a sandbox (R12, R16).
- **Each sha met one model.** The R01–R10 summary's plan to run both models
  on one sha was not followed, so model and tau effects are still mixed.
- **fang ideas 2, 6 and 7** (a stronger driver, the sampling check, one
  nudge for a prose-only turn) are not mentioned in any R11–R20 notes.
- Upstream beagle items from R12 and R13 (`upstream.md`): split leaves
  uncommitted work with no owner, prove's tests-only route is hard to find,
  and the open rehearsal misses git's exit 129. All are waiting on beagle.

## Next

1. **R21 (mimo) and R22 (qwen) on one sha, unchanged.** They are the first
   test of T0170–T0175. Score them on whether the known-answers task locks a
   test that reads the data and that some task can pass, as much as on the
   grader.
2. **Seed the oracle from the paper, not the model.** Lock a few of the
   paper's own worked examples (seed, fork, event on a forked id, join) as
   cases before the model writes any. That puts the event tree's shape into
   the locked test, which no run has had.
3. **A passability rule for locked checks.** Before locking, run the cases
   test against a stub of the imported names, and refuse a test that no
   implementation could pass (absent cases, one attribute used as both
   method and value). That would replace one more per-shape patch.
4. **Give the driver a stronger model: fang idea 2** (fang-ideas.md:70).
   Most breaker stops are the 9B driver resending a refused call.
5. **Check the sampling settings: fang idea 6** (fang-ideas.md:190), before
   blaming identical resends on the model alone.
