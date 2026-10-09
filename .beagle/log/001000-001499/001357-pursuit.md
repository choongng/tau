+++
id = "001357-pursuit"
ordinal = 1357
kind = "pursuit"
timestamp = "2026-10-09T23:03:04+00:00"
summary = "pursuit sweep at close T0324: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6818 chunks, 6818 sampled, 23 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 16 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2015 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_repeat_breaker_reset.py:24 execute
        tests/test_session_template_tokens.py:68 record
  1.00  tests/test_session_output_limit.py:164 _nudges
        tests/test_session_template_tokens.py:249 _follow_ups
  0.88  src/tau_coding/session.py:4247 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5097 _resolved_labels
  ... (+18 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
