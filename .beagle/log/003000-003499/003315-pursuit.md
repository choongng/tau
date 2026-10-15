+++
id = "003315-pursuit"
ordinal = 3315
kind = "pursuit"
timestamp = "2026-10-15T14:59:14+00:00"
summary = "pursuit open T0641: Fix 28: a numbered or initialization setup milestone is layout"
metric_command = ""
drains = []
hooks = []
+++

criteria: _layout_only_milestone reads a title past a leading step number (1:, 2., 3), Step 2.) and counts initialization, initialisation and bootstrap as layout words; work titles so numbered stay work
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_a_numbered_or_initialization_setup_milestone_is_layout'
budget: 40000 tokens
