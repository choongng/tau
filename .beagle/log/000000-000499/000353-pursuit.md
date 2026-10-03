+++
id = "000353-pursuit"
ordinal = 353
kind = "pursuit"
timestamp = "2026-10-03T20:52:43+00:00"
summary = "pursuit prove T0083: WITNESSED — refuses when beagle.py's `if _setup_abandonable(task, nodes): return None` is put back as `if False: return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9b118bb3445602e1ba0e4f948e15b16d2396cf42a8769865446a0125d488c59e  .beagle/checks/T0083/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0083/check.sh'
refutes: refuses when beagle.py's `if _setup_abandonable(task, nodes): return None` is put back as `if False: return None` (proven 2026-10-03T20:52:00+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_never_opened_setup_milestone_can_be_abandoned)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_never_opened_setup_milestone_can_be_abandoned
refused with: 1 failed, 2 passed, 286 deselected in 0.46s
