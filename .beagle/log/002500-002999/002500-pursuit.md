+++
id = "002500-pursuit"
ordinal = 2500
kind = "pursuit"
timestamp = "2026-10-12T16:50:55+00:00"
summary = "pursuit prove T0495: WITNESSED — refuses when contract.py's `return expand(root, settings.sealed_paths)` is put back as `return list(settings.sealed_paths)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "91b033d39860d69a2f75bca5911beb97cda4718e952cca8d7c84ffcd48ec091a  .beagle/checks/T0495/T0495.sh" | sha256sum -c --quiet && bash .beagle/checks/T0495/T0495.sh'
refutes: refuses when contract.py's `return expand(root, settings.sealed_paths)` is put back as `return list(settings.sealed_paths)` (proven 2026-10-12T16:49:58+00:00; refused at FAILED tests/test_contract.py::test_a_sealed_directory_holds_every_file_under_it[git])
refused after 0s of a 1s check at: FAILED tests/test_contract.py::test_a_sealed_directory_holds_every_file_under_it[git]
refused with: 2 failed, 1 passed, 36 deselected in 0.16s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
