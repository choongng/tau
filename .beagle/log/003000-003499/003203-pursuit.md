+++
id = "003203-pursuit"
ordinal = 3203
kind = "pursuit"
timestamp = "2026-10-15T03:11:07+00:00"
summary = "pursuit open T0620: Fix 9: the cases brief stops telling the worker to work out expected outputs"
metric_command = ""
drains = []
hooks = []
+++

criteria: The cases worker's brief has no 'expected outputs' instruction and says expected values come from the cited lines; the code worker's brief keeps the work-it-out note.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
budget: 40000 tokens
