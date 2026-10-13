+++
id = "002603-pursuit"
ordinal = 2603
kind = "pursuit"
timestamp = "2026-10-13T00:42:12+00:00"
summary = "pursuit prove T0513: WITNESSED — refuses when beagle.py's `wrote = wrote or (bool(command) and _bash_find(…` is put back as `wrote = wrote`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "888dca7d3fefe7ea904e65b07699f76e6228aa3cc4b45b3b52fef734fb9741ed  .beagle/checks/T0513/T0513.sh" | sha256sum -c --quiet && bash .beagle/checks/T0513/T0513.sh'
refutes: refuses when beagle.py's `wrote = wrote or (bool(command) and _bash_find(…` is put back as `wrote = wrote` (proven 2026-10-13T00:41:14+00:00; refused at 1 failed, 2 passed, 832 deselected in 1.14s)
refused after 2s of a 2s check at: 1 failed, 2 passed, 832 deselected in 1.14s
refused with: 1 failed, 2 passed, 832 deselected in 1.14s
