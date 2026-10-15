+++
id = "003310-pursuit"
ordinal = 3310
kind = "pursuit"
timestamp = "2026-10-15T14:22:52+00:00"
summary = "pursuit open T0640: Fix 27: the found-first steer lists a cut reference's numbered sections"
metric_command = ""
drains = []
hooks = []
+++

criteria: The found-first steer lists, after a cut reference's opening, the reference's numbered section titles
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_found_first_steer_lists_a_cut_references_numbered_sections'
budget: 40000 tokens
