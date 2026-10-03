+++
id = "000255-pursuit"
ordinal = 255
kind = "pursuit"
timestamp = "2026-10-03T19:53:56+00:00"
summary = "pursuit open T0065: already-passes on a container part names the done sibling, no abandon hint"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step refuses a task because its check already passes, and the task is a part of a non-root container, the text carries no abandon= hint (T0058 would refuse it) and, when an earlier done sibling closed on the same check, names it and says this task must add something beyond it: bind a test of what is left, or call pursuit_step {} for other work. A root child keeps today's abandon hint. R09: T0010 (P5) after T0009 (P4) closed done on the same check; the driver repeated the refused call 9 times.
decided by: sh -c 'echo "690a04302e1bcaecc7e9a07f89238a0278d87942bd49bf3b8e1497898e52b52c  .beagle/checks/T0065/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0065/check.sh'
budget: 50000 tokens
