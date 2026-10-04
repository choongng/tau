+++
id = "000570-pursuit"
ordinal = 570
kind = "pursuit"
timestamp = "2026-10-04T07:36:57+00:00"
summary = "pursuit sweep at close T0136: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5964 chunks, 5964 sampled, 63 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 56 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:882 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1138 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1640 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1088 _worker_model
        examples/extensions/beagle.py:1095 _worker_provider
  1.00  examples/extensions/beagle.py:1138 _make_dispatch_result
        examples/extensions/beagle.py:1640 _step_result
  ... (+58 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
