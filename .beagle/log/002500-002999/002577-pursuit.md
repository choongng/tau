+++
id = "002577-pursuit"
ordinal = 2577
kind = "pursuit"
timestamp = "2026-10-12T21:54:07+00:00"
summary = "pursuit open T0504: eval: q35 on itc and cobs with line anchors, workers able to run refs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R77 (q35 itc) and R78 (q35 cobs) ran on contract-first beagle at or after fce5dac and tau at or after 0de5e0b7, each graded by its task's grader with an adapter, scorecards made, and eval.md has a row per run with the grade the grader gives and what anchors and worker refs access changed (R75's stopped run noted)
decided by: sh -c 'echo "d5de0a269e6b803453218c94dac37b2c8dd444c95c8f5510901edf5f029b5c0b  .beagle/checks/T0504/T0504.sh" | sha256sum -c --quiet && bash .beagle/checks/T0504/T0504.sh'
budget: 60000 tokens
opened over T0493: krang is idle; T0493 waits on this eval's outcome
