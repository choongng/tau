+++
id = "001294-pursuit"
ordinal = 1294
kind = "pursuit"
timestamp = "2026-10-09T21:23:37+00:00"
summary = "pursuit sweep at close T0308: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6775 chunks, 6775 sampled, 57 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 3 path(s): 9 identical, 48 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1988 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_coding_session.py:6240 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  1.00  tests/test_coding_session.py:6520 fail_provider
        tests/test_updater.py:174 fail_launch
  0.88  src/tau_coding/session.py:4188 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5038 _resolved_labels
  ... (+52 more in this bucket)
sample_cruft: 3 sampled, 0 flagged
