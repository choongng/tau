+++
id = "000176-pursuit"
ordinal = 176
kind = "pursuit"
timestamp = "2026-10-03T17:04:18+00:00"
summary = "pursuit open T0055: R08 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R08 (qwen) ran under launch.sh within its 1h cap; runs/R08 holds exit.json, meta.json with session, grade.json and scorecard.json (with --meta); dev-notes/itc-runs/R08.md has the grader line matching grade.json and a Scorecard block matching scorecard.json
decided by: sh -c 'echo "2ae208e92e51bfceeb75d148b2f73a83bb3fdb482270af92411042a04a7c3b8a  .beagle/checks/T0055/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0055/scored.sh R08'
budget: 40000 tokens
