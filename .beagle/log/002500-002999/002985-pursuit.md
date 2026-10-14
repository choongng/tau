+++
id = "002985-pursuit"
ordinal = 2985
kind = "pursuit"
timestamp = "2026-10-14T04:03:50+00:00"
summary = "pursuit sweep at close T0578: 5 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6952 chunks, 6952 sampled, 113 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 8 identical, 105 diverged; every pair touching them is listed, copies across files first
  0.73  examples/extensions/beagle.py:1507 _AwaitedScope
        src/tau_coding/extensions/runtime.py:179 ExtensionCommand
  0.70  examples/extensions/beagle.py:1881 _make_dispatch_result
        src/tau_agent/loop.py:458 _error_result
  0.70  examples/extensions/beagle.py:2888 _step_result
        src/tau_agent/loop.py:458 _error_result
  1.00  examples/extensions/beagle.py:1782 _worker_output_tokens
        examples/extensions/beagle.py:1791 _worker_max_turns
  1.00  examples/extensions/beagle.py:1881 _make_dispatch_result
        examples/extensions/beagle.py:2888 _step_result
  ... (+108 more in this bucket)
sample_similarity: 1987 chunks, 1987 sampled, 0 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 3 path(s): 0 identical, 0 diverged; every pair touching them is listed, copies across files first
sample_cruft: 5 sampled, 3 flagged
  FLAG  dev-notes/contract-first/design.md  <- untracked-not-ignored
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
