+++
id = "003153-pursuit"
ordinal = 3153
kind = "pursuit"
timestamp = "2026-10-15T00:33:31+00:00"
summary = "pursuit open T0611: fix 1: cases assert only what their cited lines say; smoke S03"
metric_command = ""
drains = []
hooks = []
+++

criteria: the cases brief says to copy outputs the cited lines give and assert rules, not worked-out values
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'spec_tied_writes_cases_then_opens_with_cites_and_cases'
budget: 200000 tokens
