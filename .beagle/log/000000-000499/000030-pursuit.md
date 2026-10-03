+++
id = "000030-pursuit"
ordinal = 30
kind = "pursuit"
timestamp = "2026-10-03T11:04:12+00:00"
summary = "pursuit prove T0022: WITNESSED — refuses when beagle.py's `refusal = _founded_dispatch_refusal(cwd)` is put back as `refusal = None and _founded_dispatch_refusal(cw…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0022/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0022/named_tests.sh tests/test_beagle_example_extension.py 4 test_founded_driver_dispatch_refused test_unfounded_dispatch_runs test_founded_driver_reference_read_refused test_worker_reference_read_allowed'
refutes: refuses when beagle.py's `refusal = _founded_dispatch_refusal(cwd)` is put back as `refusal = None and _founded_dispatch_refusal(cw…` (proven 2026-10-03T11:04:12+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founded_driver_dispatch_refused)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founded_driver_dispatch_refused
refused with: 1 failed, 3 passed, 188 deselected in 0.48s
