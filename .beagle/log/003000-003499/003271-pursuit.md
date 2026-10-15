+++
id = "003271-pursuit"
ordinal = 3271
kind = "pursuit"
timestamp = "2026-10-15T09:19:02+00:00"
summary = "pursuit prove T0630: WITNESSED — refuses when beagle.py's `wrong_scope = _no_scope_problem(carried_scope, …` is put back as `wrong_scope = _no_scope_problem(carried_scope, …`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'no_scope or scoped_into_references or scope_names or carries_its_predecessors'
refutes: refuses when beagle.py's `wrong_scope = _no_scope_problem(carried_scope, …` is put back as `wrong_scope = _no_scope_problem(carried_scope, …` (proven 2026-10-15T09:18:05+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_scoped_into_references_is_refused_bef
refused after 3s of a 3s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_scoped_into_references_is_refused_before_its…
refused with: 1 failed, 3 passed, 724 deselected in 2.78s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
