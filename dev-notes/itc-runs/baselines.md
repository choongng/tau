# Baselines B01-B03 against the pursuit runs

B01-B03 ran plain `tau -p --no-extensions` on the beagle-free prompts in
itc-harness/prompts/ (the pursuit prompt minus its beagle setup and pursuit-run
lines), with the same model, the same 60-min cap and 8G memory limit as the
pursuit runs, and driver thinking medium (sent). Each is set beside every
pursuit run of the same model and prompt: qwen cobs, mimo itc and gemma cobs.
Rows are picked by `model` and `task` in each run's meta.json, not by run
number. R41 (mimo cobs) ran to the cap and graded 0/44, but has no baseline
pair (no mimo cobs baseline was run), so it is left out.

## Sources and what is missing

- Grade: `passed/total` from runs/<run>/grade.json, as written there.
- Stage: `python3 itc-harness/progress.py` for R21-R40 and B01-B03. progress.py
  stages only R21-R50 (`FIRST, LAST = 21, 50`), so it prints no stage for
  R01-R19. For those rows (marked †) the stage is progress.py's own
  `run_stage` rule, run by importing progress.py on those run directories with
  the harness unchanged. This is not progress.py output. Each of those runs'
  repos (~/itc.rNN) is still on disk, so the known-answers test could run and
  no † stage carries a `?`.
- Wall: (exit.json `end` - meta.json `start`) / 60 for every row. Older
  scorecards lack `wall_minutes_process`, and scorecard `wall_minutes` is
  session time, which can be shorter than process time. For example, R38's
  scorecard says 1.1 min, but its process ran to the cap.
- Ended: scorecard.json `ended` (capped, breaker, finished, error) and exit
  code, with the circumstances paraphrased from the run's own note (B0n.md,
  Rnn.md). Times in that column are the note's own.
- Missing for R01-R19: their meta.json has no `task`, `prompt_file` or
  `driver_thinking` field. They are counted as itc because their
  `launch_command` carries the same ITC prompt text as itc_prompt.txt. Their
  thinking setting is not recorded per run (see Confounds). grade.json,
  meta.json, exit.json and scorecard.json do exist for every row used here.
- Even-numbered R01-R20 runs are qwen itc, and no baseline covers qwen itc or
  any mimo cobs run, so those cells have no baseline and are not rows.

## Comparison

| run | model | prompt | mode | grade | stage | wall (min) | ended | how it ended |
|-----|-------|--------|------|-------|-------|-----------:|-------|--------------|
| B01 | qwen | cobs | baseline | 0/44 | implementation | 35.0 | finished, exit 0 | stopped on its own, claimed all its 18 tests pass; scheme not COBS (0xFF delimiter); nothing committed |
| R22 | qwen | cobs | pursuit | 3/44 | any-pass | 56.0 | error, exit 143 (OOM) | OOM-killed by a looping encoder test run; 1/21 done, cobs/ uncommitted |
| R26 | qwen | cobs | pursuit | 0/44 | founded | 34.0 | breaker, exit 0 | breaker at 33.9 min after 8 refusals (T0011 deadlock); 0/14 done, no implementation |
| R30 | qwen | cobs | pursuit | 3/44 | any-pass | 60.0 | capped, exit 124 | capped during a pre-open check; 1/7 done, cobs.py uncommitted |
| R34 | qwen | cobs | pursuit | 7/44 | any-pass | 60.0 | capped, exit 124 | capped with workers W11/W12 running; 1/12 done, cobs.py and test uncommitted |
| R37 | qwen | cobs | pursuit | 0/44 | founded | 20.2 | finished, exit 0 | stopped after the third stop used up the stop-gate follow-ups; 0 done, tests uncommitted |
| B02 | mimo | itc | baseline | 5/42 | any-pass | 60.0 | capped, exit 124 | killed at the cap mid-`pytest -x` loop; real id/event trees, 18 cases die on anonymous fork; nothing committed |
| R01 | mimo | itc | pursuit | 0/42 | founded † | 60.0 | capped, exit 124 | capped while the driver hand-derived cases after both workers were killed; nothing in ~/itc |
| R03 | mimo | itc | pursuit | 0/42 | none † | 2.9 | breaker, exit 1 | breaker at 2.9 min after repeated refused pursuit_found calls; never founded, no code |
| R05 | mimo | itc | pursuit | 0/42 | none † | 0.3 | finished, exit 0 | stopped at 18 s asking the user to confirm criteria in print mode; not founded |
| R07 | mimo | itc | pursuit | 0/42 | none † | 0.7 | breaker, exit 1 | breaker at 44 s after 8 refusals of a setup-only milestone; never founded, no code |
| R09 | mimo | itc | pursuit | 4/42 | any-pass † | 40.2 | breaker, exit 1 | breaker at 40.2 min (surfaced as a provider stream error); founded, 2/10 tasks done |
| R11 | mimo | itc | pursuit | 0/42 | none † | 3.4 | breaker, exit 1 | breaker at 3.4 min after 8 refused calls; never founded, nothing built |
| R13 | mimo | itc | pursuit | 0/42 | founded † | 11.4 | breaker, exit 1 | breaker at 11.3 min after resending a refused check; founded, 0/2 done |
| R15 | mimo | itc | pursuit | 0/42 | founded † | 36.0 | breaker, exit 1 | breaker at 36.0 min after resent pursuit_step calls; 0/2 done, test files uncommitted |
| R17 | mimo | itc | pursuit | 6/42 | any-pass † | 60.0 | capped, exit 124 | capped mid-worker; 1/10 done (T0008 committed), T0009 rework uncommitted |
| R19 | mimo | itc | pursuit | 0/42 | founded † | 2.8 | breaker, exit 0 | breaker at 2.7 min, ended aborted; founded, no task opened |
| R21 | mimo | itc | pursuit | 0/42 | founded | 60.0 | capped, exit 124 | capped with T0005 open; 0/7 done, tests uncommitted, no implementation |
| R25 | mimo | itc | pursuit | 0/42 | founded | 60.0 | capped, exit 124 | capped, cap killed worker W13; 0/10 done, tests uncommitted, no implementation |
| R29 | mimo | itc | pursuit | 0/42 | founded | 7.4 | breaker, exit 0 | breaker at 7.4 min after 8 refused calls; 0/7 done, no implementation |
| R33 | mimo | itc | pursuit | 0/42 | founded | 40.3 | breaker, exit 0 | breaker at 40.2 min after 8 refused calls; 1 done (reading notes), no implementation |
| R38 | mimo | itc | pursuit | 0/42 | none | 60.0 | capped, exit 124 | capped while a pre-founding sub-agent call never returned; not founded, nothing written |
| B03 | gemma | cobs | baseline | 0/44 | implementation | 6.5 | finished, exit 0 | one unrun 66-line draft, then a one-line "done" report with 53.5 min unused; scheme not COBS; nothing committed |
| R39 | gemma | cobs | pursuit | 4/44 | any-pass | 60.0 | capped, exit 124 | capped mid-worker on T0004; T0002 (known answers) done, cobs.py and two tests uncommitted |

No row reached `complete`. Every baseline row has 0 commits. Pursuit rows
commit the pursuit's own records (scorecard `commits` 0-3), and in no row is
the graded implementation a committed, passing result.

## Confounds

- Thinking. Bane's 9B models ran with driver thinking off, whatever the
  level, because the catalog lacked `thinking_parameter`. This was fixed on
  2026-10-08. R21-R35's meta.json has no `driver_thinking`, and R01-R20 record
  no thinking setting at all, so those rows are taken as thinking-off on the
  strength of that catalog finding, not a per-run record. R36 onward, and B01-B03, record
  `driver_thinking: {level: medium, sent: true}`. In every pursuit run in this
  table, beagle workers passed `--thinking off`, so the code was written
  thinking-off. In a baseline, the thinking driver writes it. From R41 on,
  launch.sh dispatches workers at the driver's thinking level (T0362,
  itc-harness eaa83cb), so R41-R50's workers write code thinking-on. In this table, only R37, R38 and
  R39 match their baseline's driver thinking.
- tau version. Pursuit rows span many tau commits, with fixes between runs.
  Each baseline ran on one commit (B01 1fad2d17, B02 ad8fbd7, B03 41a1fa2).
- n = 1 per baseline. One run per model cannot separate a model's mean from
  its spread, and the pursuit rows show a wide spread (mimo itc ranges from
  0.3 to 60 min and from 0/42 to 6/42).

## What it implies

Per model. The question is whether the pursuit workflow or the model is the
bottleneck.

- mimo itc. With no structure, B02 reached 5/42, against a best of 6/42 over
  15 pursuit runs (R17). Only 2 of those 15 passed any case (R09, R17), and 4
  stopped within 3.4 min at stage none (R03, R05, R07, R11). It read the
  references unprompted and spent the hour writing and testing, which the
  pursuit's known-answers step exists to force. For mimo, the pursuit's added
  structure has not bought grade. Mimo's pursuit rows end mostly in the workflow
  itself: 9 of 15 by breaker stop, often after 8 refused calls; 5 never
  founded; and of the 5 capped runs, only R17 passed a case, while R01, R21,
  R25 and R38 wrote no implementation. Here the workflow is the bottleneck more than the model.
  The ceiling near 5-6/42 that both reach suggests mimo's own ITC capability
  also caps it well short of complete.
- qwen cobs. B01 stayed at stage implementation (0/44). It wrote a
  self-consistent scheme that is not COBS, never consulted the reference, and
  rewrote its tests until they passed. Three of 5 pursuit runs passed some
  case (R22 3/44, R30 3/44, R34 7/44). For qwen, the pursuit adds value: the
  known-answers step aims it at the real spec, which B01 never had. Even so, a
  best of 7/44 says model capability, or the thinking-off workers, bounds what
  it can reach.
- gemma cobs. B03 drafted 66 lines from memory once, never ran them, and
  stopped at 6.5 min. R39, under the pursuit, founded, closed known-answers
  (done and witnessed), ran 9 workers and kept working until the cap,
  reaching 4/44. For gemma, the workflow is what kept the model working, and
  without it the model quits. This is the one cell where the pursuit clearly
  beats the baseline. It is still one run against one.

Across models. The baselines do not say the pursuit is uniformly a cost or a
gain. It turns gemma's one-shot finish into an hour of work and points qwen at
the spec, while for mimo it mostly absorbs the hour. In every cell, the grade
ceiling (4-7 of 42-44) sits far below complete, with or without the pursuit.
The thinking confound cuts against the pursuit: its workers wrote code
thinking-off through R40, and its best mimo and qwen rows (R17, R34) predate the
thinking fix, so by the catalog finding their drivers ran thinking-off too.

## Recommendation for R41-R50

For the owner to decide. This is a recommendation, not a decision.

- Keep the pursuit for gemma and qwen. It is what kept gemma at work (R39 vs
  B03) and what aimed qwen at the reference (R22/R30/R34 vs B01). Dropping it
  for them would likely lose what grade they have.
- For mimo, consider spending some of the remaining runs on cutting pursuit
  overhead before driver structure. Look at what the B02 hour did that the
  pursuit hours did not: references read and then a steady write/test loop.
  Then target the early breaker stops and stalled steps that dominate mimo's
  rows. Treat B02's 5/42 as the bar a mimo pursuit run should clear.
- Read R41-R50 with the thinking change in mind. They are the first pursuit
  runs whose workers think (T0362), so a jump in grade from R41 on mixes worker
  thinking with every other fix. To separate the two, one run for one model
  could dispatch its workers thinking-off again. launch.sh sets worker thinking
  from the driver's level today, so that needs an option there.
  Otherwise a gain from thinking would be credited to the workflow.
- Track stage alongside grade for R41-R50, since no cell has completed. Rerun
  one baseline later in the series (same prompt, newer tau) to see whether
  tau's fixes move plain tau as well, which would test whether a gain is the
  pursuit's or the tool's.
