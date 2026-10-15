+++
id = "003237-pursuit"
ordinal = 3237
kind = "pursuit"
timestamp = "2026-10-15T05:17:15+00:00"
summary = "pursuit prove T0625: WITNESSED — refuses when beagle.py's `if unwritten is not None: _test, module, _via =…` is put back as `if unwritten is not None and False: _test, modu…`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_spec_tied_scope_of_tests_only_gains_the_code_its_cases_import
refutes: refuses when beagle.py's `if unwritten is not None: _test, module, _via =…` is put back as `if unwritten is not None and False: _test, modu…` (proven 2026-10-15T05:16:17+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_scope_of_tests_only_gains_the_code_it
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_scope_of_tests_only_gains_the_code_its_cases…
refused with: 1 failed, 722 deselected in 0.93s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
