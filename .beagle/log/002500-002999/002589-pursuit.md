+++
id = "002589-pursuit"
ordinal = 2589
kind = "pursuit"
timestamp = "2026-10-12T22:27:30+00:00"
summary = "pursuit prove T0507: WITNESSED — refuses when beagle.py's `known or (bool(command) and _contract_refs_call…` is put back as `known`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "57a41e253892417ccb72581c8133a5d05be737cff1a869e0d790ed888b070ce2  .beagle/checks/T0507/T0507.sh" | sha256sum -c --quiet && bash .beagle/checks/T0507/T0507.sh'
refutes: refuses when beagle.py's `known or (bool(command) and _contract_refs_call…` is put back as `known` (proven 2026-10-12T22:26:33+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_contract_worker_reads_the_references_by_contract_refs)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_contract_worker_reads_the_references_by_contract_refs
refused with: 1 failed, 3 passed, 830 deselected in 0.83s
