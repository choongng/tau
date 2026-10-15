+++
id = "003185-pursuit"
ordinal = 3185
kind = "pursuit"
timestamp = "2026-10-15T01:58:25+00:00"
summary = "pursuit open T0618: fix 7: a worker's turn reasons for at most 240 s before tau cuts it and asks it to act"
metric_command = ""
drains = []
hooks = []
+++

criteria: with TAU_TURN_REASONING_SECONDS set, the request guard ends a turn whose reasoning outlasts it before a tool call as a length stop with a reasoning_time_cut diagnostic, replays its reasoning and sends TIME_CUT_NUDGE; unset, no budget; beagle workers run with 240 s unless the env sets one
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_session_output_limit_nudge.py tests/test_beagle_example_extension.py -k 'turn_budget or no_time_budget or worker_bash_default_timeout_is_short'
budget: 200000 tokens
