+++
id = "002840-pursuit"
ordinal = 2840
kind = "pursuit"
timestamp = "2026-10-13T23:28:36+00:00"
summary = "pursuit prove T0546: WITNESSED — refuses when contract.py's `if eid not in failed:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "31a59bdfa8ba88741cdfec20ef5f5bfc86839deee4d4f768b750a4597a580823  .beagle/checks/T0546/T0546.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0546/T0546.v2.sh'
refutes: refuses when contract.py's `if eid not in failed:` is put back as `if False:` (proven 2026-10-13T23:28:35+00:00; refused at 1 failed, 1 passed, 60 deselected in 0.26s)
refused after 0s of a 1s check at: 1 failed, 1 passed, 60 deselected in 0.26s
refused with: 1 failed, 1 passed, 60 deselected in 0.26s
