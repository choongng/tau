+++
id = "001123-pursuit"
ordinal = 1123
kind = "pursuit"
timestamp = "2026-10-05T14:25:09+00:00"
summary = "pursuit sweep at close T0268: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6406 chunks, 6406 sampled, 118 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 17 identical, 101 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1729 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  0.88  src/tau_coding/session.py:3746 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  examples/extensions/beagle.py:2205 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4598 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1014 tools
  ... (+113 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
