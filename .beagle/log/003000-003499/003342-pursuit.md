+++
id = "003342-pursuit"
ordinal = 3342
kind = "pursuit"
timestamp = "2026-10-15T18:01:52+00:00"
summary = "pursuit prove T0646: WITNESSED — refuses when beagle.py's `CASES_REASONING_SECONDS if role == CASES_ROLE e…` is put back as `WORKER_REASONING_SECONDS`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'reasons_for_less_per_turn or worker_bash_timeout or spec_tied_writes_cases'
refutes: refuses when beagle.py's `CASES_REASONING_SECONDS if role == CASES_ROLE e…` is put back as `WORKER_REASONING_SECONDS` (proven 2026-10-15T18:00:52+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_cases_worker_reasons_for_less_per_turn_than_the_code_w…)
refused after 3s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_cases_worker_reasons_for_less_per_turn_than_the_code_w…
refused with: 1 failed, 2 passed, 738 deselected in 2.04s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
