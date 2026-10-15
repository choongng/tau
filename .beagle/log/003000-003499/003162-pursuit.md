+++
id = "003162-pursuit"
ordinal = 3162
kind = "pursuit"
timestamp = "2026-10-15T00:55:47+00:00"
summary = "pursuit prove T0611: WITNESSED — refuses when beagle.py's `Where they give the output, copy it` is put back as `Where they give the output, use it`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'spec_tied_writes_cases_then_opens_with_cites_and_cases'
refutes: refuses when beagle.py's `Where they give the output, copy it` is put back as `Where they give the output, use it` (proven 2026-10-15T00:55:47+00:00; predates the task: the fix was committed on beagle-0.48 and merged before T0611 was opened (audit 10-14: opened late); the needle is T0611's own line 
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refused with: 1 failed, 712 deselected in 1.22s
