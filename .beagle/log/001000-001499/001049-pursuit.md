+++
id = "001049-pursuit"
ordinal = 1049
kind = "pursuit"
timestamp = "2026-10-05T11:08:08+00:00"
summary = "pursuit sweep at close T0254: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6327 chunks, 6327 sampled, 99 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 12 identical, 87 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2180 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.73  examples/extensions/beagle.py:1017 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1284 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:1926 _step_result
        src/tau_agent/loop.py:453 _error_result
  1.00  examples/extensions/beagle.py:1234 _worker_model
        examples/extensions/beagle.py:1241 _worker_provider
  ... (+94 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
