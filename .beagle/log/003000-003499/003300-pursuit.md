+++
id = "003300-pursuit"
ordinal = 3300
kind = "pursuit"
timestamp = "2026-10-15T13:09:47+00:00"
summary = "pursuit open T0638: Fix 25: the found-first steer carries a short reference whole"
metric_command = ""
drains = []
hooks = []
+++

criteria: The found-first steer shows a reference of at most REFERENCE_WHOLE_CHARS whole with its lines kept, and says of a longer one that the extract is its opening and how many lines it has
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_found_first_steer_carries'
budget: 40000 tokens
