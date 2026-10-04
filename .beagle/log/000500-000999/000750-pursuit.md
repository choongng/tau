+++
id = "000750-pursuit"
ordinal = 750
kind = "pursuit"
timestamp = "2026-10-04T16:59:48+00:00"
summary = "pursuit prove T0173: WITNESSED — refuses when beagle.py's `passed_on_disk = (pre_rc, pre_out)` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a374cb5d572a865d8cf84fba328dedda3712a04f18caaa47807e63654918f998  .beagle/checks/T0173/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0173/check.sh'
refutes: refuses when beagle.py's `passed_on_disk = (pre_rc, pre_out)` is put back as `pass` (proven 2026-10-04T16:59:24+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_closes_without_a_worker_when_uncommitted_work_already_passes)
refused after 2s of a 1m03s check at: FAILED tests/test_beagle_example_extension.py::test_open_closes_without_a_worker_when_uncommitted_work_already_passes
refused with: 1 failed in 1.85s
