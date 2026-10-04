+++
id = "000425-pursuit"
ordinal = 425
kind = "pursuit"
timestamp = "2026-10-04T01:39:08+00:00"
summary = "pursuit open T0110: prove: tests-only task gets a mutate route through the module its tests import"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step: (a) a tests-only task (scope has no non-test source) whose check passes proves by --mutate on a project module the scoped tests import, when the WITNESS names it; with a test-file WITNESS the result names that module as the place for the NEEDLE and the task is not put in _UNPROVEN (worker re-sent once, like weak); (b) TESTS_ONLY_PROOF_NOTE only when the scope holds a data file, otherwise 'mutate the module the test imports'; (c) a new route whose check passes only because of uncommitted files in the task's own scope is opened, not refused as already passing. Named tests pass, extension test file passes, ruff clean.
decided by: sh -c 'echo "cc14422ed20cd2a6668cb2b43c66056ffb46880817034cfa35081a8064bb77d3  .beagle/checks/T0110/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0110/check.sh'
budget: 150000 tokens
