+++
id = "000433-pursuit"
ordinal = 433
kind = "pursuit"
timestamp = "2026-10-04T01:52:35+00:00"
summary = "pursuit prove T0111: WITNESSED — refuses when beagle.py's `and (_SCRIPT_WRITE.search(command) or _SCRIPT_S…` is put back as `and _SCRIPT_WRITE.search(command) is not None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9903479c441c8080c522a1ee3c971ce54805a6de361441ac64b82947e66e2299  .beagle/checks/T0111/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0111/check.sh'
refutes: refuses when beagle.py's `and (_SCRIPT_WRITE.search(command) or _SCRIPT_S…` is put back as `and _SCRIPT_WRITE.search(command) is not None` (proven 2026-10-04T01:51:47+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_blocks_sed_through_os_system_in_inline_python)
refused after 1s of a 29s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_blocks_sed_through_os_system_in_inline_python
refused with: 1 failed in 0.61s
