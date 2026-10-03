+++
id = "000155-pursuit"
ordinal = 155
kind = "pursuit"
timestamp = "2026-10-03T16:28:27+00:00"
summary = "pursuit sweep at close T0049: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5690 chunks, 5690 sampled, 40 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 6 identical, 34 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:870 _AwaitedScope
        src/tau_coding/extensions/runtime.py:153 ExtensionCommand
  0.70  examples/extensions/beagle.py:1126 _make_dispatch_result
        src/tau_agent/loop.py:429 _error_result
  0.70  examples/extensions/beagle.py:1561 _step_result
        src/tau_agent/loop.py:429 _error_result
  1.00  examples/extensions/beagle.py:1076 _worker_model
        examples/extensions/beagle.py:1083 _worker_provider
  1.00  examples/extensions/beagle.py:1126 _make_dispatch_result
        examples/extensions/beagle.py:1561 _step_result
  ... (+35 more in this bucket)
sample_similarity: 1248 chunks, 1248 sampled, 2 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 1 path(s): 0 identical, 2 diverged; every pair touching them is listed, copies across files first
  0.27  dev-notes/itc-runs/R04.md:7 Scorecard
        dev-notes/itc-runs/R06.md:7 Scorecard
  0.25  dev-notes/itc-runs/R04.md:7 Scorecard
        dev-notes/itc-runs/R05.md:7 Scorecard
sample_cruft: 3 sampled, 0 flagged
