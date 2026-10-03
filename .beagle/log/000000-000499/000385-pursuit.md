+++
id = "000385-pursuit"
ordinal = 385
kind = "pursuit"
timestamp = "2026-10-03T21:23:14+00:00"
summary = "pursuit prove T0089: WITNESSED — refuses when beagle.py's `and not d.endswith(\"_cache\")` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "01b7531aebef9b4d276e4a09d115cf12323afdf64dd482c21c65d25f0eb6829b  .beagle/checks/T0089/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0089/check.sh'
refutes: refuses when beagle.py's `and not d.endswith("_cache")` is put back as `` (proven 2026-10-03T21:22:23+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_scope_dir_walk_skips_cache_directories)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_scope_dir_walk_skips_cache_directories
refused with: 1 failed, 301 deselected in 0.63s
