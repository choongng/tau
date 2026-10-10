+++
id = "001426-pursuit"
ordinal = 1426
kind = "pursuit"
timestamp = "2026-10-10T02:24:10+00:00"
summary = "pursuit amend T0128"
metric_command = ""
drains = []
hooks = []
+++

T0319: under set -e a '! cmd' line never fails the check, so its assertion was vacuous; stated as 'if cmd; then exit 1; fi'
was: sh -c 'echo "c713a4d05b3ad5d5c8f8cfa79a11e161e9dfdd4a2afdacaa5b28429899c16994  .beagle/checks/T0128/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0128/check.sh'
  c713a4d05b3ad5d5c8f8cfa79a11e161e9dfdd4a2afdacaa5b28429899c16994  .beagle/checks/T0128/check.sh
now: sh -c 'echo "b9d6e10eb58348c2d54c59f43734c099bba3175900c93317e11318a4ca610bc1  .beagle/checks/T0128/T0128.sh" | sha256sum -c --quiet && bash .beagle/checks/T0128/T0128.sh'
