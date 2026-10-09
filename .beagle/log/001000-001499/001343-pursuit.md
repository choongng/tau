+++
id = "001343-pursuit"
ordinal = 1343
kind = "pursuit"
timestamp = "2026-10-09T22:31:11+00:00"
summary = "pursuit open T0320: R37 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R37 (qwen3.5-9b-q4-mtp-thinking-coding, cobs_prompt.txt, driver thinking medium) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R37.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "5f98525ad31647105b6d7f0f125e52911f8c77a9346d4fd84b67ba876ce31646  .beagle/checks/T0320/T0320.sh" | sha256sum -c --quiet && bash .beagle/checks/T0320/T0320.sh'
budget: 20000 tokens
