+++
id = "003061-pursuit"
ordinal = 3061
kind = "pursuit"
timestamp = "2026-10-14T06:28:36+00:00"
summary = "pursuit prove T0587: WITNESSED — refuses when contract.py's `if draft and (empty := nothing_drafted(root, se…` is put back as `if False and (empty := nothing_drafted(root, se…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ccac0f26ecf46518190bab3ed7cbff23d575dff36c2e25c9dff8b42bad90f349  .beagle/checks/T0587/T0587.sh" | sha256sum -c --quiet && bash .beagle/checks/T0587/T0587.sh'
refutes: refuses when contract.py's `if draft and (empty := nothing_drafted(root, se…` is put back as `if False and (empty := nothing_drafted(root, se…` (proven 2026-10-14T06:28:35+00:00; refused at 2 failed, 1 passed, 2632 deselected in 4.34s)
refused after 5s of a 3m15s check at: 2 failed, 1 passed, 2632 deselected in 4.34s
refused with: 2 failed, 1 passed, 2632 deselected in 4.34s
