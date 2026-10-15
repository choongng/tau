+++
id = "003295-pursuit"
ordinal = 3295
kind = "pursuit"
timestamp = "2026-10-15T12:32:46+00:00"
summary = "pursuit open T0637: Fix 24: the cases worker does not write the code to check the source"
metric_command = ""
drains = []
hooks = []
+++

criteria: The cases worker's brief tells it not to write the code, or a version of it, to check the source, and to write a row the source shortens out from the pattern it shows
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases'
budget: 40000 tokens
