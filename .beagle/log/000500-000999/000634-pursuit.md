+++
id = "000634-pursuit"
ordinal = 634
kind = "pursuit"
timestamp = "2026-10-04T11:05:47+00:00"
summary = "pursuit sweep at close T0150: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6025 chunks, 6025 sampled, 68 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 60 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:901 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1168 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1700 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1118 _worker_model
        examples/extensions/beagle.py:1125 _worker_provider
  1.00  examples/extensions/beagle.py:1168 _make_dispatch_result
        examples/extensions/beagle.py:1700 _step_result
  ... (+63 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
