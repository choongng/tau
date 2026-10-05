+++
id = "000820-pursuit"
ordinal = 820
kind = "pursuit"
timestamp = "2026-10-05T01:32:27+00:00"
summary = "pursuit sweep at close T0208: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6176 chunks, 6176 sampled, 93 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 10 identical, 83 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:1015 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1282 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:1853 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1232 _worker_model
        examples/extensions/beagle.py:1239 _worker_provider
  1.00  examples/extensions/beagle.py:1282 _make_dispatch_result
        examples/extensions/beagle.py:1853 _step_result
  ... (+88 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
