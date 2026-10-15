+++
id = "003322-pursuit"
ordinal = 3322
kind = "pursuit"
timestamp = "2026-10-15T15:43:48+00:00"
summary = "pursuit prove T0642: WITNESSED — refuses when beagle.py's `if root is None or _names_a_reference(source, r…` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_milestone_source_that_names_no_reference_joins_its_intent'
refutes: refuses when beagle.py's `if root is None or _names_a_reference(source, r…` is put back as `if True:` (proven 2026-10-15T15:42:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_milestone_source_that_names_no_reference_joins_its_intent)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_a_milestone_source_that_names_no_reference_joins_its_intent
refused with: 1 failed, 736 deselected in 0.73s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
