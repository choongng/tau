+++
id = "000658-pursuit"
ordinal = 658
kind = "pursuit"
timestamp = "2026-10-04T11:34:43+00:00"
summary = "pursuit sweep at close T0155: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6053 chunks, 6053 sampled, 85 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 10 identical, 75 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:902 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1169 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1738 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1119 _worker_model
        examples/extensions/beagle.py:1126 _worker_provider
  1.00  examples/extensions/beagle.py:1169 _make_dispatch_result
        examples/extensions/beagle.py:1738 _step_result
  ... (+80 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
