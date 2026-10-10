+++
id = "001587-pursuit"
ordinal = 1587
kind = "pursuit"
timestamp = "2026-10-10T17:04:05+00:00"
summary = "pursuit open T0370: R41 fix: not-done names a data test that imports the unwritten module"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a step on a known-answers task (scope of data and tests, no code) ends not done and the scope's data test in the tree imports a top-level module that neither the project tree nor the worker's environment provides (found by AST and a file/spec lookup, no domain words), the step's result names the test file, the import line and that the data test must import none of the code (it loads the data only), and its Next is a notes-only pursuit_step on the same task that keeps the bound check, not a new done_when. A data test importing only stdlib or installed modules, or a module the tree has, gets the result as before. Tests test_not_done_names_data_test_importing_unwritten_module, test_data_test_import_next_is_notes_not_done_when; whole file passes, ruff clean.
decided by: sh -c 'echo "f955ac78d7088cec51c9968ab9fd2acd8ac4551892f9c5d7668203b86c85f643  .beagle/checks/T0370/T0370.sh" | sha256sum -c --quiet && bash .beagle/checks/T0370/T0370.sh'
budget: 80000 tokens
