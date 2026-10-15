+++
id = "003275-pursuit"
ordinal = 3275
kind = "pursuit"
timestamp = "2026-10-15T09:52:15+00:00"
summary = "pursuit open T0633: Fix 20: the host runs a cases worker's dry run and hands a refusal back to the same worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a spec-tied step's cases worker ends, tau runs the task's open with --dry-run on its cases; a refusal over the cases resumes that same worker session with the refusal, at most twice, before the step relays it; the real open runs only after a dry run passes.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'same_worker or cases_fail_at_the_open'
budget: 40000 tokens
