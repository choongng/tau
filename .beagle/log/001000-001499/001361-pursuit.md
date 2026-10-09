+++
id = "001361-pursuit"
ordinal = 1361
kind = "pursuit"
timestamp = "2026-10-09T23:14:18+00:00"
summary = "pursuit sweep at close T0322: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6830 chunks, 6830 sampled, 138 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 19 identical, 119 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2015 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_repeat_breaker_reset.py:24 execute
        tests/test_session_template_tokens.py:68 record
  1.00  tests/test_session_output_limit.py:164 _nudges
        tests/test_session_template_tokens.py:249 _follow_ups
  0.88  src/tau_coding/session.py:4247 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:921 normalize_to_lf
  ... (+133 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
