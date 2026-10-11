+++
id = "001701-pursuit"
ordinal = 1701
kind = "pursuit"
timestamp = "2026-10-11T00:02:03+00:00"
summary = "pursuit prove T0400: WITNESSED — refuses when session.py's `match = TEMPLATE_ARGUMENT_TOKEN.search(value)` is put back as `match = TEMPLATE_TOOL_CALL_TOKEN.search(value)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7e25a540bcd3a0ba428ee31dcc0d218fb093a25f19a035a59b6f039523c716f3  .beagle/checks/T0400/T0400.sh" | sha256sum -c --quiet && bash .beagle/checks/T0400/T0400.sh'
refutes: refuses when session.py's `match = TEMPLATE_ARGUMENT_TOKEN.search(value)` is put back as `match = TEMPLATE_TOOL_CALL_TOKEN.search(value)` (proven 2026-10-11T00:01:04+00:00; refused at FAILED tests/test_session_template_tokens.py::test_argument_scan_accepts_unopened_call_markup_in_a_write[asyncio])
refused after 1s of a 1s check at: FAILED tests/test_session_template_tokens.py::test_argument_scan_accepts_unopened_call_markup_in_a_write[asyncio]
refused with: 1 failed, 1 passed, 10 deselected in 0.37s
standing checks red: T0081, T0082, T0085, T0088, T0089, T0368
