+++
id = "001949-pursuit"
ordinal = 1949
kind = "pursuit"
timestamp = "2026-10-12T04:38:52+00:00"
summary = "pursuit prove T0452: WITNESSED — refuses when beagle.py's `elif reported is not None:` is put back as `elif False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d39f3ef876cf5afebe407e663a07d6a8facde8b482e45d3bd8857126eda81c00  .beagle/checks/T0452/T0452.sh" | sha256sum -c --quiet && bash .beagle/checks/T0452/T0452.sh'
refutes: refuses when beagle.py's `elif reported is not None:` is put back as `elif False:` (proven 2026-10-12T04:38:51+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_result_keeps_last_nonempty_report)
refused after 4s of a 2m34s check at: FAILED tests/test_beagle_example_extension.py::test_step_result_keeps_last_nonempty_report
refused with: 1 failed, 1 passed, 796 deselected in 3.28s
