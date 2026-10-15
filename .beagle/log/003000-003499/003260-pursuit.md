+++
id = "003260-pursuit"
ordinal = 3260
kind = "pursuit"
timestamp = "2026-10-15T08:16:26+00:00"
summary = "pursuit open T0629: Fix 18: refuse a spec-tied step with no scope before its cases worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: A spec-tied pursuit_step with no scope (and no predecessor's scope to carry) is refused 'no scope given' before any cases worker runs.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'no_scope'
budget: 40000 tokens
