+++
id = "002448-pursuit"
ordinal = 2448
kind = "pursuit"
timestamp = "2026-10-12T15:53:16+00:00"
summary = "pursuit prove T0480: WITNESSED — refuses when contract.py's `return [s for s in spans if not any(s.overlaps(…` is put back as `return []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a2478a631c8aad5066daff577ebedbdc5e86cc62ff0dbb1aa3f3bf44cf3bb294  .beagle/checks/T0480/T0480.sh" | sha256sum -c --quiet && bash .beagle/checks/T0480/T0480.sh'
refutes: refuses when contract.py's `return [s for s in spans if not any(s.overlaps(…` is put back as `return []` (proven 2026-10-12T15:52:19+00:00; refused at FAILED tests/test_contract.py::test_contract_diff_reports_spans_and_operations_only_one_side_cites)
refused after 0s of a 2s check at: FAILED tests/test_contract.py::test_contract_diff_reports_spans_and_operations_only_one_side_cites
refused with: 3 failed, 2 passed, 9 deselected in 0.14s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
