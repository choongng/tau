+++
id = "000567-pursuit"
ordinal = 567
kind = "pursuit"
timestamp = "2026-10-04T07:28:29+00:00"
summary = "pursuit open T0136: Worker reports survive walls and raw tool calls"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the second sub-agent on a step is killed at the wall, the step's result still carries the first attempt's report, the check's output tail, and the changed files in scope; the timeout text blames turns at the output limit when the worker's last turns hit it, rather than naming the turn-cap env var. A worker report that ends in raw tool-call markup keeps the text before the markup (a report that is only markup is still replaced as before).
decided by: sh -c 'echo "b3d97eeaa103d44de6f434173b5e6c0ddf7510ecdbfe586e9c013e66e779159b  .beagle/checks/T0136/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0136/check.sh'
budget: 80000 tokens
