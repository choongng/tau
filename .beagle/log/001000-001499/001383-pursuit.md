+++
id = "001383-pursuit"
ordinal = 1383
kind = "pursuit"
timestamp = "2026-10-10T00:34:49+00:00"
summary = "pursuit open T0329: Cut-off tool arguments name the cut-off in every session"
metric_command = ""
drains = []
hooks = []
+++

criteria: R38 class 2: outside a pursuit_step worker a write cut off at the output limit reached the tool as _raw_arguments and was told 'path must be a string' twelve times. ToolDefinition.to_agent_tool's execute raises a ToolInputError naming the cut-off, after extension hooks.
decided by: sh -c 'echo "9fd7d0b003dad6f90db8eda15b6e35dc33ce7379c4b87ce8cc3540d736e4149c  .beagle/checks/T0329/T0329.sh" | sha256sum -c --quiet && bash .beagle/checks/T0329/T0329.sh'
budget: 60000 tokens
