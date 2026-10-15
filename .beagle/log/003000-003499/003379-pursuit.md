+++
id = "003379-pursuit"
ordinal = 3379
kind = "pursuit"
timestamp = "2026-10-15T22:29:46+00:00"
summary = "pursuit open T0632: Pin the clauses the 10-15 audit found untested"
metric_command = ""
drains = []
hooks = []
+++

criteria: Each clause the 10-15 audit found untested has a test that fails without it: T0617's design fold keeps the target's Source: last (and folds a part with no intent of its own); T0624's link guidance in pursuit_plan's parts; T0625's src/ scope; T0616's criterion is amended to what T0620 left (the code worker's brief only).
decided by: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'design_milestone_ahead or part_source or gains_src_code or sourced_layout or spec_tied_writes_cases_then_opens_with_cites_and_cases'
budget: 60000 tokens
