+++
id = "001625-pursuit"
ordinal = 1625
kind = "pursuit"
timestamp = "2026-10-10T19:08:18+00:00"
summary = "pursuit open T0380: R43 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R43 (qwen3.5-9b-q4-mtp-thinking-coding, cobs_prompt.txt, driver thinking medium, workers thinking at the driver's level) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R43.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "ac5d8f687f5fe7b3c4c0443bd7af7035d19e9bcbdb2f9805e654af33eeb97ca0  .beagle/checks/T0380/T0380.sh" | sha256sum -c --quiet && bash .beagle/checks/T0380/T0380.sh'
budget: 50000 tokens
