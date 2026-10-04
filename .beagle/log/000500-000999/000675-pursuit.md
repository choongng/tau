+++
id = "000675-pursuit"
ordinal = 675
kind = "pursuit"
timestamp = "2026-10-04T12:55:42+00:00"
summary = "pursuit prove T0159: WITNESSED — refuses when beagle.py's `async def _passes_only_by_uncommitted(check: st…` is put back as `async def _passes_only_by_uncommitted(check: st…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a79832bf144ae099c96c56063552f2be8bc63a5b573124f8d5f2ba79b68fffc3  .beagle/checks/T0159/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0159/check.sh'
refutes: refuses when beagle.py's `async def _passes_only_by_uncommitted(check: st…` is put back as `async def _passes_only_by_uncommitted(check: st…` (proven 2026-10-04T12:55:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_on_a_check_passing_only_by_uncommitted_scope_work_is_no
refused after 2s of a 1m00s check at: FAILED tests/test_beagle_example_extension.py::test_open_on_a_check_passing_only_by_uncommitted_scope_work_is_not_refus…
refused with: 1 failed in 1.64s
