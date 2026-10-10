+++
id = "001427-pursuit"
ordinal = 1427
kind = "pursuit"
timestamp = "2026-10-10T02:25:52+00:00"
summary = "pursuit amend T0226"
metric_command = ""
drains = []
hooks = []
+++

T0319: under set -e a '! cmd' line never fails the check, so its assertion was vacuous; stated as 'if cmd; then exit 1; fi'
was: sh -c 'echo "4d0d5fc4090593ac1ae2129d19f363a233dd8571459d9ec9f3f2da2f084f1f16  .beagle/checks/T0226/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/check.sh'
  4d0d5fc4090593ac1ae2129d19f363a233dd8571459d9ec9f3f2da2f084f1f16  .beagle/checks/T0226/check.sh
now: sh -c 'echo "afcb86835f24d310a545ab2c7dd419812c6e8f3c5a49b61d10a3de56fd8c3b91  .beagle/checks/T0226/T0226.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/T0226.sh'
