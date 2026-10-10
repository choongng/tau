+++
id = "001458-pursuit"
ordinal = 1458
kind = "pursuit"
timestamp = "2026-10-10T02:50:59+00:00"
summary = "pursuit prove T0341: WITNESSED — refuses when beagle.py's `attempt_timeout = min(timeout, left)` is put back as `attempt_timeout = timeout`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "62990b18bed06b0ee70ad89a3b792a165a058fc46115be1c5fb0bd37fea54389  .beagle/checks/T0341/T0341.sh" | sha256sum -c --quiet && bash .beagle/checks/T0341/T0341.sh'
refutes: refuses when beagle.py's `attempt_timeout = min(timeout, left)` is put back as `attempt_timeout = timeout` (proven 2026-10-10T02:50:59+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_second_attempt_gets_remaining_step_budget)
refused after 1s of a 1m46s check at: FAILED tests/test_beagle_example_extension.py::test_second_attempt_gets_remaining_step_budget
refused with: 1 failed, 1 passed, 671 deselected in 1.01s
