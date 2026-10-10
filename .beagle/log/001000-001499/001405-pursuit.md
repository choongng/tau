+++
id = "001405-pursuit"
ordinal = 1405
kind = "pursuit"
timestamp = "2026-10-10T02:15:31+00:00"
summary = "pursuit open T0334: R39 run and score (v8 check)"
metric_command = ""
drains = []
hooks = []
+++

criteria: R39 (gemma4-12b-q4, cobs_prompt.txt, driver thinking medium) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R39.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "f7192981dc7c7fbaf610872ecee4c68cee2acbc8a4fb5fa8cc57c5b2aa4a660c  .beagle/checks/T0334/T0334.sh" | sha256sum -c --quiet && bash .beagle/checks/T0334/T0334.sh'
budget: 3000 tokens
