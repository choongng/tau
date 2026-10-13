+++
id = "002639-pursuit"
ordinal = 2639
kind = "pursuit"
timestamp = "2026-10-13T05:52:00+00:00"
summary = "pursuit prove T0509: WITNESSED — refuses when contract.py's `problems.extend(report_problems(root, settings,…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ce79a011e23aa01a419aacd3236056907510cf43e0e608b27cbee4b98fdba6b5  .beagle/checks/T0509/T0509.sh" | sha256sum -c --quiet && bash .beagle/checks/T0509/T0509.sh'
refutes: refuses when contract.py's `problems.extend(report_problems(root, settings,…` is put back as `pass` (proven 2026-10-13T05:51:01+00:00; refused at 1 failed, 2 passed, 49 deselected in 0.32s)
refused after 1s of a 1s check at: 1 failed, 2 passed, 49 deselected in 0.32s
refused with: 1 failed, 2 passed, 49 deselected in 0.32s
