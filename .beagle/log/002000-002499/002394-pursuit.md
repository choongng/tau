+++
id = "002394-pursuit"
ordinal = 2394
kind = "pursuit"
timestamp = "2026-10-12T14:27:13+00:00"
summary = "pursuit sweep at close T0468: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 7174 chunks, 7174 sampled, 26 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 20 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:2145 queue_update_event
        tests/test_tui_app.py:559 queue_update_event
  1.00  tests/test_session_output_limit.py:160 _nudges
        tests/test_session_template_tokens.py:287 _follow_ups
  0.88  src/tau_coding/session.py:4388 _diagnostic_context
        tests/test_tui_app.py:559 queue_update_event
  0.84  tests/test_session_output_limit.py:310 test_in_a_row_bound_still_stops_a_model_that_never_acts
        tests/test_session_output_limit_nudge.py:43 test_nudges_in_a_row_stay_bounded_with_a_steering_message_beside_one
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:5238 _resolved_labels
  ... (+21 more in this bucket)
sample_similarity: 1931 chunks, 1931 sampled, 0 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 2 path(s): 0 identical, 0 diverged; every pair touching them is listed, copies across files first
sample_cruft: 4 sampled, 2 flagged
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
