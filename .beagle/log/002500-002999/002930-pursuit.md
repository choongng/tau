+++
id = "002930-pursuit"
ordinal = 2930
kind = "pursuit"
timestamp = "2026-10-14T02:33:22+00:00"
summary = "pursuit prove T0566: WITNESSED — refuses when contract.py's `return kind, name[found.end():].split()[0].stri…` is put back as `return kind, \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6c989ab3a039205452e5d90bcaf17b8729c1f1dda51571587364228b7c992e40  .beagle/checks/T0566/T0566.sh" | sha256sum -c --quiet && bash .beagle/checks/T0566/T0566.sh'
refutes: refuses when contract.py's `return kind, name[found.end():].split()[0].stri…` is put back as `return kind, ""` (proven 2026-10-14T02:32:51+00:00; refused at 1 failed, 2607 deselected in 0.50s)
refused after 1s of a 57s check at: 1 failed, 2607 deselected in 0.50s
refused with: 1 failed, 2607 deselected in 0.50s
standing checks red: T0335, T0360, T0386, T0496
