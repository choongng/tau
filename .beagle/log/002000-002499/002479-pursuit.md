+++
id = "002479-pursuit"
ordinal = 2479
kind = "pursuit"
timestamp = "2026-10-12T16:27:58+00:00"
summary = "pursuit prove T0484: WITNESSED — refuses when hooks.py's `if rel not in settings.sealed_paths:` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "59827c474fa267de99e5719caa55685d7e132e3028d6c3f356ec5ea6bcf0ae3e  .beagle/checks/T0484/T0484.sh" | sha256sum -c --quiet && bash .beagle/checks/T0484/T0484.sh'
refutes: refuses when hooks.py's `if rel not in settings.sealed_paths:` is put back as `if True:` (proven 2026-10-12T16:27:01+00:00; refused at FAILED tests/test_contract.py::test_contract_guard_refuses_an_edit_to_a_sealed_file)
refused after 0s of a 1s check at: FAILED tests/test_contract.py::test_contract_guard_refuses_an_edit_to_a_sealed_file
refused with: 1 failed, 1 passed, 34 deselected in 0.12s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
