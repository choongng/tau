+++
id = "001371-pursuit"
ordinal = 1371
kind = "pursuit"
timestamp = "2026-10-10T00:28:03+00:00"
summary = "pursuit spawn T0327: another route to T0325"
metric_command = ""
drains = []
hooks = []
+++

superseded: [T0325] R38 run and score
because: v6 scored.sh asserts a dated root commit; R38's driver never founded, so ~/itc has no repo and first_commit_ts is null. The check tested repo-start cleanliness, which an unfounded run satisfies vacuously, not a property R38 lacks.
delta: Same run and note; the bound check moves to .beagle/checks/runs/v7/scored.sh, which lets a run that never founded (founded False, commits 0, record_commits 0) have a null first_commit_ts; v7 selftest adds a pass and a refuse case for it.
