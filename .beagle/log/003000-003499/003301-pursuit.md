+++
id = "003301-pursuit"
ordinal = 3301
kind = "pursuit"
timestamp = "2026-10-15T13:14:47+00:00"
summary = "pursuit prove T0638: WITNESSED — refuses when beagle.py's `REFERENCE_WHOLE_CHARS = 6000` is put back as `REFERENCE_WHOLE_CHARS = 600`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_found_first_steer_carries'
refutes: refuses when beagle.py's `REFERENCE_WHOLE_CHARS = 6000` is put back as `REFERENCE_WHOLE_CHARS = 600` (proven 2026-10-15T13:13:46+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_first_steer_carries_a_short_reference_whole)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_first_steer_carries_a_short_reference_whole
refused with: 1 failed, 1 passed, 731 deselected in 0.89s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
