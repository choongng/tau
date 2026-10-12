+++
id = "002546-pursuit"
ordinal = 2546
kind = "pursuit"
timestamp = "2026-10-12T18:46:58+00:00"
summary = "pursuit open T0497: beagle: a worked-example table row is quotable as it stands"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle pursuit contract check accepts a quote shorter than MIN_QUOTE when it is the whole of exactly one source line (a worked-example table row such as '0 | 00 3F'), citing that line; a short quote inside a longer line, or a short line the source repeats, is still refused as too short. R71's own reference and contract, with each example quoting its row alone, pass the draft check. beagle CI green on branch contract-first.
decided by: sh -c 'echo "9647d8059f7d59757be496ba52932c2fa441a1a3ea968d3bb826901ea462e5ab  .beagle/checks/T0497/T0497.sh" | sha256sum -c --quiet && bash .beagle/checks/T0497/T0497.sh'
budget: 60000 tokens
