+++
id = "002587-pursuit"
ordinal = 2587
kind = "pursuit"
timestamp = "2026-10-12T22:11:52+00:00"
summary = "pursuit open T0506: eval: q35 on itc and cobs with line anchors, task workers able to run refs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R79 (q35 itc) and R80 (q35 cobs) ran on contract-first beagle at or after fce5dac and tau at or after 8633f50a, each graded by its task's grader with an adapter, scorecards made, and eval.md has a row per run with the grade the grader gives and what anchors and worker refs access changed (R75 and R77's stopped runs noted)
decided by: sh -c 'echo "b9da31188986f74cba7b4afea0a7e66ae4c82e3134fe2b1a4dc37d67b7854f90  .beagle/checks/T0506/T0506.sh" | sha256sum -c --quiet && bash .beagle/checks/T0506/T0506.sh'
budget: 60000 tokens
opened over T0493: krang is idle; T0493 waits on this eval's outcome
