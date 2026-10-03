+++
id = "000071-pursuit"
ordinal = 71
kind = "pursuit"
timestamp = "2026-10-03T12:52:31+00:00"
summary = "pursuit open T0031: R03 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R03 (mimo-v2.6-9b-q4, tau at the R02 fixes) ran under the 1h cap via launch.sh; exit.json, meta.json with the driver session, scorecard.json (with --meta worker block), grade.json and R03.md with a Scorecard section and grader line exist.
decided by: sh -c 'echo "266946c887e0f64f177a3b25cd64b49a0ac0adb5abe5439113d5c489046a83d7  .beagle/checks/T0031/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0031/scored.sh R03'
budget: 60000 tokens
