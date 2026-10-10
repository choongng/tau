+++
id = "001455-pursuit"
ordinal = 1455
kind = "pursuit"
timestamp = "2026-10-10T02:44:44+00:00"
summary = "pursuit sweep at close T0338: 6 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6881 chunks, 6881 sampled, 146 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 6 path(s): 21 identical, 125 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2088 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_repeat_breaker_reset.py:24 execute
        tests/test_session_template_tokens.py:76 record
  1.00  tests/test_session_output_limit.py:164 _nudges
        tests/test_session_template_tokens.py:261 _follow_ups
  0.88  src/tau_coding/session.py:4377 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  ... (+141 more in this bucket)
sample_cruft: 6 sampled, 0 flagged
