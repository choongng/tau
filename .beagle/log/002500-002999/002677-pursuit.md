+++
id = "002677-pursuit"
ordinal = 2677
kind = "pursuit"
timestamp = "2026-10-13T06:17:27+00:00"
summary = "pursuit prove T0521: WITNESSED — refuses when T0518.v2.sh is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "efc37ce416ee7039e459349d241bb89c86848ced502ea5456d4bb7d14f1628b9  .beagle/checks/T0521/T0521.sh" | sha256sum -c --quiet && bash .beagle/checks/T0521/T0521.sh'
refutes: refuses when T0518.v2.sh is absent (proven 2026-10-13T06:16:27+00:00; predates the task: T0521's amends were made before its open (the audit's gaps were the task); T0518.v2.sh is one of them, written by T0521's dispatch and bound to T0518 by the amend; refused at Traceback (most recent call last):)
refused after 5s of a 11s check at: Traceback (most recent call last):
refused with: FileNotFoundError: [Errno 2] No such file or directory: '.beagle/checks/T0518/T0518.v2.sh'
