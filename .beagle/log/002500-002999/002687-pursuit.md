+++
id = "002687-pursuit"
ordinal = 2687
kind = "pursuit"
timestamp = "2026-10-13T07:28:51+00:00"
summary = "pursuit prove T0525: WITNESSED — refuses when contract.py's `out.extend(_case_value_problems(entry, where, k…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5321f872ed7f28c85bf82b389720e74ed93de7fe50edc211335eca9ddc6ec3b  .beagle/checks/T0525/T0525.sh" | sha256sum -c --quiet && bash .beagle/checks/T0525/T0525.sh'
refutes: refuses when contract.py's `out.extend(_case_value_problems(entry, where, k…` is put back as `pass` (proven 2026-10-13T07:27:49+00:00; refused at 1 failed, 53 deselected in 0.42s)
refused after 1s of a 1s check at: 1 failed, 53 deselected in 0.42s
refused with: 1 failed, 53 deselected in 0.42s
