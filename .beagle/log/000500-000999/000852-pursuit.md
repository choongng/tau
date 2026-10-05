+++
id = "000852-pursuit"
ordinal = 852
kind = "pursuit"
timestamp = "2026-10-05T02:24:30+00:00"
summary = "pursuit prove T0216: WITNESSED — refuses when beagle.py's `_UNPROVEN.discard((str(root), task))` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5c0adbda9a69997a2cd12ebd5d7eb4b467a98acde33e894b3d69ecd2711a6338  .beagle/checks/T0216/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0216/check.sh'
refutes: refuses when beagle.py's `_UNPROVEN.discard((str(root), task))` is put back as `pass` (proven 2026-10-05T02:24:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_amended_check_is_not_refused_as_already_passing)
refused after 2s of a 1m12s check at: FAILED tests/test_beagle_example_extension.py::test_amended_check_is_not_refused_as_already_passing
refused with: 1 failed in 1.62s
