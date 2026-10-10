+++
id = "001555-pursuit"
ordinal = 1555
kind = "pursuit"
timestamp = "2026-10-10T15:11:06+00:00"
summary = "pursuit sweep at close T0364: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6927 chunks, 6927 sampled, 115 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
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
sample_similarity: 1663 chunks, 1663 sampled, 9 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 1 path(s): 0 identical, 9 diverged; every pair touching them is listed, copies across files first
  0.52  dev-notes/itc-runs/B02.md:15 Scorecard
        dev-notes/itc-runs/R38.md:7 Scorecard
  0.45  dev-notes/itc-runs/B01.md:13 Scorecard
        dev-notes/itc-runs/B02.md:15 Scorecard
  0.38  dev-notes/itc-runs/B02.md:15 Scorecard
        dev-notes/itc-runs/R07.md:7 Scorecard
  0.34  dev-notes/itc-runs/B02.md:15 Scorecard
        dev-notes/itc-runs/R03.md:5 Scorecard
  0.34  dev-notes/itc-runs/B02.md:15 Scorecard
        dev-notes/itc-runs/R05.md:7 Scorecard
  ... (+4 more in this bucket)
sample_cruft: 3 sampled, 0 flagged
