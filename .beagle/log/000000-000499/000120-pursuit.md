+++
id = "000120-pursuit"
ordinal = 120
kind = "pursuit"
timestamp = "2026-10-03T14:56:03+00:00"
summary = "pursuit open T0042: R05 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R05 (mimo 9B) was launched by launch.sh at a recorded tau sha, ran to exit under the 1h cap, and has scorecard.json (with the --meta workers block), grade.json, and R05.md with a Scorecard section and a grader line.
decided by: sh -c 'echo "78f588778dd8afbfcad14f30a9e028cf43167afc74f644cdb1764504f6549eb6  .beagle/checks/T0042/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0042/scored.sh R05'
budget: 40000 tokens
