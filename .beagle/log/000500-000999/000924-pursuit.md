+++
id = "000924-pursuit"
ordinal = 924
kind = "pursuit"
timestamp = "2026-10-05T06:23:27+00:00"
summary = "pursuit prove T0230: WITNESSED — refuses when beagle.py's `data_only = _data_only_bind(done_when, own, roo…` is put back as `data_only = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "af079428ee0eeea09eafebb9306216a839adfdbce8e6af4a016bf15fb98e347c  .beagle/checks/T0230/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0230/check.sh'
refutes: refuses when beagle.py's `data_only = _data_only_bind(done_when, own, roo…` is put back as `data_only = None` (proven 2026-10-05T06:23:20+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_amend_binds_data_test_when_cases_test_not_on_disk)
refused after 3s of a 1m18s check at: FAILED tests/test_beagle_example_extension.py::test_amend_binds_data_test_when_cases_test_not_on_disk
refused with: 1 failed in 3.00s
