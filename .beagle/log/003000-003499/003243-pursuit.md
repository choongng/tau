+++
id = "003243-pursuit"
ordinal = 3243
kind = "pursuit"
timestamp = "2026-10-15T05:55:13+00:00"
summary = "pursuit prove T0626: WITNESSED — refuses when beagle.py's `if right is not None and right != anchor:` is put back as `if right is not None and right != anchor and Fa…`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_reanchors_a_cite_to_the_line_it_names
refutes: refuses when beagle.py's `if right is not None and right != anchor:` is put back as `if right is not None and right != anchor and Fa…` (proven 2026-10-15T05:54:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_reanchors_a_cite_to_the_line_it_names)
refused after 4s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_reanchors_a_cite_to_the_line_it_names
refused with: 1 failed, 723 deselected in 3.42s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
