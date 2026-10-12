+++
id = "002469-pursuit"
ordinal = 2469
kind = "pursuit"
timestamp = "2026-10-12T16:17:56+00:00"
summary = "pursuit prove T0482: WITNESSED — refuses when contract.py's `and self.acceptance.get(\"code\") == 0 and self.c…` is put back as `and self.acceptance.get(\"code\") == 0)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c7a9966c76f2f0fa16e67a4ebae1ac09b17f29fa7bd5f9990f201b833473cd6c  .beagle/checks/T0482/T0482.sh" | sha256sum -c --quiet && bash .beagle/checks/T0482/T0482.sh'
refutes: refuses when contract.py's `and self.acceptance.get("code") == 0 and self.c…` is put back as `and self.acceptance.get("code") == 0)` (proven 2026-10-12T16:16:57+00:00; refused at FAILED tests/test_contract.py::test_done_gate_keeps_acceptance_with_the_tree_it_ran_on)
refused after 1s of a 2s check at: FAILED tests/test_contract.py::test_done_gate_keeps_acceptance_with_the_tree_it_ran_on
refused with: 1 failed, 3 passed, 26 deselected in 0.36s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
