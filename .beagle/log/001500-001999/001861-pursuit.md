+++
id = "001861-pursuit"
ordinal = 1861
kind = "pursuit"
timestamp = "2026-10-12T00:41:08+00:00"
summary = "pursuit open T0446: R51 fix: a killed worker's last words reach the driver and a new route"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a worker is killed (wall or step-budget), the step result the driver reads shows the killed worker's last words (a short trimmed tail) beside its changed files, and when the driver takes a new route the kept progress is carried to the sibling's first brief, given once. q35 R51. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "06d0b702cc0d5a57b21d9826b10792eb4057c7fd542655f58847db7e3e75c018  .beagle/checks/T0446/T0446.sh" | sha256sum -c --quiet && bash .beagle/checks/T0446/T0446.sh'
budget: 150000 tokens
