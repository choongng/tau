+++
id = "002638-pursuit"
ordinal = 2638
kind = "pursuit"
timestamp = "2026-10-13T05:50:54+00:00"
summary = "pursuit open T0509: beagle contract: the acceptance test reports every entry by id, or the contract does not seal"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract check and seal run the acceptance and refuse one that does not report every runnable entry as ok/FAIL <id> (R86's accept.sh refused); contract run --operation passes only when that operation's entries are reported ok
decided by: sh -c 'echo "ce79a011e23aa01a419aacd3236056907510cf43e0e608b27cbee4b98fdba6b5  .beagle/checks/T0509/T0509.sh" | sha256sum -c --quiet && bash .beagle/checks/T0509/T0509.sh'
budget: 60000 tokens
opened over T0493, T0517: d5c7a750
