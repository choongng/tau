+++
id = "000599-pursuit"
ordinal = 599
kind = "pursuit"
timestamp = "2026-10-04T09:04:18+00:00"
summary = "pursuit prove T0143: WITNESSED — refuses when beagle.py's `_sibling_read(event.tool_name, arguments, cwd, …` is put back as `None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a791836bbc7255d6830bfe7a90f370f878275f13cf4d4a142ac047c1db2dd601  .beagle/checks/T0143/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0143/check.sh'
refutes: refuses when beagle.py's `_sibling_read(event.tool_name, arguments, cwd, …` is put back as `None` (proven 2026-10-04T09:03:41+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_reading_a_sibling_project_tree)
refused after 2s of a 49s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_reading_a_sibling_project_tree
refused with: 1 failed, 2 passed in 1.42s
