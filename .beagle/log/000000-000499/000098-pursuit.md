+++
id = "000098-pursuit"
ordinal = 98
kind = "pursuit"
timestamp = "2026-10-03T13:18:06+00:00"
summary = "pursuit open T0037: R04 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R04 (qwen 9B) was launched by launch.sh at a recorded tau sha, ran to exit under the 1h cap, and has scorecard.json (with the --meta workers block), grade.json, and R04.md with a Scorecard section and a grader line.
decided by: sh -c 'echo "78f588778dd8afbfcad14f30a9e028cf43167afc74f644cdb1764504f6549eb6  .beagle/checks/T0037/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0037/scored.sh R04'
budget: 40000 tokens
