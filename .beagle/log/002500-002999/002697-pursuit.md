+++
id = "002697-pursuit"
ordinal = 2697
kind = "pursuit"
timestamp = "2026-10-13T15:02:55+00:00"
summary = "pursuit open T0528: Worker wall excludes cut-off turns; end a worker at its third cut-off, not its second"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's wall does not count the time of turns cut off at the output limit, and a worker is ended at its third cut-off, not its second
decided by: sh -c 'echo "1cc39b78739024be96b7afc69b0ef64a1f8d20be706e5bd2ffc3dd46df237a68  .beagle/checks/T0528/T0528.sh" | sha256sum -c --quiet && bash .beagle/checks/T0528/T0528.sh'
budget: 60000 tokens
opened over T0493, T0517: 2db46f63d586c45fc3208987a75babd73f0d4fde
