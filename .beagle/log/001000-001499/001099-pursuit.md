+++
id = "001099-pursuit"
ordinal = 1099
kind = "pursuit"
timestamp = "2026-10-05T13:36:42+00:00"
summary = "pursuit prove T0265: WITNESSED — refuses when beagle.py's `return \" \".join(_capped([\"timeout\", str(seconds…` is put back as `return f\"timeout {seconds}\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f87bcb586fbcc5c6f17d8bf23b3b6eae003cc1a7cb6b92b4f0cef9e8d245f16a  .beagle/checks/T0265/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0265/check.sh'
refutes: refuses when beagle.py's `return " ".join(_capped(["timeout", str(seconds…` is put back as `return f"timeout {seconds}"` (proven 2026-10-05T13:36:42+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_habit_bounds_command_memory_below_worker_cap)
refused after 3s of a 1m32s check at: FAILED tests/test_beagle_example_extension.py::test_worker_habit_bounds_command_memory_below_worker_cap
refused with: 1 failed in 2.53s
