+++
id = "003290-pursuit"
ordinal = 3290
kind = "pursuit"
timestamp = "2026-10-15T11:55:23+00:00"
summary = "pursuit open T0636: Fix 23: a setup milestone whose purpose names the pursuit is dropped"
metric_command = ""
drains = []
hooks = []
+++

criteria: _setup_milestone drops a milestone whose title holds a setup act other than a generic verb (create, start) and whose text names beagle or the pursuit; 'Create the clock type: the pursuit's first module' and 'Implement the beagle exporter - configure its output paths' are kept
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'setup_milestone'
budget: 40000 tokens
