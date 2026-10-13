+++
id = "002766-pursuit"
ordinal = 2766
kind = "pursuit"
timestamp = "2026-10-13T20:18:41+00:00"
summary = "pursuit prove T0537: WITNESSED — refuses when contract.py's `return reasons[min(failing)]` is put back as `return \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6801e71928eeddabec2fb2b0d1d07a69f99df915e64ec0ac4018e4bfcb99f70c  .beagle/checks/T0537/T0537.sh" | sha256sum -c --quiet && bash .beagle/checks/T0537/T0537.sh'
refutes: refuses when contract.py's `return reasons[min(failing)]` is put back as `return ""` (proven 2026-10-13T20:17:45+00:00; refused at 1 failed, 1 passed, 59 deselected in 0.17s)
refused after 0s of a 0s check at: 1 failed, 1 passed, 59 deselected in 0.17s
refused with: 1 failed, 1 passed, 59 deselected in 0.17s
standing checks red: T0519
