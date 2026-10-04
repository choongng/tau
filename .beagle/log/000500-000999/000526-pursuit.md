+++
id = "000526-pursuit"
ordinal = 526
kind = "pursuit"
timestamp = "2026-10-04T04:57:37+00:00"
summary = "pursuit prove T0129: WITNESSED — refuses when beagle.py's `fields = proc.stdout.split(\"\\0\")` is put back as `fields = proc.stdout.strip().split(\"\\0\")`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bd597bf3871f69b5b94ff5ae789290c1f56c651d74a999d8db1c01c6f3fbc3ba  .beagle/checks/T0129/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0129/check.sh'
refutes: refuses when beagle.py's `fields = proc.stdout.split("\0")` is put back as `fields = proc.stdout.strip().split("\0")` (proven 2026-10-04T04:56:46+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_changed_files_keeps_the_first_path_whole)
refused after 1s of a 33s check at: FAILED tests/test_beagle_example_extension.py::test_changed_files_keeps_the_first_path_whole
refused with: 1 failed in 0.49s
