+++
id = "000965-pursuit"
ordinal = 965
kind = "pursuit"
timestamp = "2026-10-05T07:43:51+00:00"
summary = "pursuit prove T0237: WITNESSED — refuses when beagle.py's `reach = _check_test_reach(check, root) if check…` is put back as `reach = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e2d60758beecb3e176a05f415e1d8af48e894f9418db7e2ea10728ac59a90d19  .beagle/checks/T0237/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0237/check.sh'
refutes: refuses when beagle.py's `reach = _check_test_reach(check, root) if check…` is put back as `reach = None` (proven 2026-10-05T07:43:44+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_task_closes_done_when_proven_by_data_absence)
refused after 3s of a 1m19s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_task_closes_done_when_proven_by_data_absence
refused with: 1 failed in 2.66s
