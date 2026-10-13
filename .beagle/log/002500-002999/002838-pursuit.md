+++
id = "002838-pursuit"
ordinal = 2838
kind = "pursuit"
timestamp = "2026-10-13T23:28:13+00:00"
summary = "pursuit prove T0554: WITNESSED — refuses when contract.py's `return [p for p in paths if p not in sealed or …` is put back as `return []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fbff64f3e15bee27d62c31c5e594b6b8bc255d274e5d8d378845c2fbeecc2f02  .beagle/checks/T0554/T0554.sh" | sha256sum -c --quiet && bash .beagle/checks/T0554/T0554.sh'
refutes: refuses when contract.py's `return [p for p in paths if p not in sealed or …` is put back as `return []` (proven 2026-10-13T23:27:59+00:00; refused at 1 failed, 5 passed, 56 deselected in 1.55s)
refused after 2s of a 1m13s check at: 1 failed, 5 passed, 56 deselected in 1.55s
refused with: 1 failed, 5 passed, 56 deselected in 1.55s
