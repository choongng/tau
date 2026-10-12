+++
id = "002418-pursuit"
ordinal = 2418
kind = "pursuit"
timestamp = "2026-10-12T14:52:44+00:00"
summary = "pursuit open T0473: M12's locked-data route does not list a test already in scope twice (R59)"
metric_command = ""
drains = []
hooks = []
+++

criteria: M12's locked-data route lists a test already in scope once (R59). Named test test_cases_first_locked_data_route_does_not_repeat_a_scoped_test passes; suite and ruff pass.
decided by: sh -c 'echo "39f40ebd7fc9782994ed421e4fac5cb126ce5ae1b224f0dcb6866752b1089f08  .beagle/checks/T0473/T0473.sh" | sha256sum -c --quiet && bash .beagle/checks/T0473/T0473.sh'
budget: 150000 tokens
