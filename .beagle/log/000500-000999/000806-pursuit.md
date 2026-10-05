+++
id = "000806-pursuit"
ordinal = 806
kind = "pursuit"
timestamp = "2026-10-05T01:06:14+00:00"
summary = "pursuit sweep at close T0206: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6162 chunks, 6162 sampled, 91 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 10 identical, 81 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:992 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1259 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:1830 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1209 _worker_model
        examples/extensions/beagle.py:1216 _worker_provider
  1.00  examples/extensions/beagle.py:1259 _make_dispatch_result
        examples/extensions/beagle.py:1830 _step_result
  ... (+86 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
