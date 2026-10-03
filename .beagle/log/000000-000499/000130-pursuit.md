+++
id = "000130-pursuit"
ordinal = 130
kind = "pursuit"
timestamp = "2026-10-03T15:32:50+00:00"
summary = "pursuit open T0045: R06 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R06 (qwen 9B) was launched by launch.sh at a recorded tau sha, ran to exit under the 1h cap, and has scorecard.json (with the --meta workers block), grade.json, and R06.md with a Scorecard section and a grader line.
decided by: sh -c 'echo "78f588778dd8afbfcad14f30a9e028cf43167afc74f644cdb1764504f6549eb6  .beagle/checks/T0045/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0045/scored.sh R06'
budget: 40000 tokens
