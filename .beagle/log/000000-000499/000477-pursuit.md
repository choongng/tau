+++
id = "000477-pursuit"
ordinal = 477
kind = "pursuit"
timestamp = "2026-10-04T03:00:49+00:00"
summary = "pursuit sweep at close T0120: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5860 chunks, 5860 sampled, 51 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 45 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:880 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1136 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1608 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1086 _worker_model
        examples/extensions/beagle.py:1093 _worker_provider
  1.00  examples/extensions/beagle.py:1136 _make_dispatch_result
        examples/extensions/beagle.py:1608 _step_result
  ... (+46 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
