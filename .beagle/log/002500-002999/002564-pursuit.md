+++
id = "002564-pursuit"
ordinal = 2564
kind = "pursuit"
timestamp = "2026-10-12T21:48:26+00:00"
summary = "pursuit prove T0502: WITNESSED — refuses when beagle.py's `return None if then is None or then in _CONTRAC…` is put back as `return \"contract\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e5c5454917920aa0080ac04df66a709061d463910e89d7b622412ce235e6a68c  .beagle/checks/T0502/T0502.sh" | sha256sum -c --quiet && bash .beagle/checks/T0502/T0502.sh'
refutes: refuses when beagle.py's `return None if then is None or then in _CONTRAC…` is put back as `return "contract"` (proven 2026-10-12T21:47:26+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_worker_may_read_the_pursuit_but_not_change_it[beagle pursuit cont…)
refused after 2s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_a_worker_may_read_the_pursuit_but_not_change_it[beagle pursuit cont…
refused with: 3 failed, 10 passed, 820 deselected in 1.37s
