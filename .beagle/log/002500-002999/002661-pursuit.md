+++
id = "002661-pursuit"
ordinal = 2661
kind = "pursuit"
timestamp = "2026-10-13T06:10:06+00:00"
summary = "pursuit open T0523: beagle contract-first ci/check.sh green"
metric_command = ""
drains = []
hooks = []
+++

criteria: bash ci/check.sh in /home/choong/beagle-wt/contract-first exits 0 and prints 'ci: all gates green': every gate and the whole beagle suite pass on the contract-first branch. It stands for the 'beagle CI green' clauses of T0498, T0503, T0512, T0513, T0514 and T0516, whose own checks run -k subsets.
decided by: sh -c 'echo "efc6f520edd04445c565c2dc45e5ca675b97288d90361ab066918767ea230641  .beagle/checks/T0523/T0523.sh" | sha256sum -c --quiet && bash .beagle/checks/T0523/T0523.sh'
budget: 20000 tokens
opened over T0493, T0517: T0521's audit work: the standing beagle CI check the amended tasks' 'beagle CI green' clauses now point to; done before the queue resumes
