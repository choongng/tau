+++
id = "002562-pursuit"
ordinal = 2562
kind = "pursuit"
timestamp = "2026-10-12T21:11:15+00:00"
summary = "pursuit open T0501: eval: q35 on itc and cobs with line anchors"
metric_command = ""
drains = []
hooks = []
+++

criteria: R75 (q35 itc) and R76 (q35 cobs) ran on contract-first beagle at or after 809d194 (T0498), each graded by its task's grader with an adapter, scorecards made, and eval.md has a row per run with the grade the grader gives and what the anchors changed
decided by: sh -c 'echo "ccfcb3e85d00050f835316c1cc8c14371905789a4ccd5039225c9ffb371781f3  .beagle/checks/T0501/T0501.sh" | sha256sum -c --quiet && bash .beagle/checks/T0501/T0501.sh'
budget: 60000 tokens
opened over T0493: krang is idle and the runs take two hours; T0493 can proceed in a separate tau worktree while they run, and merges after
