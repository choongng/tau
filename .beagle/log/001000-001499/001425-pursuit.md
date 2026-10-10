+++
id = "001425-pursuit"
ordinal = 1425
kind = "pursuit"
timestamp = "2026-10-10T02:24:09+00:00"
summary = "pursuit amend T0054"
metric_command = ""
drains = []
hooks = []
+++

T0319: under set -e a '! cmd' line never fails the check, so its assertion was vacuous; stated as 'if cmd; then exit 1; fi'
was: sh -c 'echo "04b3be87fcf27ed0da30e4829c07eb9b6fe739ec7862fb34f950bbc6b8d5024c  .beagle/checks/T0054/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0054/check.sh'
  04b3be87fcf27ed0da30e4829c07eb9b6fe739ec7862fb34f950bbc6b8d5024c  .beagle/checks/T0054/check.sh
now: sh -c 'echo "56c27810037d2d5e6fb95051e1a532a1ae1ce18562d1277ca8ccbe004623244a  .beagle/checks/T0054/T0054.sh" | sha256sum -c --quiet && bash .beagle/checks/T0054/T0054.sh'
