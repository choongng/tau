+++
id = "001410-pursuit"
ordinal = 1410
kind = "pursuit"
timestamp = "2026-10-10T02:17:34+00:00"
summary = "pursuit open T0335: Audit 12: R36.md's test names all resolve, and the check resolves them"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every test named on a Tests: line of R36.md, R37.md and R38.md exists (a def or async def of that name in that file); R36.md's template-token class names the tests that were actually written for it.
decided by: sh -c 'echo "449b5938ad86b2213f9f8313ae599e73d532800c027ba6dfdbd039cdd6aae4aa  .beagle/checks/T0335/T0335.sh" | sha256sum -c --quiet && bash .beagle/checks/T0335/T0335.sh'
budget: 8000 tokens
