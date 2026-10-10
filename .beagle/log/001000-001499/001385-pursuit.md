+++
id = "001385-pursuit"
ordinal = 1385
kind = "pursuit"
timestamp = "2026-10-10T00:37:39+00:00"
summary = "pursuit prove T0329: WITNESSED — refuses when tools.py's `if set(arguments) == {\"_raw_arguments\"}:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9fd7d0b003dad6f90db8eda15b6e35dc33ce7379c4b87ce8cc3540d736e4149c  .beagle/checks/T0329/T0329.sh" | sha256sum -c --quiet && bash .beagle/checks/T0329/T0329.sh'
refutes: refuses when tools.py's `if set(arguments) == {"_raw_arguments"}:` is put back as `if False:` (proven 2026-10-10T00:36:43+00:00; refused at FAILED tests/test_tool_cut_off_arguments.py::test_cut_off_write_names_the_cut_off_not_the_path[asyncio])
refused after 1s of a 3s check at: FAILED tests/test_tool_cut_off_arguments.py::test_cut_off_write_names_the_cut_off_not_the_path[asyncio]
refused with: 1 failed in 0.38s
