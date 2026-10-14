+++
id = "002864-pursuit"
ordinal = 2864
kind = "pursuit"
timestamp = "2026-10-14T00:31:47+00:00"
summary = "pursuit prove T0557: WITNESSED — refuses when contract.py's `problems.extend(_conflict_problems(live, report…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bbd9dde8a31ca1a6195e036dbb7af2aa5793957c2e97e599ec62cda299185a27  .beagle/checks/T0557/T0557.sh" | sha256sum -c --quiet && bash .beagle/checks/T0557/T0557.sh'
refutes: refuses when contract.py's `problems.extend(_conflict_problems(live, report…` is put back as `pass` (proven 2026-10-14T00:31:22+00:00; refused at 1 failed, 3 passed, 71 deselected in 0.92s)
refused after 1s of a 1m01s check at: 1 failed, 3 passed, 71 deselected in 0.92s
refused with: 1 failed, 3 passed, 71 deselected in 0.92s
