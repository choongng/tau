+++
id = "000447-pursuit"
ordinal = 447
kind = "pursuit"
timestamp = "2026-10-04T02:11:34+00:00"
summary = "pursuit prove T0113: WITNESSED — refuses when beagle.py's `or _cases_first_problem(scope, task, title, goa…` is put back as `or None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7d0d0bdfd4a9c18f858dff6091149e7ffafe91d37bf18eca479de414adec449f  .beagle/checks/T0113/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0113/check.sh'
refutes: refuses when beagle.py's `or _cases_first_problem(scope, task, title, goa…` is put back as `or None` (proven 2026-10-04T02:10:45+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_opening_a_new_source_module_before_a_locked_cases_test_is_refused)
refused after 1s of a 30s check at: FAILED tests/test_beagle_example_extension.py::test_opening_a_new_source_module_before_a_locked_cases_test_is_refused
refused with: 1 failed in 0.75s
