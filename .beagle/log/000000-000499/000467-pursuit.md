+++
id = "000467-pursuit"
ordinal = 467
kind = "pursuit"
timestamp = "2026-10-04T02:42:33+00:00"
summary = "pursuit open T0119: Bare-operator checks get a move the driver can make"
metric_command = ""
drains = []
hooks = []
+++

criteria: A done_when whose only shell problem is bare && is judged per segment: always-pass segments (git diff without --exit-code/--quiet) are dropped; one segment left is quoted in the refusal as the check to send; several left with no objection are bound as bash -c '<cmd>' and the result says so; every segment objected to gives the first segment's objection. The same per-segment check applies inside bash -c '...'. The operator refusal says to name a new test file in scope for the sub-agent to write, not to write it.
decided by: sh -c 'echo "6ca9e58f1711f9a6e23cf8b017597d0fba6d8ace4c9b286dd99272a6b6a82410  .beagle/checks/T0119/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0119/check.sh'
budget: 150000 tokens
