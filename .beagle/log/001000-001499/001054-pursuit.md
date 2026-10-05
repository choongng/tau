+++
id = "001054-pursuit"
ordinal = 1054
kind = "pursuit"
timestamp = "2026-10-05T11:18:27+00:00"
summary = "pursuit open T0256: R29 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R29 ran mimo on itc_prompt.txt from a clean ~/itc under the 1h cap with tau at HEAD; dev-notes/itc-runs/R29.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "b8b1e645830904961452a7483620fd9d00c467dc5d3f803fbd43e57cb519a13b  .beagle/checks/T0256/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0256/check.sh'
budget: 40000 tokens
