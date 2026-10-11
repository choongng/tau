+++
id = "001847-pursuit"
ordinal = 1847
kind = "pursuit"
timestamp = "2026-10-11T23:14:44+00:00"
summary = "pursuit open T0438: Splitting a task keeps its parts provable and their locks with the part that writes them"
metric_command = ""
drains = []
hooks = []
+++

criteria: After a split that commits the parent's passing work (_commit_before_split, R12), a part whose bound check passes on that work can still be opened and proven: the 'already passes' refusal and _prove's 'new since it opened' baseline use the parent's opened commit, so files the split commit added or changed count as the part's work (q35 10-11: 19 workers and 4 infeasible closes after the split). _move_pending_locks hands each pending lock to the part whose scope, title or intent names that file, and only a lock no part names goes to the first part (q38fn 10-11: all three locks went to T0007). Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "ad9d719fdcdc613fb1f3b08a2739a6081f6650831f985580227600bd0f97ba13  .beagle/checks/T0438/T0438.sh" | sha256sum -c --quiet && bash .beagle/checks/T0438/T0438.sh'
budget: 300000 tokens
