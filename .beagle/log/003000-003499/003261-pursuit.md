+++
id = "003261-pursuit"
ordinal = 3261
kind = "pursuit"
timestamp = "2026-10-15T08:21:19+00:00"
summary = "pursuit prove T0629: WITNESSED — refuses when beagle.py's `if source else None )` is put back as `if not source else None )`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'no_scope'
refutes: refuses when beagle.py's `if source else None )` is put back as `if not source else None )` (proven 2026-10-15T08:20:20+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_with_no_scope_is_refused_before_its_cases_wo…)
refused after 3s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_with_no_scope_is_refused_before_its_cases_wo…
refused with: 1 failed, 1 passed, 724 deselected in 2.29s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
