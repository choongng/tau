+++
id = "003270-pursuit"
ordinal = 3270
kind = "pursuit"
timestamp = "2026-10-15T09:13:58+00:00"
summary = "pursuit open T0630: Fix 19: refuse a spec-tied step's wrong scope before its cases worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: A spec-tied pursuit_step whose scope is refused on its own (none given, references/, or .beagle/) is refused before any cases worker runs; a successor with no scope of its own carries its predecessor's to the cases worker.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'no_scope or scoped_into_references or scope_names or carries_its_predecessors'
budget: 40000 tokens
