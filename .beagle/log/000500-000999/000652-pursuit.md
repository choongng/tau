+++
id = "000652-pursuit"
ordinal = 652
kind = "pursuit"
timestamp = "2026-10-04T11:29:42+00:00"
summary = "pursuit prove T0154: WITNESSED — refuses when beagle.py's `if rc != 5:` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9609505b9f4927b6ef4d8e1e2a0e477231a7c7b18b668cb9bde750ef4376f0b9  .beagle/checks/T0154/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0154/check.sh'
refutes: refuses when beagle.py's `if rc != 5:` is put back as `if True:` (proven 2026-10-04T11:29:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_not_done_explains_pytest_exit_5_no_tests_collected)
refused after 2s of a 55s check at: FAILED tests/test_beagle_example_extension.py::test_not_done_explains_pytest_exit_5_no_tests_collected
refused with: 1 failed in 1.86s
