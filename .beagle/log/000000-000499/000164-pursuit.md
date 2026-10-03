+++
id = "000164-pursuit"
ordinal = 164
kind = "pursuit"
timestamp = "2026-10-03T16:59:41+00:00"
summary = "pursuit prove T0052: NOT-DISCRIMINATING — `sh -c 'echo \"14fa7929a0520fd0374acabd6a8f6eb1230c61c1cd626161bd07108b7a628817  .beagle/checks/T0052/scored.sh\" | sha256sum -c --quiet && bash .beagle/checks/T0052/scored.sh R07'`"
metric_command = ""
drains = []
hooks = []
+++

criteria: R07 (mimo 9B) was launched by launch.sh at a recorded tau sha, ran to exit under the 1h cap, and has scorecard.json (with the --meta workers block), grade.json, and R07.md with a Scorecard section agreeing with the json and a grader line.
measured: still passes with the defect put back in R07.md (exit 0), measured 2026-10-03T16:59:41+00:00
replaces: still passes with the defect put back in R07.md (exit 0), measured 2026-10-03T16:59:38+00:00
