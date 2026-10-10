+++
id = "001638-pursuit"
ordinal = 1638
kind = "pursuit"
timestamp = "2026-10-10T20:45:05+00:00"
summary = "pursuit open T0383: R43 fix: a check that selects no tests is not accepted as failing now"
metric_command = ""
drains = []
hooks = []
+++

criteria: An open whose bound pytest check exits 5 before any work (it collected or selected no tests, e.g. a -k that matched nothing) is refused as a check that cannot fail for this task's reason, naming the selection, not accepted as fails-now; _pytest_collected_none names a -k (or other selection) that matched nothing instead of saying the file defines no test_ function when it does; a refusal that suggests a call (_locked_scope_problem and kin) does not echo back a selection that matches nothing. A check that collects tests and fails opens as before. Structural, no domain words. Tests test_open_refuses_a_check_whose_selection_deselects_every_test, test_collected_none_note_names_a_k_that_matched_nothing; whole file passes, ruff clean.
decided by: sh -c 'echo "4829f1ca1597cc80ebc85794ce8b3e269e85b85dec9ca3efed361d923ce4b025  .beagle/checks/T0383/T0383.sh" | sha256sum -c --quiet && bash .beagle/checks/T0383/T0383.sh'
budget: 80000 tokens
