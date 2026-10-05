+++
id = "000887-pursuit"
ordinal = 887
kind = "pursuit"
timestamp = "2026-10-05T04:13:15+00:00"
summary = "pursuit open T0223: A step that keeps the done_when says what it did with the call's new scope and locks"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step works an open task whose record scope differs from the call's, the result says which scope the worker ran on and how to change it, and pending locks filed from the call keep only test and data paths, never a module the task's scope does not hold.
decided by: sh -c 'echo "eb07158d64a2cf1e42ca94350517657b03a606315b4cd72f6fec0026e7388f2e  .beagle/checks/T0223/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0223/check.sh'
budget: 50000 tokens
