+++
id = "001392-pursuit"
ordinal = 1392
kind = "pursuit"
timestamp = "2026-10-10T00:45:13+00:00"
summary = "pursuit prove T0330: WITNESSED — refuses when session.py's `self._queued_nudge = None self._awaiting_nudge_…` is put back as `self._queued_nudge = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "34f787de5b7d7db91b753a70fd8d7d9153880e1d5b4e019439a61c957950fd28  .beagle/checks/T0330/T0330.sh" | sha256sum -c --quiet && bash .beagle/checks/T0330/T0330.sh'
refutes: refuses when session.py's `self._queued_nudge = None self._awaiting_nudge_…` is put back as `self._queued_nudge = None` (proven 2026-10-10T00:44:16+00:00; refused at FAILED tests/test_session_output_limit_nudge.py::test_thinking_off_request_is_the_nudges_not_a_steering_reply[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_session_output_limit_nudge.py::test_thinking_off_request_is_the_nudges_not_a_steering_reply[asyncio]
refused with: 1 failed, 1 passed in 0.39s
replaces: still passes with the defect put back in session.py (exit 0), measured 2026-10-10T00:44:08+00:00
