+++
id = "000642-pursuit"
ordinal = 642
kind = "pursuit"
timestamp = "2026-10-04T11:20:15+00:00"
summary = "pursuit prove T0152: WITNESSED — refuses when beagle.py's `absent = _absent_locks(locks, root)` is put back as `absent = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "08fd4778ce686b59d2ed9388162510f39da00a56401ab4af7f6e3f25132b762b  .beagle/checks/T0152/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0152/check.sh'
refutes: refuses when beagle.py's `absent = _absent_locks(locks, root)` is put back as `absent = []` (proven 2026-10-04T11:19:42+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_close_refused_when_a_lock_is_not_on_disk)
refused after 2s of a 52s check at: FAILED tests/test_beagle_example_extension.py::test_close_refused_when_a_lock_is_not_on_disk
refused with: 1 failed in 1.44s
