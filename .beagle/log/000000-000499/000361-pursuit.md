+++
id = "000361-pursuit"
ordinal = 361
kind = "pursuit"
timestamp = "2026-10-03T21:06:13+00:00"
summary = "pursuit sweep at close T0082: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5791 chunks, 5791 sampled, 46 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 40 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:874 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1130 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1602 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1080 _worker_model
        examples/extensions/beagle.py:1087 _worker_provider
  1.00  examples/extensions/beagle.py:1130 _make_dispatch_result
        examples/extensions/beagle.py:1602 _step_result
  ... (+41 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
