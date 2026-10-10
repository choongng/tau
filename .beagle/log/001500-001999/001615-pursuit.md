+++
id = "001615-pursuit"
ordinal = 1615
kind = "pursuit"
timestamp = "2026-10-10T18:52:55+00:00"
summary = "pursuit prove T0378: WITNESSED — refuses when session.py's `self._next_request_thinking_off = self._queued_…` is put back as `self._next_request_thinking_off = True`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "789804ca43004090b8ec28c42bb7b7a721fa58f493f029e9d7eee532f619f31a  .beagle/checks/T0378/T0378.sh" | sha256sum -c --quiet && bash .beagle/checks/T0378/T0378.sh'
refutes: refuses when session.py's `self._next_request_thinking_off = self._queued_…` is put back as `self._next_request_thinking_off = True` (proven 2026-10-10T18:51:56+00:00; refused at FAILED tests/test_session_output_limit_nudge.py::test_loop_cut_nudge_keeps_the_session_provider[asyncio])
refused after 1s of a 4s check at: FAILED tests/test_session_output_limit_nudge.py::test_loop_cut_nudge_keeps_the_session_provider[asyncio]
refused with: 1 failed, 1 passed, 2 deselected in 0.38s
standing checks red: T0368
