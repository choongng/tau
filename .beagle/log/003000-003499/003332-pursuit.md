+++
id = "003332-pursuit"
ordinal = 3332
kind = "pursuit"
timestamp = "2026-10-15T16:57:34+00:00"
summary = "pursuit prove T0644: WITNESSED — refuses when beagle.py's `\"examine\",` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_founding_folds_examine_and_understand_milestones_into_the_work'
refutes: refuses when beagle.py's `"examine",` is put back as `` (proven 2026-10-15T16:56:36+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_folds_examine_and_understand_milestones_into_the_work)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_folds_examine_and_understand_milestones_into_the_work
refused with: 1 failed, 738 deselected in 0.71s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
