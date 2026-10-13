+++
id = "002796-pursuit"
ordinal = 2796
kind = "pursuit"
timestamp = "2026-10-13T20:53:22+00:00"
summary = "pursuit prove T0546: WITNESSED — refuses when contract.py's `if eid not in failed:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f9a9f4aa344d1cef4e4774a0587afddc4f1325859a91a40453ae1ba806532edb  .beagle/checks/T0546/T0546.sh" | sha256sum -c --quiet && bash .beagle/checks/T0546/T0546.sh'
refutes: refuses when contract.py's `if eid not in failed:` is put back as `if False:` (proven 2026-10-13T20:52:19+00:00; refused at 1 failed, 2 passed, 62 deselected in 0.66s)
refused after 1s of a 1s check at: 1 failed, 2 passed, 62 deselected in 0.66s
refused with: 1 failed, 2 passed, 62 deselected in 0.66s
