+++
id = "000200-pursuit"
ordinal = 200
kind = "pursuit"
timestamp = "2026-10-03T18:24:19+00:00"
summary = "pursuit open T0059: step scope must not mix known-answer data with source"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses, before any worker runs, a task whose scope holds both a known-answer data file (a non-.py file that is a test path, e.g. tests/cases.json or itc/tests/cases.json) that is not already locked, and a non-test source file (R08: T0004's scope [itc/tests/cases.json, itc/tests/test_cases.py, itc/interval_tree_clocks.py] let the worker write wrong expected values beside the code, and every later task was judged against them). The refusal says to split: data and its cases test first, closed with locks, then the code in a later task. A scope with only the data and test files is accepted. A data file already locked by an earlier task does not trigger the refusal.
decided by: sh -c 'echo "40c745dc2079317c28b5a8b90c78f526f00c543f0235d21039ce81bb0e724d11  .beagle/checks/T0059/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0059/check.sh'
budget: 60000 tokens
