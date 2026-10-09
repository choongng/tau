+++
id = "001349-pursuit"
ordinal = 1349
kind = "pursuit"
timestamp = "2026-10-09T22:59:02+00:00"
summary = "pursuit prove T0321: WITNESSED — refuses when R37.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b470cb633d6665b3edc99da5f6b1a74dc8173a3721985ad3c7c66326879f66b8  .beagle/checks/T0321/T0321.sh" | sha256sum -c --quiet && bash .beagle/checks/T0321/T0321.sh'
refutes: refuses when R37.md is absent (proven 2026-10-09T22:58:05+00:00; refused at grep: dev-notes/itc-runs/R37.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/R37.md: No such file or directory
refused with: grep: dev-notes/itc-runs/R37.md: No such file or directory
