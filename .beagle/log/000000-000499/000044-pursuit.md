+++
id = "000044-pursuit"
ordinal = 44
kind = "pursuit"
timestamp = "2026-10-03T11:15:44+00:00"
summary = "pursuit open T0025: R02 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R02 (qwen3.5-9b-q4-mtp-thinking-coding, tau at the R01 fixes) ran under the 1h cap via launch.sh; exit.json, meta.json with the driver session, scorecard.json, grade.json and R02.md with a Scorecard section and grader line exist.
decided by: sh -c 'echo "266946c887e0f64f177a3b25cd64b49a0ac0adb5abe5439113d5c489046a83d7  .beagle/checks/T0025/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0025/scored.sh R02'
budget: 60000 tokens
