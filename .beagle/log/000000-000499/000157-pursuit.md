+++
id = "000157-pursuit"
ordinal = 157
kind = "pursuit"
timestamp = "2026-10-03T16:33:06+00:00"
summary = "pursuit prove T0051: WITNESSED — refuses when beagle.py's `if _FOUND_AWAITS_USER and not context.has_ui:` is put back as `if _FOUND_AWAITS_USER:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "46ac3feb2124a17aae921b80036ba8c04542c9c924fa06ec282646565f8fb6ad  .beagle/checks/T0051/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0051/check.sh'
refutes: refuses when beagle.py's `if _FOUND_AWAITS_USER and not context.has_ui:` is put back as `if _FOUND_AWAITS_USER:` (proven 2026-10-03T16:32:47+00:00; predates the task: the task's change is only tests, and one of them refused; refused at FAILED tests/test_beagle_example_extension.py::test_stop_gate_sa
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_stop_gate_says_nothing_unfounded_in_an_interactive_session
refused with: 1 failed, 5 passed, 245 deselected in 1.69s
