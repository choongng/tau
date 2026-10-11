+++
id = "001822-pursuit"
ordinal = 1822
kind = "pursuit"
timestamp = "2026-10-11T22:26:47+00:00"
summary = "pursuit open T0416: B05 q35 cobs baseline"
metric_command = ""
drains = []
hooks = []
+++

criteria: B05 ran plain tau -p --no-extensions with q35 (qwen3.6-35b-q6-mtp-thinking-coding, krang) on the beagle-free COBS prompt under the hour cap from a clean tau; runs/B05 holds meta (mode baseline), exit, scorecard and grade; dev-notes/itc-runs/B05.md has the v8 header and summary naming the tau sha, a 'Built:' line, an 'Ended:' line, a 'Wall:' line with wall time and token totals, the grader line and the Scorecard.
decided by: sh -c 'echo "b761ba908bcb8f142816fa22981f3ea758c9a3b1310005251029b8889e65324b  .beagle/checks/T0416/T0416.sh" | sha256sum -c --quiet && bash .beagle/checks/T0416/T0416.sh'
budget: 150000 tokens
