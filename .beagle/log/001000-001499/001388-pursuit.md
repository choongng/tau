+++
id = "001388-pursuit"
ordinal = 1388
kind = "pursuit"
timestamp = "2026-10-10T00:42:10+00:00"
summary = "pursuit prove T0328: WITNESSED — refuses when beagle.py's `if event.tool_name == \"agent\": return ToolCallH…` is put back as `if False: return ToolCallHookResult( block=True…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a814862d385a32c6fb6f671070f83c098c138cf8dc52164241808fc6a7730163  .beagle/checks/T0328/T0328.sh" | sha256sum -c --quiet && bash .beagle/checks/T0328/T0328.sh'
refutes: refuses when beagle.py's `if event.tool_name == "agent": return ToolCallH…` is put back as `if False: return ToolCallHookResult( block=True…` (proven 2026-10-10T00:42:10+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_first_gate_refuses_agent_before_founding)
refused after 2s of a 2m07s check at: FAILED tests/test_beagle_example_extension.py::test_found_first_gate_refuses_agent_before_founding
refused with: 1 failed in 1.69s
