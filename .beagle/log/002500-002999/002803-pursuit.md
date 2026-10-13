+++
id = "002803-pursuit"
ordinal = 2803
kind = "pursuit"
timestamp = "2026-10-13T21:14:22+00:00"
summary = "pursuit prove T0547: WITNESSED — refuses when beagle.py's `argv = [\"contract\", \"seal\", *([\"--reason\", reas…` is put back as `argv = [\"contract\", \"seal\"]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "131c26a167ac7272b90640186c30b0982344ccf67dbf5a495739855fe50ddc87  .beagle/checks/T0547/T0547.sh" | sha256sum -c --quiet && bash .beagle/checks/T0547/T0547.sh'
refutes: refuses when beagle.py's `argv = ["contract", "seal", *(["--reason", reas…` is put back as `argv = ["contract", "seal"]` (proven 2026-10-13T21:13:22+00:00; refused at 1 failed, 2 passed, 856 deselected in 4.68s)
refused after 6s of a 5s check at: 1 failed, 2 passed, 856 deselected in 4.68s
refused with: 1 failed, 2 passed, 856 deselected in 4.68s
