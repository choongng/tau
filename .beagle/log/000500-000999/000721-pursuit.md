+++
id = "000721-pursuit"
ordinal = 721
kind = "pursuit"
timestamp = "2026-10-04T16:14:25+00:00"
summary = "pursuit prove T0169: WITNESSED — refuses when R20.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a2afd1069873aa13c6795d26f325d52e80cc3a71df8acf5b04faa14d550501bb  .beagle/checks/T0169/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0169/check.sh'
refutes: refuses when R20.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-04T16:13:29+00:00)
refused after 0s of a 0s check
