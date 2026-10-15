+++
id = "003324-pursuit"
ordinal = 3324
kind = "pursuit"
timestamp = "2026-10-15T15:44:23+00:00"
summary = "pursuit sweep at close T0642: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6997 chunks, 6997 sampled, 114 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 106 diverged; every pair touching them is listed, copies across files first
  0.70  examples/extensions/beagle.py:1722 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2710 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1623 _worker_output_tokens
        examples/extensions/beagle.py:1632 _worker_max_turns
  1.00  examples/extensions/beagle.py:1722 _make_dispatch_result
        examples/extensions/beagle.py:2710 _step_result
  1.00  examples/extensions/beagle.py:16508 _command_pursuit
        examples/extensions/beagle.py:16517 _command_pursuit_run
  ... (+109 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
