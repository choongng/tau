+++
id = "000273-pursuit"
ordinal = 273
kind = "pursuit"
timestamp = "2026-10-03T19:59:15+00:00"
summary = "pursuit sweep at close T0066: 5 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5740 chunks, 5740 sampled, 62 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 5 path(s): 11 identical, 51 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1722 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  0.88  src/tau_coding/session.py:3739 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4529 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1007 tools
  0.81  src/tau_coding/extensions/provider_registry.py:171 diagnostics
        src/tau_coding/session.py:1007 tools
  ... (+57 more in this bucket)
sample_cruft: 5 sampled, 0 flagged
