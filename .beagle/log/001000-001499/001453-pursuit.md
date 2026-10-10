+++
id = "001453-pursuit"
ordinal = 1453
kind = "pursuit"
timestamp = "2026-10-10T02:44:17+00:00"
summary = "pursuit prove T0338: WITNESSED — refuses when session.py's `call.arguments[leak.path] = leak.clean` is put back as `return leak`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2959040c5899a55336b14e84bc7da6e65831d9b7f326ac577cef0890bc99e15a  .beagle/checks/T0338/T0338.sh" | sha256sum -c --quiet && bash .beagle/checks/T0338/T0338.sh'
refutes: refuses when session.py's `call.arguments[leak.path] = leak.clean` is put back as `return leak` (proven 2026-10-10T02:43:21+00:00; refused at FAILED tests/test_session_template_tokens.py::test_leak_in_optional_argument_runs_the_clean_call[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_session_template_tokens.py::test_leak_in_optional_argument_runs_the_clean_call[asyncio]
refused with: 1 failed, 2 passed, 7 deselected in 0.41s
standing checks red: T0335
