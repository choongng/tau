+++
id = "000402-pursuit"
ordinal = 402
kind = "pursuit"
timestamp = "2026-10-04T00:38:46+00:00"
summary = "pursuit open T0103: R11 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R11 launched via ~/tautest/itc-harness/launch.sh R11 mimo on committed tau HEAD (clean tree), unchanged itc_prompt.txt, 1h cap, model explicit; after exit: adapter.py written for whatever ITC code exists, grade.json and scorecard.{txt,json} made, dev-notes/itc-runs/R11.md with header, grader line and Scorecard block matching them. v2/scored.sh R11 passes.
decided by: sh -c 'echo "572093f2321cbfc5107b6c8749ef1a1c682895c7e93cadd7a9f0792d8ddabc28  .beagle/checks/T0103/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0103/check.sh'
budget: 40000 tokens
