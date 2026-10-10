+++
id = "001397-pursuit"
ordinal = 1397
kind = "pursuit"
timestamp = "2026-10-10T01:00:53+00:00"
summary = "pursuit prove T0331: WITNESSED — refuses when session.py's `self._thinking_off_twin = (provider, None) self…` is put back as `self._thinking_off_twin = (provider, None)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2422b3bac322f8a934e09117bf1991c4eba2262ef47b4145cfe8594346a402ba  .beagle/checks/T0331/T0331.sh" | sha256sum -c --quiet && bash .beagle/checks/T0331/T0331.sh'
refutes: refuses when session.py's `self._thinking_off_twin = (provider, None) self…` is put back as `self._thinking_off_twin = (provider, None)` (proven 2026-10-10T00:59:56+00:00; refused at FAILED tests/test_session_thinking_off_twin.py::test_thinking_off_twin_warns_once_when_the_build_fails[asyncio])
refused after 13s of a 13s check at: FAILED tests/test_session_thinking_off_twin.py::test_thinking_off_twin_warns_once_when_the_build_fails[asyncio]
refused with: 2 failed, 1 passed, 2862 deselected in 1.03s
