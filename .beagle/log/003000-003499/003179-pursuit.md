+++
id = "003179-pursuit"
ordinal = 3179
kind = "pursuit"
timestamp = "2026-10-15T01:25:01+00:00"
summary = "pursuit open T0617: fix 6: founding folds a layout-only milestone into the first work, keeping that part's source last"
metric_command = ""
drains = []
hooks = []
+++

criteria: _repair_milestones folds a layout-only milestone (sourced or not) into the next part, ahead of that part's Source:, with a note; the design fold keeps a target's source last too
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'founding_folds'
budget: 200000 tokens
