+++
id = "000790-pursuit"
ordinal = 790
kind = "pursuit"
timestamp = "2026-10-04T23:26:13+00:00"
summary = "pursuit open T0203: R22 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R22 (qwen3.5-9b-q4-mtp-thinking-coding, cobs_prompt.txt) launched by launch.sh from a clean ~/cobs under the 1h cap on a clean tau commit; scorecard.json and grade.json (grade_cobs.py) made; dev-notes/itc-runs/R22.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "3564f5cd38bc86f5ae14cb98aa273adea837582290f57ca6d820c02aa3b70cfe  .beagle/checks/T0203/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0203/check.sh'
budget: 40000 tokens
