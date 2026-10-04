+++
id = "000614-pursuit"
ordinal = 614
kind = "pursuit"
timestamp = "2026-10-04T09:18:52+00:00"
summary = "pursuit prove T0146: WITNESSED — refuses when beagle.py's `if _script_reads_store(argv):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a47cfb0f4d96aa879f1bfaeac59e7665030f795916d1daf4c92856094513610a  .beagle/checks/T0146/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0146/check.sh'
refutes: refuses when beagle.py's `if _script_reads_store(argv):` is put back as `if False:` (proven 2026-10-04T09:18:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_other_readers_of_dot_beagle)
refused after 2s of a 49s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_other_readers_of_dot_beagle
refused with: 1 failed in 1.45s
