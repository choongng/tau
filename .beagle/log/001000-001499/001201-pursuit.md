+++
id = "001201-pursuit"
ordinal = 1201
kind = "pursuit"
timestamp = "2026-10-05T19:34:36+00:00"
summary = "pursuit sweep at close T0285: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6482 chunks, 6482 sampled, 113 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 16 identical, 97 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_agent/harness.py:52 SimpleCancellationToken
        tests/test_coding_tools.py:44 FakeCancellationToken
  0.83  examples/extensions/beagle.py:2301 _newline_only
        src/tau_coding/tools.py:921 normalize_to_lf
  0.83  tests/test_coding_tools.py:31 image_bytes
        tests/test_image_processing.py:16 image_bytes
  0.77  src/tau_coding/rpc.py:546 _required_string
        src/tau_coding/tools.py:1035 _str_arg
  0.73  examples/extensions/beagle.py:1042 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  ... (+108 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
