+++
id = "003021-pursuit"
ordinal = 3021
kind = "pursuit"
timestamp = "2026-10-14T04:32:02+00:00"
summary = "pursuit amend T0319"
metric_command = ""
drains = []
hooks = []
+++

T0565 follow-up: the criterion is about live tasks, and the check also read retired T0498's v2 (lines 66-67), red since T0554 retired it; it now skips a task with retired_by set, and runs T0226's v2 (amended for T0493's deletion)
was: sh -c 'echo "559a1b62b9bd06ff4d92ff1cfe4c9339a03575679c8f9db00f338ff5b7ef1af4  .beagle/checks/T0319/T0319.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.sh'
  559a1b62b9bd06ff4d92ff1cfe4c9339a03575679c8f9db00f338ff5b7ef1af4  .beagle/checks/T0319/T0319.sh
now: sh -c 'echo "d5bc793e11244ae9bd1bd27ca26ed421f43c671e83f8add40779fb48f190a27d  .beagle/checks/T0319/T0319.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.v2.sh'
