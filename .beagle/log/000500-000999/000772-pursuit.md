+++
id = "000772-pursuit"
ordinal = 772
kind = "pursuit"
timestamp = "2026-10-04T22:55:16+00:00"
summary = "pursuit open T0199: R21 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R21.md holds a trace analysis and failure classes, each with evidence and an action or disposition, and an upstream line.
decided by: sh -c 'echo "753fca333814cae3b28d01b49a8ae44a221239e51794208aa3a8992748b1861b  .beagle/checks/T0199/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0199/check.sh'
budget: 80000 tokens
