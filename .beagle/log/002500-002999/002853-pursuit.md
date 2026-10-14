+++
id = "002853-pursuit"
ordinal = 2853
kind = "pursuit"
timestamp = "2026-10-13T23:48:23+00:00"
summary = "pursuit amend T0540"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-13: the last line piped T0523's CI run through tail without pipefail, so a red CI passed; now it greps the green line
was: sh -c 'echo "24918a0a042bc867b8738f73640f937eae43cc993acd23bd5a0cc099feda4b1d  .beagle/checks/T0540/T0540.sh" | sha256sum -c --quiet && bash .beagle/checks/T0540/T0540.sh'
  24918a0a042bc867b8738f73640f937eae43cc993acd23bd5a0cc099feda4b1d  .beagle/checks/T0540/T0540.sh
now: sh -c 'echo "81105354969dad39b565c53d4fe29becad43cca5550a9781caff62d52a5f0185  .beagle/checks/T0540/T0540.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0540/T0540.v2.sh'
