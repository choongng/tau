+++
id = "000153-pursuit"
ordinal = 153
kind = "pursuit"
timestamp = "2026-10-03T16:28:14+00:00"
summary = "pursuit prove T0049: WITNESSED — refuses when beagle.py's `if name == \"touch\":` is put back as `if name == \"touch-never\":`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "075ab2cda170c950c8a0d49e0d365f80e0632b7c9b300321763f55b2ba9f63a1  .beagle/checks/T0049/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0049/check.sh'
refutes: refuses when beagle.py's `if name == "touch":` is put back as `if name == "touch-never":` (proven 2026-10-03T16:27:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_touch_and_mkdir_out_of_scope)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_touch_and_mkdir_out_of_scope
refused with: 1 failed, 3 passed, 244 deselected in 1.06s
