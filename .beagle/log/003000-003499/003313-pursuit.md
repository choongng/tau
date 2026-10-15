+++
id = "003313-pursuit"
ordinal = 3313
kind = "pursuit"
timestamp = "2026-10-15T14:27:59+00:00"
summary = "pursuit sweep at close T0640: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6994 chunks, 6994 sampled, 33 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 3 identical, 30 diverged; every pair touching them is listed, copies across files first
  0.70  examples/extensions/beagle.py:1722 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2710 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1623 _worker_output_tokens
        examples/extensions/beagle.py:1632 _worker_max_turns
  1.00  examples/extensions/beagle.py:1722 _make_dispatch_result
        examples/extensions/beagle.py:2710 _step_result
  1.00  examples/extensions/beagle.py:16460 _command_pursuit
        examples/extensions/beagle.py:16469 _command_pursuit_run
  ... (+28 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
