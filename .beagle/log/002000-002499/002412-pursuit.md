+++
id = "002412-pursuit"
ordinal = 2412
kind = "pursuit"
timestamp = "2026-10-12T14:48:59+00:00"
summary = "pursuit open T0472: A tests-only task whose test imports an unwritten module is not offered routes prove always refuses (R59)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A tests-only task whose test imports a module not yet on disk is offered the joint cases route (code scope plus the test, the cases test as done_when; locked only under full) at the step close and in the data-route refusal, instead of routes prove refuses (R59). Named test test_tests_only_task_importing_unwritten_module_is_offered_the_cases_first_route passes; suite and ruff pass.
decided by: sh -c 'echo "9275a91888a826f2d141b74870d26c1d15d21c173eea4c3d47b4c5007def3a44  .beagle/checks/T0472/T0472.sh" | sha256sum -c --quiet && bash .beagle/checks/T0472/T0472.sh'
budget: 150000 tokens
