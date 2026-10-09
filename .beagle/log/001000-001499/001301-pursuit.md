+++
id = "001301-pursuit"
ordinal = 1301
kind = "pursuit"
timestamp = "2026-10-09T21:30:54+00:00"
summary = "pursuit prove T0313: WITNESSED — refuses when session.py's `_template_tokens_in_arguments(call)` is put back as `None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cccd087687dd25f0c86c2a3a515317de4ea18f693dd400bfbe635f9bb8699e8a  .beagle/checks/T0313/T0313.sh" | sha256sum -c --quiet && bash .beagle/checks/T0313/T0313.sh'
refutes: refuses when session.py's `_template_tokens_in_arguments(call)` is put back as `None` (proven 2026-10-09T21:29:58+00:00; refused at FAILED tests/test_session_template_tokens.py::test_tool_args_with_template_tokens_refused[asyncio])
refused after 1s of a 4s check at: FAILED tests/test_session_template_tokens.py::test_tool_args_with_template_tokens_refused[asyncio]
refused with: 1 failed in 0.41s
