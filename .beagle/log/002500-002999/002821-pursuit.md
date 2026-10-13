+++
id = "002821-pursuit"
ordinal = 2821
kind = "pursuit"
timestamp = "2026-10-13T21:50:00+00:00"
summary = "pursuit prove T0548: WITNESSED — refuses when contract.py's `if len(same) > 1:` is put back as `if len(same) > 2:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1defc5cba0c5e6bac8fffcbaad7d155ed103024d4e4cfd3b5eee15677549c911  .beagle/checks/T0548/T0548.sh" | sha256sum -c --quiet && bash .beagle/checks/T0548/T0548.sh'
refutes: refuses when contract.py's `if len(same) > 1:` is put back as `if len(same) > 2:` (proven 2026-10-13T21:49:03+00:00; refused at 1 failed, 1 passed, 65 deselected in 0.15s)
refused after 0s of a 0s check at: 1 failed, 1 passed, 65 deselected in 0.15s
refused with: 1 failed, 1 passed, 65 deselected in 0.15s
standing checks red: T0512, T0519
