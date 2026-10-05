+++
id = "000798-pursuit"
ordinal = 798
kind = "pursuit"
timestamp = "2026-10-05T00:38:28+00:00"
summary = "pursuit open T0205: Beagle subprocesses run under the memory cap, die as a group, and a memory-killed pre-run refuses the open"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every beagle subprocess tau runs (_pursuit/_run) runs under the worker memory cap in its own process group, and a timeout kills the whole group; a check pre-run killed by the memory cap (-9) refuses the open with the killed note instead of rehearsing; a worker killed by its cap has the killed note appended even when its report is non-empty.
decided by: sh -c 'echo "a3a3948093108957cad8dbe1341dfa46f009918ee1043b3d7513c90af2d0aea0  .beagle/checks/T0205/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0205/check.sh'
budget: 120000 tokens
