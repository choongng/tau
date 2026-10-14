+++
id = "002897-pursuit"
ordinal = 2897
kind = "pursuit"
timestamp = "2026-10-14T01:35:56+00:00"
summary = "pursuit amend T0557"
metric_command = ""
drains = []
hooks = []
+++

under set -e, bash does not exit on a failing command negated with !, so the mid-script '! grep' step never refused; rewritten as if grep ...; then exit 1 (found at T0493's prove)
was: sh -c 'echo "bbd9dde8a31ca1a6195e036dbb7af2aa5793957c2e97e599ec62cda299185a27  .beagle/checks/T0557/T0557.sh" | sha256sum -c --quiet && bash .beagle/checks/T0557/T0557.sh'
  bbd9dde8a31ca1a6195e036dbb7af2aa5793957c2e97e599ec62cda299185a27  .beagle/checks/T0557/T0557.sh
now: sh -c 'echo "9fe3b9c96fdc1f9789e4ecf7a0b8c7fdaecc88f13ee2206485d747fa53f0f9a8  .beagle/checks/T0557/T0557.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0557/T0557.v2.sh'
