+++
id = "000606-pursuit"
ordinal = 606
kind = "pursuit"
timestamp = "2026-10-04T09:08:07+00:00"
summary = "pursuit sweep at close T0144: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6008 chunks, 6008 sampled, 67 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 60 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:901 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1168 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1702 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1118 _worker_model
        examples/extensions/beagle.py:1125 _worker_provider
  1.00  examples/extensions/beagle.py:1168 _make_dispatch_result
        examples/extensions/beagle.py:1702 _step_result
  ... (+62 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
