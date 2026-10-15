+++
id = "003387-pursuit"
ordinal = 3387
kind = "pursuit"
timestamp = "2026-10-15T22:58:07+00:00"
summary = "pursuit open T0657: Fix 35: a cite whose line and anchor are another reference's is moved there, not re-anchored"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a cases worker, a cite whose anchor is not its named reference's at that line, but whose every line#anchor is exactly one other references/ file's, is rewritten in the case file and the open's --cites to that reference with its anchors kept, and the step's reply says it was moved; other mismatched cites are re-anchored by line as before.
decided by: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'moves_a_cite or reanchors'
budget: 60000 tokens
