+++
id = "003180-pursuit"
ordinal = 3180
kind = "pursuit"
timestamp = "2026-10-15T01:25:18+00:00"
summary = "pursuit amend T0617"
metric_command = ""
drains = []
hooks = []
+++

the first check also matched the existing design-fold test, so it passed before the fix
was: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'founding_folds'
now: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'founding_folds_a_sourced_layout'
