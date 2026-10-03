+++
id = "000220-pursuit"
ordinal = 220
kind = "pursuit"
timestamp = "2026-10-03T18:34:59+00:00"
summary = "pursuit prove T0062: WITNESSED — refuses when beagle.py's `if not specs: return None rc, out = _run( [\"git…` is put back as `if True: return None rc, out = _run( [\"git\", \"c…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7a6f6fe81562630de3e2484a36bdafdd8a74dd2f1fd753c408b8f73d44f93a59  .beagle/checks/T0062/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0062/check.sh'
refutes: refuses when beagle.py's `if not specs: return None rc, out = _run( ["git…` is put back as `if True: return None rc, out = _run( ["git", "c…` (proven 2026-10-03T18:34:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_commits_beagle_setup_files)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_commits_beagle_setup_files
refused with: 2 failed, 260 deselected in 0.61s
