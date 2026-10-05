+++
id = "001197-pursuit"
ordinal = 1197
kind = "pursuit"
timestamp = "2026-10-05T19:25:25+00:00"
summary = "pursuit sweep at close T0284: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6473 chunks, 6473 sampled, 106 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 13 identical, 93 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2284 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.73  examples/extensions/beagle.py:1035 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1311 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2030 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1252 _worker_model
        examples/extensions/beagle.py:1259 _worker_provider
  ... (+101 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
