+++
id = "001604-pursuit"
ordinal = 1604
kind = "pursuit"
timestamp = "2026-10-10T18:45:34+00:00"
summary = "pursuit open T0375: R42 fix: a task that wrote no cases data is not judged as known answers"
metric_command = ""
drains = []
hooks = []
+++

criteria: A step that passes its check on a task that wrote no cases data (no data file in scope changed, no locks passed) is closed as an ordinary task: it does not lock its docs or tests as known answers and is not held to an earlier task's locked cases data. _unread_cases does not hold a test that imports no project code to earlier-locked data. A task that wrote cases data is handled as before. Structural (file roles from the tree and AST), no domain words. Tests test_close_does_not_lock_docs_and_test_of_a_task_that_wrote_no_cases, test_unread_cases_skips_a_test_importing_no_project_code_for_earlier_locked_data; whole file passes, ruff clean.
decided by: sh -c 'echo "4b1e84f496d530e19fbce82537fc364e675001b1a89a0ed7748be36ec71dbeec  .beagle/checks/T0375/T0375.sh" | sha256sum -c --quiet && bash .beagle/checks/T0375/T0375.sh'
budget: 80000 tokens
