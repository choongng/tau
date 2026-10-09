+++
id = "001355-pursuit"
ordinal = 1355
kind = "pursuit"
timestamp = "2026-10-09T23:02:51+00:00"
summary = "pursuit prove T0324: WITNESSED — refuses when session.py's `or not TEMPLATE_TOOL_CALL_TOKEN.search(message.…` is put back as `or TEMPLATE_TOOL_CALL_TOKEN.search(message.text)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "253f383f27d63407de4c173c7bc6582eef6790794b5a4f5c4e8af90e5dee6aa3  .beagle/checks/T0324/T0324.sh" | sha256sum -c --quiet && bash .beagle/checks/T0324/T0324.sh'
refutes: refuses when session.py's `or not TEMPLATE_TOOL_CALL_TOKEN.search(message.…` is put back as `or TEMPLATE_TOOL_CALL_TOKEN.search(message.text)` (proven 2026-10-09T23:01:54+00:00; refused at FAILED tests/test_session_template_tokens.py::test_text_reply_with_tool_call_markup_is_followed_up[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_session_template_tokens.py::test_text_reply_with_tool_call_markup_is_followed_up[asyncio]
refused with: 1 failed in 0.40s
