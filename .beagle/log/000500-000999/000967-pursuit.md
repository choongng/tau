+++
id = "000967-pursuit"
ordinal = 967
kind = "pursuit"
timestamp = "2026-10-05T07:44:11+00:00"
summary = "pursuit sweep at close T0237: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6258 chunks, 6258 sampled, 145 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 18 identical, 127 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1725 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  1.00  tests/test_coding_session.py:5947 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  0.88  src/tau_coding/session.py:3742 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  examples/extensions/beagle.py:2125 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4579 _resolved_labels
  ... (+140 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
