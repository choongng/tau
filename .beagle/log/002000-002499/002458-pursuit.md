+++
id = "002458-pursuit"
ordinal = 2458
kind = "pursuit"
timestamp = "2026-10-12T16:09:17+00:00"
summary = "pursuit open T0494: Audit fix: test contract check's untested clauses (T0479, T0480)"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: tests/test_contract.py has a test whose quote and source differ only in curly vs straight quote marks (matched), one where an entry lacking an id, a known kind, or an operation is each refused by name, and one where two extractions citing the same experiment command under different source keys compare as covered while a different command does not; each fails when its code (_FOLD, the id/kind/operation rules, the command identity) is removed. The 3 named tests and the file pass.
decided by: sh -c 'echo "291560d8520fd5ed9c5409f3c2317df20c6994dc70d2465aace34962cf78067b  .beagle/checks/T0494/T0494.sh" | sha256sum -c --quiet && bash .beagle/checks/T0494/T0494.sh'
budget: 100000 tokens
opened over T0481: audit defect: becomes work before more is opened
