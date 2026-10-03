+++
id = "000311-pursuit"
ordinal = 311
kind = "pursuit"
timestamp = "2026-10-03T20:19:52+00:00"
summary = "pursuit prove T0074: WITNESSED — refuses when beagle.py's `notes += f\"{uncommitted}\\n\\n\"` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b354dabeb732ce15b2335d893ef9e86609b36461f53a71db9e21b79495ab7e96  .beagle/checks/T0074/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0074/check.sh'
refutes: refuses when beagle.py's `notes += f"{uncommitted}\n\n"` is put back as `pass` (proven 2026-10-03T20:19:16+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_names_uncommitted_files_in_the_split_tasks_scope)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_plan_names_uncommitted_files_in_the_split_tasks_scope
refused with: 1 failed, 1 passed, 278 deselected in 0.61s
