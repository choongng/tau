+++
id = "001617-pursuit"
ordinal = 1617
kind = "pursuit"
timestamp = "2026-10-10T18:53:07+00:00"
summary = "pursuit sweep at close T0378: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6955 chunks, 6955 sampled, 19 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 5 identical, 14 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2108 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  0.88  src/tau_coding/session.py:4410 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.84  tests/test_session_output_limit.py:325 test_in_a_row_bound_still_stops_a_model_that_never_acts
        tests/test_session_output_limit_nudge.py:43 test_nudges_in_a_row_stay_bounded_with_a_steering_message_beside_one
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5260 _resolved_labels
  0.81  src/tau_coding/extensions/provider_registry.py:166 durable_providers
        src/tau_coding/session.py:1294 tools
  ... (+14 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
