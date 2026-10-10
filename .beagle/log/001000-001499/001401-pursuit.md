+++
id = "001401-pursuit"
ordinal = 1401
kind = "pursuit"
timestamp = "2026-10-10T01:01:31+00:00"
summary = "pursuit open T0332: R39 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R39 (gemma4-12b-q4, cobs_prompt.txt, driver thinking medium) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R39.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "28c17eb5a3f4743f65b734f64811f5c5cbfb18d42867187da99d6812299ca731  .beagle/checks/T0332/T0332.sh" | sha256sum -c --quiet && bash .beagle/checks/T0332/T0332.sh'
budget: 5000 tokens
