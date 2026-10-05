+++
id = "001169-pursuit"
ordinal = 1169
kind = "pursuit"
timestamp = "2026-10-05T17:30:59+00:00"
summary = "pursuit open T0279: Escalation offers a notes-only call when only the close judge kept the task open"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the not-done escalation fires and every stays-open verdict came from the close's own judge (the check itself passed), the escalation offers pursuit_step task=<id> notes=<the judge's reason> with no done_when, and never demands a new done_when; when the only other check in scope would be rewritten back to the bound one by the data-route rewrite, it is not offered; a repeat of the same refused call names that notes-only call.
decided by: sh -c 'echo "1eabc7bc47a6d2c169d1ba73f57420bf1a6aa8fec267c3a2947ed1963b6e362c  .beagle/checks/T0279/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0279/check.sh'
budget: 60000 tokens
