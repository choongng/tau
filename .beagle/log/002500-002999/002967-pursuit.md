+++
id = "002967-pursuit"
ordinal = 2967
kind = "pursuit"
timestamp = "2026-10-14T03:41:41+00:00"
summary = "pursuit prove T0576: WITNESSED — refuses when contract.py's `if \"command\" in item or (\"path\" in item and \"na…` is put back as `if \"command\" in item:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "17cf03560dbce44f04dc0923b3ceb9b254fd0aa5148e34e21ff38423c7f75a0e  .beagle/checks/T0576/T0576.sh" | sha256sum -c --quiet && bash .beagle/checks/T0576/T0576.sh'
refutes: refuses when contract.py's `if "command" in item or ("path" in item and "na…` is put back as `if "command" in item:` (proven 2026-10-14T03:40:49+00:00; refused at 1 failed, 2 passed, 2610 deselected in 0.55s)
refused after 1s of a 57s check at: 1 failed, 2 passed, 2610 deselected in 0.55s
refused with: 1 failed, 2 passed, 2610 deselected in 0.55s
standing checks red: T0335, T0360, T0386, T0496
