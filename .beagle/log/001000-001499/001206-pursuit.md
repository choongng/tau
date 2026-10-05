+++
id = "001206-pursuit"
ordinal = 1206
kind = "pursuit"
timestamp = "2026-10-05T20:36:26+00:00"
summary = "pursuit open T0287: R35 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R35.md holds a trace analysis: failure classes tagged [tau]/[model] each with evidence, action, tests and prompt-independence; R34 fixes' effect; upstream line.
decided by: sh -c 'echo "a0fa42eca49daf67f28276c033050b60386021dc3696c60cd776ee6f2a6830e8  .beagle/checks/T0287/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0287/check.sh'
budget: 90000 tokens
