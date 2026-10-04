+++
id = "000691-pursuit"
ordinal = 691
kind = "pursuit"
timestamp = "2026-10-04T13:17:25+00:00"
summary = "pursuit sweep at close T0162: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6078 chunks, 6078 sampled, 43 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 3 path(s): 6 identical, 37 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_agent_loop_turn_cap.py:21 _collect
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_anthropic_sse.py:10 _collect
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_request_gate.py:69 _drain
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_tau_ai.py:47 _collect
  1.00  tests/test_coding_session.py:5878 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  ... (+38 more in this bucket)
sample_cruft: 3 sampled, 0 flagged
