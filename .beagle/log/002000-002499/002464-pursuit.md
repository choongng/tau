+++
id = "002464-pursuit"
ordinal = 2464
kind = "pursuit"
timestamp = "2026-10-12T16:12:12+00:00"
summary = "pursuit prove T0481: WITNESSED — refuses when pursuit.py's `if early and not before_contract.strip():` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ec15a3634a13bc3c579fffd90997d29a99b3cae837f8a1eca46562092226955f  .beagle/checks/T0481/T0481.sh" | sha256sum -c --quiet && bash .beagle/checks/T0481/T0481.sh'
refutes: refuses when pursuit.py's `if early and not before_contract.strip():` is put back as `if False:` (proven 2026-10-12T16:11:15+00:00; refused at FAILED tests/test_contract.py::test_open_refuses_non_contract_work_before_the_seal)
refused after 1s of a 2s check at: FAILED tests/test_contract.py::test_open_refuses_non_contract_work_before_the_seal
refused with: 1 failed, 8 passed, 17 deselected in 0.34s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
