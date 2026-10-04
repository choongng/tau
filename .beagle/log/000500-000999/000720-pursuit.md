+++
id = "000720-pursuit"
ordinal = 720
kind = "pursuit"
timestamp = "2026-10-04T16:05:36+00:00"
summary = "pursuit open T0169: R20 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R20.md holds a trace analysis and failure classes, each with evidence and an action or disposition, and an upstream line.
decided by: sh -c 'echo "a2afd1069873aa13c6795d26f325d52e80cc3a71df8acf5b04faa14d550501bb  .beagle/checks/T0169/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0169/check.sh'
budget: 80000 tokens
