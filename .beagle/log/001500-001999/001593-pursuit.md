+++
id = "001593-pursuit"
ordinal = 1593
kind = "pursuit"
timestamp = "2026-10-10T17:15:59+00:00"
summary = "pursuit sweep at close T0370: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6939 chunks, 6939 sampled, 116 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 11 identical, 105 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2332 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.73  examples/extensions/beagle.py:1047 _AwaitedScope
        src/tau_coding/extensions/runtime.py:176 ExtensionCommand
  0.70  examples/extensions/beagle.py:1333 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2078 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1264 _worker_model
        examples/extensions/beagle.py:1271 _worker_provider
  ... (+111 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
