+++
id = "001424-pursuit"
ordinal = 1424
kind = "pursuit"
timestamp = "2026-10-10T02:24:04+00:00"
summary = "pursuit open T0319: Checks whose '! cmd' lines cannot fail under set -e are made to fail"
metric_command = ""
drains = []
hooks = []
+++

criteria: No check of a live task has a '! cmd' line (set -e never fails on one); T0054's, T0128's and T0226's checks state each such assertion as 'if cmd; then exit 1; fi', still pass, and are proven again.
decided by: sh -c 'echo "f48b30bb76595ae0a8702ff72f94982c4082517c69c829a4c7bd91cd2c45e743  .beagle/checks/T0319/T0319.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.sh'
budget: 15000 tokens
