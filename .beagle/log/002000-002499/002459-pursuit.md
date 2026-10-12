+++
id = "002459-pursuit"
ordinal = 2459
kind = "pursuit"
timestamp = "2026-10-12T16:10:43+00:00"
summary = "pursuit prove T0494: WITNESSED — refuses when contract.py's `ident=f\"$ {command}\")` is put back as `ident=name)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "291560d8520fd5ed9c5409f3c2317df20c6994dc70d2465aace34962cf78067b  .beagle/checks/T0494/T0494.sh" | sha256sum -c --quiet && bash .beagle/checks/T0494/T0494.sh'
refutes: refuses when contract.py's `ident=f"$ {command}")` is put back as `ident=name)` (proven 2026-10-12T16:09:47+00:00; refused at FAILED tests/test_contract.py::test_contract_diff_identifies_an_experiment_by_its_command)
refused after 0s of a 1s check at: FAILED tests/test_contract.py::test_contract_diff_identifies_an_experiment_by_its_command
refused with: 1 failed, 2 passed, 23 deselected in 0.11s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
