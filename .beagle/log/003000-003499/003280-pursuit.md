+++
id = "003280-pursuit"
ordinal = 3280
kind = "pursuit"
timestamp = "2026-10-15T10:37:55+00:00"
summary = "pursuit open T0634: Fix 21: a close body leaves out the worker's WITNESS block"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step's done close passes the worker's report as its body without the WITNESS ... END WITNESS block, which prove already recorded.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'report_but_not_its_witness or proves_the_workers_witness'
budget: 40000 tokens
