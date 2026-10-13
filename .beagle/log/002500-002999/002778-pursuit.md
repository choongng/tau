+++
id = "002778-pursuit"
ordinal = 2778
kind = "pursuit"
timestamp = "2026-10-13T20:28:12+00:00"
summary = "pursuit open T0534: B07: plain-tau q35 baseline on the bare-goal prompt"
metric_command = ""
drains = []
hooks = []
+++

criteria: B07 (plain tau, q35, bare-goal semver prompt) has run to its end, is graded by grade_semver.py over an adapter for the code it left (75/76), and eval.md carries its table row and a section saying what the bare-goal pursuit runs must beat
decided by: sh -c 'echo "c5ad65f7e68e1eb94a505621aa5474ba9a704196590f5926c7a7c8896bb4eea9  .beagle/checks/T0534/T0534.sh" | sha256sum -c --quiet && bash .beagle/checks/T0534/T0534.sh'
budget: 40000 tokens
