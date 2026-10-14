+++
id = "003104-pursuit"
ordinal = 3104
kind = "pursuit"
timestamp = "2026-10-14T19:50:16+00:00"
summary = "pursuit prove T0598: WITNESSED — refuses when launch.sh's `BEAGLE_ROOT:-$HOME/beagle-wt/0.48}` is put back as `BEAGLE_ROOT:-$HOME/beagle}`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4462166c68099b74108dc731e7c96371ef02def2aebaac1dd90f7684926870ec  .beagle/checks/T0598/T0598.sh" | sha256sum -c --quiet && bash .beagle/checks/T0598/T0598.sh'
refutes: refuses when launch.sh's `BEAGLE_ROOT:-$HOME/beagle-wt/0.48}` is put back as `BEAGLE_ROOT:-$HOME/beagle}` (proven 2026-10-14T19:49:19+00:00)
refused after 0s of a 1s check
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0509, T0519, T0524, T0525, T0536, T0541, T0039
