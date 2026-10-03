# ITC runs R01–R10: summary

Ten unattended runs on 2026-10-03, alternating mimo-v2.6-9b-q4 (odd runs) and
qwen3.5-9b-q4-mtp-thinking-coding (even runs). Each one used tau + beagle on
`~/tautest/itc_prompt.txt` (interval tree clocks in Python). After each run,
tau was fixed from the trace. Each run's notes are in `RNN.md`. The harness is
described in `harness.md`, beagle-side items are in `upstream.md`, and the
ideas from fang are in `fang-ideas.md`.

## Headline lessons

1. **Founding is where most runs died.** Five runs (R03, R05, R07, R10, and in
   effect R01) never got a worker to write ITC code. Every one of them stalled
   on founding or setup: a setup milestone, a long title, a confirmation with
   no user, or beagle's own config. Only R08 (5/42) and R09 (4/42) scored at
   all. A 9B model needs founding to *succeed for it*. Tau should repair what
   it can and drop what it cannot, and never refuse with a fix the model has
   to make itself.
2. **A 9B model cannot edit its own call in answer to a refusal.** It resends
   the same arguments (R03 13 times, R07 11 times, R10 to the breaker). It
   follows the first instruction in a refusal and rewrites the field that was
   not refused. Refusals work only when they carry one route, and that route
   has to come first. Repairs work better than refusals.
3. **Once the driver is stuck or compacted, it leaves the step loop.** It
   dispatches by hand (R01), debugs worker code (R04, R08), hand-edits
   `.beagle/` (R08, R10), or follows a summary into bash (R10). Advice in a
   prompt does not hold it. Only gates on the driver's seat do (T0022, T0040,
   T0082, T0084).
4. **Every hole in the task tree's liveness becomes a deadlock, and each run
   found a new one.** We saw an unprovable task re-stepped forever (R02), a
   cases task with no data-only proof (R04), a cycle through a superseded
   heir (R06), a wait on a stalled container (R08), and a part with nothing
   left to do (R09). Patching each shape as it appeared worked, but only one
   shape at a time. Tau still lacks a general rule that every open task
   always has a legal exit.
5. **The oracle must be kept apart from the code by structure, not by
   advice.** Given the chance, the model writes its known answers and its
   implementation in the same step, or fits one to the other (R02, R04, R08,
   R09). Cases-first held only after it became a refusal (T0039, T0059), and
   R09 found a gap even in that (directory scopes).

## Runs

Minutes are wall clock from `meta.json` start to `exit.json` end. The sha is
the tau commit the run used.

| Run | Model | tau sha | Min | Grader | How it ended |
|---|---|---|---|---|---|
| R01 | mimo | 6e9bee5 | 60.0 | 0/42 | Wall-clock cap. Driver dispatched instead of stepping, and workers ran to the kill with no code |
| R02 | qwen | 0f6737c | 27.8 | 0/42 | Driver stopped "complete" with the root stalled. Built an interval *tree*, not ITC |
| R03 | mimo | 275e7ef | 2.9 | 0/42 | Breaker stop. The same `pursuit_found` with a setup milestone, resent 13 times; never founded |
| R04 | qwen | e8cd795 | 60.0 | 0/42 | Wall-clock cap on the first (cases) task, which could not prove |
| R05 | mimo | 7fa5075 | 0.3 | 0/42 | Founding asked an absent user to confirm (print mode), and the model stopped |
| R06 | qwen | 14eeb64 | 15.4 | 0/42 | Deadlocked in a hard-depend cycle through a superseded heir; looping stops |
| R07 | mimo | 786b807 | 0.7 | 0/42 | Breaker stop. The only milestone was setup, and founding refused outright |
| R08 | qwen | 8fb14ac | 59.6 | 5/42 | Breaker stop after a deadlock on a stalled container; one implementation task closed |
| R09 | mimo | a27605a | 40.2 | 4/42 | Breaker stop while the driver chased a stale worker report; library committed under T0009 |
| R10 | qwen | 6411e7a | 2.5 | 0/42 | Breaker stop. A missed setup milestone, then 53 calls on beagle config, compaction, then bash |

The model made no visible difference to the score. Both models scored once
the tree let workers run (R08 qwen, R09 mimo). mimo was more brittle at
founding (R03, R05, R07), where it followed the first instruction of a
refusal. qwen got further and then deadlocked.

## Recurring failure classes

Only classes seen in two or more runs are listed. Evidence is `RNN.md:line`,
pointing at the failure-class heading in that run's notes.

### Founding or setup refuses, and the 9B cannot repair its own call
Runs: R01, R03, R05, R07, R10
Evidence: R01.md:168, R03.md:91, R05.md:51, R07.md:54, R10.md:113, R10.md:165
Status: partly fixed — T0024 (c862b98), T0033 (85b38a3), T0044 (b06d117), T0054 (1534601), T0072 (bba8543), T0081 (ee89795, 4322a28), T0083 (3a34acc), T0088 (44ede11). After four fixes, R10 still slipped through with a reworded setup title. T0081, T0083 and T0088 have not run.

### Identical retries after a refusal, ended by the breaker
Runs: R03, R06, R07, R08, R10
Evidence: R03.md:125, R03.md:103, R06.md:272, R07.md:58, R07.md:62, R08.md:215, R10.md:219
Status: model — tau's part is to make the first retry unnecessary. The breaker quotes the earlier result (T0033, 85b38a3). The underlying causes are fixed class by class, but a refused call still has nowhere to go except another identical call.

### Driver leaves the step loop and does the work itself
Runs: R01, R04, R08, R09, R10
Evidence: R01.md:102, R01.md:141, R04.md:191, R08.md:215, R09.md:276, R10.md:139, R10.md:185
Status: partly fixed — T0022 (e9d4dc4), T0040 (0315ebe), T0047 (06e39a1), T0082 (4971c5a), T0084 (7a4a705). R10 showed it again after T0040. The driver seat gate and the post-compaction note are untested.

### The task tree reaches a state with no legal exit
Runs: R02, R04, R06, R08, R09
Evidence: R02.md:212, R04.md:130, R04.md:153, R06.md:175, R06.md:226, R08.md:131, R08.md:150, R09.md:160
Status: partly fixed — T0028 (4c27637), T0039 (8c4edc1), T0040 (0315ebe), T0047 (06e39a1), T0048 (51ccd9b), T0057 (3b4464f), T0058 (16e655b), T0065 (b88c231), T0066 (ada0271), T0078 (4f96b3f). Every run that got past founding hit a different shape.

### Oracle written with the code, or fitted to it
Runs: R02, R04, R08, R09
Evidence: R02.md:326, R04.md:178, R04.md:235, R08.md:162, R09.md:134, R09.md:197, R09.md:266
Status: partly fixed — T0039 (8c4edc1), T0059 (d695e76), T0067 (ddd8116), T0068 (c8d6342), T0074 (3eceac9), T0087 (a355a30). R09 got around T0059 through a directory scope. The directory walk (T0067, T0089) has not run.

### Domain not grounded in the references: ITC becomes "interval tree"
Runs: R01, R02, R03, R06, R08, R09
Evidence: R01.md:130, R02.md:193, R03.md:111, R06.md:279, R08.md:177, R09.md:217
Status: partly fixed — T0027 (54853a4, references fetched at founding and carried in briefs), T0034 (b5d131a, extracts before `pursuit_found`), T0060 (7b0656f), T0070 (779903b, cut reads name lines and next offset), T0071 (64aabe2, fetch retry). No later grader line shows the interval-tree mix-up again. But reading the paper still cost workers most of their turns in R09, and T0070/T0071 have not reached a worker.

### Workers run out of turns and hand back nothing usable
Runs: R01, R02, R04, R06, R08, R09
Evidence: R01.md:116, R02.md:306, R04.md:167, R04.md:246, R06.md:279, R08.md:223, R09.md:254
Status: partly fixed — T0023 (2f7f9f3, turn cap and thinking off: fang idea 1 and 3), T0029 (e6e0b9a, report fallback), T0041 (5c6dd93, kept off beagle), T0073 (2e19840, breaker-stopped worker reports its last refused call). The wall-clock kill is gone, but raw tool-call reports and false "fixed" claims are still model behaviour.

### Workers write outside their scope
Runs: R02, R04, R06, R08, R09
Evidence: R02.md:283, R04.md:201, R06.md:246, R08.md:192, R09.md:197
Status: partly fixed — T0029 (e6e0b9a), T0041 (5c6dd93, one-liners), T0049 (d5a3aef, touch/mkdir), T0061 (8de44dd, out-of-scope imports), T0067 (ddd8116), T0089 (ef5f6f5). Each run found a new write path, which shows the guard is a list of known paths and not a boundary.

### Weak checks and unguarded done/abandon/stop
Runs: R02, R04, R08
Evidence: R02.md:231, R02.md:246, R02.md:296, R04.md:211, R04.md:228, R08.md:231
Status: partly fixed — T0028 (4c27637, stop and abandon gated), T0041 (5c6dd93, import-only checks and root abandon refused), T0061 (8de44dd). No run after R04 showed a bad check closing the root. R08's driver still wrote checks that did not fit the artifact (model).

### Worker brief carries beagle habits that the worker guards refuse
Runs: R02, R06
Evidence: R02.md:264, R06.md:237
Status: fixed — T0029 (e6e0b9a), T0049 (d5a3aef). Workers ran in R08 and R09 without it showing up.

## What changed in tau

The commits run from 52f615e (fang survey, before R01) to 44ede11 (audit 4,
after R10). Each run's sha above marks where it cut in.

- **Founding and setup** (R01, R03, R05, R07, R08, R10): c862b98 (T0024),
  85b38a3 (T0033), b06d117 (T0044), 1534601 (T0054), fc7fb73 (T0062, commit
  beagle init's files), bba8543 (T0072), a277a0a and d468e9a (T0077, T0086,
  unstaging after a failed setup commit), ee89795–4322a28 (T0081), 3a34acc
  (T0083), 44ede11 (T0088). The direction moved from refusing to repairing:
  drop setup milestones, seed milestones from the criteria, drop re-run-only
  milestones.
- **The driver's seat** (R01, R04, R09, R10): e9d4dc4 (T0022), 0315ebe
  (T0040), 06e39a1 (T0047), 760f779 (T0069, superseded reports marked),
  4971c5a (T0082), 7a4a705 (T0084), 2d67c51 (T0085).
- **Tree liveness** (R02, R04, R06, R08, R09): 4c27637 (T0028), 8c4edc1
  (T0039), 0315ebe (T0040 escalation), 06e39a1–51ccd9b (T0047, T0048),
  3b4464f–16e655b (T0057, T0058), b88c231–ada0271 (T0065, T0066), 4f96b3f
  (T0078).
- **Oracle and cases-first** (R04, R08, R09): 8c4edc1 (T0039), d695e76
  (T0059), ddd8116–c8d6342 (T0067, T0068), 3eceac9 (T0074), a355a30 (T0087),
  ef5f6f5 (T0089).
- **Workers** (R01, R02, R04, R06, R09): 2f7f9f3 and cc36d21 (T0023, T0036),
  e6e0b9a (T0029), 5c6dd93 (T0041), d5a3aef (T0049), 2e19840 (T0073).
- **References and reading** (R02, R03, R08, R09): 54853a4 (T0027), b5d131a
  (T0034), 7b0656f (T0060), 779903b (T0070), 64aabe2 (T0071).
- **Harness** (not tau): 563efac (T0019), 0f6737c, f635120 (T0050), 0c82738.

## Still open

- **Untested by any run:** the R10 fixes T0081–T0084 (setup detector, abandon
  of a setup milestone, driver seat gate, post-compaction note), and the
  audit-4 fixes T0085–T0089 (stale-report detector, setup-commit unstage,
  implementation-under-tests lead, directory walk skips caches, re-run-only
  milestones dropped). Each passed its own check. None has met a 9B model.
- **Setup detection is a word list.** R10's "Setup beagle pursuit
  infrastructure - …" got past four earlier fixes. The next rewording may too.
  T0083's abandon route is the fallback.
- **The driver after compaction.** Two compactions (R06) and one (R08, R10)
  each turned into off-loop behaviour. T0084 repeats the last step result.
  Whether a 9B follows it is unknown.
- **No general liveness invariant.** Each deadlock shape is handled
  separately (see the class above).
- **Scope guarding is a list of write paths** (python one-liner, touch/mkdir,
  directory scopes), not a sandbox.
- **Correctness ceiling.** The best run passed 5 of 42 grader cases. R08 and
  R09 got the seed and fork of the seed right, then failed on nested ids
  (join in R08; event, split and norm in R09). Nothing in tau yet checks the
  code against the paper's semantics,
  beyond the cases the model writes itself.
- Upstream beagle items (`upstream.md`), such as `abandon --duplicate-of` and
  `contain run`'s venv leak, are waiting on beagle.
- R10 harness: `uncommitted_files` hides the driver's config edits, and guard
  blocks are counted as breaker refusals (R10.md:226).

## Next

1. **R11 (mimo) on HEAD, unchanged.** It is the first run of T0081–T0089. It
   will show whether founding now gets mimo past setup, and whether the seat
   gate holds the driver. Score it on founding and on the first close as
   much as on the grader.
2. **R12 (qwen) on the same sha** before fixing anything else, if R11 gets
   past founding. That way one sha meets both models. So far every sha has
   met only one.
3. **Give the driver a stronger model: fang idea 2** (fang-ideas.md:70).
   Lessons 2–4 are all failures of the 9B as the *driver*. Workers produced
   the only code that scored. A run with a stronger driver and 9B workers
   would show how far tau's worker structure alone carries.
4. **Turn a prose-only turn into one nudge: fang idea 7**
   (fang-ideas.md:210). Also, **answer malformed tool-call JSON with the
   model's own string: idea 4** (fang-ideas.md:129). Tau already wraps bad
   arguments as `_raw_arguments`. What tau returns for them is unverified
   (fang-ideas.md:250).
5. **Check the sampling settings: fang idea 6** (fang-ideas.md:190). Find out
   whether the bane preset sets a presence penalty before blaming identical
   retries on the model alone.
6. **A liveness rule for the tree.** Every open task should always have at
   least one route the driver can call, and a test should walk R02/R04/R06/
   R08/R09's tree shapes against it. That would replace one more per-shape
   patch.
7. **Seed the oracle from the paper, not the model.** A cases task that
   starts from a few known answers lifted from the references would raise
   the correctness ceiling. Without that, the model is grading itself.
