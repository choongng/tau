+++
id = "001067-pursuit"
ordinal = 1067
kind = "pursuit"
timestamp = "2026-10-05T11:38:10+00:00"
summary = "pursuit open T0260: Locks root-relative; cases-first plans never repeat the task title"
metric_command = ""
drains = []
hooks = []
+++

criteria: Locks given to pursuit_step are made root-relative and deduplicated (refused outside the root like scope); _pending_locks stores and reads relative paths; _amend_problem accepts a check that names a lock given absolute; cases-first on a known-answers task refuses with only the scope fix; every plan cases-first or the cases-on-disk route offers passes _live_title_clash (second part never takes the task's own title).
decided by: sh -c 'echo "aec6a4c92555d4c013cacc0826f44cbfa4d0e6e2196a51e22b3aef35402ebf6a  .beagle/checks/T0260/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0260/check.sh'
budget: 90000 tokens
