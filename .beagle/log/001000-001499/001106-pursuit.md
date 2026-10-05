+++
id = "001106-pursuit"
ordinal = 1106
kind = "pursuit"
timestamp = "2026-10-05T14:05:41+00:00"
summary = "pursuit open T0267: R31 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R31.md holds a trace analysis: each failure class (tau or model) with evidence, an action for tau classes, prompt-independence, the R30 fixes' effect, and an upstream line or ## R31 in upstream.md.
decided by: sh -c 'echo "8eb8512779a5c09020ccdd75cb17593a0ca64faea9faddba5fe846e713436f3e  .beagle/checks/T0267/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0267/check.sh'
budget: 40000 tokens
