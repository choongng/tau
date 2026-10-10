+++
id = "001602-pursuit"
ordinal = 1602
kind = "pursuit"
timestamp = "2026-10-10T18:44:36+00:00"
summary = "pursuit prove T0374: WITNESSED — refuses when R42.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1c819ecc83ff9086e59611cd7b3f6af41dc10aa1b42f88e07be849a8a95eb0c4  .beagle/checks/T0374/T0374.sh" | sha256sum -c --quiet && bash .beagle/checks/T0374/T0374.sh'
refutes: refuses when R42.md is absent (proven 2026-10-10T18:43:39+00:00; refused at grep: dev-notes/itc-runs/R42.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/R42.md: No such file or directory
refused with: grep: dev-notes/itc-runs/R42.md: No such file or directory
standing checks red: T0368
