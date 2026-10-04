+++
id = "000647-pursuit"
ordinal = 647
kind = "pursuit"
timestamp = "2026-10-04T11:25:37+00:00"
summary = "pursuit prove T0153: WITNESSED — refuses when beagle.py's `if not (root / rel).exists()` is put back as `if False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "db248df389b5b6b7218017b3de8bd9823d7f70700b2302c3c2f9fff4e092506e  .beagle/checks/T0153/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0153/check.sh'
refutes: refuses when beagle.py's `if not (root / rel).exists()` is put back as `if False` (proven 2026-10-04T11:25:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_result_flags_report_paths_not_on_disk)
refused after 2s of a 54s check at: FAILED tests/test_beagle_example_extension.py::test_step_result_flags_report_paths_not_on_disk
refused with: 1 failed in 1.65s
