+++
id = "002858-pursuit"
ordinal = 2858
kind = "pursuit"
timestamp = "2026-10-14T00:12:19+00:00"
summary = "pursuit prove T0556: WITNESSED — refuses when contract.py's `MAX_EXCLUDED_LINES = 40` is put back as `MAX_EXCLUDED_LINES = 41`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3b2781154f2a14a2bfbd19be4872db364374cda1ac0b0fecaf5f56f0c933c017  .beagle/checks/T0556/T0556.sh" | sha256sum -c --quiet && bash .beagle/checks/T0556/T0556.sh'
refutes: refuses when contract.py's `MAX_EXCLUDED_LINES = 40` is put back as `MAX_EXCLUDED_LINES = 41` (proven 2026-10-14T00:11:58+00:00; refused at 1 failed, 5 passed, 67 deselected in 0.40s)
refused after 1s of a 1m08s check at: 1 failed, 5 passed, 67 deselected in 0.40s
refused with: 1 failed, 5 passed, 67 deselected in 0.40s
