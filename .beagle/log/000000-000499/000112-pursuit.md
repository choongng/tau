+++
id = "000112-pursuit"
ordinal = 112
kind = "pursuit"
timestamp = "2026-10-03T14:44:21+00:00"
summary = "pursuit prove T0040: WITNESSED — refuses when beagle.py's `ESCALATE_AFTER = 3` is put back as `ESCALATE_AFTER = 99`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4cd101a91edc8d41c127e75eed47463a3809a7901bf94b95376b9188562affdd  .beagle/checks/T0040/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0040/check.sh'
refutes: refuses when beagle.py's `ESCALATE_AFTER = 3` is put back as `ESCALATE_AFTER = 99` (proven 2026-10-03T14:44:08+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_fourth_step_after_three_not_done_is_refused_with_choices)
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_fourth_step_after_three_not_done_is_refused_with_choices
refused with: 1 failed, 2 passed, 226 deselected in 1.67s
