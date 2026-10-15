+++
id = "003341-pursuit"
ordinal = 3341
kind = "pursuit"
timestamp = "2026-10-15T17:56:46+00:00"
summary = "pursuit open T0646: Fix 33: a shorter reasoning budget per turn for the cases worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: A cases worker is spawned with a per-turn reasoning budget (TAU_TURN_REASONING_SECONDS) below the code worker's; the code worker keeps WORKER_REASONING_SECONDS.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'reasons_for_less_per_turn or worker_bash_timeout or spec_tied_writes_cases'
budget: 40000 tokens
