+++
id = "000417-pursuit"
ordinal = 417
kind = "pursuit"
timestamp = "2026-10-04T00:51:39+00:00"
summary = "pursuit sweep at close T0107: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5809 chunks, 5809 sampled, 48 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 42 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:879 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1135 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1607 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1085 _worker_model
        examples/extensions/beagle.py:1092 _worker_provider
  1.00  examples/extensions/beagle.py:1135 _make_dispatch_result
        examples/extensions/beagle.py:1607 _step_result
  ... (+43 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
