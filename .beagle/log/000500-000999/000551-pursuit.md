+++
id = "000551-pursuit"
ordinal = 551
kind = "pursuit"
timestamp = "2026-10-04T06:39:03+00:00"
summary = "pursuit open T0133: Escalation refusal names what the call lacks"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step refuses another sub-agent on a task that steps have left not done, the refusal reads the call's arguments and says what it lacks: a call with no new_route=true is told that flag is missing; a call whose criteria differ from the bound ones is told to leave criteria out; when the bound check imports a module no scope writes, it names the data-only check a sub-agent can pass. The same call sent twice gets the same specific text.
decided by: sh -c 'echo "97a005730249b545fb11d2a6d092d5a8d9456d72416a04d6b48856db3b466a78  .beagle/checks/T0133/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0133/check.sh'
budget: 80000 tokens
