+++
id = "002507-pursuit"
ordinal = 2507
kind = "pursuit"
timestamp = "2026-10-12T17:05:12+00:00"
summary = "pursuit prove T0488: WITNESSED — refuses when beagle.py's `f\"{CONTRACT_TABLE}\",` is put back as `\"\",`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "363f2aa59eb8137437eade1709ccd9e46d1c7b0dd71be744bb5d20482001f415  .beagle/checks/T0488/T0488.sh" | sha256sum -c --quiet && bash .beagle/checks/T0488/T0488.sh'
refutes: refuses when beagle.py's `f"{CONTRACT_TABLE}",` is put back as `"",` (proven 2026-10-12T17:04:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_declares_the_contract_and_seeds_it_first)
refused after 1s of a 29s check at: FAILED tests/test_beagle_example_extension.py::test_founding_declares_the_contract_and_seeds_it_first
refused with: 1 failed, 1 passed, 824 deselected in 0.89s
replaces: refuses when beagle.py's `f"{CONTRACT_TABLE}",` is put back as `"",` (proven 2026-10-12T17:02:45+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_declares_the_contract_and_seeds_it_first)
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
