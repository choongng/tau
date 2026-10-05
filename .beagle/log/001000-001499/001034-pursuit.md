+++
id = "001034-pursuit"
ordinal = 1034
kind = "pursuit"
timestamp = "2026-10-05T10:38:33+00:00"
summary = "pursuit open T0252: R28 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R28.md holds a trace analysis: each failure class (tau or model) with evidence, an action for tau classes, prompt-independence, the R27 fixes' effect, and an upstream line or ## R28 in upstream.md.
decided by: sh -c 'echo "19b32420aff2b51aaac8598fdbff4c1acd5f32727cac38e98202b87b4ea6ad61  .beagle/checks/T0252/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0252/check.sh'
budget: 40000 tokens
