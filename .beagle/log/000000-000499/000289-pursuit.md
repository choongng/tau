+++
id = "000289-pursuit"
ordinal = 289
kind = "pursuit"
timestamp = "2026-10-03T20:06:09+00:00"
summary = "pursuit sweep at close T0068: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5750 chunks, 5750 sampled, 43 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 37 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:870 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1126 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1561 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1076 _worker_model
        examples/extensions/beagle.py:1083 _worker_provider
  1.00  examples/extensions/beagle.py:1126 _make_dispatch_result
        examples/extensions/beagle.py:1561 _step_result
  ... (+38 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
