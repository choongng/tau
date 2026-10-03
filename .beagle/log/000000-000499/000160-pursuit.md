+++
id = "000160-pursuit"
ordinal = 160
kind = "pursuit"
timestamp = "2026-10-03T16:33:22+00:00"
summary = "pursuit open T0052: R07 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R07 (mimo 9B) was launched by launch.sh at a recorded tau sha, ran to exit under the 1h cap, and has scorecard.json (with the --meta workers block), grade.json, and R07.md with a Scorecard section agreeing with the json and a grader line.
decided by: sh -c 'echo "14fa7929a0520fd0374acabd6a8f6eb1230c61c1cd626161bd07108b7a628817  .beagle/checks/T0052/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0052/scored.sh R07'
budget: 40000 tokens
