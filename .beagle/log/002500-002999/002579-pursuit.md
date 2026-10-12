+++
id = "002579-pursuit"
ordinal = 2579
kind = "pursuit"
timestamp = "2026-10-12T22:10:29+00:00"
summary = "pursuit prove T0505: WITNESSED — refuses when beagle.py's `if _pursuit_verb(argv) == \"contract\" and _pursu…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b5400aad53b63bd9c65394dce202add40c93dfce6c0cd197e2b48b4165b32029  .beagle/checks/T0505/T0505.sh" | sha256sum -c --quiet && bash .beagle/checks/T0505/T0505.sh'
refutes: refuses when beagle.py's `if _pursuit_verb(argv) == "contract" and _pursu…` is put back as `if False:` (proven 2026-10-12T22:09:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_beagle_commands_and_beagle_reads)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_beagle_commands_and_beagle_reads
refused with: 1 failed, 14 passed, 818 deselected in 1.13s
