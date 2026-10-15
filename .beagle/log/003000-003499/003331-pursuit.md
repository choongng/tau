+++
id = "003331-pursuit"
ordinal = 3331
kind = "pursuit"
timestamp = "2026-10-15T16:52:46+00:00"
summary = "pursuit open T0644: Fix 31: examine, inspect and survey are reading words"
metric_command = ""
drains = []
hooks = []
+++

criteria: examine, inspect, survey, familiarize/familiarise and skim are reading words, so a milestone that only examines a reference folds into the work after it; one that also fixes or writes is kept
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_founding_folds_examine_and_understand_milestones_into_the_work'
budget: 40000 tokens
