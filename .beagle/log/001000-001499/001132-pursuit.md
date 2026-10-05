+++
id = "001132-pursuit"
ordinal = 1132
kind = "pursuit"
timestamp = "2026-10-05T15:34:41+00:00"
summary = "pursuit open T0272: R32 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R32.md holds a trace analysis: failure classes tagged [tau]/[model] each with evidence, action, tests and prompt-independence; R31 fixes' effect; upstream line.
decided by: sh -c 'echo "03771a398341c04c50a9c4d2867caa267d3984270a0e651ded8c8b0a1a9f1f25  .beagle/checks/T0272/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0272/check.sh'
budget: 40000 tokens
