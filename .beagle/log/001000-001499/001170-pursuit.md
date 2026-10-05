+++
id = "001170-pursuit"
ordinal = 1170
kind = "pursuit"
timestamp = "2026-10-05T17:37:07+00:00"
summary = "pursuit prove T0279: WITNESSED — refuses when beagle.py's `return _NOT_DONE_DEMAND.get(key, \"\")` is put back as `return \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1eabc7bc47a6d2c169d1ba73f57420bf1a6aa8fec267c3a2947ed1963b6e362c  .beagle/checks/T0279/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0279/check.sh'
refutes: refuses when beagle.py's `return _NOT_DONE_DEMAND.get(key, "")` is put back as `return ""` (proven 2026-10-05T17:37:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_escalation_after_judge_only_stays_open_offers_notes_only_call)
refused after 2s of a 1m32s check at: FAILED tests/test_beagle_example_extension.py::test_escalation_after_judge_only_stays_open_offers_notes_only_call
refused with: 1 failed in 1.90s
