+++
id = "000857-pursuit"
ordinal = 857
kind = "pursuit"
timestamp = "2026-10-05T02:38:58+00:00"
summary = "pursuit prove T0217: WITNESSED — refuses when beagle.py's `lead = f\"pursuit_step: {task} not run — call in…` is put back as `lead = f\"pursuit_step: {task} not run: \"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7dc16fa2e3db09df2cc484b0691f33422f339366881715d40f8cacb597359f45  .beagle/checks/T0217/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0217/check.sh'
refutes: refuses when beagle.py's `lead = f"pursuit_step: {task} not run — call in…` is put back as `lead = f"pursuit_step: {task} not run: "` (proven 2026-10-05T02:38:41+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_escalation_first_line_holds_the_working_call)
refused after 2s of a 1m09s check at: FAILED tests/test_beagle_example_extension.py::test_escalation_first_line_holds_the_working_call
refused with: 1 failed in 1.72s
