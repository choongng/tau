+++
id = "000730-pursuit"
ordinal = 730
kind = "pursuit"
timestamp = "2026-10-04T16:19:20+00:00"
summary = "pursuit prove T0170: WITNESSED — refuses when beagle.py's `flawed = _cases_test_problem(root, locks) if lo…` is put back as `flawed = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9f6a51941be00a82ef4a4f81cb7755b9bcd170ed5e0abbab8e74ea6c96b80b90  .beagle/checks/T0170/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0170/check.sh'
refutes: refuses when beagle.py's `flawed = _cases_test_problem(root, locks) if lo…` is put back as `flawed = None` (proven 2026-10-04T16:18:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_close_refuses_a_cases_test_naming_absent_cases)
refused after 2s of a 1m01s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_close_refuses_a_cases_test_naming_absent_cases
refused with: 1 failed in 1.52s
