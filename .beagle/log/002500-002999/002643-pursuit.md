+++
id = "002643-pursuit"
ordinal = 2643
kind = "pursuit"
timestamp = "2026-10-13T05:52:27+00:00"
summary = "pursuit open T0510: contract-first: implementation tasks are held to the sealed contract, not their own tests"
metric_command = ""
drains = []
hooks = []
+++

criteria: after the seal: the seal note tells the driver to check each milestone with beagle pursuit contract run --operation <op> and names the contract's operations; pursuit_step accepts that check; an inline check asserting answers (python3 -c with assert/==) is refused under a sealed contract, not before it and not for the contract's own steps
decided by: sh -c 'echo "07b5fa20f833927c51f971a7fe71def0072a80884b3eb92486a762d4739181b2  .beagle/checks/T0510/T0510.sh" | sha256sum -c --quiet && bash .beagle/checks/T0510/T0510.sh'
budget: 60000 tokens
opened over T0493, T0517: 2b387762
