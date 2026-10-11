+++
id = "001720-pursuit"
ordinal = 1720
kind = "pursuit"
timestamp = "2026-10-11T00:28:56+00:00"
summary = "pursuit prove T0401: WITNESSED — refuses when beagle.py's `if not _scope_has_data(scope, root) and not rea…` is put back as `if not _scope_has_data(scope) and not reads:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "99725eb7ae8820ec278d7383e9ed4e35ab2cdb4ce1d89a758e8f963864a07dcf  .beagle/checks/T0401/T0401.sh" | sha256sum -c --quiet && bash .beagle/checks/T0401/T0401.sh'
refutes: refuses when beagle.py's `if not _scope_has_data(scope, root) and not rea…` is put back as `if not _scope_has_data(scope) and not reads:` (proven 2026-10-11T00:28:56+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_directory_scope_data_reaches_every_scope_has_data_route)
refused after 1s of a 2m11s check at: FAILED tests/test_beagle_example_extension.py::test_directory_scope_data_reaches_every_scope_has_data_route
refused with: 1 failed, 1 passed, 727 deselected in 1.02s
