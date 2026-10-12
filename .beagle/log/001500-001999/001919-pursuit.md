+++
id = "001919-pursuit"
ordinal = 1919
kind = "pursuit"
timestamp = "2026-10-12T04:18:46+00:00"
summary = "pursuit prove T0448: WITNESSED — refuses when beagle.py's `wide = [*(source for source in sources if sourc…` is put back as `wide = [*sources, *after]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ec47201eb9604df53fab818b4e895bfd912292063dbfec52a18be42071f3084b  .beagle/checks/T0448/T0448.sh" | sha256sum -c --quiet && bash .beagle/checks/T0448/T0448.sh'
refutes: refuses when beagle.py's `wide = [*(source for source in sources if sourc…` is put back as `wide = [*sources, *after]` (proven 2026-10-12T04:18:46+00:00; predates the task: T0448's fix 14f59569 was merged onto choong-dev before the task opened, because the due audit refused the open; this line is th
refused after 1s of a 2m42s check at: FAILED tests/test_beagle_example_extension.py::test_unquoted_cases_rejects_example_index_row_as_source
refused with: 1 failed, 1 passed, 782 deselected in 0.74s
