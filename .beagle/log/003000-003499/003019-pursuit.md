+++
id = "003019-pursuit"
ordinal = 3019
kind = "pursuit"
timestamp = "2026-10-14T04:31:50+00:00"
summary = "pursuit amend T0226"
metric_command = ""
drains = []
hooks = []
+++

T0565 follow-up: the two cases-first holder tests were deleted with cases-first in T0493 (d3bc903f), so this standing check has been red since; its live clauses (unproven refusal's first line, R24 wording) keep their steps; the whole-suite run is dropped (other standing checks run it) to fit the 120 s amend run
was: sh -c 'echo "afcb86835f24d310a545ab2c7dd419812c6e8f3c5a49b61d10a3de56fd8c3b91  .beagle/checks/T0226/T0226.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/T0226.sh'
  afcb86835f24d310a545ab2c7dd419812c6e8f3c5a49b61d10a3de56fd8c3b91  .beagle/checks/T0226/T0226.sh
now: sh -c 'echo "d327d2ce69d0fa1d23092d158c1e9f761440068adef4c770eb89446334d99ed6  .beagle/checks/T0226/T0226.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/T0226.v2.sh'
