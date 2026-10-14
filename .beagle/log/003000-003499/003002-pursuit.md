+++
id = "003002-pursuit"
ordinal = 3002
kind = "pursuit"
timestamp = "2026-10-14T04:19:38+00:00"
summary = "pursuit amend T0533"
metric_command = ""
drains = []
hooks = []
+++

T0565: '! grep' under set -e at line 9 could never refuse (T0564 lint)
was: sh -c 'echo "d54b9081f18886fc91c313d4c9b9bdb749a1cc214d4a95ae4d4f369cacb1690f  .beagle/checks/T0533/T0533.sh" | sha256sum -c --quiet && bash .beagle/checks/T0533/T0533.sh'
  d54b9081f18886fc91c313d4c9b9bdb749a1cc214d4a95ae4d4f369cacb1690f  .beagle/checks/T0533/T0533.sh
now: sh -c 'echo "0966c6b38026d385016ab7a62350de73f633dc6133ec9886f713a08050e6cf8f  .beagle/checks/T0533/T0533.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0533/T0533.v2.sh'
