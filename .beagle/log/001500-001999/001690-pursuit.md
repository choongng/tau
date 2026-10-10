+++
id = "001690-pursuit"
ordinal = 1690
kind = "pursuit"
timestamp = "2026-10-10T23:51:32+00:00"
summary = "pursuit prove T0391: WITNESSED — refuses when beagle.py's `return _judge_escalation(task, count, demand, r…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "175fcf109ca4e9fbddddac9ae6bbb9a869c75b26d94229702a082e31a280b017  .beagle/checks/T0391/T0391.sh" | sha256sum -c --quiet && bash .beagle/checks/T0391/T0391.sh'
refutes: refuses when beagle.py's `return _judge_escalation(task, count, demand, r…` is put back as `pass` (proven 2026-10-10T23:51:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_cap_keeps_a_passing_bound_check)
refused after 1s of a 2m07s check at: FAILED tests/test_beagle_example_extension.py::test_step_cap_keeps_a_passing_bound_check
refused with: 1 failed, 2 passed, 722 deselected in 0.65s
replaces: refuses when beagle.py's `if ran and _LAST_CHECK_EXIT.get(key, 0) == 0 an…` is put back as `if False:` (proven 2026-10-10T23:49:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_source_judge_escalation_after_an_early_failed_check)
