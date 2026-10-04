+++
id = "000549-pursuit"
ordinal = 549
kind = "pursuit"
timestamp = "2026-10-04T06:38:55+00:00"
summary = "pursuit sweep at close T0132: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5939 chunks, 5939 sampled, 61 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 7 identical, 54 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:882 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1138 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1610 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1088 _worker_model
        examples/extensions/beagle.py:1095 _worker_provider
  1.00  examples/extensions/beagle.py:1138 _make_dispatch_result
        examples/extensions/beagle.py:1610 _step_result
  ... (+56 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
