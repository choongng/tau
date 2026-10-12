+++
id = "002530-pursuit"
ordinal = 2530
kind = "pursuit"
timestamp = "2026-10-12T17:17:54+00:00"
summary = "pursuit open T0489: tau ext: pursuit_step seals and takes beagle's gates"
metric_command = ""
drains = []
hooks = []
+++

criteria: With [contract] declared in .beagle/pursuit.toml: a done_when of 'beagle pursuit contract check [--draft]' or 'beagle pursuit contract run' passes _check_problem (other beagle commands are still refused); the lock store, cases-first refusals, known-answers routes, worker known-answers guard and close-time cases gates (source judge included) step aside (_cases_off), and locks a driver passes are dropped with a note; a done close that leaves 'contract status' ready runs 'contract seal' and says so; with nothing ready, beagle's next --json contract verdict decides what the driver is told (not sealed, altered, acceptance failing with its tail, or met with the assumptions to put to the user); a task on contract/ gets a witness note naming a quote made wrong, not code. Without [contract] nothing changes: the whole extension suite passes.
decided by: sh -c 'echo "d23826c6ae37186cb51cc17905a0c805a411e96e6c6dd4628e714128b2cdfb03  .beagle/checks/T0489/T0489.sh" | sha256sum -c --quiet && bash .beagle/checks/T0489/T0489.sh'
budget: 120000 tokens
