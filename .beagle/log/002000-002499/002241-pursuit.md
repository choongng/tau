+++
id = "002241-pursuit"
ordinal = 2241
kind = "pursuit"
timestamp = "2026-10-12T12:12:24+00:00"
summary = "pursuit sweep at close T0424: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 1895 chunks, 1895 sampled, 5 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 3 path(s): 0 identical, 5 diverged; every pair touching them is listed, copies across files first
  0.36  dev-notes/itc-runs/R57.md:417 T0447 (the lean switch) in this run
        dev-notes/itc-runs/R58.md:388 T0447 (the lean switch) in this run
  0.33  dev-notes/itc-runs/R55.md:406 T0447 (the lean switch) in this run
        dev-notes/itc-runs/R58.md:388 T0447 (the lean switch) in this run
  0.27  dev-notes/itc-runs/R57.md:387 [harness] W7's cap kill is counted as a wall timeout, and ta
        dev-notes/itc-runs/R58.md:361 [harness] W10's cap kill is counted as a wall timeout, and t
  0.25  dev-notes/itc-runs/R56.md:351 T0447 (the lean switch) in this run
        dev-notes/itc-runs/R58.md:388 T0447 (the lean switch) in this run
  0.25  dev-notes/itc-runs/R57.md:85 Scorecard
        dev-notes/itc-runs/R58.md:75 Scorecard
sample_cruft: 3 sampled, 2 flagged
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
