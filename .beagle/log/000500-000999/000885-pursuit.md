+++
id = "000885-pursuit"
ordinal = 885
kind = "pursuit"
timestamp = "2026-10-05T04:13:08+00:00"
summary = "pursuit sweep at close T0222: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6217 chunks, 6217 sampled, 93 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 10 identical, 83 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:1016 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1283 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:1870 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1233 _worker_model
        examples/extensions/beagle.py:1240 _worker_provider
  1.00  examples/extensions/beagle.py:1283 _make_dispatch_result
        examples/extensions/beagle.py:1870 _step_result
  ... (+88 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
