+++
id = "000396-pursuit"
ordinal = 396
kind = "pursuit"
timestamp = "2026-10-04T00:37:34+00:00"
summary = "pursuit open T0105: R10.md tau Actions name the file they change"
metric_command = ""
drains = []
hooks = []
+++

criteria: Each [tau] class Action in dev-notes/itc-runs/R10.md names examples/extensions/beagle.py, the file its functions live in; no other content changes. v2/diagnosed.sh R10 passes.
decided by: sh -c 'echo "e9a246579f06a0c1460c2af996976881e26f231e83b6f594d13c4ea558b12556  .beagle/checks/T0105/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0105/check.sh'
budget: 3000 tokens
