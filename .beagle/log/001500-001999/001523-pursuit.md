+++
id = "001523-pursuit"
ordinal = 1523
kind = "pursuit"
timestamp = "2026-10-10T04:39:04+00:00"
summary = "pursuit open T0350: Refuse a check that runs a test file absent and out of scope"
metric_command = ""
drains = []
hooks = []
+++

criteria: Open refuses a done_when whose test file is neither on disk nor in the task's scope, with the call that works (scope plus that file). A not-done result and the new_route refusal from a check that exits pytest 4 'file or directory not found: X', X outside scope, call the check broken and name X and the scope. The brief's scope line says writes outside the scope are refused. Structural, no domain words. Regression tests test_open_refuses_check_running_absent_file_outside_scope, test_not_done_names_absent_check_file_outside_scope, test_brief_scope_line_says_outside_writes_are_refused; whole file passes, ruff clean.
decided by: sh -c 'echo "733979462aee4f8dd176f4dd1e08b58da7ed547d7c87641cd5d4e7f9b7009da5  .beagle/checks/T0350/T0350.sh" | sha256sum -c --quiet && bash .beagle/checks/T0350/T0350.sh'
budget: 90000 tokens
