+++
id = "003316-pursuit"
ordinal = 3316
kind = "pursuit"
timestamp = "2026-10-15T15:04:07+00:00"
summary = "pursuit prove T0641: WITNESSED — refuses when beagle.py's `head = _STEP_NUMBER.sub(\"\", _split_part(part)[0…` is put back as `head = _split_part(part)[0]`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_numbered_or_initialization_setup_milestone_is_layout'
refutes: refuses when beagle.py's `head = _STEP_NUMBER.sub("", _split_part(part)[0…` is put back as `head = _split_part(part)[0]` (proven 2026-10-15T15:03:10+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_numbered_or_initialization_setup_milestone_is_layout)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_a_numbered_or_initialization_setup_milestone_is_layout
refused with: 1 failed, 735 deselected in 0.72s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
