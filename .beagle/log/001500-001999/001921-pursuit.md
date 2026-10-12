+++
id = "001921-pursuit"
ordinal = 1921
kind = "pursuit"
timestamp = "2026-10-12T04:23:21+00:00"
summary = "pursuit prove T0447: WITNESSED — refuses when beagle.py's `return os.environ.get(LEAN_ENV, \"\") not in (\"\",…` is put back as `return False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ce1555fc7a8fdd3eb1ca6ca331a5c126fe0e093630b59ac9daa8e1a0739303e9  .beagle/checks/T0447/T0447.sh" | sha256sum -c --quiet && bash .beagle/checks/T0447/T0447.sh'
refutes: refuses when beagle.py's `return os.environ.get(LEAN_ENV, "") not in ("",…` is put back as `return False` (proven 2026-10-12T04:23:20+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_lean_switch_turns_off_known_answers_locks)
refused after 8s of a 2m46s check at: FAILED tests/test_beagle_example_extension.py::test_lean_switch_turns_off_known_answers_locks
refused with: 10 failed, 1 passed, 784 deselected in 7.70s
