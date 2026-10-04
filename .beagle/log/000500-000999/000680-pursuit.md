+++
id = "000680-pursuit"
ordinal = 680
kind = "pursuit"
timestamp = "2026-10-04T13:04:48+00:00"
summary = "pursuit prove T0160: WITNESSED — refuses when beagle.py's `if amends_open:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "dcf98cb32e82d797d23d4b93035a710fbe5167be7b29056d7538c425d5f8d633  .beagle/checks/T0160/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0160/check.sh'
refutes: refuses when beagle.py's `if amends_open:` is put back as `if False:` (proven 2026-10-04T13:04:24+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_data_test_resend_on_an_open_task_amends_instead_of_spawning)
refused after 2s of a 1m03s check at: FAILED tests/test_beagle_example_extension.py::test_data_test_resend_on_an_open_task_amends_instead_of_spawning
refused with: 1 failed in 2.03s
