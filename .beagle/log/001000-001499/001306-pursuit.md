+++
id = "001306-pursuit"
ordinal = 1306
kind = "pursuit"
timestamp = "2026-10-09T21:33:50+00:00"
summary = "pursuit open T0311: R36 fix: the not-done escalation offers the notes rerun when only the close kept the task open"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a task's not-done steps all passed their check and only the close kept it open (_judge_kept_open), the text a not-done result appends (_not_done) and the refusal a further step meets (_escalated_calls) both render _judge_escalation: they offer the notes-only rerun (or split/stop once JUDGE_NOTES_UNTIL is reached) and never say the next step 'runs no sub-agent' or ask for a rewritten done_when. For a task kept open by its check, the existing escalation text is unchanged. The result text and the step refusal say the same thing for the same task state (a test compares them). Keyed on tau's own not-done bookkeeping.
decided by: sh -c 'echo "02a0d9ac999ebb0ad1b44c6386eb55ea602551057474734afeb5759b97b770b5  .beagle/checks/T0311/T0311.sh" | sha256sum -c --quiet && bash .beagle/checks/T0311/T0311.sh'
budget: 120000 tokens
