+++
id = "002998-pursuit"
ordinal = 2998
kind = "pursuit"
timestamp = "2026-10-14T04:16:44+00:00"
summary = "pursuit open T0579: Recon: what language-neutral signal tells a stand-in FAIL that disagrees with an answer from one where the acceptance itself crashed"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/contract-first/standin-crash-recon.md, committed, records: what S01's sealed acceptance printed per entry under codeless and stand-in runs (run in a scratch copy, not ~/semver itself), how beagle reads FAIL reasons today (cited file:line), two or more candidate signals that tell 'the test disagrees with the stand-in's answer' from 'the test crashed', each measured against S01, R96 and R97 (which entries it refuses, which it falsely refuses), and a ## Recommendation with the rule and its refusal text.
decided by: sh -c 'echo "5a469d9fe76c5b652120832f34c847951db62d7101acfcba196bf242459ee2b0  .beagle/checks/T0579/T0579.sh" | sha256sum -c --quiet && bash .beagle/checks/T0579/T0579.sh'
budget: 60000 tokens
opened over T0565, T0577: read-only recon on a disjoint scope, run beside the check upkeep; gates T0572 before R98
