+++
id = "001145-pursuit"
ordinal = 1145
kind = "pursuit"
timestamp = "2026-10-05T16:05:01+00:00"
summary = "pursuit prove T0273: WITNESSED — refuses when beagle.py's `unread = _unread_cases(root, entries)` is put back as `unread = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1b16afaba18a5cfbc3981348b99a6c8792b47802f541dea442ce62b6b55e6862  .beagle/checks/T0273/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0273/check.sh'
refutes: refuses when beagle.py's `unread = _unread_cases(root, entries)` is put back as `unread = None` (proven 2026-10-05T16:05:01+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_data_route_open_task_names_unread_cases_instead_of_closing)
refused after 3s of a 1m39s check at: FAILED tests/test_beagle_example_extension.py::test_data_route_open_task_names_unread_cases_instead_of_closing
refused with: 1 failed in 2.61s
