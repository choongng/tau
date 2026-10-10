+++
id = "001665-pursuit"
ordinal = 1665
kind = "pursuit"
timestamp = "2026-10-10T23:15:15+00:00"
summary = "pursuit prove T0393: WITNESSED — refuses when session.py's `r\"|<function=[\\w.-]+>\\s*<parameter=|</function>…` is put back as `r\"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3da1a9ea62c22659a1ff5cd2045673faff48dc251ad521ba5129e8c8cff54592  .beagle/checks/T0393/T0393.sh" | sha256sum -c --quiet && bash .beagle/checks/T0393/T0393.sh'
refutes: refuses when session.py's `r"|<function=[\w.-]+>\s*<parameter=|</function>…` is put back as `r""` (proven 2026-10-10T23:14:16+00:00; refused at FAILED tests/test_session_template_tokens.py::test_text_tool_call_follow_ups_are_bounded[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_session_template_tokens.py::test_text_tool_call_follow_ups_are_bounded[asyncio]
refused with: 2 failed, 9 deselected in 0.41s
standing checks red: T0368
