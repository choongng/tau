+++
id = "003186-pursuit"
ordinal = 3186
kind = "pursuit"
timestamp = "2026-10-15T02:16:22+00:00"
summary = "pursuit prove T0618: WITNESSED — refuses when session.py's `elif budget is not None and _reasoning_clock() …` is put back as `elif False:`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_session_output_limit_nudge.py tests/test_beagle_example_extension.py -k 'turn_budget or no_time_budget or worker_bash_default_timeout_is_short'
refutes: refuses when session.py's `elif budget is not None and _reasoning_clock() …` is put back as `elif False:` (proven 2026-10-15T02:15:24+00:00; refused at FAILED tests/test_session_output_limit_nudge.py::test_reasoning_past_the_turn_budget_is_cut_and_asked_to_act[asyncio])
refused after 4s of a 1s check at: FAILED tests/test_session_output_limit_nudge.py::test_reasoning_past_the_turn_budget_is_cut_and_asked_to_act[asyncio]
refused with: 1 failed, 2 passed, 717 deselected in 3.33s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
