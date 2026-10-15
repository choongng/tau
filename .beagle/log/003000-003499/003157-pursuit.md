+++
id = "003157-pursuit"
ordinal = 3157
kind = "pursuit"
timestamp = "2026-10-15T00:33:54+00:00"
summary = "pursuit open T0612: fix 2: a code worker corrects a pinned case only with the source's words; smoke S04"
metric_command = ""
drains = []
hooks = []
+++

criteria: a pinned case the code worker changes is amended on the record when it quotes its cited lines, else put back
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_real_step.py -k 'corrects_from_the_source or changed_without_the_source_words'
budget: 200000 tokens
