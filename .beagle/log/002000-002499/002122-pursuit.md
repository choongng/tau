+++
id = "002122-pursuit"
ordinal = 2122
kind = "pursuit"
timestamp = "2026-10-12T09:10:52+00:00"
summary = "pursuit prove T0454: WITNESSED — refuses when beagle.py's `if run.unreported or (run.stop_reason == \"lengt…` is put back as `if run.unreported`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2b8db83651158cb5b7617ab4d4aa843da8881607d7ea7fcf0a289b97123fd34b  .beagle/checks/T0454/T0454.sh" | sha256sum -c --quiet && bash .beagle/checks/T0454/T0454.sh'
refutes: refuses when beagle.py's `if run.unreported or (run.stop_reason == "lengt…` is put back as `if run.unreported` (proven 2026-10-12T09:10:51+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_retry_note_after_killed_attempt_does_not_say_reported_back)
refused after 3s of a 2m44s check at: FAILED tests/test_beagle_example_extension.py::test_retry_note_after_killed_attempt_does_not_say_reported_back
refused with: 1 failed, 799 deselected in 3.08s
