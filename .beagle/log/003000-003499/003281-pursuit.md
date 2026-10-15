+++
id = "003281-pursuit"
ordinal = 3281
kind = "pursuit"
timestamp = "2026-10-15T10:42:35+00:00"
summary = "pursuit prove T0634: WITNESSED — refuses when beagle.py's `shown_on = _WITNESS.sub(\"\", report).strip()` is put back as `shown_on = report`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'report_but_not_its_witness or proves_the_workers_witness'
refutes: refuses when beagle.py's `shown_on = _WITNESS.sub("", report).strip()` is put back as `shown_on = report` (proven 2026-10-15T10:41:38+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_closes_with_the_report_but_not_its_witness)
refused after 2s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_closes_with_the_report_but_not_its_witness
refused with: 1 failed, 1 passed, 728 deselected in 1.27s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
