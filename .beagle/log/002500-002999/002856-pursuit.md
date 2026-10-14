+++
id = "002856-pursuit"
ordinal = 2856
kind = "pursuit"
timestamp = "2026-10-13T23:54:29+00:00"
summary = "pursuit open T0556: beagle: contract coverage and the done gate"
metric_command = ""
drains = []
hooks = []
+++

criteria: As incremental-contract.md 'Coverage: what done means' and build task 3 say, with the owner's decisions: the normative-line rule; contract coverage prints uncovered lines as citable spans; DoneGate.met is refused while any normative line is neither cited by a live entry nor in an excluded item with a why; an excluded passage over 40 lines is refused; a retired entry's FAIL does not block done. The wrenfold-r3 fixture marks 29 of 56 lines. The six named tests pass and ci/check.sh is green.
decided by: sh -c 'echo "3b2781154f2a14a2bfbd19be4872db364374cda1ac0b0fecaf5f56f0c933c017  .beagle/checks/T0556/T0556.sh" | sha256sum -c --quiet && bash .beagle/checks/T0556/T0556.sh'
budget: 250000 tokens
