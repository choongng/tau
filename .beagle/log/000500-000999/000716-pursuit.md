+++
id = "000716-pursuit"
ordinal = 716
kind = "pursuit"
timestamp = "2026-10-04T15:03:34+00:00"
summary = "pursuit open T0168: R20 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R20 (qwen) ran on itc_prompt.txt at the current tau, and dev-notes/itc-runs/R20.md records its grade and scorecard.
decided by: sh -c 'echo "91161823701ff5b94c8ceaefe4e38cd664ca4f7d2775dec6ef886738df02c44e  .beagle/checks/T0168/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0168/check.sh'
budget: 40000 tokens
