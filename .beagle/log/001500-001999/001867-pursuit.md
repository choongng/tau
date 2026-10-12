+++
id = "001867-pursuit"
ordinal = 1867
kind = "pursuit"
timestamp = "2026-10-12T00:49:01+00:00"
summary = "pursuit prove T0445: WITNESSED — refuses when beagle.py's `calls -= 1 # q35 R51: not counted toward the no…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7a035fffab63f905bdb591b1e5f2c9f4585beeab58f47ba9ba5d50826dd91cf2  .beagle/checks/T0445/T0445.sh" | sha256sum -c --quiet && bash .beagle/checks/T0445/T0445.sh'
refutes: refuses when beagle.py's `calls -= 1 # q35 R51: not counted toward the no…` is put back as `pass` (proven 2026-10-12T00:49:01+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_worker_ranged_reference_read_is_not_refused)
refused after 5s of a 2m37s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_worker_ranged_reference_read_is_not_refused
refused with: 2 failed, 1 passed, 779 deselected in 4.24s
