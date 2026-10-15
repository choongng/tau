+++
id = "003321-pursuit"
ordinal = 3321
kind = "pursuit"
timestamp = "2026-10-15T15:37:22+00:00"
summary = "pursuit open T0642: Fix 29: a milestone source that names no reference joins its intent"
metric_command = ""
drains = []
hooks = []
+++

criteria: _milestone_parts(value, root, notes) keeps a source only when it carries an http(s) link or names a references/ file by name or stem (index.json excluded); any other source's words join the part's intent with a note; with no root a source is taken at its word; found and plan pass the project root
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_milestone_source_that_names_no_reference_joins_its_intent'
budget: 40000 tokens
