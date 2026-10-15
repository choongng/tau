+++
id = "003388-pursuit"
ordinal = 3388
kind = "pursuit"
timestamp = "2026-10-15T22:59:10+00:00"
summary = "pursuit prove T0657: WITNESSED — refuses when beagle.py's `if len(holders) == 1:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'moves_a_cite or reanchors'
refutes: refuses when beagle.py's `if len(holders) == 1:` is put back as `if False:` (proven 2026-10-15T22:58:11+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_moves_a_cite_to_the_reference_whose_line_it_names)
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_moves_a_cite_to_the_reference_whose_line_it_names
refused with: 1 failed, 1 passed, 746 deselected in 1.66s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
