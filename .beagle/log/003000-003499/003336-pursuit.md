+++
id = "003336-pursuit"
ordinal = 3336
kind = "pursuit"
timestamp = "2026-10-15T17:15:24+00:00"
summary = "pursuit open T0645: Fix 32: follow up the driver cut-off that tau no longer nudges"
metric_command = ""
drains = []
hooks = []
+++

criteria: A driver turn cut at the output limit past the nudges tau sends in a row (more for time cuts) gets the stop gate's follow-up while the pursuit is unfinished; cut-offs tau still nudges, and runs where a turn acts in between, get none.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'stop_gate'
budget: 40000 tokens
