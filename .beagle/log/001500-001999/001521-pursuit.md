+++
id = "001521-pursuit"
ordinal = 1521
kind = "pursuit"
timestamp = "2026-10-10T04:38:57+00:00"
summary = "pursuit sweep at close T0349: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6910 chunks, 6910 sampled, 115 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 11 identical, 104 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2323 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.73  examples/extensions/beagle.py:1047 _AwaitedScope
        src/tau_coding/extensions/runtime.py:176 ExtensionCommand
  0.70  examples/extensions/beagle.py:1333 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2069 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1264 _worker_model
        examples/extensions/beagle.py:1271 _worker_provider
  ... (+110 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
