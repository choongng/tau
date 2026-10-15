+++
id = "003353-pursuit"
ordinal = 3353
kind = "pursuit"
timestamp = "2026-10-15T21:45:55+00:00"
summary = "pursuit prove T0649: WITNESSED — refuses when grade_founding.py's `return bool(words & (SETUP_WORDS | STUDY_WORDS))` is put back as `return False`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider /home/choong/tautest/itc-harness/test_grade_founding.py
refutes: refuses when grade_founding.py's `return bool(words & (SETUP_WORDS | STUDY_WORDS))` is put back as `return False` (proven 2026-10-15T21:44:56+00:00; refused at FAILED ../itc-harness/test_grade_founding.py::test_a_recorded_founding_failure_is_flagged[R105-IDLE])
refused after 0s of a 0s check at: FAILED ../itc-harness/test_grade_founding.py::test_a_recorded_founding_failure_is_flagged[R105-IDLE]
refused with: 7 failed, 10 passed in 0.33s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
