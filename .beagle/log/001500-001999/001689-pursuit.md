+++
id = "001689-pursuit"
ordinal = 1689
kind = "pursuit"
timestamp = "2026-10-10T23:49:23+00:00"
summary = "pursuit prove T0391: WITNESSED — refuses when beagle.py's `if ran and _LAST_CHECK_EXIT.get(key, 0) == 0 an…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "175fcf109ca4e9fbddddac9ae6bbb9a869c75b26d94229702a082e31a280b017  .beagle/checks/T0391/T0391.sh" | sha256sum -c --quiet && bash .beagle/checks/T0391/T0391.sh'
refutes: refuses when beagle.py's `if ran and _LAST_CHECK_EXIT.get(key, 0) == 0 an…` is put back as `if False:` (proven 2026-10-10T23:49:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_source_judge_escalation_after_an_early_failed_check)
refused after 1s of a 2m18s check at: FAILED tests/test_beagle_example_extension.py::test_source_judge_escalation_after_an_early_failed_check
refused with: 2 failed, 1 passed, 722 deselected in 0.94s
