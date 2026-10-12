+++
id = "002568-pursuit"
ordinal = 2568
kind = "pursuit"
timestamp = "2026-10-12T21:51:29+00:00"
summary = "pursuit open T0503: beagle contract: a bare line-number cite is refused with the anchor to cite"
metric_command = ""
drains = []
hooks = []
+++

criteria: A contract cite given as a bare line number or range (N, LN, N-M) is refused, and the refusal names the anchored cite for those lines (N#hhh-M#hhh) and the text they read; bounds and width refusals still apply; beagle CI green.
decided by: sh -c 'echo "f0b70b8052dad06d5ff02d8bcafae17a32f513bd1f9ac05b82f08bc4f173c49e  .beagle/checks/T0503/T0503.sh" | sha256sum -c --quiet && bash .beagle/checks/T0503/T0503.sh'
budget: 30000 tokens
opened over T0493: the anchor re-run waits on it
