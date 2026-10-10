+++
id = "001538-pursuit"
ordinal = 1538
kind = "pursuit"
timestamp = "2026-10-10T05:21:06+00:00"
summary = "pursuit open T0362: Worker thinking on for pursuit runs"
metric_command = ""
drains = []
hooks = []
+++

criteria: R runs dispatch workers at the driver's thinking level via BEAGLE_TAU_DISPATCH_THINKING for every model; B runs show worker thinking off; dry-run prints worker thinking; meta.json records worker_thinking.
decided by: sh -c 'echo "2a4e183834ad806213380015a15c97a86a2ef0b766e0de98bcbfd56c0ef430f3  .beagle/checks/T0362/T0362.sh" | sha256sum -c --quiet && bash .beagle/checks/T0362/T0362.sh'
budget: 15000 tokens
