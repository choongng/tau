+++
id = "002950-pursuit"
ordinal = 2950
kind = "pursuit"
timestamp = "2026-10-14T03:21:15+00:00"
summary = "pursuit sweep at close T0571: 5 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6945 chunks, 6945 sampled, 110 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 102 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:1496 _AwaitedScope
        src/tau_coding/extensions/runtime.py:179 ExtensionCommand
  0.70  examples/extensions/beagle.py:1870 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2877 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1771 _worker_output_tokens
        examples/extensions/beagle.py:1780 _worker_max_turns
  1.00  examples/extensions/beagle.py:1870 _make_dispatch_result
        examples/extensions/beagle.py:2877 _step_result
  ... (+105 more in this bucket)
sample_similarity: 1987 chunks, 1987 sampled, 0 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 3 path(s): 0 identical, 0 diverged; every pair touching them is listed, copies across files first
sample_cruft: 5 sampled, 3 flagged
  FLAG  dev-notes/contract-first/design.md  <- untracked-not-ignored
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
