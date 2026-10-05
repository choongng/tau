+++
id = "001012-pursuit"
ordinal = 1012
kind = "pursuit"
timestamp = "2026-10-05T08:33:42+00:00"
summary = "pursuit open T0247: R27 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R27 ran mimo on cobs_prompt.txt from a clean ~/cobs under the 1h cap with tau at HEAD; dev-notes/itc-runs/R27.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "2d0586c976bb424ada97c40c35a530c2eaba1c38878828c4c525112b2e56adac  .beagle/checks/T0247/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0247/check.sh'
budget: 40000 tokens
