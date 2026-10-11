+++
id = "001816-pursuit"
ordinal = 1816
kind = "pursuit"
timestamp = "2026-10-11T22:22:18+00:00"
summary = "pursuit open T0443: B04 q35 itc baseline"
metric_command = ""
drains = []
hooks = []
+++

criteria: B04 ran plain tau -p --no-extensions with q35 (qwen3.6-35b-q6-mtp-thinking-coding, krang) on the beagle-free ITC prompt under the hour cap from a clean tau; runs/B04 holds meta (mode baseline), exit, scorecard and grade; dev-notes/itc-runs/B04.md has the v8 header and summary naming the tau sha, a 'Built:' line, an 'Ended:' line, a 'Wall:' line with wall time and token totals, the grader line and the Scorecard.
decided by: sh -c 'echo "64aa6a4222e0252745f10227242b54e3aa7382d4d7adc1c0d06af3736d4dddd9  .beagle/checks/T0443/T0443.sh" | sha256sum -c --quiet && bash .beagle/checks/T0443/T0443.sh'
budget: 150000 tokens
opened over T0437, T0438, T0439, T0440, T0441, T0442: baseline is plain tau --no-extensions, independent of the T0414 fixes; runs while they are worked (R0001)
