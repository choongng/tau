+++
id = "002401-pursuit"
ordinal = 2401
kind = "pursuit"
timestamp = "2026-10-12T14:30:28+00:00"
summary = "pursuit open T0470: A new-route successor that opened and ran is not reported as not opened (R58)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A new-route successor is reported as 'not opened' only when its open was refused (R58). Named test test_new_route_successor_killed_at_its_wall_is_not_reported_as_not_opened passes; suite and ruff pass.
decided by: sh -c 'echo "94dd89e2142597aa47cdc4e5b1d475c6e9d5a86b92b94f1b2c24feb8e9c134c8  .beagle/checks/T0470/T0470.sh" | sha256sum -c --quiet && bash .beagle/checks/T0470/T0470.sh'
budget: 150000 tokens
