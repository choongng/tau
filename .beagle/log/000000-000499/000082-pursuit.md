+++
id = "000082-pursuit"
ordinal = 82
kind = "pursuit"
timestamp = "2026-10-03T13:03:25+00:00"
summary = "pursuit open T0035: Audit fix: T0030 check pinned to the archived R02 repo, ended_with_abandoned by per-task successor"
metric_command = ""
drains = []
hooks = []
+++

criteria: The T0030 check reads the archived R02 repo (~/itc.r02), not the live ~/itc. ended_with_abandoned is true only when some abandoned task has neither a done task with sibling_of pointing at it nor a reason 'duplicate of Tnnnn' naming a done task.
decided by: sh -c 'echo "3b998d3911452ad8e38b0689fd8fd0fedbdd94239a2e4fbb1ba17ba5e8aaa58d  .beagle/checks/T0035/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0035/check.sh'
budget: 30000 tokens
