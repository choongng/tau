+++
id = "000994-pursuit"
ordinal = 994
kind = "pursuit"
timestamp = "2026-10-05T08:10:20+00:00"
summary = "pursuit spawn T0246: another route to T0245"
metric_command = ""
drains = []
hooks = []
+++

superseded: [T0245] R26.md's upstream line agrees with upstream.md
because: bound check could not refuse
delta: same R26.md edit; check uses 'if grep -q ...; then exit 1; fi' instead of a '! grep' under set -e
