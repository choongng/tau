+++
id = "003165-pursuit"
ordinal = 3165
kind = "pursuit"
timestamp = "2026-10-15T00:57:44+00:00"
summary = "pursuit prove T0613: WITNESSED — refuses when beagle.py's `_repair_case_markers(root, cases_scope) files, …` is put back as `files, cites`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_real_step.py -k 'names_cases_whose_markers_have_no_name'
refutes: refuses when beagle.py's `_repair_case_markers(root, cases_scope) files, …` is put back as `files, cites` (proven 2026-10-15T00:56:45+00:00; predates the task: the fix was committed on beagle-0.48 and merged before the task was opened (audit 10-14: opened late); the needle is the task's own line (3f
refused after 8s of a 14s check at: FAILED tests/test_beagle_real_step.py::test_real_spec_tied_step_names_cases_whose_markers_have_no_name
refused with: 1 failed, 5 deselected in 7.01s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0581, T0502, T0505, T0507, T0509, T0519
