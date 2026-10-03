+++
id = "000223-pursuit"
ordinal = 223
kind = "pursuit"
timestamp = "2026-10-03T18:38:04+00:00"
summary = "pursuit open T0063: R09 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R09 (mimo) ran under launch.sh within its 1h cap; runs/R09 holds exit.json, meta.json with session, grade.json and scorecard.json (with --meta); dev-notes/itc-runs/R09.md has the grader line matching grade.json and a Scorecard block matching scorecard.json
decided by: sh -c 'echo "2ae208e92e51bfceeb75d148b2f73a83bb3fdb482270af92411042a04a7c3b8a  .beagle/checks/T0063/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0063/scored.sh R09'
budget: 40000 tokens
