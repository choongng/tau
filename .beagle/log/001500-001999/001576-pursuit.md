+++
id = "001576-pursuit"
ordinal = 1576
kind = "pursuit"
timestamp = "2026-10-10T16:40:15+00:00"
summary = "pursuit open T0369: Cases-test note: never name the data test when the scope has no room"
metric_command = ""
drains = []
hooks = []
+++

criteria: _cases_test_close_note never names a test that reads the data file and imports no project module (the data test) as the cases test, whatever the scope: with no other test in scope and no directory, it says the cases test is still to be written. A test that imports the code and reads the data is still named. The docstring says so. Regression test test_cases_test_close_note_never_names_the_data_test_without_room (scope holding only the data test, no dir); T0351's tests still pass; whole file passes, ruff clean.
decided by: sh -c 'echo "0acbe6d5c2bf4d7744f8624b10825d1df67ec4168038aadf6dbb6a3e11e91a23  .beagle/checks/T0369/T0369.sh" | sha256sum -c --quiet && bash .beagle/checks/T0369/T0369.sh'
budget: 40000 tokens
