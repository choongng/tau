+++
id = "003242-pursuit"
ordinal = 3242
kind = "pursuit"
timestamp = "2026-10-15T05:49:33+00:00"
summary = "pursuit open T0626: Fix 15: a case cite is re-anchored to the line it names"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a cases worker, each case cite whose anchor is not its line's, by `beagle refs show`, is rewritten in the case file and in the open's --cites with that line's anchor, and the step's reply names the change.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_reanchors_a_cite_to_the_line_it_names
budget: 40000 tokens
