+++
id = "002989-pursuit"
ordinal = 2989
kind = "pursuit"
timestamp = "2026-10-14T04:12:49+00:00"
summary = "pursuit prove T0569: WITNESSED — refuses when contract.py's `report = check(root, settings, draft=True, run_…` is put back as `report = check(root, settings)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "79f11d581ac7167f50986035a2b99009ba1d51332f6fbf5099126540e0598c60  .beagle/checks/T0569/T0569.sh" | sha256sum -c --quiet && bash .beagle/checks/T0569/T0569.sh'
refutes: refuses when contract.py's `report = check(root, settings, draft=True, run_…` is put back as `report = check(root, settings)` (proven 2026-10-14T04:12:21+00:00; refused at 1 failed, 1 passed, 2614 deselected in 0.57s)
refused after 1s of a 1m00s check at: 1 failed, 1 passed, 2614 deselected in 0.57s
refused with: 1 failed, 1 passed, 2614 deselected in 0.57s
standing checks red: T0335, T0360, T0386, T0496
