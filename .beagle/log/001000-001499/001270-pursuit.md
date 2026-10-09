+++
id = "001270-pursuit"
ordinal = 1270
kind = "pursuit"
timestamp = "2026-10-09T20:46:51+00:00"
summary = "pursuit amend T0030"
metric_command = ""
drains = []
hooks = []
+++

the check read R02's pursuit from /home/choong/itc, which launch.sh now archives to ~/itc.r02 before each new itc run; R36 is live in ~/itc
was: sh -c 'echo "f7f52e5047785b6d7d8426418544b28363d96416166677601580db757b86fe22  .beagle/checks/T0030/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0030/check.sh'
  f7f52e5047785b6d7d8426418544b28363d96416166677601580db757b86fe22  .beagle/checks/T0030/check.sh
now: sh -c 'echo "6026983ea4173523444aa1ab813040abef26cf443c317dd6f0383edacb5473c7  .beagle/checks/T0030/T0030.sh" | sha256sum -c --quiet && bash .beagle/checks/T0030/T0030.sh'
