+++
id = "003204-pursuit"
ordinal = 3204
kind = "pursuit"
timestamp = "2026-10-15T03:15:46+00:00"
summary = "pursuit prove T0620: WITNESSED — refuses when beagle.py's `_turn_cap_note(CASES_WORK_IT_OUT_NOTE)` is put back as `_turn_cap_note()`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refutes: refuses when beagle.py's `_turn_cap_note(CASES_WORK_IT_OUT_NOTE)` is put back as `_turn_cap_note()` (proven 2026-10-15T03:14:48+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases)
refused after 5s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refused with: 1 failed, 715 deselected in 4.02s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
