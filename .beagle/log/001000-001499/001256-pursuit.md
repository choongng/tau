+++
id = "001256-pursuit"
ordinal = 1256
kind = "pursuit"
timestamp = "2026-10-09T19:19:45+00:00"
summary = "pursuit open T0290: R35 fix: workers may not write tau's store under .git/beagle"
metric_command = ""
drains = []
hooks = []
+++

criteria: A dispatched worker's write, edit or shell redirect into .git/beagle/ is refused by the worker scope guard, except a path tau itself names to the worker (the task's log, if the brief names one); the refusal says beagle's store and the close are the driver's and the worker's result goes in its report. Whether anything under .git/beagle is legitimately written by a worker today is established from the code first; if nothing is, no exception is kept. Keyed on paths, no prompt words. Regression tests: test_worker_scope_guard_refuses_writes_into_beagle_store (the R35 W15-W17 paths: logs/T0006.result.md, T0006.md, finding/, memory/, obligations/) and test_worker_scope_guard_allows_task_log_named_in_brief (or, if no such path exists, that test asserts every .git/beagle write is refused).
decided by: sh -c 'echo "58c76423721d7ec56be868540f3f858ebbb37c1a7b753a25b9d9535d5688af61  .beagle/checks/T0290/T0290.sh" | sha256sum -c --quiet && bash .beagle/checks/T0290/T0290.sh'
budget: 100000 tokens
