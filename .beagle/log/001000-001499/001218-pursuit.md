+++
id = "001218-pursuit"
ordinal = 1218
kind = "pursuit"
timestamp = "2026-10-05T20:57:44+00:00"
summary = "pursuit sweep at close T0288: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6487 chunks, 6487 sampled, 107 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 13 identical, 94 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2301 _newline_only
        src/tau_coding/tools.py:921 normalize_to_lf
  0.73  examples/extensions/beagle.py:1042 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1328 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2047 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1259 _worker_model
        examples/extensions/beagle.py:1266 _worker_provider
  ... (+102 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
