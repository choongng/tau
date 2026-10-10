+++
id = "001610-pursuit"
ordinal = 1610
kind = "pursuit"
timestamp = "2026-10-10T18:49:31+00:00"
summary = "pursuit prove T0377: WITNESSED — refuses when session.py's `head = note[:REPEATED_CALL_QUOTE] or head` is put back as `head = head`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ef7a7fd351b42e7e610b3d7a7088f8060c74b30d0fac4fd8bc264bd8dc5f70f2  .beagle/checks/T0377/T0377.sh" | sha256sum -c --quiet && bash .beagle/checks/T0377/T0377.sh'
refutes: refuses when session.py's `head = note[:REPEATED_CALL_QUOTE] or head` is put back as `head = head` (proven 2026-10-10T18:48:34+00:00; refused at FAILED tests/test_tool_history.py::test_repeat_refusal_quotes_the_read_cut_continuation)
refused after 1s of a 3s check at: FAILED tests/test_tool_history.py::test_repeat_refusal_quotes_the_read_cut_continuation
refused with: 1 failed, 1 passed, 8 deselected in 0.41s
standing checks red: T0368
