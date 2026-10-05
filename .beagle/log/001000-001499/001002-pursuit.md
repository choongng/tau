+++
id = "001002-pursuit"
ordinal = 1002
kind = "pursuit"
timestamp = "2026-10-05T08:16:10+00:00"
summary = "pursuit sweep at close T0240: 5 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6275 chunks, 6275 sampled, 147 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 4 path(s): 18 identical, 129 diverged; every pair touching them is listed, copies across files first
  1.00  src/tau_coding/session.py:1729 queue_update_event
        tests/test_tui_app.py:556 queue_update_event
  1.00  tests/test_coding_session.py:6004 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  0.88  src/tau_coding/session.py:3746 _diagnostic_context
        tests/test_tui_app.py:556 queue_update_event
  0.83  examples/extensions/beagle.py:2125 _newline_only
        src/tau_coding/tools.py:896 normalize_to_lf
  0.83  src/tau_agent/session/memory.py:128 _resolve_labels
        src/tau_coding/session.py:4598 _resolved_labels
  ... (+142 more in this bucket)
sample_similarity: 1473 chunks, 1473 sampled, 10 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 1 path(s): 0 identical, 10 diverged; every pair touching them is listed, copies across files first
  0.45  dev-notes/itc-runs/R23.md:7 Scorecard
        dev-notes/itc-runs/R26.md:7 Scorecard
  0.39  dev-notes/itc-runs/R19.md:7 Scorecard
        dev-notes/itc-runs/R26.md:7 Scorecard
  0.31  dev-notes/itc-runs/R13.md:7 Scorecard
        dev-notes/itc-runs/R26.md:7 Scorecard
  0.28  dev-notes/itc-runs/R10.md:7 Scorecard
        dev-notes/itc-runs/R26.md:7 Scorecard
  0.25  dev-notes/itc-runs/R04.md:7 Scorecard
        dev-notes/itc-runs/R26.md:7 Scorecard
  ... (+5 more in this bucket)
sample_cruft: 5 sampled, 0 flagged
