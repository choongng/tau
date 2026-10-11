+++
id = "001706-pursuit"
ordinal = 1706
kind = "pursuit"
timestamp = "2026-10-11T00:03:14+00:00"
summary = "pursuit amend T0396"
metric_command = ""
drains = []
hooks = []
+++

beagle's sources are under ~/beagle/plugins, not ~/beagle/src (which does not exist, so the not-live search would have read nothing); the check now asserts each source root exists. Amended before any work.
was: sh -c 'echo "c8497a54c1924614619e45b5b2c7c9a032fdaee31a901184107ea65beb326744  .beagle/checks/T0396/T0396.sh" | sha256sum -c --quiet && bash .beagle/checks/T0396/T0396.sh'
  c8497a54c1924614619e45b5b2c7c9a032fdaee31a901184107ea65beb326744  .beagle/checks/T0396/T0396.sh
now: sh -c 'echo "f76d8a88fdddb8708eca07b5adf2d563ae9af5b172f2dd4bad93e6f80164a633  .beagle/checks/T0396/T0396.sh" | sha256sum -c --quiet && bash .beagle/checks/T0396/T0396.sh'
