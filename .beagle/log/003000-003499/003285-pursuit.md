+++
id = "003285-pursuit"
ordinal = 3285
kind = "pursuit"
timestamp = "2026-10-15T11:17:16+00:00"
summary = "pursuit open T0635: Fix 22: a refused witness goes back to the same worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the check passes and prove refuses the worker's witness, the next attempt resumes the same worker session with prove's refusal, not a fresh brief; the brief says a refused witness is asked again and asks for a NEEDLE that is part of one line
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'refused_witness_back_to_the_same_worker'
budget: 40000 tokens
