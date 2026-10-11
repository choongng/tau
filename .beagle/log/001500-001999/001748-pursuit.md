+++
id = "001748-pursuit"
ordinal = 1748
kind = "pursuit"
timestamp = "2026-10-11T01:36:23+00:00"
summary = "pursuit open T0405: The bash close steer offers abandon only where _abandon_problem would take it"
metric_command = ""
drains = []
hooks = []
+++

criteria: make_driver_pursuit_guard's refusal of `beagle pursuit close T ...` from bash reads the tree: for a T that _abandon_problem refuses for any reason the driver could give (the root, a founding milestone), it offers no abandon= and says what that refusal says to do instead; for a T it would take as a duplicate, the offered call is one _abandon_problem accepts (test feeds the offered abandon back to _abandon_problem). With no task parsed, the text offers only abandon='duplicate of Tnnnn', never a bare abandon='<why>'. Fails open. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "0b8343793aecdea0785198f098d6c5f1e0b4ec19d00a0e57bdb7822994031234  .beagle/checks/T0405/T0405.sh" | sha256sum -c --quiet && bash .beagle/checks/T0405/T0405.sh'
budget: 60000 tokens
