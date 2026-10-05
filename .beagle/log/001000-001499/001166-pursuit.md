+++
id = "001166-pursuit"
ordinal = 1166
kind = "pursuit"
timestamp = "2026-10-05T17:30:38+00:00"
summary = "pursuit prove T0278: WITNESSED — refuses when beagle.py's `broken = _test_structure_problem(tree)` is put back as `broken = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6ca44cd765747735cea69bbcf2935a52864992f0e335207ab39d0b22b27c8889  .beagle/checks/T0278/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0278/check.sh'
refutes: refuses when beagle.py's `broken = _test_structure_problem(tree)` is put back as `broken = None` (proven 2026-10-05T17:30:37+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_names_no_collectable_test)
refused after 3s of a 1m33s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_names_no_collectable_test
refused with: 1 failed, 1 passed in 2.37s
