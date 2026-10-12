+++
id = "002419-pursuit"
ordinal = 2419
kind = "pursuit"
timestamp = "2026-10-12T14:55:32+00:00"
summary = "pursuit prove T0473: WITNESSED — refuses when beagle.py's `dict.fromkeys([*scope, test])` is put back as `[*scope, test]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "39f40ebd7fc9782994ed421e4fac5cb126ce5ae1b224f0dcb6866752b1089f08  .beagle/checks/T0473/T0473.sh" | sha256sum -c --quiet && bash .beagle/checks/T0473/T0473.sh'
refutes: refuses when beagle.py's `dict.fromkeys([*scope, test])` is put back as `[*scope, test]` (proven 2026-10-12T14:55:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_first_locked_data_route_does_not_repeat_a_scoped_test)
refused after 4s of a 2m43s check at: FAILED tests/test_beagle_example_extension.py::test_cases_first_locked_data_route_does_not_repeat_a_scoped_test
refused with: 1 failed, 822 deselected in 3.28s
