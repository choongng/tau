+++
id = "003258-pursuit"
ordinal = 3258
kind = "pursuit"
timestamp = "2026-10-15T07:44:13+00:00"
summary = "pursuit sweep at close T0628: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6981 chunks, 6981 sampled, 18 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 5 identical, 13 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2220 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  0.88  src/tau_coding/session.py:4469 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5319 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1406 tools
  0.81  src/tau_coding/extensions/provider_registry.py:171 diagnostics
        src/tau_coding/session.py:1406 tools
  ... (+13 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
