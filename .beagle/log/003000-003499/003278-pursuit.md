+++
id = "003278-pursuit"
ordinal = 3278
kind = "pursuit"
timestamp = "2026-10-15T10:05:51+00:00"
summary = "pursuit sweep at close T0633: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6987 chunks, 6987 sampled, 113 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 105 diverged; every pair touching them is listed, copies across files first
  0.70  examples/extensions/beagle.py:1717 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2705 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1618 _worker_output_tokens
        examples/extensions/beagle.py:1627 _worker_max_turns
  1.00  examples/extensions/beagle.py:1717 _make_dispatch_result
        examples/extensions/beagle.py:2705 _step_result
  1.00  examples/extensions/beagle.py:16399 _command_pursuit
        examples/extensions/beagle.py:16408 _command_pursuit_run
  ... (+108 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
