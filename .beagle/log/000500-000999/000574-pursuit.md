+++
id = "000574-pursuit"
ordinal = 574
kind = "pursuit"
timestamp = "2026-10-04T07:43:44+00:00"
summary = "pursuit sweep at close T0137: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5969 chunks, 5969 sampled, 63 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 56 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:901 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1157 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1661 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1107 _worker_model
        examples/extensions/beagle.py:1114 _worker_provider
  1.00  examples/extensions/beagle.py:1157 _make_dispatch_result
        examples/extensions/beagle.py:1661 _step_result
  ... (+58 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
