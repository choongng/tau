+++
id = "002736-pursuit"
ordinal = 2736
kind = "pursuit"
timestamp = "2026-10-13T19:39:00+00:00"
summary = "pursuit prove T0538: WITNESSED — refuses when beagle.py's `reversion = _open_reversion(opened, scope, root…` is put back as `reversion = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "18bd0836f8439f8c95638d9eef13ed2c813a3f041fc350cf5e5cbddc26de920a  .beagle/checks/T0538/T0538.sh" | sha256sum -c --quiet && bash .beagle/checks/T0538/T0538.sh'
refutes: refuses when beagle.py's `reversion = _open_reversion(opened, scope, root…` is put back as `reversion = None` (proven 2026-10-13T19:37:59+00:00; refused at 1 failed, 1 passed, 852 deselected in 2.49s)
refused after 3s of a 2s check at: 1 failed, 1 passed, 852 deselected in 2.49s
refused with: 1 failed, 1 passed, 852 deselected in 2.49s
