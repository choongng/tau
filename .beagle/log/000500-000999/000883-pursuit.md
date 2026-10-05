+++
id = "000883-pursuit"
ordinal = 883
kind = "pursuit"
timestamp = "2026-10-05T04:12:50+00:00"
summary = "pursuit prove T0222: WITNESSED — refuses when beagle.py's `imports_project = bool(_test_project_imports(ro…` is put back as `imports_project = True`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5cb46269df3c975443a5766a9fdab77daf46bac3252cd21bb93950fe9ed7205c  .beagle/checks/T0222/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0222/check.sh'
refutes: refuses when beagle.py's `imports_project = bool(_test_project_imports(ro…` is put back as `imports_project = True` (proven 2026-10-05T04:12:33+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_long_helper_in_data_test_is_not_misplaced)
refused after 2s of a 1m09s check at: FAILED tests/test_beagle_example_extension.py::test_long_helper_in_data_test_is_not_misplaced
refused with: 1 failed in 1.71s
