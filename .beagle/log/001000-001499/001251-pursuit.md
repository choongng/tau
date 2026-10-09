+++
id = "001251-pursuit"
ordinal = 1251
kind = "pursuit"
timestamp = "2026-10-09T19:01:35+00:00"
summary = "pursuit prove T0023: WITNESSED — refuses when beagle.py's `.strip() or \"off\"` is put back as `.strip() or \"low\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "473108eb846e652523c3791653cd5717401ebfc3671f87b60660ff7b1f9b5bf8  .beagle/checks/T0023/T0023.sh" | sha256sum -c --quiet && bash .beagle/checks/T0023/T0023.sh'
refutes: refuses when beagle.py's `.strip() or "off"` is put back as `.strip() or "low"` (proven 2026-10-09T19:01:35+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_argv_thinking_level)
refused after 1s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_worker_argv_thinking_level
refused with: 1 failed, 2 passed, 621 deselected in 0.90s
