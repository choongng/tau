+++
id = "003039-pursuit"
ordinal = 3039
kind = "pursuit"
timestamp = "2026-10-14T05:30:29+00:00"
summary = "pursuit prove T0517: WITNESSED — refuses when invalid-silence-recon.md's `Decision: build` is put back as `Decided: build`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a6a87351e05f200ec088cef88ca2590af2dae1b56d2b03aa229b10d1fa4d85d1  .beagle/checks/T0517/T0517.sh" | sha256sum -c --quiet && bash .beagle/checks/T0517/T0517.sh'
refutes: refuses when invalid-silence-recon.md's `Decision: build` is put back as `Decided: build` (proven 2026-10-14T05:30:28+00:00)
refused after 0s of a 0s check
