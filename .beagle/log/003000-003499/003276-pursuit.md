+++
id = "003276-pursuit"
ordinal = 3276
kind = "pursuit"
timestamp = "2026-10-15T10:05:29+00:00"
summary = "pursuit prove T0633: WITNESSED — refuses when beagle.py's `refused = _cases_dry_run_refusal(` is put back as `refused = None and _cases_dry_run_refusal(`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'same_worker or cases_fail_at_the_open'
refutes: refuses when beagle.py's `refused = _cases_dry_run_refusal(` is put back as `refused = None and _cases_dry_run_refusal(` (proven 2026-10-15T10:04:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_cases_fail_at_the_open_with_beagles_refusal)
refused after 4s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_cases_fail_at_the_open_with_beagles_refusal
refused with: 2 failed, 727 deselected in 3.58s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
