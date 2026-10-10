+++
id = "001598-pursuit"
ordinal = 1598
kind = "pursuit"
timestamp = "2026-10-10T17:27:02+00:00"
summary = "pursuit open T0373: R42 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R42 (gemma4-12b-q4, itc_prompt.txt, driver thinking medium, workers thinking at the driver's level) ran from a clean ~/itc under the one-hour cap; dev-notes/itc-runs/R42.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "1c47cd66c0ea6894242392b7951f5d4bcfa14bcaecf6d7eb7c9f5113826c34b4  .beagle/checks/T0373/T0373.sh" | sha256sum -c --quiet && bash .beagle/checks/T0373/T0373.sh'
budget: 40000 tokens
