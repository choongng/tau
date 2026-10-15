+++
id = "003305-pursuit"
ordinal = 3305
kind = "pursuit"
timestamp = "2026-10-15T13:46:27+00:00"
summary = "pursuit open T0639: Fix 26: a placeholder source is no source"
metric_command = ""
drains = []
hooks = []
+++

criteria: A milestone whose source is a placeholder (N/A, none, a dash, TBD, not applicable) gets no Source, and _task_source reads such a Source as none
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_milestone_whose_source_is_a_placeholder_has_no_source'
budget: 40000 tokens
