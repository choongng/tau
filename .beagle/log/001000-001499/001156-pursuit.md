+++
id = "001156-pursuit"
ordinal = 1156
kind = "pursuit"
timestamp = "2026-10-05T17:14:27+00:00"
summary = "pursuit open T0277: R33 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R33.md holds a trace analysis: failure classes tagged [tau]/[model] each with evidence, action, tests and prompt-independence; R32 fixes' effect; upstream line.
decided by: sh -c 'echo "b10f2c28c797996ef2379c7972c06ab2ac4fa69dac6236c87c2227caf7dd900d  .beagle/checks/T0277/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0277/check.sh'
budget: 40000 tokens
