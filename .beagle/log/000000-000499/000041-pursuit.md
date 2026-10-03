+++
id = "000041-pursuit"
ordinal = 41
kind = "pursuit"
timestamp = "2026-10-03T11:15:15+00:00"
summary = "pursuit prove T0024: WITNESSED — refuses when beagle.py's `if length > MAX_TASK_TITLE:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0024/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0024/named_tests.sh tests/test_beagle_example_extension.py 2 test_found_refuses_long_milestone_before_writing test_found_accepts_max_length_milestone'
refutes: refuses when beagle.py's `if length > MAX_TASK_TITLE:` is put back as `if False:` (proven 2026-10-03T11:15:12+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_refuses_long_milestone_before_writing)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_refuses_long_milestone_before_writing
refused with: 1 failed, 1 passed, 195 deselected in 0.46s
