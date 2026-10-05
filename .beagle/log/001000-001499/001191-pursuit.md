+++
id = "001191-pursuit"
ordinal = 1191
kind = "pursuit"
timestamp = "2026-10-05T19:11:39+00:00"
summary = "pursuit prove T0283: WITNESSED — refuses when beagle.py's `not node_id` is put back as `True`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "dabd2d0efcf7da152428bc7e74210e5251dc7e505640761ebe68ef25e58a4dac  .beagle/checks/T0283/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0283/check.sh'
refutes: refuses when beagle.py's `not node_id` is put back as `True` (proven 2026-10-05T19:11:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_missing_pytest_node_in_unwritable_file_refused)
refused after 3s of a 1m33s check at: FAILED tests/test_beagle_example_extension.py::test_missing_pytest_node_in_unwritable_file_refused
refused with: 1 failed, 3 passed in 2.31s
