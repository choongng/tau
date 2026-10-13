+++
id = "002746-pursuit"
ordinal = 2746
kind = "pursuit"
timestamp = "2026-10-13T20:00:29+00:00"
summary = "pursuit amend T0522"
metric_command = ""
drains = []
hooks = []
+++

audit 10-13 part 1: the check ran in a frozen side worktree, so a regression on choong-dev (where the commit now lives) would not trip it; same assertions, run from the main checkout
was: sh -c 'echo "d289d867ab29aa4eef8277845faf465941964dfa227b27a39262209b37de4599  .beagle/checks/T0522/T0522.sh" | sha256sum -c --quiet && bash .beagle/checks/T0522/T0522.sh'
  d289d867ab29aa4eef8277845faf465941964dfa227b27a39262209b37de4599  .beagle/checks/T0522/T0522.sh
now: sh -c 'echo "8d78a3b5cf8edf2731b313611e8af28a2b93b58850c38f6dc4bef75230d844ea  .beagle/checks/T0522/T0522.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0522/T0522.v2.sh'
