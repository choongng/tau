+++
id = "003170-pursuit"
ordinal = 3170
kind = "pursuit"
timestamp = "2026-10-15T00:58:52+00:00"
summary = "pursuit prove T0614: WITNESSED — refuses when beagle.py's `Above each case put one marker line, `# beagle-…` is put back as `Above each case put one marker line, `# beagle-…`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'spec_tied_writes_cases_then_opens_with_cites_and_cases'
refutes: refuses when beagle.py's `Above each case put one marker line, `# beagle-…` is put back as `Above each case put one marker line, `# beagle-…` (proven 2026-10-15T00:57:55+00:00; predates the task: the fix was committed on beagle-0.48 and merged before the task was opened (audit 10-14: opened late); t
refused after 2s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refused with: 1 failed, 712 deselected in 1.30s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
