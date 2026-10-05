+++
id = "001144-pursuit"
ordinal = 1144
kind = "pursuit"
timestamp = "2026-10-05T15:56:22+00:00"
summary = "pursuit sweep at close T0275: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6420 chunks, 6420 sampled, 18 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 5 identical, 13 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1736 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  0.88  src/tau_coding/session.py:3753 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4605 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1014 tools
  0.81  src/tau_coding/extensions/provider_registry.py:171 diagnostics
        src/tau_coding/session.py:1014 tools
  ... (+13 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
