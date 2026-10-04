+++
id = "000463-pursuit"
ordinal = 463
kind = "pursuit"
timestamp = "2026-10-04T02:42:08+00:00"
summary = "pursuit prove T0118: WITNESSED — refuses when beagle.py's `if rc not in (127, 129) and not usage:` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8c3b44205cc1d8286160b4c6358fcd7532989a2905083ccd802db48ba0391eb9  .beagle/checks/T0118/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0118/check.sh'
refutes: refuses when beagle.py's `if rc not in (127, 129) and not usage:` is put back as `if True:` (proven 2026-10-04T02:41:18+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_check_that_exits_with_a_git_usage_error)
refused after 1s of a 30s check at: FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_check_that_exits_with_a_git_usage_error
refused with: 1 failed in 1.14s
