+++
id = "000572-pursuit"
ordinal = 572
kind = "pursuit"
timestamp = "2026-10-04T07:43:28+00:00"
summary = "pursuit prove T0137: WITNESSED — refuses when beagle.py's `if _named(argv, \"git\") and _git_reads_store(arg…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a740f698bb8f97421c970d85a4a9d8c08d7256c6901aaf864838b321afa388cd  .beagle/checks/T0137/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0137/check.sh'
refutes: refuses when beagle.py's `if _named(argv, "git") and _git_reads_store(arg…` is put back as `if False:` (proven 2026-10-04T07:42:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_git_show_of_a_dot_beagle_path)
refused after 2s of a 54s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_git_show_of_a_dot_beagle_path
refused with: 1 failed, 1 passed in 1.38s
