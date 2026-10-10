+++
id = "001559-pursuit"
ordinal = 1559
kind = "pursuit"
timestamp = "2026-10-10T15:20:40+00:00"
summary = "pursuit prove T0365: WITNESSED — refuses when beagle.py's `_offered_task(store.parent)` is put back as `\"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3911a126e28c0bed548ae56dc388ab008dafe4d19790bb7c59e04fe5331b6ba5  .beagle/checks/T0365/T0365.sh" | sha256sum -c --quiet && bash .beagle/checks/T0365/T0365.sh'
refutes: refuses when beagle.py's `_offered_task(store.parent)` is put back as `""` (proven 2026-10-10T15:20:40+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_driver_edit_refusal_names_the_step_for_the_ready_task)
refused after 3s of a 1m48s check at: FAILED tests/test_beagle_example_extension.py::test_driver_edit_refusal_names_the_step_for_the_ready_task
refused with: 1 failed, 1 passed, 694 deselected in 2.74s
