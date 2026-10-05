+++
id = "001181-pursuit"
ordinal = 1181
kind = "pursuit"
timestamp = "2026-10-05T18:50:37+00:00"
summary = "pursuit open T0282: R34 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R34.md holds a trace analysis: failure classes tagged [tau]/[model] each with evidence, action, tests and prompt-independence; R33 fixes' effect; upstream line.
decided by: sh -c 'echo "7a2934acddcfba47454129af43938f3502b93e6d7d4b846c75f3d938483c631a  .beagle/checks/T0282/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0282/check.sh'
budget: 40000 tokens
