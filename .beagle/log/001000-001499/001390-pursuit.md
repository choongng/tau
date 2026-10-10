+++
id = "001390-pursuit"
ordinal = 1390
kind = "pursuit"
timestamp = "2026-10-10T00:42:40+00:00"
summary = "pursuit sweep at close T0328: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6847 chunks, 6847 sampled, 121 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 14 identical, 107 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.77  src/tau_coding/rpc.py:546 _required_string
        src/tau_coding/tools.py:1067 _str_arg
  0.73  examples/extensions/beagle.py:1047 _AwaitedScope
        src/tau_coding/extensions/runtime.py:176 ExtensionCommand
  0.70  examples/extensions/beagle.py:1333 _make_dispatch_result
        src/tau_agent/loop.py:453 _error_result
  0.70  examples/extensions/beagle.py:2059 _step_result
        src/tau_agent/loop.py:453 _error_result
  ... (+116 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
