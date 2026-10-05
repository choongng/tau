+++
id = "001074-pursuit"
ordinal = 1074
kind = "pursuit"
timestamp = "2026-10-05T11:53:41+00:00"
summary = "pursuit sweep at close T0260: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6361 chunks, 6361 sampled, 134 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 3 path(s): 14 identical, 120 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_coding_session.py:6071 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  0.83  examples/extensions/beagle.py:2180 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.78  tests/test_coding_session.py:7587 bash
        tests/test_repeat_breaker_reset.py:24 execute
  0.73  examples/extensions/beagle.py:1017 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.72  tests/test_coding_session.py:7438 iterator
        tests/test_request_gate.py:41 iterator
  ... (+129 more in this bucket)
sample_cruft: 3 sampled, 0 flagged
