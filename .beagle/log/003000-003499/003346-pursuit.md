+++
id = "003346-pursuit"
ordinal = 3346
kind = "pursuit"
timestamp = "2026-10-15T21:22:43+00:00"
summary = "pursuit open T0647: Fix 34: carry a do-not-rewrite witness note to the next worker on a passing check"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a step dispatches a worker on a task whose check passed in an earlier step but whose witness was not accepted (ask_module), the brief tells it the implementation already passes and to add only the WITNESS, not rewrite it.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'warns_a_fresh_worker or hands_a_refused_witness or takes_the_work_away'
budget: 40000 tokens
