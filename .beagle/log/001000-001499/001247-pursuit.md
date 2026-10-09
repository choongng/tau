+++
id = "001247-pursuit"
ordinal = 1247
kind = "pursuit"
timestamp = "2026-10-09T19:00:39+00:00"
summary = "pursuit prove T0291: WITNESSED — refuses when beagle.py's `found = _unwritten_import(sibling, scope, root,…` is put back as `found = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0f247735d47d3349591234aea45ce4a1ac6905ed28a79fdbc022ef9100f63809  .beagle/checks/T0291/T0291.sh" | sha256sum -c --quiet && bash .beagle/checks/T0291/T0291.sh'
refutes: refuses when beagle.py's `found = _unwritten_import(sibling, scope, root,…` is put back as `found = None` (proven 2026-10-09T19:00:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_imports_unwritten_follows_sibling_test_import)
refused after 1s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_imports_unwritten_follows_sibling_test_import
refused with: 1 failed in 0.89s
