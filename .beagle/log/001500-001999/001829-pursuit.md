+++
id = "001829-pursuit"
ordinal = 1829
kind = "pursuit"
timestamp = "2026-10-11T22:55:07+00:00"
summary = "pursuit prove T0442: WITNESSED — refuses when beagle.py's `WALL_MAXIMAL_TURNS = 3` is put back as `WALL_MAXIMAL_TURNS = 2` and beagle.py's `_KILLED_PROGRESS[(root_key, task)] = kept` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b586a5500fd6a4f2e67a880eb7c20ebd6c96d2fc02cdfd7d47015d05c8d00de6  .beagle/checks/T0442/T0442.sh" | sha256sum -c --quiet && bash .beagle/checks/T0442/T0442.sh'
refutes: refuses when beagle.py's `WALL_MAXIMAL_TURNS = 3` is put back as `WALL_MAXIMAL_TURNS = 2` and beagle.py's `_KILLED_PROGRESS[(root_key, task)] = kept` is put back as `pass` (proven 2026-10-11T22:55:05+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_wall_scales_with_max_to
refused after 9s of a 5m13s check at: FAILED tests/test_beagle_example_extension.py::test_worker_wall_scales_with_max_tokens_and_measured_rate
refused with: 2 failed, 1 passed, 760 deselected in 7.92s
replaces: refuses when beagle.py's `_KILLED_PROGRESS[(root_key, task)] = kept` is put back as `` (proven 2026-10-11T22:49:33+00:00; refused at ERROR tests/test_beagle_example_extension.py::test_worker_wall_scales_with_max_tokens_and_measured_rate)
