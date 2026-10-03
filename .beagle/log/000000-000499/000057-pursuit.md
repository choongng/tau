+++
id = "000057-pursuit"
ordinal = 57
kind = "pursuit"
timestamp = "2026-10-03T12:32:20+00:00"
summary = "pursuit prove T0027: WITNESSED — refuses when beagle.py's `references = await asyncio.to_thread(_fetch_ref…` is put back as `references = {}`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0027/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0027/named_tests.sh tests/test_beagle_example_extension.py 3 test_found_fetches_references test_step_brief_carries_references_and_prompt test_found_reference_fetch_failure_is_noted'
refutes: refuses when beagle.py's `references = await asyncio.to_thread(_fetch_ref…` is put back as `references = {}` (proven 2026-10-03T12:32:16+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_fetches_references)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_fetches_references
refused with: 2 failed, 1 passed, 197 deselected in 0.71s
