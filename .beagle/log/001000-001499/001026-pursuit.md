+++
id = "001026-pursuit"
ordinal = 1026
kind = "pursuit"
timestamp = "2026-10-05T09:51:57+00:00"
summary = "pursuit open T0250: Data test is told it imports no code, in brief and scope guard"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a task's scope holds only data and tests: the first brief says the data test reads only the data file and imports none of the code, and omits the code-directed witness note; the worker scope guard's refusal of an out-of-scope module that a data test in scope imports says to remove that import (the self-import note), not that the check needs the module; tau's offered calls do not carry notes asking to add or restore that import.
decided by: sh -c 'echo "bdfce9d8c7fd7c1ba9fc36ea2eb488eac36dc8db34d4ac5735a169577887a953  .beagle/checks/T0250/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0250/check.sh'
budget: 50000 tokens
