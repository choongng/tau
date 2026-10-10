+++
id = "001470-pursuit"
ordinal = 1470
kind = "pursuit"
timestamp = "2026-10-10T03:05:02+00:00"
summary = "pursuit open T0345: R40 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R40 (qwen3.5-9b-q4-mtp-thinking-coding, itc_prompt.txt, driver thinking medium) ran from a clean ~/itc under the one-hour cap; dev-notes/itc-runs/R40.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "4db98a543bdda27c56290a8fdb6195154b5a90ac7910a9251ef1a9c125681ab4  .beagle/checks/T0345/T0345.sh" | sha256sum -c --quiet && bash .beagle/checks/T0345/T0345.sh'
budget: 6000 tokens
