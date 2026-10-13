+++
id = "002747-pursuit"
ordinal = 2747
kind = "pursuit"
timestamp = "2026-10-13T20:00:35+00:00"
summary = "pursuit amend T0527"
metric_command = ""
drains = []
hooks = []
+++

audit 10-13 part 1: the check ran in a frozen side worktree, so a regression on choong-dev (where the commit now lives) would not trip it; same assertions, run from the main checkout
was: sh -c 'echo "64cfc54562745acdbf515c35c91642ef91b9c7b703650fe52c8d41e887136699  .beagle/checks/T0527/T0527.sh" | sha256sum -c --quiet && bash .beagle/checks/T0527/T0527.sh'
  64cfc54562745acdbf515c35c91642ef91b9c7b703650fe52c8d41e887136699  .beagle/checks/T0527/T0527.sh
now: sh -c 'echo "f78f5f24c5836e651267d5976ab7e49a64a8eee02392c6e0f5cab8608048f0a8  .beagle/checks/T0527/T0527.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0527/T0527.v2.sh'
