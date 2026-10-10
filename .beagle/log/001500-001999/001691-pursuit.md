+++
id = "001691-pursuit"
ordinal = 1691
kind = "pursuit"
timestamp = "2026-10-10T23:53:41+00:00"
summary = "pursuit prove T0391: WITNESSED — refuses when beagle.py's `or _STOP_OFFERED` is put back as `or False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "175fcf109ca4e9fbddddac9ae6bbb9a869c75b26d94229702a082e31a280b017  .beagle/checks/T0391/T0391.sh" | sha256sum -c --quiet && bash .beagle/checks/T0391/T0391.sh'
refutes: refuses when beagle.py's `or _STOP_OFFERED` is put back as `or False` (proven 2026-10-10T23:53:40+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_stop_gate_accepts_a_stop_the_step_cap_offered)
refused after 1s of a 2m07s check at: FAILED tests/test_beagle_example_extension.py::test_stop_gate_accepts_a_stop_the_step_cap_offered
refused with: 1 failed, 2 passed, 722 deselected in 0.92s
replaces: refuses when beagle.py's `return _judge_escalation(task, count, demand, r…` is put back as `pass` (proven 2026-10-10T23:51:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_cap_keeps_a_passing_bound_check)
