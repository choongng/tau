+++
id = "002597-pursuit"
ordinal = 2597
kind = "pursuit"
timestamp = "2026-10-12T22:28:46+00:00"
summary = "pursuit open T0508: eval: q35 on itc and cobs with line anchors, contract refs briefed and uncounted"
metric_command = ""
drains = []
hooks = []
+++

criteria: R81 (q35 itc) and R82 (q35 cobs) ran on contract-first beagle at or after fce5dac and tau at or after eab231f1, each graded by its task's grader with an adapter, scorecards made, and eval.md has a row per run with the grade the grader gives and what anchors and contract refs access changed (R75, R77 and R79's stopped runs noted)
decided by: sh -c 'echo "2bfb637bdd129b2d35d3ec44b9b2896d49a83f0244b862015316c5069401dc57  .beagle/checks/T0508/T0508.sh" | sha256sum -c --quiet && bash .beagle/checks/T0508/T0508.sh'
budget: 60000 tokens
opened over T0493: krang is idle; T0493 waits on this eval's outcome
