+++
id = "003291-pursuit"
ordinal = 3291
kind = "pursuit"
timestamp = "2026-10-15T12:00:15+00:00"
summary = "pursuit prove T0636: WITNESSED — refuses when beagle.py's `bool(words & _SETUP_ACTS - _GENERIC_ACTS)` is put back as `False`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'setup_milestone'
refutes: refuses when beagle.py's `bool(words & _SETUP_ACTS - _GENERIC_ACTS)` is put back as `False` (proven 2026-10-15T11:59:18+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_setup_milestone_whose_purpose_names_the_pursuit_is_dropped)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_setup_milestone_whose_purpose_names_the_pursuit_is_dropped
refused with: 1 failed, 3 passed, 728 deselected in 0.93s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
