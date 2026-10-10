+++
id = "001463-pursuit"
ordinal = 1463
kind = "pursuit"
timestamp = "2026-10-10T02:57:55+00:00"
summary = "pursuit prove T0342: WITNESSED — refuses when beagle.py's `copied = _copied_cases_test(root, tests, data)` is put back as `copied = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "877cc0b3ebc1596abb8cdf716ddfb5f71e641132f2c61de0b7923ef9afd94a08  .beagle/checks/T0342/T0342.sh" | sha256sum -c --quiet && bash .beagle/checks/T0342/T0342.sh'
refutes: refuses when beagle.py's `copied = _copied_cases_test(root, tests, data)` is put back as `copied = None` (proven 2026-10-10T02:57:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_close_refuses_cases_test_copying_data_test)
refused after 1s of a 1m44s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_close_refuses_cases_test_copying_data_test
refused with: 1 failed, 1 passed, 673 deselected in 1.00s
