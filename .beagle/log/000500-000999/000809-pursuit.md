+++
id = "000809-pursuit"
ordinal = 809
kind = "pursuit"
timestamp = "2026-10-05T01:15:47+00:00"
summary = "pursuit prove T0207: WITNESSED — refuses when beagle.py's `return sorted(rel for rel in _lock_manifest(goa…` is put back as `return sorted(str(p.relative_to(store)) for p i…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6c1078f35022f34b987fc6a8fb366e9c3b3a14f60459cc13f4c7d33b57475e3f  .beagle/checks/T0207/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0207/check.sh'
refutes: refuses when beagle.py's `return sorted(rel for rel in _lock_manifest(goa…` is put back as `return sorted(str(p.relative_to(store)) for p i…` (proven 2026-10-05T01:15:29+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_locked_ignores_files_not_in_the_manifest)
refused after 2s of a 1m08s check at: FAILED tests/test_beagle_example_extension.py::test_locked_ignores_files_not_in_the_manifest
refused with: 1 failed, 8 passed in 1.99s
