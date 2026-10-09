+++
id = "001359-pursuit"
ordinal = 1359
kind = "pursuit"
timestamp = "2026-10-09T23:13:53+00:00"
summary = "pursuit prove T0322: WITNESSED — refuses when beagle.py's `or _NOT_DONE_CHECK_FAILED.get(key) != count` is put back as `or _NOT_DONE_CHECK_FAILED.get(key) != count + 1`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "52ba3ec03f3a2d1cb49d5c0c5d68e6d4ffe0ff6ff011b679a308017cb152e7ac  .beagle/checks/T0322/T0322.sh" | sha256sum -c --quiet && bash .beagle/checks/T0322/T0322.sh'
refutes: refuses when beagle.py's `or _NOT_DONE_CHECK_FAILED.get(key) != count` is put back as `or _NOT_DONE_CHECK_FAILED.get(key) != count + 1` (proven 2026-10-09T23:13:53+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_check_broken_after_passing_steps_earns_one_notes_rerun)
refused after 1s of a 1m42s check at: FAILED tests/test_beagle_example_extension.py::test_check_broken_after_passing_steps_earns_one_notes_rerun
refused with: 1 failed, 1 passed in 0.62s
