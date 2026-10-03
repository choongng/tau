+++
id = "000093-pursuit"
ordinal = 93
kind = "pursuit"
timestamp = "2026-10-03T13:09:23+00:00"
summary = "pursuit open T0034: R03 fix: reference extracts reach the driver before its first pursuit_found"
metric_command = ""
drains = []
hooks = []
+++

criteria: Before its first pursuit_found, the driver of a request naming beagle/pursuit is shown a short extract (title plus opening/abstract, about 1500 chars at most) of each URL in the request, with an instruction that the criteria must describe this in the reference's own terms; a failed fetch is named instead. Founding reuses those fetched references/ files rather than fetching again.
decided by: sh -c 'echo "94f973c11df717164bb12f304b86eecd51602b7d9642e1d5781985f3eff0063e  .beagle/checks/T0034/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0034/check.sh'
budget: 120000 tokens
