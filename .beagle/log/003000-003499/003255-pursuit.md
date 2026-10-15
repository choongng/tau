+++
id = "003255-pursuit"
ordinal = 3255
kind = "pursuit"
timestamp = "2026-10-15T07:44:01+00:00"
summary = "pursuit prove T0628: WITNESSED — refuses when session.py's `TIME_CUT_REPLY_SHARE = 0.25` is put back as `TIME_CUT_REPLY_SHARE = 1.0`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_session_output_limit_nudge.py tests/test_session_output_limit.py -k 'quarter_budget or nudge or limit'
refutes: refuses when session.py's `TIME_CUT_REPLY_SHARE = 0.25` is put back as `TIME_CUT_REPLY_SHARE = 1.0` (proven 2026-10-15T07:43:03+00:00; refused at FAILED tests/test_session_output_limit_nudge.py::test_a_time_cut_nudges_reply_reasons_on_a_quarter_budget_four_times_in…)
refused after 1s of a 1s check at: FAILED tests/test_session_output_limit_nudge.py::test_a_time_cut_nudges_reply_reasons_on_a_quarter_budget_four_times_in…
refused with: 1 failed, 16 passed in 0.83s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
