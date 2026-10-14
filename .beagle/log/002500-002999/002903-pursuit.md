+++
id = "002903-pursuit"
ordinal = 2903
kind = "pursuit"
timestamp = "2026-10-14T01:41:34+00:00"
summary = "pursuit prove T0557: WITNESSED — refuses when contract.py's `problems.extend(_conflict_problems(live, report…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9fe3b9c96fdc1f9789e4ecf7a0b8c7fdaecc88f13ee2206485d747fa53f0f9a8  .beagle/checks/T0557/T0557.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0557/T0557.v2.sh'
refutes: refuses when contract.py's `problems.extend(_conflict_problems(live, report…` is put back as `pass` (proven 2026-10-14T01:41:34+00:00; refused at 1 failed, 3 passed, 72 deselected in 0.90s)
refused after 1s of a 57s check at: 1 failed, 3 passed, 72 deselected in 0.90s
refused with: 1 failed, 3 passed, 72 deselected in 0.90s
