+++
id = "001779-pursuit"
ordinal = 1779
kind = "pursuit"
timestamp = "2026-10-11T02:53:40+00:00"
summary = "pursuit prove T0412: WITNESSED — refuses when beagle.py's `so it is right only if the expression means a f…` is put back as `so a pass condition there passes bad work and f…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "38edd181666586017b4297980d9bb836fedf6551ca3c16eaeedcd380b23dc9f8  .beagle/checks/T0412/T0412.sh" | sha256sum -c --quiet && bash .beagle/checks/T0412/T0412.sh'
refutes: refuses when beagle.py's `so it is right only if the expression means a f…` is put back as `so a pass condition there passes bad work and f…` (proven 2026-10-11T02:53:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_bool_exit_refusal_does_not_say_a_failure_condition_passes_ba
refused after 3s of a 2m16s check at: FAILED tests/test_beagle_example_extension.py::test_bool_exit_refusal_does_not_say_a_failure_condition_passes_bad_work
refused with: 1 failed, 2 passed, 750 deselected in 2.95s
