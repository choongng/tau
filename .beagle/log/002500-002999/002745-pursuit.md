+++
id = "002745-pursuit"
ordinal = 2745
kind = "pursuit"
timestamp = "2026-10-13T20:00:24+00:00"
summary = "pursuit amend T0520"
metric_command = ""
drains = []
hooks = []
+++

audit 10-13 part 1: the check ran in a frozen side worktree, so a regression on choong-dev (where the commit now lives) would not trip it; same assertions, run from the main checkout
was: sh -c 'echo "fb6c9aa55682b326033162d5f10cbad3127fb823a833fd3003ca47aa3d452145  .beagle/checks/T0520/T0520.sh" | sha256sum -c --quiet && bash .beagle/checks/T0520/T0520.sh'
  fb6c9aa55682b326033162d5f10cbad3127fb823a833fd3003ca47aa3d452145  .beagle/checks/T0520/T0520.sh
now: sh -c 'echo "ca308b98b475274d090d6750a42b7ce0db514d9af49e0c71bcceec0e7d687091  .beagle/checks/T0520/T0520.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0520/T0520.v2.sh'
