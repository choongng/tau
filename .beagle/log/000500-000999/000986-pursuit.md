+++
id = "000986-pursuit"
ordinal = 986
kind = "pursuit"
timestamp = "2026-10-05T08:09:48+00:00"
summary = "pursuit sweep at close T0243: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6275 chunks, 6275 sampled, 51 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 44 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1729 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  1.00  tests/test_coding_session.py:6004 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  0.88  src/tau_coding/session.py:3746 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4598 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1014 tools
  ... (+46 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
