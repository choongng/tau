+++
id = "001331-pursuit"
ordinal = 1331
kind = "pursuit"
timestamp = "2026-10-09T22:13:53+00:00"
summary = "pursuit amend T0316"
metric_command = ""
drains = []
hooks = []
+++

set -e does not stop on a command negated with !, so the first assertion could not fail
was: sh -c 'echo "e75161af561d822c2d0af168b5b48d4a8c97bf21fa3b0c4cadba8e07e81cecda  .beagle/checks/T0316/T0316.sh" | sha256sum -c --quiet && bash .beagle/checks/T0316/T0316.sh'
  e75161af561d822c2d0af168b5b48d4a8c97bf21fa3b0c4cadba8e07e81cecda  .beagle/checks/T0316/T0316.sh
now: sh -c 'echo "f241518d924cf4b1806af0695802f4a1d7f691d5469f1d4f498ab07f320acf78  .beagle/checks/T0316/T0316.sh" | sha256sum -c --quiet && bash .beagle/checks/T0316/T0316.sh'
