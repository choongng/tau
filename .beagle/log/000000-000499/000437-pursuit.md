+++
id = "000437-pursuit"
ordinal = 437
kind = "pursuit"
timestamp = "2026-10-04T01:52:56+00:00"
summary = "pursuit open T0112: split: commit the open task's passing uncommitted work before splitting"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan splitting an open task whose scope holds uncommitted files, when that task's check passed at its last verdict, commits those files as '<task>: work in progress before split' before creating the parts and says so in the result; git status --porcelain is then empty for that scope. When the last verdict failed (or there is none), nothing is committed and the existing 'Give each to the part' note stays. Named tests pass, extension test file passes, ruff clean.
decided by: sh -c 'echo "3638c570b54cf98a900ba28940d82cc10736a04b9dfd35747f2aec17b8edcfe6  .beagle/checks/T0112/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0112/check.sh'
budget: 100000 tokens
