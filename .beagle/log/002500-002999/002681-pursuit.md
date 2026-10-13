+++
id = "002681-pursuit"
ordinal = 2681
kind = "pursuit"
timestamp = "2026-10-13T07:00:12+00:00"
summary = "pursuit open T0524: beagle contract: an acceptance that runs beagle pursuit contract again is refused, not run"
metric_command = ""
drains = []
hooks = []
+++

criteria: an acceptance run by beagle that runs beagle's contract again is refused (exit non-zero, says it would start itself again) instead of recursing; contract check --draft names an acceptance file that runs beagle's contract; R88's accept.sh under a 1G/64-task cap ends refused
decided by: sh -c 'echo "8d7a464a230155b87ba938436b93918fbdfe37a6ce1dc71a9a60ad47244a3ab6  .beagle/checks/T0524/T0524.sh" | sha256sum -c --quiet && bash .beagle/checks/T0524/T0524.sh'
budget: 60000 tokens
opened over T0493, T0517: f3ef0994dc6edc8e3f14ffa5be068b4cfc1c5903
