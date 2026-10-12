+++
id = "002484-pursuit"
ordinal = 2484
kind = "pursuit"
timestamp = "2026-10-12T16:34:47+00:00"
summary = "pursuit prove T0485: WITNESSED — refuses when refs.py's `if name and (where / name).is_file() and not re…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d03e65a39b3e167af61d1fa91c4be41fbfe0ec01c0a9218c7bda9e586cb15efe  .beagle/checks/T0485/T0485.sh" | sha256sum -c --quiet && bash .beagle/checks/T0485/T0485.sh'
refutes: refuses when refs.py's `if name and (where / name).is_file() and not re…` is put back as `if False:` (proven 2026-10-12T16:33:48+00:00; refused at FAILED tests/test_refs.py::test_refs_fetch_keeps_what_is_on_disk_and_records_a_failure)
refused after 2s of a 4s check at: FAILED tests/test_refs.py::test_refs_fetch_keeps_what_is_on_disk_and_records_a_failure
refused with: 1 failed, 3 passed in 1.72s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
