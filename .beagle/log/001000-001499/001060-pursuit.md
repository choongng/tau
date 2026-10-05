+++
id = "001060-pursuit"
ordinal = 1060
kind = "pursuit"
timestamp = "2026-10-05T11:37:40+00:00"
summary = "pursuit open T0257: R29 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R29.md holds a trace analysis: each failure class (tau or model) with evidence, an action for tau classes, prompt-independence, the R28 fixes' effect, and an upstream line or ## R29 in upstream.md.
decided by: sh -c 'echo "4f268cd345313500fa0cf15a5316a96771f84e14e288d5270bf2d62aa89a7308  .beagle/checks/T0257/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0257/check.sh'
budget: 40000 tokens
opened over T0258, T0259: the diagnosis is already written and its check passes; closing it records R29 before the fix tasks
