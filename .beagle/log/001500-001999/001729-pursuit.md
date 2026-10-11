+++
id = "001729-pursuit"
ordinal = 1729
kind = "pursuit"
timestamp = "2026-10-11T00:50:41+00:00"
summary = "pursuit prove T0398: WITNESSED — refuses when indicators.py's `return \"capped\", end[\"kind\"], ev` is put back as `return \"no_report\", end[\"kind\"], ev`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "806bfd099655b93325fe4e723e4b84950ac88d1526edb9099c12456810b6f607  .beagle/checks/T0398/T0398.sh" | sha256sum -c --quiet && bash .beagle/checks/T0398/T0398.sh'
refutes: refuses when indicators.py's `return "capped", end["kind"], ev` is put back as `return "no_report", end["kind"], ev` (proven 2026-10-11T00:49:41+00:00; refused at FAILED mine/test_indicators.py::test_worker_outcomes_come_from_how_each_session_ended)
refused after 0s of a 3s check at: FAILED mine/test_indicators.py::test_worker_outcomes_come_from_how_each_session_ended
refused with: 1 failed, 9 passed in 0.02s
standing checks red: T0368
