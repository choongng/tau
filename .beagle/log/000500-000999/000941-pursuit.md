+++
id = "000941-pursuit"
ordinal = 941
kind = "pursuit"
timestamp = "2026-10-05T06:44:23+00:00"
summary = "pursuit open T0234: R26 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R26 (qwen3.5-9b-q4-mtp-thinking-coding, cobs_prompt.txt) launched by launch.sh from a clean ~/cobs under the 1h cap on a clean tau commit; scorecard.json and grade.json (grade_cobs.py) made; dev-notes/itc-runs/R26.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "8ce37f6ab4deeb53189732af0ef6a50a55a8d7c708842a67b1534e9925363f89  .beagle/checks/T0234/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0234/check.sh'
budget: 40000 tokens
