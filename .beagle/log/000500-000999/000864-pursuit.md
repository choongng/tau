+++
id = "000864-pursuit"
ordinal = 864
kind = "pursuit"
timestamp = "2026-10-05T02:43:45+00:00"
summary = "pursuit open T0219: R24 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R24 (qwen3.5-9b-q4-mtp-thinking-coding, itc_prompt.txt) launched by launch.sh from a clean ~/itc under the 1h cap on a clean tau commit; scorecard.json and grade.json (grade.py) made; dev-notes/itc-runs/R24.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "3b690ad8a24c6aab36166543483263f42d0ada72ffc51b8729aa6cfd2b8fe010  .beagle/checks/T0219/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0219/check.sh'
budget: 40000 tokens
