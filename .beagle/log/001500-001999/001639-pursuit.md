+++
id = "001639-pursuit"
ordinal = 1639
kind = "pursuit"
timestamp = "2026-10-10T20:54:55+00:00"
summary = "pursuit prove T0386: WITNESSED — refuses when R42.md's `tests/test_tool_history.py::test_repeat_refusal…` is put back as `tests/test_repeat_breaker_reset.py::test_repeat…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e4951b6b9afce621cf32c86148808f8a30cac5f28a8bb854f0f20afac051e1d0  .beagle/checks/T0386/T0386.sh" | sha256sum -c --quiet && bash .beagle/checks/T0386/T0386.sh'
refutes: refuses when R42.md's `tests/test_tool_history.py::test_repeat_refusal…` is put back as `tests/test_repeat_breaker_reset.py::test_repeat…` (proven 2026-10-10T20:53:57+00:00; refused at R42.md still names the old test files)
refused after 0s of a 0s check at: R42.md still names the old test files
refused with: R42.md still names the old test files
standing checks red: T0368
