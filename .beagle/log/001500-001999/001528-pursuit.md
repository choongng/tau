+++
id = "001528-pursuit"
ordinal = 1528
kind = "pursuit"
timestamp = "2026-10-10T04:50:05+00:00"
summary = "pursuit open T0351: Cases test naming: never call the data test the cases test; flag a self-contained one"
metric_command = ""
drains = []
hooks = []
+++

criteria: _cases_test_close_note never names the bound data test (a test importing no project module) as the cases test: it names the scope's other test or says the cases test is still to be written. _cases_test_problem flags a locked cases test that defines the functions it calls and imports no project module. Structural (AST, imports), no domain words. Regression tests test_cases_test_close_note_never_names_the_data_test and test_cases_test_problem_flags_in_file_implementation; whole file passes, ruff clean.
decided by: sh -c 'echo "2fc90b8125fa266bdbe447a420144dd386054493d39567e2557787023cdcc2cc  .beagle/checks/T0351/T0351.sh" | sha256sum -c --quiet && bash .beagle/checks/T0351/T0351.sh'
budget: 70000 tokens
