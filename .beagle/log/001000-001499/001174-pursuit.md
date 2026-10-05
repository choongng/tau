+++
id = "001174-pursuit"
ordinal = 1174
kind = "pursuit"
timestamp = "2026-10-05T17:47:57+00:00"
summary = "pursuit prove T0280: WITNESSED — refuses when beagle.py's `if events.cut_offs >= WORKER_CUT_OFFS:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "88133e6cd85e5e6f2481ba4ade51b4de6dbd638a85875cae58f9d631a0379ce1  .beagle/checks/T0280/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0280/check.sh'
refutes: refuses when beagle.py's `if events.cut_offs >= WORKER_CUT_OFFS:` is put back as `if False:` (proven 2026-10-05T17:47:56+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_ended_on_second_output_cap_cutoff_over_run)
refused after 33s of a 1m38s check at: FAILED tests/test_beagle_example_extension.py::test_worker_ended_on_second_output_cap_cutoff_over_run
refused with: 1 failed, 1 passed in 32.94s
