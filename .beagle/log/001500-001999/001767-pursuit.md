+++
id = "001767-pursuit"
ordinal = 1767
kind = "pursuit"
timestamp = "2026-10-11T02:17:36+00:00"
summary = "pursuit open T0409: The locked-test done_when offer is checked against already-passes"
metric_command = ""
drains = []
hooks = []
+++

criteria: Where pursuit_step refuses a done_when that runs none of the locked tests (_locked_test_problem), and the locked test it would name already passes before any work, the refusal does not offer binding that test (the pre-run then refuses it as already passing, R22/R43). It offers what that pre-run refusal would offer instead. When the locked test fails today, the offer is unchanged. The driver-edit/bash/agent refusal's offered pursuit_step call (d0978b70), fed back as given for the offered task, is not refused by pursuit_step's done_when guards; where it would be, the refusal names the call that passes. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "7082ebfea49d44786be383021bc866bc74327688fb25cc2089d790f7c1ab6968  .beagle/checks/T0409/T0409.sh" | sha256sum -c --quiet && bash .beagle/checks/T0409/T0409.sh'
budget: 60000 tokens
