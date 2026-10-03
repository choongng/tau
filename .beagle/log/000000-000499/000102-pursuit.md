+++
id = "000102-pursuit"
ordinal = 102
kind = "pursuit"
timestamp = "2026-10-03T14:26:07+00:00"
summary = "pursuit prove T0038: WITNESSED — refuses when R04.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0038/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0038/diagnosed.sh R04'
refutes: refuses when R04.md is absent (proven 2026-10-03T14:25:55+00:00; refused at grep: dev-notes/itc-runs/R04.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/R04.md: No such file or directory
refused with: grep: dev-notes/itc-runs/R04.md: No such file or directory
