+++
id = "001568-pursuit"
ordinal = 1568
kind = "pursuit"
timestamp = "2026-10-10T15:24:15+00:00"
summary = "pursuit open T0366: R41 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R41 (mimo-v2.6-9b-q4, cobs_prompt.txt, driver thinking medium) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R41.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "5f32aa4f8efb2ae3cc0638630fc39bdfc0b54947affa93cf9eea2dcaee1a376f  .beagle/checks/T0366/T0366.sh" | sha256sum -c --quiet && bash .beagle/checks/T0366/T0366.sh'
budget: 10000 tokens
