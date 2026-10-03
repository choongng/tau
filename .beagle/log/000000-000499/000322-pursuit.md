+++
id = "000322-pursuit"
ordinal = 322
kind = "pursuit"
timestamp = "2026-10-03T20:25:48+00:00"
summary = "pursuit prove T0077: WITNESSED — refuses when beagle.py's `_run([\"git\", \"reset\", \"-q\", \"--\", *staged], roo…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f139f11b3050db5a23cf4ba39cce7f7fcc14085ac06cef861c36be4b7917b449  .beagle/checks/T0077/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0077/check.sh'
refutes: refuses when beagle.py's `_run(["git", "reset", "-q", "--", *staged], roo…` is put back as `pass` (proven 2026-10-03T20:25:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_failed_setup_commit_leaves_nothing_staged)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_failed_setup_commit_leaves_nothing_staged
refused with: 1 failed, 1 passed, 280 deselected in 0.64s
