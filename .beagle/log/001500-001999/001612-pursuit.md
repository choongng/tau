+++
id = "001612-pursuit"
ordinal = 1612
kind = "pursuit"
timestamp = "2026-10-10T18:49:51+00:00"
summary = "pursuit sweep at close T0377: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6949 chunks, 6949 sampled, 20 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 5 identical, 15 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2106 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  0.88  src/tau_coding/session.py:4395 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5245 _resolved_labels
  0.83  tests/test_coding_session.py:5037 fetch
        tests/test_tool_history.py:165 execute
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1292 tools
  ... (+15 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
