+++
id = "001629-pursuit"
ordinal = 1629
kind = "pursuit"
timestamp = "2026-10-10T20:23:41+00:00"
summary = "pursuit prove T0381: WITNESSED — refuses when R43.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f532aac342fa64e6fc0f879c0090b3c8444ff10395816c9c45862febb3d30910  .beagle/checks/T0381/T0381.sh" | sha256sum -c --quiet && bash .beagle/checks/T0381/T0381.sh'
refutes: refuses when R43.md is absent (proven 2026-10-10T20:22:45+00:00; refused at grep: dev-notes/itc-runs/R43.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/R43.md: No such file or directory
refused with: grep: dev-notes/itc-runs/R43.md: No such file or directory
standing checks red: T0368
