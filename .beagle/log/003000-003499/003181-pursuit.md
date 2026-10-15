+++
id = "003181-pursuit"
ordinal = 3181
kind = "pursuit"
timestamp = "2026-10-15T01:26:27+00:00"
summary = "pursuit prove T0617: WITNESSED — refuses when beagle.py's `return bool(words) and words <= _LAYOUT_WORDS` is put back as `return False`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'founding_folds_a_sourced_layout'
refutes: refuses when beagle.py's `return bool(words) and words <= _LAYOUT_WORDS` is put back as `return False` (proven 2026-10-15T01:25:27+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_sourced_layout_milestone_into_the_first_work)
refused after 5s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_sourced_layout_milestone_into_the_first_work
refused with: 1 failed, 713 deselected in 4.76s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
