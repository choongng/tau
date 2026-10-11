+++
id = "001820-pursuit"
ordinal = 1820
kind = "pursuit"
timestamp = "2026-10-11T22:26:34+00:00"
summary = "pursuit sweep at close T0443: 3 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 1778 chunks, 1778 sampled, 13 candidate pair(s) at Jaccard >= 0.25 (docs, k=3)
  focused on 3 path(s): 0 identical, 13 diverged; every pair touching them is listed, copies across files first
  0.55  dev-notes/itc-runs/B03.md:17 Scorecard
        dev-notes/itc-runs/B04.md:15 Scorecard
  0.53  dev-notes/itc-runs/B01.md:13 Scorecard
        dev-notes/itc-runs/B04.md:15 Scorecard
  0.42  dev-notes/itc-runs/R05.md:7 Scorecard
        dev-notes/itc-runs/B04.md:15 Scorecard
  0.42  dev-notes/itc-runs/R38.md:7 Scorecard
        dev-notes/itc-runs/B04.md:15 Scorecard
  0.36  dev-notes/itc-runs/B02.md:15 Scorecard
        dev-notes/itc-runs/B04.md:15 Scorecard
  ... (+8 more in this bucket)
sample_cruft: 3 sampled, 3 flagged
  FLAG  dev-notes/itc-runs/B04.md  <- untracked-not-ignored
  FLAG  dev-notes/tui-stream-cpu/upstream-pr.md  <- untracked-not-ignored
  FLAG  dev-notes/upstreaming-candidates.md  <- untracked-not-ignored
