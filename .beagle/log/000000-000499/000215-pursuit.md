+++
id = "000215-pursuit"
ordinal = 215
kind = "pursuit"
timestamp = "2026-10-03T18:31:00+00:00"
summary = "pursuit sweep at close T0061: 5 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5719 chunks, 5719 sampled, 60 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 5 path(s): 11 identical, 49 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1715 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  0.88  src/tau_coding/session.py:3732 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4522 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1007 tools
  0.81  src/tau_coding/extensions/provider_registry.py:171 diagnostics
        src/tau_coding/session.py:1007 tools
  ... (+55 more in this bucket)
sample_cruft: 5 sampled, 0 flagged
