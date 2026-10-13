+++
id = "002714-pursuit"
ordinal = 2714
kind = "pursuit"
timestamp = "2026-10-13T16:52:49+00:00"
summary = "pursuit prove T0530: WITNESSED — refuses when contract.py's `if not _is_json(text): tests.append(text)` is put back as `if True: tests.append(text)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6914e4ab5e3ffce300286c93c4ff9aee42b0ee2b0673caca2b09982fa54905f5  .beagle/checks/T0530/T0530.sh" | sha256sum -c --quiet && bash .beagle/checks/T0530/T0530.sh'
refutes: refuses when contract.py's `if not _is_json(text): tests.append(text)` is put back as `if True: tests.append(text)` (proven 2026-10-13T16:51:50+00:00; refused at 1 failed, 2 passed, 54 deselected in 0.14s)
refused after 0s of a 0s check at: 1 failed, 2 passed, 54 deselected in 0.14s
refused with: 1 failed, 2 passed, 54 deselected in 0.14s
replaces: refuses when contract.py's `if not _is_json(text): tests.append(text)` is put back as `if True: tests.append(text)` (proven 2026-10-13T16:50:47+00:00; refused at 1 failed, 2 passed, 54 deselected in 0.18s)
standing checks red: T0211, T0492, T0508, T0525, T0526, T0502, T0503, T0505, T0507, T0509, T0512, T0513, T0519, T0524
