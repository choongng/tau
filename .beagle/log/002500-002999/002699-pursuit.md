+++
id = "002699-pursuit"
ordinal = 2699
kind = "pursuit"
timestamp = "2026-10-13T15:04:06+00:00"
summary = "pursuit prove T0529: WITNESSED — refuses when pursuit.py's `\"before you work a case through by hand. A case…` is put back as `\"A case traced in your \"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a29de8f9a25c56b35b44dd4225cf419c5c1f238a311dc508bc17631650f4a1e8  .beagle/checks/T0529/T0529.sh" | sha256sum -c --quiet && bash .beagle/checks/T0529/T0529.sh'
refutes: refuses when pursuit.py's `"before you work a case through by hand. A case…` is put back as `"A case traced in your "` (proven 2026-10-13T15:03:07+00:00; refused at 1 failed, 2 passed, 508 deselected in 0.37s)
refused after 1s of a 0s check at: 1 failed, 2 passed, 508 deselected in 0.37s
refused with: 1 failed, 2 passed, 508 deselected in 0.37s
