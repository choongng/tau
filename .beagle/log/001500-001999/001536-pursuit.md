+++
id = "001536-pursuit"
ordinal = 1536
kind = "pursuit"
timestamp = "2026-10-10T05:01:49+00:00"
summary = "pursuit open T0356: B02 mimo itc baseline"
metric_command = ""
drains = []
hooks = []
+++

criteria: B02 ran plain tau -p --no-extensions with mimo on the beagle-free ITC prompt under the hour cap from a clean tau; runs/B02 holds meta (mode baseline), exit, scorecard and grade; dev-notes/itc-runs/B02.md has the v8 header and summary naming the tau sha, a 'Built:' line saying what the run left in ~/itc, an 'Ended:' line saying how it ended, the grader line and the Scorecard.
decided by: sh -c 'echo "f935f8d9e87f6e349693e4cb5113c19232b84c5711d1a30ec19ac4a11bc000cc  .beagle/checks/T0356/T0356.sh" | sha256sum -c --quiet && bash .beagle/checks/T0356/T0356.sh'
budget: 30000 tokens
opened over T0296: owner-approved baseline; calibrates the pursuit before R41 is read
