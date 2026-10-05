+++
id = "001050-pursuit"
ordinal = 1050
kind = "pursuit"
timestamp = "2026-10-05T11:08:17+00:00"
summary = "pursuit open T0255: done-by closes only what the done task's check proves; pytest-form import-only checks refused"
metric_command = ""
drains = []
hooks = []
+++

criteria: done-by refuses to close a task that is to fix the done task's work (tau's own fix-route titles) or whose check already passed when the done task closed; its unwitnessed repair does not offer an unrelated data file the done task committed; a check running a pytest node whose body uses nothing from the module the task writes is refused as import-only; a witness whose only failure is an ImportError of the task's own module is not proof.
decided by: sh -c 'echo "8cec1472c97378e52dc04b0a540bece52f2cdeab8984bef559c535afc87eddd0  .beagle/checks/T0255/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0255/check.sh'
budget: 60000 tokens
