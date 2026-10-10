+++
id = "001512-pursuit"
ordinal = 1512
kind = "pursuit"
timestamp = "2026-10-10T04:15:22+00:00"
summary = "pursuit open T0355: B01 qwen cobs baseline"
metric_command = ""
drains = []
hooks = []
+++

criteria: B01 ran plain tau -p --no-extensions with qwen on the beagle-free COBS prompt under the hour cap from a clean tau; runs/B01 holds meta (mode baseline), exit, scorecard and grade; dev-notes/itc-runs/B01.md has the v8 header and summary naming the tau sha, a 'Built:' line saying what the run left in ~/cobs, an 'Ended:' line saying how it ended, the grader line and the Scorecard.
decided by: sh -c 'echo "1236215a8daa330a93cc8d06b081d89be271569e68e54dbc63d4ea9501760071  .beagle/checks/T0355/T0355.sh" | sha256sum -c --quiet && bash .beagle/checks/T0355/T0355.sh'
budget: 8000 tokens
opened over T0348, T0349, T0350, T0351: baseline run, approved by the owner; runs beside the R40 fixes (disjoint scope)
