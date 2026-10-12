+++
id = "002137-pursuit"
ordinal = 2137
kind = "pursuit"
timestamp = "2026-10-12T09:20:44+00:00"
summary = "pursuit prove T0457: WITNESSED — refuses when beagle.py's `and not _in_scope(how[1], scope, root)` is put back as `and False` and beagle.py's `if proof.weak and tests_in_scope` is put back as `if proof.weak`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "112e8eb6cc5ac03096ba09df8985fc9263afb1e302d52676c3f3b2ad3197f9ac  .beagle/checks/T0457/T0457.sh" | sha256sum -c --quiet && bash .beagle/checks/T0457/T0457.sh'
refutes: refuses when beagle.py's `and not _in_scope(how[1], scope, root)` is put back as `and False` and beagle.py's `if proof.weak and tests_in_scope` is put back as `if proof.weak` (proven 2026-10-12T09:20:43+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_prove_witness_outside_scope
refused after 4s of a 2m46s check at: FAILED tests/test_beagle_example_extension.py::test_prove_witness_outside_scope_does_not_preempt_absence_of_the_tasks_o…
refused with: 2 failed, 804 deselected in 3.41s
