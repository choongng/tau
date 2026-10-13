+++
id = "002648-pursuit"
ordinal = 2648
kind = "pursuit"
timestamp = "2026-10-13T05:59:37+00:00"
summary = "pursuit open T0520: tau ext: worker and task-worker guards tested on contract status, diff and run (audit 2026-10-12)"
metric_command = ""
drains = []
hooks = []
+++

criteria: the worker and task-worker guard tests run contract status, diff and run --operation and see them allowed, seal still refused; NO_BEAGLE_NOTE names contract run --operation
decided by: sh -c 'echo "fb6c9aa55682b326033162d5f10cbad3127fb823a833fd3003ca47aa3d452145  .beagle/checks/T0520/T0520.sh" | sha256sum -c --quiet && bash .beagle/checks/T0520/T0520.sh'
budget: 30000 tokens
opened over T0493, T0517: 77f22166
