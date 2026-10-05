+++
id = "000905-pursuit"
ordinal = 905
kind = "pursuit"
timestamp = "2026-10-05T04:53:41+00:00"
summary = "pursuit open T0227: R25 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R25 (mimo-v2.6-9b-q4, itc_prompt.txt) launched by launch.sh from a clean ~/itc under the 1h cap on a clean tau commit; scorecard.json and grade.json (grade.py) made; dev-notes/itc-runs/R25.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "6f2062f6f258b48b7bd0ef0b8f7e4c76f6f38b00bc1b22f783f5f04222ec217e  .beagle/checks/T0227/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0227/check.sh'
budget: 40000 tokens
