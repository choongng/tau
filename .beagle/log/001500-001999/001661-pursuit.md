+++
id = "001661-pursuit"
ordinal = 1661
kind = "pursuit"
timestamp = "2026-10-10T23:07:03+00:00"
summary = "pursuit prove T0388: WITNESSED — refuses when R44.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9ecef1794ad27351218a538941cf9f48f085eb0375247ace544b089fe775b79f  .beagle/checks/T0388/T0388.sh" | sha256sum -c --quiet && bash .beagle/checks/T0388/T0388.sh'
refutes: refuses when R44.md is absent (proven 2026-10-10T23:06:04+00:00; refused at grep: dev-notes/itc-runs/R44.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/R44.md: No such file or directory
refused with: grep: dev-notes/itc-runs/R44.md: No such file or directory
standing checks red: T0368
