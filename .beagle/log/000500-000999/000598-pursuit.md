+++
id = "000598-pursuit"
ordinal = 598
kind = "pursuit"
timestamp = "2026-10-04T08:57:11+00:00"
summary = "pursuit open T0143: Worker guard: symlinks out of scope and reads of sibling project trees"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker scope guard refuses os.symlink (python -c / scripts run inline) whose link is out of scope or whose target is outside the project; an in-tree symlink is judged by its own path, not followed out; and reads (read tool, cat/grep/sed/head/tail/less/ls/find) of a path under the project's parent directory but outside the project are refused with a line saying other trees beside the project are not this task's.
decided by: sh -c 'echo "a791836bbc7255d6830bfe7a90f370f878275f13cf4d4a142ac047c1db2dd601  .beagle/checks/T0143/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0143/check.sh'
budget: 60000 tokens
