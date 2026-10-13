+++
id = "002644-pursuit"
ordinal = 2644
kind = "pursuit"
timestamp = "2026-10-13T05:53:41+00:00"
summary = "pursuit prove T0510: WITNESSED — refuses when beagle.py's `if _bash_find(command, inline) is None: return …` is put back as `if True: return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "07b5fa20f833927c51f971a7fe71def0072a80884b3eb92486a762d4739181b2  .beagle/checks/T0510/T0510.sh" | sha256sum -c --quiet && bash .beagle/checks/T0510/T0510.sh'
refutes: refuses when beagle.py's `if _bash_find(command, inline) is None: return …` is put back as `if True: return None` (proven 2026-10-13T05:52:41+00:00; refused at 2 failed, 3 passed, 838 deselected in 4.67s)
refused after 5s of a 3s check at: 2 failed, 3 passed, 838 deselected in 4.67s
refused with: 2 failed, 3 passed, 838 deselected in 4.67s
