+++
id = "002578-pursuit"
ordinal = 2578
kind = "pursuit"
timestamp = "2026-10-12T22:05:57+00:00"
summary = "pursuit open T0505: tau ext: a worker sent on a task may run the contract's read verbs"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker sent on a task (BEAGLE_TAU_WORKER_TASK set) can run beagle pursuit contract status/check/refs/diff/run, including R77's 'PATH=... beagle pursuit contract check --draft 2>&1 | tail -100'; every other beagle call, contract seal included, is still refused; the task brief's no-beagle note says contract reads are allowed.
decided by: sh -c 'echo "b5400aad53b63bd9c65394dce202add40c93dfce6c0cd197e2b48b4165b32029  .beagle/checks/T0505/T0505.sh" | sha256sum -c --quiet && bash .beagle/checks/T0505/T0505.sh'
budget: 30000 tokens
opened over T0493: R77 stopped on it; the anchor eval waits on it
