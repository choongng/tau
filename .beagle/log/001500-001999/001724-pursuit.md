+++
id = "001724-pursuit"
ordinal = 1724
kind = "pursuit"
timestamp = "2026-10-11T00:31:09+00:00"
summary = "pursuit prove T0397: WITNESSED — refuses when contradictions.py's `if res is None or res[\"line\"] not in s.refused:` is put back as `if res is None:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1db125fc2935bd5a756ba18c045026833e8a0af087e4764ffa16679227bb81c8  .beagle/checks/T0397/T0397.sh" | sha256sum -c --quiet && bash .beagle/checks/T0397/T0397.sh'
refutes: refuses when contradictions.py's `if res is None or res["line"] not in s.refused:` is put back as `if res is None:` (proven 2026-10-11T00:30:10+00:00; refused at FAILED mine/test_contradictions.py::test_offered_call_that_succeeds_is_not_a_finding)
refused after 0s of a 6s check at: FAILED mine/test_contradictions.py::test_offered_call_that_succeeds_is_not_a_finding
refused with: 1 failed, 9 passed in 0.02s
standing checks red: T0368
