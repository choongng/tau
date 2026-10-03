+++
id = "000364-pursuit"
ordinal = 364
kind = "pursuit"
timestamp = "2026-10-03T21:12:36+00:00"
summary = "pursuit prove T0084: WITNESSED — refuses when beagle.py's `last += f\"\\n\\nLast pursuit_step on {task} said:…` is put back as `last += \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ff6b00093ce07764e9fc6f7922be7152985805f4dbc22ebb54fccbf66c060ff2  .beagle/checks/T0084/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0084/check.sh'
refutes: refuses when beagle.py's `last += f"\n\nLast pursuit_step on {task} said:…` is put back as `last += ""` (proven 2026-10-03T21:11:52+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_state_after_compaction_repeats_last_step_result)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_state_after_compaction_repeats_last_step_result
refused with: 1 failed, 2 passed, 293 deselected in 0.72s
