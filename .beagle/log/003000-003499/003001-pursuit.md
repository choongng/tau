+++
id = "003001-pursuit"
ordinal = 3001
kind = "pursuit"
timestamp = "2026-10-14T04:19:34+00:00"
summary = "pursuit amend T0245"
metric_command = ""
drains = []
hooks = []
+++

T0565: '! grep' under set -e at line 4 could never refuse (T0564 lint)
was: sh -c 'echo "3d9e10d2879acbd343d9911e7ee978ccd7926768112945d498b1d08ed445b610  .beagle/checks/T0245/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0245/check.sh'
  3d9e10d2879acbd343d9911e7ee978ccd7926768112945d498b1d08ed445b610  .beagle/checks/T0245/check.sh
now: sh -c 'echo "c51f2151584ebdb40f6ca917a6c93f91768d8f16088be56c725f181dfe6c53ab  .beagle/checks/T0245/T0245.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0245/T0245.v2.sh'
