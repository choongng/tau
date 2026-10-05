+++
id = "001069-pursuit"
ordinal = 1069
kind = "pursuit"
timestamp = "2026-10-05T11:40:06+00:00"
summary = "pursuit prove T0258: WITNESSED — refuses when session.py's `text=_hold_summary_to_budget(summary),` is put back as `text=summary,`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5c18901a8afccb93666871c260e4cddc49743fb5d6ac9056555c46a288bb7db6  .beagle/checks/T0258/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0258/check.sh'
refutes: refuses when session.py's `text=_hold_summary_to_budget(summary),` is put back as `text=summary,` (proven 2026-10-05T11:39:10+00:00; predates the task: the task's change is only tests, and one of them refused; refused at FAILED tests/test_coding_session.py::test_compaction_summary_over_cap_is_trunca
refused after 1s of a 3s check at: FAILED tests/test_coding_session.py::test_compaction_summary_over_cap_is_truncated_with_marker[asyncio]
refused with: 1 failed in 0.79s
standing checks red: T0054, T0057, T0058, T0059, T0061, T0065, T0066, T0067, T0068, T0069, T0072, T0074, T0084, T0087
