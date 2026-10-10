+++
id = "001549-pursuit"
ordinal = 1549
kind = "pursuit"
timestamp = "2026-10-10T14:52:55+00:00"
summary = "pursuit prove T0356: WITNESSED — refuses when B02.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f935f8d9e87f6e349693e4cb5113c19232b84c5711d1a30ec19ac4a11bc000cc  .beagle/checks/T0356/T0356.sh" | sha256sum -c --quiet && bash .beagle/checks/T0356/T0356.sh'
refutes: refuses when B02.md is absent (proven 2026-10-10T14:52:55+00:00)
refused after 0s of a 0s check
