+++
id = "001651-pursuit"
ordinal = 1651
kind = "pursuit"
timestamp = "2026-10-10T21:16:44+00:00"
summary = "pursuit sweep at close T0384: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6977 chunks, 6977 sampled, 117 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 11 identical, 106 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2385 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.73  examples/extensions/beagle.py:1047 _AwaitedScope
        src/tau_coding/extensions/runtime.py:176 ExtensionCommand
  0.70  examples/extensions/beagle.py:1333 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2131 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1264 _worker_model
        examples/extensions/beagle.py:1271 _worker_provider
  ... (+112 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
