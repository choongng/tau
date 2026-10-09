+++
id = "001264-pursuit"
ordinal = 1264
kind = "pursuit"
timestamp = "2026-10-09T19:37:43+00:00"
summary = "pursuit open T0294: Audit 10: an open task's rejected done_when runs the notes against the bound check on every rejection"
metric_command = ""
drains = []
hooks = []
+++

criteria: In pursuit_step on an open task, when the call carries notes and the task's bound check is runnable (_check_problem is None), every rejection of a rewritten done_when in the 'check not changed' branch (prose or unchainable, _amend_problem, the locked-scope/sibling-owned/pytest-node/unwritten-check problems, already passes before any work, the check could not run) keeps the bound check and runs the notes against it, as the _kept_data_check rebind does, with the rejection's reason prepended to the step's result as a note saying the bound check was kept and why the new one was not taken. Without notes, or when the bound check itself has a problem, the call is refused as before. Keyed on structure, no prompt words. Tests for already-passes, amend-problem, unwritten-check rejections each running the notes (a worker dispatched, bound check unchanged in the record), and for the refusal when the bound check is not runnable.
decided by: sh -c 'echo "991be7f859c4cad59e96f6aa734a8acedeb75b350eb0bf5188c1796c983788ba  .beagle/checks/T0294/T0294.sh" | sha256sum -c --quiet && bash .beagle/checks/T0294/T0294.sh'
budget: 120000 tokens
