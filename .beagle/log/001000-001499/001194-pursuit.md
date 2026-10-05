+++
id = "001194-pursuit"
ordinal = 1194
kind = "pursuit"
timestamp = "2026-10-05T19:12:08+00:00"
summary = "pursuit open T0284: R34 fix: known-answer sources must hold the expected result; locked-data fixes provable"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answers case whose quoted source does not contain its expected result (as decimal, hex or string forms, with no domain keyword lists) is refused at close and by _unquoted_cases, naming the case; a task fixing a locked data file can be proved by putting back the file's committed version as the defect; the check a failed-prove close suggests is never one _already_passes then refuses. Regression tests for each.
decided by: sh -c 'echo "da99bc5d876d6106bca32f328394147ada805fcc103d03dd7d56d55c9a849460  .beagle/checks/T0284/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0284/check.sh'
budget: 150000 tokens
