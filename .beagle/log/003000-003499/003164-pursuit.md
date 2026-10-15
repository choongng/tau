+++
id = "003164-pursuit"
ordinal = 3164
kind = "pursuit"
timestamp = "2026-10-15T00:56:21+00:00"
summary = "pursuit open T0613: fix 3: name case markers written without a name; smoke S04"
metric_command = ""
drains = []
hooks = []
+++

criteria: case markers with the cite as the name, or with no name, are named before ties are read, and the task opens tied
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_real_step.py -k 'names_cases_whose_markers_have_no_name'
budget: 200000 tokens
