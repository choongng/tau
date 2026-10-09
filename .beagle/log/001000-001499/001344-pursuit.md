+++
id = "001344-pursuit"
ordinal = 1344
kind = "pursuit"
timestamp = "2026-10-09T22:56:40+00:00"
summary = "pursuit prove T0320: WITNESSED — refuses when R37.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5f98525ad31647105b6d7f0f125e52911f8c77a9346d4fd84b67ba876ce31646  .beagle/checks/T0320/T0320.sh" | sha256sum -c --quiet && bash .beagle/checks/T0320/T0320.sh'
refutes: refuses when R37.md is absent (proven 2026-10-09T22:55:44+00:00)
refused after 0s of a 0s check
