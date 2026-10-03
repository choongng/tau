+++
id = "000106-pursuit"
ordinal = 106
kind = "pursuit"
timestamp = "2026-10-03T14:36:14+00:00"
summary = "pursuit prove T0039: WITNESSED — refuses when beagle.py's `if _in_scope(rel, scope) and not rel.endswith(\"…` is put back as `if False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a031e46e87ddab5f2f223b45af9b47d9e908adb5702c834ee367d25b000a3f08  .beagle/checks/T0039/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0039/check.sh'
refutes: refuses when beagle.py's `if _in_scope(rel, scope) and not rel.endswith("…` is put back as `if False` (proven 2026-10-03T14:36:03+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_task_proves_by_absent_data_file)
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_cases_task_proves_by_absent_data_file
refused with: 2 failed, 2 passed, 220 deselected in 1.28s
