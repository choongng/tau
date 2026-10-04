+++
id = "000604-pursuit"
ordinal = 604
kind = "pursuit"
timestamp = "2026-10-04T09:07:53+00:00"
summary = "pursuit prove T0144: WITNESSED — refuses when beagle.py's `if len(lines) < 2:` is put back as `if len(lines) < 2 or len(parts) != 1:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "13a22e589e93ec0b5c349a6e94afbd1ae5d0c7e4d8c422e89d8e52e239969067  .beagle/checks/T0144/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0144/check.sh'
refutes: refuses when beagle.py's `if len(lines) < 2:` is put back as `if len(lines) < 2 or len(parts) != 1:` (proven 2026-10-04T09:07:16+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_splits_a_multi_line_part_among_others)
refused after 2s of a 49s check at: FAILED tests/test_beagle_example_extension.py::test_plan_splits_a_multi_line_part_among_others
refused with: 1 failed in 1.27s
