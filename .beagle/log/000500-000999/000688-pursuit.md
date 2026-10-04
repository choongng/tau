+++
id = "000688-pursuit"
ordinal = 688
kind = "pursuit"
timestamp = "2026-10-04T13:11:22+00:00"
summary = "pursuit open T0162: Breaker stop ends the run as aborted, not a provider error"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the before_tool_call breaker stops the run, the agent loop issues no further provider request after the cancel, and the run ends with stop_reason aborted carrying the breaker's reason, not 'Provider stream ended without a terminal event'.
decided by: sh -c 'echo "14e16f7dc873a65e95d831b70ad45d262ea8b8b32a5a0217c58156b16d31c144  .beagle/checks/T0162/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0162/check.sh'
budget: 50000 tokens
