+++
id = "003029-pursuit"
ordinal = 3029
kind = "pursuit"
timestamp = "2026-10-14T04:51:16+00:00"
summary = "pursuit prove T0581: WITNESSED — refuses when beagle.py's `f\"{CONTRACT_DRAFT}/oracle/, laid out the same: …` is put back as `f\"{CONTRACT_DRAFT}/, laid out the same: a liter…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d11bcdedf57a2830c9697fe6bbea59e619486929196eafa5660ad4631e17a2aa  .beagle/checks/T0581/T0581.sh" | sha256sum -c --quiet && bash .beagle/checks/T0581/T0581.sh'
refutes: refuses when beagle.py's `f"{CONTRACT_DRAFT}/oracle/, laid out the same: …` is put back as `f"{CONTRACT_DRAFT}/, laid out the same: a liter…` (proven 2026-10-14T04:50:17+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_contract_slice_names_the_oracle_standin)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_contract_slice_names_the_oracle_standin
refused with: 1 failed, 724 deselected in 0.82s
standing checks red: T0335, T0360, T0386, T0496, T0519
