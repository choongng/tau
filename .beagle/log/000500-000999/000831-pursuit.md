+++
id = "000831-pursuit"
ordinal = 831
kind = "pursuit"
timestamp = "2026-10-05T01:50:31+00:00"
summary = "pursuit prove T0212: WITNESSED — refuses when beagle.py's `if _find_goal(session_cwd) is not None:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a4e3a9305b018c765daaded68053ea03ee91a0f35f959da625ca7561f7f074e5  .beagle/checks/T0212/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0212/check.sh'
refutes: refuses when beagle.py's `if _find_goal(session_cwd) is not None:` is put back as `if False:` (proven 2026-10-05T01:50:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_dispatch_text_in_a_founded_session_names_no_guard_refused_bash_comm…)
refused after 2s of a 1m08s check at: FAILED tests/test_beagle_example_extension.py::test_dispatch_text_in_a_founded_session_names_no_guard_refused_bash_comm…
refused with: 1 failed in 1.79s
