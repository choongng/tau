+++
id = "001047-pursuit"
ordinal = 1047
kind = "pursuit"
timestamp = "2026-10-05T11:07:50+00:00"
summary = "pursuit prove T0254: WITNESSED — refuses when beagle.py's `restored = _restore_locked(goal, root, spare)` is put back as `restored = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "10c8de4f8eae49a1bf4604bf6161c909dffb3c3c5d6bd9b47f199350734868f2  .beagle/checks/T0254/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0254/check.sh'
refutes: refuses when beagle.py's `restored = _restore_locked(goal, root, spare)` is put back as `restored = []` (proven 2026-10-05T11:07:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_split_commit_restores_locked_file)
refused after 2s of a 1m25s check at: FAILED tests/test_beagle_example_extension.py::test_split_commit_restores_locked_file
refused with: 1 failed in 2.10s
