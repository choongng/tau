+++
id = "003003-pursuit"
ordinal = 3003
kind = "pursuit"
timestamp = "2026-10-14T04:20:09+00:00"
summary = "pursuit amend T0490"
metric_command = ""
drains = []
hooks = []
+++

T0565: '! grep' under set -e at line 10 could never refuse (T0564 lint)
was: sh -c 'echo "39dfdcc9799799b12452399986687b90342d51b854b4ccedf6273908e6f8c2b2  .beagle/checks/T0490/T0490.sh" | sha256sum -c --quiet && bash .beagle/checks/T0490/T0490.sh'
  39dfdcc9799799b12452399986687b90342d51b854b4ccedf6273908e6f8c2b2  .beagle/checks/T0490/T0490.sh
now: sh -c 'echo "59d759e6e96533b54fbb7ec0aa9b9c501471b3014c46fac62af504be1053fc91  .beagle/checks/T0490/T0490.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0490/T0490.v2.sh'
