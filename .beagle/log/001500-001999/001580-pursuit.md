+++
id = "001580-pursuit"
ordinal = 1580
kind = "pursuit"
timestamp = "2026-10-10T16:50:47+00:00"
summary = "pursuit prove T0369: WITNESSED — refuses when beagle.py's `cases = test if reads and not data_test else ne…` is put back as `cases = test if reads else next(iter(others), \"…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0acbe6d5c2bf4d7744f8624b10825d1df67ec4168038aadf6dbb6a3e11e91a23  .beagle/checks/T0369/T0369.sh" | sha256sum -c --quiet && bash .beagle/checks/T0369/T0369.sh'
refutes: refuses when beagle.py's `cases = test if reads and not data_test else ne…` is put back as `cases = test if reads else next(iter(others), "…` (proven 2026-10-10T16:50:46+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_close_note_never_names_the_data_test_without_room
refused after 3s of a 1m47s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_close_note_never_names_the_data_test_without_room
refused with: 1 failed, 696 deselected in 2.69s
