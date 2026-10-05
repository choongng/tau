+++
id = "000834-pursuit"
ordinal = 834
kind = "pursuit"
timestamp = "2026-10-05T01:50:56+00:00"
summary = "pursuit open T0213: R23 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R23 (mimo-v2.6-9b-q4, cobs_prompt.txt) launched by launch.sh from a clean ~/cobs under the 1h cap on a clean tau commit; scorecard.json and grade.json (grade_cobs.py) made; dev-notes/itc-runs/R23.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "a77392aa902160824cde1b312dd2c7c1ff08661fd78f73960d65f4bd24acbb7b  .beagle/checks/T0213/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0213/check.sh'
budget: 40000 tokens
