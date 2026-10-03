+++
id = "000081-pursuit"
ordinal = 81
kind = "pursuit"
timestamp = "2026-10-03T13:03:24+00:00"
summary = "pursuit sweep at close T0036: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5616 chunks, 5616 sampled, 328 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 39 identical, 289 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_agent_loop.py:38 _collect
        tests/test_tau_ai.py:47 _collect
  1.00  tests/test_agent_loop_turn_cap.py:21 _collect
        tests/test_tau_ai.py:47 _collect
  1.00  tests/test_anthropic_sse.py:10 _collect
        tests/test_tau_ai.py:47 _collect
  1.00  tests/test_anthropic_sse.py:16 handler
        tests/test_tau_ai.py:2168 handler
  1.00  tests/test_anthropic_sse.py:16 handler
        tests/test_tau_ai.py:2288 handler
  ... (+323 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
