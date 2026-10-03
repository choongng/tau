+++
id = "000392-pursuit"
ordinal = 392
kind = "pursuit"
timestamp = "2026-10-03T21:30:38+00:00"
summary = "pursuit open T0017: summary across all ten runs"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/summary.md: (1) a '## Runs' table with one row per run R01-R10 giving model, tau sha, minutes, grader score (matching each RNN.md's grader line), and how it ended; (2) '## Recurring failure classes': each class a ### heading with 'Runs:' (which runs showed it), evidence pointers into the RNN.md files, and 'Status: fixed|partly fixed|open|model' naming the tau commits/tasks that address it; (3) '## What changed in tau' grouped by theme with commit ranges; (4) '## Still open', including that the R10 fixes (T0081-T0084) and audit-4 fixes are untested by a run; (5) '## Next', concrete recommended next runs or changes, citing fang-ideas.md where it applies.
decided by: sh -c 'echo "4e1ed0bac8310e3da19938030e7be54a91a86d39158b223f595e80a53ac82c01  .beagle/checks/T0017/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0017/check.sh'
budget: 60000 tokens
