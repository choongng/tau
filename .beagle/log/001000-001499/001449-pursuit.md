+++
id = "001449-pursuit"
ordinal = 1449
kind = "pursuit"
timestamp = "2026-10-10T02:40:45+00:00"
summary = "pursuit prove T0340: WITNESSED — refuses when beagle.py's `min(COMMAND_TIMEOUT, below_bash, timeout * COMM…` is put back as `min(COMMAND_TIMEOUT, timeout * COMMAND_TIMEOUT_…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4c5a0cf30925f1f7bbb22f16c881575ace49809669fe9949c621b39f6bc040e7  .beagle/checks/T0340/T0340.sh" | sha256sum -c --quiet && bash .beagle/checks/T0340/T0340.sh'
refutes: refuses when beagle.py's `min(COMMAND_TIMEOUT, below_bash, timeout * COMM…` is put back as `min(COMMAND_TIMEOUT, timeout * COMMAND_TIMEOUT_…` (proven 2026-10-10T02:40:44+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_command_bound_is_below_worker_bash_timeout)
refused after 4s of a 1m49s check at: FAILED tests/test_beagle_example_extension.py::test_command_bound_is_below_worker_bash_timeout
refused with: 2 failed, 1 passed, 668 deselected in 3.15s
