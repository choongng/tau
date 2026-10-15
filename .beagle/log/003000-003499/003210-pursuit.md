+++
id = "003210-pursuit"
ordinal = 3210
kind = "pursuit"
timestamp = "2026-10-15T03:37:43+00:00"
summary = "pursuit prove T0621: WITNESSED — refuses when beagle.py's `\"environment\",` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_founding_folds_an_environment_milestone_with_no_source_into_the_first_work
refutes: refuses when beagle.py's `"environment",` is put back as `` (proven 2026-10-15T03:36:45+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_folds_an_environment_milestone_with_no_source_into_the_fir…)
refused after 4s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_folds_an_environment_milestone_with_no_source_into_the_fir…
refused with: 1 failed, 716 deselected in 3.97s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
