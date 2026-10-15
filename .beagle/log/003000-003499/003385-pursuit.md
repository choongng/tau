+++
id = "003385-pursuit"
ordinal = 3385
kind = "pursuit"
timestamp = "2026-10-15T22:36:30+00:00"
summary = "pursuit sweep at close T0632: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 7012 chunks, 7012 sampled, 115 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 107 diverged; every pair touching them is listed, copies across files first
  0.70  examples/extensions/beagle.py:1729 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2718 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1630 _worker_output_tokens
        examples/extensions/beagle.py:1639 _worker_max_turns
  1.00  examples/extensions/beagle.py:1729 _make_dispatch_result
        examples/extensions/beagle.py:2718 _step_result
  1.00  examples/extensions/beagle.py:16654 _command_pursuit
        examples/extensions/beagle.py:16663 _command_pursuit_run
  ... (+110 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
