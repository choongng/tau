+++
id = "001168-pursuit"
ordinal = 1168
kind = "pursuit"
timestamp = "2026-10-05T17:30:58+00:00"
summary = "pursuit sweep at close T0278: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6438 chunks, 6438 sampled, 104 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 12 identical, 92 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2243 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.73  examples/extensions/beagle.py:1029 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1296 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:1989 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1246 _worker_model
        examples/extensions/beagle.py:1253 _worker_provider
  ... (+99 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
