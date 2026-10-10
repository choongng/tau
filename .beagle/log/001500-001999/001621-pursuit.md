+++
id = "001621-pursuit"
ordinal = 1621
kind = "pursuit"
timestamp = "2026-10-10T18:57:33+00:00"
summary = "pursuit open T0376: R42 fix: an open task's not-run refusal offers no route it then refuses"
metric_command = ""
drains = []
hooks = []
+++

criteria: On an open task whose bound check's own in-scope test imports a module the tree and environment do not provide, pursuit_step runs the worker with a brief that says to drop that import (the test checks its own files only), instead of refusing 'not run' before any worker whatever the notes say. A not-run refusal on an open task offers no abandon='done by …' route, since that route is refused for open tasks; pending tasks keep it. Structural (AST import lookup, task status), no domain words. Tests test_open_task_whose_check_imports_unwritten_module_runs_with_drop_import_brief, test_open_task_not_run_offers_no_abandon_done_by; whole file passes, ruff clean.
decided by: sh -c 'echo "1c93246820f76a0322c6db6fa0b2cca55c29e2fe3870b8474a5214ab9090d8cd  .beagle/checks/T0376/T0376.sh" | sha256sum -c --quiet && bash .beagle/checks/T0376/T0376.sh'
budget: 80000 tokens
