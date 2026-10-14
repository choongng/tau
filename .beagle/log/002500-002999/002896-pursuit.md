+++
id = "002896-pursuit"
ordinal = 2896
kind = "pursuit"
timestamp = "2026-10-14T01:34:55+00:00"
summary = "pursuit amend T0493"
metric_command = ""
drains = []
hooks = []
+++

under set -e, bash does not exit on a failing command negated with !, so the mid-script '! grep' step never refused; rewritten as if grep ...; then exit 1 (found when prove restored CASES_DATA_SUFFIXES and the check still passed)
was: sh -c 'echo "7cc28365adcc1b556397d8e1802f8990a54cb89390762cc26631eb2a86f4e171  .beagle/checks/T0493/T0493.sh" | sha256sum -c --quiet && bash .beagle/checks/T0493/T0493.sh'
  7cc28365adcc1b556397d8e1802f8990a54cb89390762cc26631eb2a86f4e171  .beagle/checks/T0493/T0493.sh
now: sh -c 'echo "ac6351f861b897d930bd8f4dc2b7080871486fbff5515fef96a94946c431b69e  .beagle/checks/T0493/T0493.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0493/T0493.v2.sh'
