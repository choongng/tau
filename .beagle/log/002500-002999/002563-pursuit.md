+++
id = "002563-pursuit"
ordinal = 2563
kind = "pursuit"
timestamp = "2026-10-12T21:44:02+00:00"
summary = "pursuit open T0502: tau ext: a worker may run the contract's read verbs"
metric_command = ""
drains = []
hooks = []
+++

criteria: A tau worker (BEAGLE_TAU_WORKER=1) can run beagle pursuit contract refs/check/status/diff/run; contract seal (and any other contract verb) is still refused, its refusal naming 'contract seal'; the worker-guard test covers refs, check and seal.
decided by: sh -c 'echo "e5c5454917920aa0080ac04df66a709061d463910e89d7b622412ce235e6a68c  .beagle/checks/T0502/T0502.sh" | sha256sum -c --quiet && bash .beagle/checks/T0502/T0502.sh'
budget: 40000 tokens
opened over T0493: R75 showed the guard voids any anchor eval; T0501's runs wait on it
