+++
id = "001016-pursuit"
ordinal = 1016
kind = "pursuit"
timestamp = "2026-10-05T09:35:24+00:00"
summary = "pursuit open T0248: R27 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R27.md holds a trace analysis: each failure class (tau or model) with evidence, an action for tau classes, prompt-independence, the R26 fixes' effect, and an upstream line or ## R27 in upstream.md.
decided by: sh -c 'echo "66c02c32d3cfe7d310d97b0a5de931a70cdc360abc863ce5e2644df9032f8e91  .beagle/checks/T0248/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0248/check.sh'
budget: 40000 tokens
