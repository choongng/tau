+++
id = "002204-pursuit"
ordinal = 2204
kind = "pursuit"
timestamp = "2026-10-12T11:06:18+00:00"
summary = "pursuit sweep at close T0423: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 1876 chunks, 1876 sampled, 5 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 3 path(s): 0 identical, 5 diverged; every pair touching them is listed, copies across files first
  0.36  dev-notes/itc-runs/R51.md:41 Scorecard
        dev-notes/itc-runs/R57.md:85 Scorecard
  0.34  dev-notes/itc-runs/R56.md:72 Scorecard
        dev-notes/itc-runs/R57.md:85 Scorecard
  0.34  dev-notes/itc-runs/R56.md:351 T0447 (the lean switch) in this run
        dev-notes/itc-runs/R57.md:417 T0447 (the lean switch) in this run
  0.33  dev-notes/itc-runs/R55.md:406 T0447 (the lean switch) in this run
        dev-notes/itc-runs/R57.md:417 T0447 (the lean switch) in this run
  0.28  dev-notes/itc-runs/R27.md:7 Scorecard
        dev-notes/itc-runs/R57.md:85 Scorecard
sample_cruft: 3 sampled, 2 flagged
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
