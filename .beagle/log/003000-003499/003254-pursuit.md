+++
id = "003254-pursuit"
ordinal = 3254
kind = "pursuit"
timestamp = "2026-10-15T07:36:30+00:00"
summary = "pursuit open T0628: Fix 17: quick retries after a reasoning-time cut"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a reasoning-time cut, the nudge's reply is cut at a quarter of the turn budget, and four nudges may follow time cuts in a row; other output-limit stops keep the bound of two.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_session_output_limit_nudge.py tests/test_session_output_limit.py -k 'quarter_budget or nudge or limit'
budget: 40000 tokens
