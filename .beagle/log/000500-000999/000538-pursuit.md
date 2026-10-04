+++
id = "000538-pursuit"
ordinal = 538
kind = "pursuit"
timestamp = "2026-10-04T05:24:37+00:00"
summary = "pursuit open T0130: R15 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R15 ran mimo-v2.6-9b-q4 on tau HEAD (clean, 1h cap, prompt byte for byte) via launch.sh; scorecard and grade made; dev-notes/itc-runs/R15.md holds the grader line and Scorecard block matching them.
decided by: sh -c 'echo "a5d0a361db42aafceec5f5b3bd767e66029d574b1c6dfc773f880d0c2d49f6d1  .beagle/checks/T0130/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0130/check.sh'
budget: 40000 tokens
