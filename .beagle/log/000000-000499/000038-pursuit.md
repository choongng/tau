+++
id = "000038-pursuit"
ordinal = 38
kind = "pursuit"
timestamp = "2026-10-03T11:13:22+00:00"
summary = "pursuit sweep at close T0023: 8 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5553 chunks, 5553 sampled, 64 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 7 path(s): 21 identical, 43 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_agent/harness.py:52 SimpleCancellationToken
        tests/test_coding_tools.py:44 FakeCancellationToken
  1.00  src/tau_agent/harness.py:111 subscribe
        src/tau_coding/tui/app.py:5237 _register_extension_key_interceptor
  1.00  src/tau_coding/session.py:1676 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_agent_loop_turn_cap.py:21 _collect
  1.00  tests/test_agent_loop_turn_cap.py:21 _collect
        tests/test_anthropic_sse.py:10 _collect
  ... (+59 more in this bucket)
sample_similarity: 1189 chunks, 1189 sampled, 0 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 1 path(s): 0 identical, 0 diverged; every pair touching them is listed, copies across files first
sample_cruft: 8 sampled, 0 flagged
