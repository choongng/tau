+++
id = "000995-pursuit"
ordinal = 995
kind = "pursuit"
timestamp = "2026-10-05T08:10:30+00:00"
summary = "pursuit open T0246: R26.md's upstream line agrees with upstream.md — same R26.md edit; check uses 'if grep -q ...; then exit 1; fi' instead of a '! grep' under set -e"
metric_command = ""
drains = []
hooks = []
+++

criteria: R26.md's upstream line agrees with upstream.md's ## R26 section and with beagle's help: beagle close has infeasible/abandoned outcomes; tau lacked a call to reach them (T0239); beagle's own ask is an attempt count in show.
decided by: sh -c 'echo "c51f2151584ebdb40f6ca917a6c93f91768d8f16088be56c725f181dfe6c53ab  .beagle/checks/T0246/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0246/check.sh'
budget: 4000 tokens
