+++
id = "000882-pursuit"
ordinal = 882
kind = "pursuit"
timestamp = "2026-10-05T04:07:21+00:00"
summary = "pursuit open T0222: The misplaced-implementation rule spares a data test that imports no project module"
metric_command = ""
drains = []
hooks = []
+++

criteria: The misplaced-implementation rule does not flag a long helper def in a test file that imports no project module (non-Test classes and module-importing tests are still flagged); a misplaced hold on a task whose check passed on disk with no worker run does not count toward escalation.
decided by: sh -c 'echo "5cb46269df3c975443a5766a9fdab77daf46bac3252cd21bb93950fe9ed7205c  .beagle/checks/T0222/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0222/check.sh'
budget: 50000 tokens
