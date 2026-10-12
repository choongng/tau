+++
id = "002117-pursuit"
ordinal = 2117
kind = "pursuit"
timestamp = "2026-10-12T09:07:36+00:00"
summary = "pursuit prove T0453: WITNESSED — refuses when beagle.py's `task, done, check, paths, root, named, targets=…` is put back as `task, done, check, paths, root, named, targets=…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e1fc03f2bf5e934160c900afff5fdc294d5db9e6b80cad29477d9c9c3f0a8d51  .beagle/checks/T0453/T0453.sh" | sha256sum -c --quiet && bash .beagle/checks/T0453/T0453.sh'
refutes: refuses when beagle.py's `task, done, check, paths, root, named, targets=…` is put back as `task, done, check, paths, root, named, targets=…` (proven 2026-10-12T09:07:35+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_done_by_without_scope_offers_the_committed_source_the_check_
refused after 3s of a 2m42s check at: FAILED tests/test_beagle_example_extension.py::test_done_by_without_scope_offers_the_committed_source_the_check_targets…
refused with: 1 failed, 798 deselected in 2.89s
