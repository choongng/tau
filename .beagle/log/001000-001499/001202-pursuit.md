+++
id = "001202-pursuit"
ordinal = 1202
kind = "pursuit"
timestamp = "2026-10-05T19:34:51+00:00"
summary = "pursuit open T0286: R35 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R35 (mimo-v2.6-9b-q4, cobs_prompt.txt) ran from a clean ~/cobs under the one-hour cap; dev-notes/itc-runs/R35.md names model and prompt and holds the scorecard and hidden-grader result.
decided by: sh -c 'echo "fb3b693558978190609d04803e6639cc399803b7c1d602a79b0f70c1eddbf28c  .beagle/checks/T0286/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0286/check.sh'
budget: 40000 tokens
