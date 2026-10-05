+++
id = "001216-pursuit"
ordinal = 1216
kind = "pursuit"
timestamp = "2026-10-05T20:57:24+00:00"
summary = "pursuit prove T0288: WITNESSED — refuses when beagle.py's `collection = _collection_failure_lead(verdict[1…` is put back as `collection = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6da4a1193d59bc7e30d2afc3ca94be5389e6d5f4452c950c36085ec5308a35f8  .beagle/checks/T0288/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0288/check.sh'
refutes: refuses when beagle.py's `collection = _collection_failure_lead(verdict[1…` is put back as `collection = ""` (proven 2026-10-05T20:57:24+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_not_done_lead_names_failing_import)
refused after 3s of a 1m37s check at: FAILED tests/test_beagle_example_extension.py::test_not_done_lead_names_failing_import
refused with: 1 failed, 1 passed in 2.98s
