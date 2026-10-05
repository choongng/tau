+++
id = "001152-pursuit"
ordinal = 1152
kind = "pursuit"
timestamp = "2026-10-05T16:11:58+00:00"
summary = "pursuit open T0276: R33 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R33 ran mimo on itc_prompt.txt from a clean ~/itc under the 1h cap with tau at HEAD; dev-notes/itc-runs/R33.md names model, prompt, tau sha, a grader line and a scorecard.
decided by: sh -c 'echo "adcfd73c18ad2de0c0a685c1edbdfd8c3fc77a74be12f3fc7ae0abdce56bd059  .beagle/checks/T0276/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0276/check.sh'
budget: 40000 tokens
