+++
id = "000070-pursuit"
ordinal = 70
kind = "pursuit"
timestamp = "2026-10-03T12:52:19+00:00"
summary = "pursuit sweep at close T0029: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5614 chunks, 5614 sampled, 55 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 11 identical, 44 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1691 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  0.88  src/tau_coding/session.py:3707 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4497 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:998 tools
  0.81  src/tau_coding/extensions/provider_registry.py:171 diagnostics
        src/tau_coding/session.py:998 tools
  ... (+50 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
