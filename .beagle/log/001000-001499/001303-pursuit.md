+++
id = "001303-pursuit"
ordinal = 1303
kind = "pursuit"
timestamp = "2026-10-09T21:31:31+00:00"
summary = "pursuit sweep at close T0313: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6785 chunks, 6785 sampled, 133 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 18 identical, 115 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1999 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_repeat_breaker_reset.py:24 execute
        tests/test_session_template_tokens.py:54 record
  0.88  src/tau_coding/session.py:4199 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  examples/extensions/beagle.py:2308 _newline_only
        src/tau_coding/tools.py:921 normalize_to_lf
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5049 _resolved_labels
  ... (+128 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
