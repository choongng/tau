+++
id = "001557-pursuit"
ordinal = 1557
kind = "pursuit"
timestamp = "2026-10-10T15:11:35+00:00"
summary = "pursuit open T0357: B03 gemma cobs baseline"
metric_command = ""
drains = []
hooks = []
+++

criteria: B03 ran plain tau -p --no-extensions with gemma on the beagle-free COBS prompt under the hour cap from a clean tau; runs/B03 holds meta (mode baseline), exit, scorecard and grade; dev-notes/itc-runs/B03.md has the v8 header and summary naming the tau sha, a 'Built:' line saying what the run left in ~/cobs, an 'Ended:' line saying how it ended, the grader line and the Scorecard.
decided by: sh -c 'echo "b63be7246d3e557d8b137afb21479dd590e49a33a39f9912dad53a712340b292  .beagle/checks/T0357/T0357.sh" | sha256sum -c --quiet && bash .beagle/checks/T0357/T0357.sh'
budget: 100000 tokens
