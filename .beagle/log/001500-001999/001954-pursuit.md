+++
id = "001954-pursuit"
ordinal = 1954
kind = "pursuit"
timestamp = "2026-10-12T04:40:31+00:00"
summary = "pursuit prove T0450: WITNESSED — refuses when deferred.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "597f978cf487136265e9a2f439860b8c180ea72701f2ccb33ce05a09a983ece2  .beagle/checks/T0450/T0450.sh" | sha256sum -c --quiet && bash .beagle/checks/T0450/T0450.sh'
refutes: refuses when deferred.md is absent (proven 2026-10-12T04:39:32+00:00; predates the task: 83d76d11 wrote deferred.md as this task's work while T0452 being open refused T0450's open; the file is wholly this task's; refused at grep: dev-notes/itc-runs/deferred.md: No such file or directory)
refused after 0s of a 0s check at: grep: dev-notes/itc-runs/deferred.md: No such file or directory
refused with: grep: dev-notes/itc-runs/deferred.md: No such file or directory
standing checks red: T0335, T0336, T0360, T0368, T0386
