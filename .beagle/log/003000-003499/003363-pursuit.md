+++
id = "003363-pursuit"
ordinal = 3363
kind = "pursuit"
timestamp = "2026-10-15T21:56:41+00:00"
summary = "pursuit prove T0654: WITNESSED — refuses when beagle.py's `if (key := _reference_key(word)) and key in nam…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'milestone_source or placeholder'
refutes: refuses when beagle.py's `if (key := _reference_key(word)) and key in nam…` is put back as `if False:` (proven 2026-10-15T21:55:42+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_milestone_source_spelled_near_a_reference_names_that_file)
refused after 3s of a 3s check at: FAILED tests/test_beagle_example_extension.py::test_a_milestone_source_spelled_near_a_reference_names_that_file
refused with: 1 failed, 5 passed, 737 deselected in 2.59s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519
