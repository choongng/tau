+++
id = "001396-pursuit"
ordinal = 1396
kind = "pursuit"
timestamp = "2026-10-10T00:46:45+00:00"
summary = "pursuit open T0331: Sub-agent sessions can build the thinking-off twin"
metric_command = ""
drains = []
hooks = []
+++

criteria: a tau-subagents test shows a child session gets runtime_provider_config and can build the thinking-off twin; a tau test shows _thinking_off_provider warns once when the twin cannot be built; upstream.md lists the tau-subagents patch
decided by: sh -c 'echo "2422b3bac322f8a934e09117bf1991c4eba2262ef47b4145cfe8594346a402ba  .beagle/checks/T0331/T0331.sh" | sha256sum -c --quiet && bash .beagle/checks/T0331/T0331.sh'
budget: 60000 tokens
