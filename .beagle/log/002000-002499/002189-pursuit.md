+++
id = "002189-pursuit"
ordinal = 2189
kind = "pursuit"
timestamp = "2026-10-12T09:43:13+00:00"
summary = "pursuit prove T0460: WITNESSED — refuses when beagle.py's `ask_module = True` is put back as `ask_module = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a4026e4b864ca7693d647106f7918de62ec87c357443fe8c4fe847938f32c38a  .beagle/checks/T0460/T0460.sh" | sha256sum -c --quiet && bash .beagle/checks/T0460/T0460.sh'
refutes: refuses when beagle.py's `ask_module = True` is put back as `ask_module = False` (proven 2026-10-12T09:43:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_import_only_not_proof_next_asks_for_a_witness_not_a_new_check)
refused after 4s of a 2m49s check at: FAILED tests/test_beagle_example_extension.py::test_import_only_not_proof_next_asks_for_a_witness_not_a_new_check
refused with: 1 failed, 808 deselected in 3.24s
