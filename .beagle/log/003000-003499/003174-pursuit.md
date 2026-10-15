+++
id = "003174-pursuit"
ordinal = 3174
kind = "pursuit"
timestamp = "2026-10-15T01:06:32+00:00"
summary = "pursuit open T0616: fix 5: workers run arithmetic instead of reasoning it out; cases don't stub the code; smoke S05"
metric_command = ""
drains = []
hooks = []
+++

criteria: both worker briefs say to work arithmetic and expected outputs out by running them; the cases brief says the import failure is expected and not to stub the code
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k spec_tied_writes_cases_then_opens_with_cites_and_cases
budget: 200000 tokens
