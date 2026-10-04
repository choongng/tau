+++
id = "000547-pursuit"
ordinal = 547
kind = "pursuit"
timestamp = "2026-10-04T06:38:36+00:00"
summary = "pursuit prove T0132: WITNESSED — refuses when beagle.py's `found = _imports_unwritten(command, scope, root)` is put back as `found = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ebc0ae53ee320858be4cd540a075794f1a7fc5d96adade08a78daa9f0ecb7145  .beagle/checks/T0132/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0132/check.sh'
refutes: refuses when beagle.py's `found = _imports_unwritten(command, scope, root)` is put back as `found = None` (proven 2026-10-04T06:37:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_amending_a_known_answers_check_to_run_the_cases_test_is_refused)
refused after 1s of a 37s check at: FAILED tests/test_beagle_example_extension.py::test_amending_a_known_answers_check_to_run_the_cases_test_is_refused
refused with: 1 failed in 1.11s
