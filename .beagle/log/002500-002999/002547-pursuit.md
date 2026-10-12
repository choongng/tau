+++
id = "002547-pursuit"
ordinal = 2547
kind = "pursuit"
timestamp = "2026-10-12T18:48:09+00:00"
summary = "pursuit prove T0497: WITNESSED — refuses when contract.py's `line = source.whole_line(quote)` is put back as `line = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9647d8059f7d59757be496ba52932c2fa441a1a3ea968d3bb826901ea462e5ab  .beagle/checks/T0497/T0497.sh" | sha256sum -c --quiet && bash .beagle/checks/T0497/T0497.sh'
refutes: refuses when contract.py's `line = source.whole_line(quote)` is put back as `line = None` (proven 2026-10-12T18:47:08+00:00; refused at - entry E003's quote '5 | 05 3F' is too short to point anywhere, and is not a line of wrenfold-r3 that occurs once: quo…)
refused after 1s of a 4s check at: - entry E003's quote '5 | 05 3F' is too short to point anywhere, and is not a line of wrenfold-r3 that occurs once: quo…
refused with: - entry E003's quote '5 | 05 3F' is too short to point anywhere, and is not a line of wrenfold-r3 that occurs once: quote the whole line or sentence it comes from.
