+++
id = "001394-pursuit"
ordinal = 1394
kind = "pursuit"
timestamp = "2026-10-10T00:45:50+00:00"
summary = "pursuit sweep at close T0330: 6 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6851 chunks, 6851 sampled, 139 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 6 path(s): 19 identical, 120 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2017 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  0.88  src/tau_coding/session.py:4275 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.84  tests/test_session_output_limit.py:325 test_in_a_row_bound_still_stops_a_model_that_never_acts
        tests/test_session_output_limit_nudge.py:34 test_nudges_in_a_row_stay_bounded_with_a_steering_message_beside_one
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5125 _resolved_labels
  ... (+134 more in this bucket)
sample_cruft: 6 sampled, 0 flagged
