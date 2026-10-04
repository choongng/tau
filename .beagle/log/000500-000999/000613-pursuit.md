+++
id = "000613-pursuit"
ordinal = 613
kind = "pursuit"
timestamp = "2026-10-04T09:14:06+00:00"
summary = "pursuit open T0146: Worker read guard and report gaps from audit 7"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker guard refuses reading .beagle/ by awk, nl, cut, git cat-file -p, git diff -- .beagle, git grep, and python -c open() of a .beagle path (running a .beagle/checks script stays allowed); report text before raw tool-call markup is kept whatever its length when it is not empty; the timeout text blames the output limit only when the worker's last turns (at least the final one before the kill) hit it.
decided by: sh -c 'echo "a47cfb0f4d96aa879f1bfaeac59e7665030f795916d1daf4c92856094513610a  .beagle/checks/T0146/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0146/check.sh'
budget: 50000 tokens
