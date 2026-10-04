+++
id = "000689-pursuit"
ordinal = 689
kind = "pursuit"
timestamp = "2026-10-04T13:14:03+00:00"
summary = "pursuit prove T0162: WITNESSED — refuses when loop.py's `if signal is not None and signal.is_cancelled()…` is put back as `if False: # A cancel from between turns`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "14e16f7dc873a65e95d831b70ad45d262ea8b8b32a5a0217c58156b16d31c144  .beagle/checks/T0162/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0162/check.sh'
refutes: refuses when loop.py's `if signal is not None and signal.is_cancelled()…` is put back as `if False: # A cancel from between turns` (proven 2026-10-04T13:13:14+00:00; refused at FAILED tests/test_agent_loop.py::test_cancel_between_turns_issues_no_further_request[asyncio])
refused after 1s of a 3s check at: FAILED tests/test_agent_loop.py::test_cancel_between_turns_issues_no_further_request[asyncio]
refused with: 1 failed in 0.62s
