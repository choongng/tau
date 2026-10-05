+++
id = "001087-pursuit"
ordinal = 1087
kind = "pursuit"
timestamp = "2026-10-05T13:10:14+00:00"
summary = "pursuit open T0263: R30 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R30.md holds a trace analysis: each failure class (tau or model) with evidence, an action for tau classes, prompt-independence, the R29 fixes' effect, and an upstream line or ## R30 in upstream.md.
decided by: sh -c 'echo "03e4b17e32d86d7a591664134c4d570f010068754185c96f81a13b313acafb4a  .beagle/checks/T0263/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0263/check.sh'
budget: 40000 tokens
