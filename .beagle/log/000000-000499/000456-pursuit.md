+++
id = "000456-pursuit"
ordinal = 456
kind = "pursuit"
timestamp = "2026-10-04T02:28:50+00:00"
summary = "pursuit open T0117: R13 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R13.md diagnosed: each failure class has Evidence and an Action naming a file or a Disposition; upstream recorded or 'upstream: none'
decided by: sh -c 'echo "b2eb80caa7f9e407a8d125ed32797471421003b5888ac9498db4d48ba3eeb06f  .beagle/checks/T0117/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0117/check.sh'
budget: 80000 tokens
