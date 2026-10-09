+++
id = "001299-pursuit"
ordinal = 1299
kind = "pursuit"
timestamp = "2026-10-09T21:29:53+00:00"
summary = "pursuit sweep at close T0310: 4 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6785 chunks, 6785 sampled, 116 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 3 path(s): 12 identical, 104 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2308 _newline_only
        src/tau_coding/tools.py:921 normalize_to_lf
  0.83  tests/test_coding_session.py:5222 truncated
        tests/test_session_output_limit.py:135 _truncated
  0.77  tests/test_coding_session.py:5175 truncated
        tests/test_session_output_limit.py:135 _truncated
  0.75  tests/test_coding_session.py:5037 fetch
        tests/test_session_output_limit.py:97 fetch
  0.73  examples/extensions/beagle.py:1047 _AwaitedScope
        src/tau_coding/extensions/runtime.py:176 ExtensionCommand
  ... (+111 more in this bucket)
sample_similarity: 1619 chunks, 1619 sampled, 10 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 1 path(s): 0 identical, 10 diverged; every pair touching them is listed, copies across files first
  0.30  dev-notes/itc-runs/R24.md:7 Scorecard
        dev-notes/itc-runs/R36.md:7 Scorecard
  0.27  dev-notes/itc-runs/R10.md:7 Scorecard
        dev-notes/itc-runs/R36.md:7 Scorecard
  0.27  dev-notes/itc-runs/R32.md:7 Scorecard
        dev-notes/itc-runs/R36.md:7 Scorecard
  0.25  dev-notes/itc-runs/R05.md:7 Scorecard
        dev-notes/itc-runs/R36.md:7 Scorecard
  0.25  dev-notes/itc-runs/R18.md:7 Scorecard
        dev-notes/itc-runs/R36.md:7 Scorecard
  ... (+5 more in this bucket)
sample_cruft: 4 sampled, 0 flagged
