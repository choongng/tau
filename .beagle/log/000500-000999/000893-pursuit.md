+++
id = "000893-pursuit"
ordinal = 893
kind = "pursuit"
timestamp = "2026-10-05T04:32:05+00:00"
summary = "pursuit prove T0224: WITNESSED — refuses when beagle.py's `existing = _live_data_holder(task, nodes or [],…` is put back as `existing = None or next(`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "615e49d89244fdc03378875bad98b0d609661855633a3fbdd19d4db237f59d22  .beagle/checks/T0224/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0224/check.sh'
refutes: refuses when beagle.py's `existing = _live_data_holder(task, nodes or [],…` is put back as `existing = None or next(` (proven 2026-10-05T04:31:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_first_names_the_live_task_holding_the_data_file)
refused after 2s of a 1m11s check at: FAILED tests/test_beagle_example_extension.py::test_cases_first_names_the_live_task_holding_the_data_file
refused with: 1 failed in 1.72s
