+++
id = "002862-pursuit"
ordinal = 2862
kind = "pursuit"
timestamp = "2026-10-14T00:12:46+00:00"
summary = "pursuit open T0557: beagle: re-reads on evidence; second extraction retired"
metric_command = ""
drains = []
hooks = []
+++

criteria: As incremental-contract.md 'Re-reads on evidence' and build task 4 say: beagle keeps an acceptance history; contract status prints REREAD due for a section when one entry FAILs on 3 runs over distinct trees or an upheld dispute marks an entry wrong; check refuses two live entries with one operation and input but different expects, naming both cites; a re-read listing citing outside its section's range is refused; the second extraction as a stage (second, _second_problems, contract diff) is retired, its listing check kept for re-reads. The four named tests pass and ci/check.sh is green.
decided by: sh -c 'echo "bbd9dde8a31ca1a6195e036dbb7af2aa5793957c2e97e599ec62cda299185a27  .beagle/checks/T0557/T0557.sh" | sha256sum -c --quiet && bash .beagle/checks/T0557/T0557.sh'
budget: 250000 tokens
