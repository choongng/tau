+++
id = "001311-pursuit"
ordinal = 1311
kind = "pursuit"
timestamp = "2026-10-09T21:40:07+00:00"
summary = "pursuit open T0312: R36 fix: a whole-tree scope does not get past the cases-first rule"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answers (cases-first) task whose scope holds a whole-tree entry ('', '.', './') is treated as naming the code, the way a bare src/ is: _cases_first_problem refuses it with the existing 'drop it from scope (the code is a later task)' guidance and the data-and-tests scope. Independently, while a known-answers task's worker runs, make_worker_scope_guard refuses its write of a new non-test .py file outside the tests directory (a conftest or helper under tests/ is allowed), saying the code is a later task and its cases are written from the references. Tasks that are not known-answers tasks are unaffected. Keyed on scope paths and file kinds; no prompt words.
decided by: sh -c 'echo "52abacf178e8e15b208c41d7c157ff09aede915d0f66e2fcb02c126f2ce099a8  .beagle/checks/T0312/T0312.sh" | sha256sum -c --quiet && bash .beagle/checks/T0312/T0312.sh'
budget: 120000 tokens
