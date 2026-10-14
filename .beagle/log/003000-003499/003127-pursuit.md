+++
id = "003127-pursuit"
ordinal = 3127
kind = "pursuit"
timestamp = "2026-10-14T21:05:55+00:00"
summary = "pursuit open T0601: spec-tied step: pursuit_plan milestone 'source', cases worker (rules 2e, test-file scope), open --dry-run, open --cites/--cases, code worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: On branch beagle-0.48: a milestone the driver gives a 'source' (a references/ name; pursuit_plan entries, and founding milestones where the schema allows) is kept in its beagle task record and run as one pursuit_step: a cases worker (own role, writes test files only, may run open --dry-run) writes beagle-case: marked cases from the source until the dry run passes; then the real open with --cites from the markers and --cases; then the code worker. No source: unchanged, no cases worker. A failed cases worker or refusing dry run goes back to the driver with beagle's refusal, the task not opened. Tests named in the check, including a real_beagle spec_tied test where 0.48 accepts the open and the task closes done; the full suites pass.
decided by: sh -c 'echo "a1fad247eac13b5142c39437d295a468ad26b47e8d80f8caad6c79cdfae60666  .beagle/checks/T0601/T0601.sh" | sha256sum -c --quiet && bash .beagle/checks/T0601/T0601.sh'
budget: 500000 tokens
