+++
id = "002924-pursuit"
ordinal = 2924
kind = "pursuit"
timestamp = "2026-10-14T02:08:02+00:00"
summary = "pursuit open T0560: tau ext: slice-writer isolation, re-read and dispute routing"
metric_command = ""
drains = []
hooks = []
+++

criteria: As incremental-contract.md build task 7 and 'Re-reads on evidence' say: a Slice: task's worker is refused reading the code under test (only sources, references and contract/); a REREAD due from contract status becomes an offered 'Slice: reread <source> <first>-<last>' task; an upheld dispute opens a superseding slice instead of an amend, and is refused when the verdict gives no corrected value (T0547's bare TEST WRONG); AMEND_TITLE and _amend_check are removed. The four named tests and the whole extension suite pass outside beagle's venv.
decided by: sh -c 'echo "a7cf0c09049971c0f1207c006b1d3d29c81c2660fb74b01889130dfdfffa7e42  .beagle/checks/T0560/T0560.sh" | sha256sum -c --quiet && bash .beagle/checks/T0560/T0560.sh'
budget: 300000 tokens
opened over T0565: last build task before the runs the owner paused; T0565 is check upkeep outside the build
