+++
id = "003306-pursuit"
ordinal = 3306
kind = "pursuit"
timestamp = "2026-10-15T13:51:08+00:00"
summary = "pursuit prove T0639: WITNESSED — refuses when beagle.py's `if part and source and not _NO_SOURCE.match(sou…` is put back as `if part and source:`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_milestone_whose_source_is_a_placeholder_has_no_source'
refutes: refuses when beagle.py's `if part and source and not _NO_SOURCE.match(sou…` is put back as `if part and source:` (proven 2026-10-15T13:50:11+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_milestone_whose_source_is_a_placeholder_has_no_source)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_a_milestone_whose_source_is_a_placeholder_has_no_source
refused with: 1 failed, 733 deselected in 0.71s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
