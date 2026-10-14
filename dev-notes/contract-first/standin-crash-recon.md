# Telling a test that disagrees from a test that crashed (T0579)

Read 2026-10-13 against beagle contract-first at commit 949dcc6, clean
(`plugins/beagle-pursuit/tooling/beagle/src/beagle/contract.py`, shortened
below to `contract.py`). Acceptances read: S01's sealed
`~/semver/contract/slices/01-examples/accept.sh`, R96's
`~/wrenfold/contract/accept.sh`, R97's `~/semver.r97/contract/accept.sh`.
Every run below was made in a copy under `~/.cache/standin-recon/` (runs/,
impl/, tools/measure.py); nothing in ~/semver, ~/semver.r97 or ~/wrenfold
was touched, and none of the scratch is committed. "Measured" means run
there; "inferred" means read or reasoned, not run.

## What S01 sealed

The slice has 17 entries: ex-001..013 parse examples, ex-014 an invalid
parse, ex-015..017 compare examples. The acceptance imports `semver` once
per operation and, if the import fails, prints one FAIL per entry and skips
the rest (accept.sh:36-48). Then, for compare examples:

- it reads `inp["expect"]["ordered"]` and `inp["expect"]["result"]`
  (accept.sh:85, :95), but `expect` sits beside `input` in the entry, not
  inside it (accept.sh:55 reads it correctly into `expect`, then never uses
  it for compare). So every compare entry raises `KeyError: 'expect'`,
  caught at accept.sh:131-132.
- with :85 fixed, it compares `[str(v) for v in versions]` with the
  expected order (accept.sh:87-88). That is the input order round-tripped
  through parse; nothing is sorted. ex-015's and ex-017's inputs are given
  already in order, so the test checks the parser, not the comparison.

Measured, per entry (`NOMOD` = `could not import semver: No module named
'semver'`):

| entry | codeless | sealed stand-in | correct code |
| --- | --- | --- | --- |
| ex-001..013 | FAIL NOMOD | FAIL `major: got 99, expected 1; ...` | ok |
| ex-014 | FAIL NOMOD | FAIL `expected ValueError but parsing ...` | ok |
| ex-015..017 | FAIL NOMOD | FAIL `KeyError: 'expect'` | FAIL `KeyError: 'expect'` |

"Correct code" is a 30-line SemVer 2.0.0 `Version` written for this recon
(impl/correct). So ex-015..017 can never pass, and under the stand-in they
looked exactly like sound tests: they failed, for a reason that is not the
load reason.

With :85 and :95 patched to read `expect` (measured, runs/s01p-*): under a
stand-in that parses correctly but compares wrong (`__lt__` False, `__eq__`
True), ex-015 and ex-017 pass and ex-016 fails. So the :87 defect is a weak
test, not a crash, and only a stand-in that round-trips strings exposes it.

## How beagle reads FAIL reasons today

- `failure_reasons` (contract.py:2112) maps each failing entry to its FAIL
  lines, normalised by replacing the entry's own id and operation with
  placeholders (contract.py:2130-2133), so reasons can be compared across
  entries.
- `_LOAD_REASON` (contract.py:2239-2241) is a word list: import, module,
  no attribute, no such file, not found, errno 2, cannot find, does not
  exist.
- `codeless_outliers` (contract.py:2244) takes the commonest codeless
  reason; if it is a load reason held by more than half (contract.py:2266),
  any entry also failing for a non-load reason that does not name its
  operation is an outlier (contract.py:2268-2275). That is R96's check.
- `codeless_refusal` (contract.py:2282) refuses codeless passes and
  outliers, and only if neither is found runs `standin_refusal`
  (contract.py:2319-2320).
- `standin_refusal` (contract.py:2379) refuses: a stand-in naming the
  contract (contract.py:2405); entries failing under the stand-in with
  their codeless load reason (contract.py:2422-2433); invalid entries
  passing (contract.py:2435); entries passing under every stand-in
  (contract.py:2442). A FAIL under a stand-in is taken as the test
  disagreeing with a wrong answer; its reason is never read.

S01 under that code (inferred from the rules above, matching the run):
codeless, all 17 fail NOMOD and there is no outlier, because the import gate
at accept.sh:44-48 stops the loop before the KeyError can happen. Under the
stand-in nothing passes and nothing fails with NOMOD. Seal goes through.

## Candidates, measured

Ground truth for "can never pass": S01, the correct-code run above; R96,
the three invalid entries whose prose input (`'negative integer'`,
`'integer > 274877906943'`) the acceptance `eval`s before calling anything
(wrenfold/contract/accept.sh, the `inp = eval(entry["input"])` under
`kind == "invalid"`); R97, the 56 entries whose operation is their own id,
which import a module that cannot exist (discriminate-recon.md). Stand-ins
used: S01's sealed one; for R96 and R97, scratch ones (impl/r96_wrong,
impl/r97_wrong). Counts from tools/measure.py.

### A. Same reason codeless and under the stand-in, stand-in loaded

An entry the stand-in loaded that fails with a reason it also had with no
code.

| run | refused | of which falsely |
| --- | --- | --- |
| S01 | 0 of 3 | 0 |
| R96 | 3 (the prose-input invalids) | 0 |
| R97 | 0 of 56 | 0 |

Blind wherever the acceptance gates on the import, as S01 does: with no
code the crash is never reached. R96's three are already refused by
`codeless_outliers`. R97's 56 fail for the load reason, which A excludes;
`standin_refusal`'s unloaded rule already refuses them. Adds nothing.

### B. Same reason under two different wrong stand-ins

A second stand-in, wrong differently (other values, inverted comparisons;
impl/*_wrong2). An entry failing with an identical normalised reason under
both is taken to ignore the answer.

| run | refused | of which falsely |
| --- | --- | --- |
| S01 | 4: ex-014..017 | 1 (ex-014) |
| R96 | 10 invalid entries | 7 (every sound `did not raise`) |
| R97 | 56 own-id entries | 0 |

A FAIL message that does not print what the code returned is identical
under every wrong answer, so sound invalid tests and terse comparisons
(`order mismatch`, `expected 1.0.0-alpha < 1.0.0`) are falsely refused.
With S01's :85 fixed, ex-015..017 would print those terse messages, so B
would falsely refuse 4 of 4 (inferred from the patched-copy messages, run
under one wrong stand-in only). Rejected.

### C. A right-answer ("oracle") stand-in: every case entry must pass

The contract worker writes a second stand-in that answers each example's
input with that example's expect, as a literal table, and rejects each
invalid entry's input. Under it every `CASE_KINDS` entry (example, limit,
invalid; contract.py:106) must pass. Language-neutral: beagle reads only
`ok`/`FAIL`, and the table is in the project's language. Measured with
table oracles for R96 and R97 (impl/r96_oracle, impl/r97_oracle, generated
from the contract and written out as literals) and with the correct code
for S01, which on these inputs answers as a table would.

| run | refused | of which falsely |
| --- | --- | --- |
| S01 | 3: ex-015, ex-016, ex-017 | 0 |
| R96 | 3: invalid-negative, invalid-oversize, inv-overflow | 0 |
| R97 | 1: semver-118 (the one own-id entry of kind example) | 0 |

Restricted to case kinds on purpose: under R96's table oracle 9 property
entries also fail (it does not implement `count` or every value a
property probes), so applying C to properties would have falsely refused
9. R97's 55 own-id properties are outside C and stay with the unloaded
rule. C misses R97's 23 comparison-string examples, which pass under any
stand-in; the existing always-pass rule (contract.py:2442) refuses those.

### D. The exception was raised in the acceptance's own frames

Not measurable from output: all three acceptances catch and print only
`str(exc)` or `type: msg` (S01 accept.sh:131-132), never a traceback, so
there is no file to read. Getting one would mean running the acceptance
under a tracer, which is Python-only. Refuses 0 as things stand. Rejected.

### E. The reason quotes one of the contract's own field names

A FAIL reason containing `'id'`, `'kind'`, `'operation'`, `'input'`,
`'expect'` or `'statement'` in quotes.

| run | refused | of which falsely |
| --- | --- | --- |
| S01 | 3: ex-015..017 | 0 |
| R96 | 0 of 3 | 0 |
| R97 | 0 of 56 | 0 |

Exact for S01's bug, blind to R96's (a `SyntaxError`/`NameError` from
`eval`). The quoting is Python's `KeyError` format; other languages name a
missing key differently (inferred: serde's ``missing field `expect` ``,
JavaScript's `reading 'ordered'` for a nested key). Too narrow to gate on.

## Cost of C

- One more acceptance run per seal. S01's took 0.01 s (measured, wall).
- The contract worker writes the table. For S01: 13 parse answers, one
  rejected input, and a rank per version for the compare entries (inferred
  size: about as long as the slice's examples). The brief needs one
  sentence beside the stand-in one (contract.py:3469-3471).
- `codeless_run` already lays any stand-in path out at the copy's root
  (contract.py:2202-2220), so the oracle reuses it. It needs its own
  directory: `standins` reads numbered directories under `standin/` as
  several wrong stand-ins (contract.py:2361), so an oracle among them would
  be held to "every entry fails". The contract-name rule
  (contract.py:2405) applies to it too, which keeps it a literal table.
- Risk: a wrong table. The refusal shows the FAIL reason, so the worker can
  see whether the test or the table is at fault.

## Recommendation

Adopt C. Sealing a slice requires, beside the wrong stand-in, a
right-answer stand-in in its own directory (proposed `<draft>/oracle/`,
sealed with the slice), and refuses any example, limit or invalid entry
that does not pass under it. Its load failure reuses the wrong stand-in's
"did not load" message.

Refusal text:

> not sealed: under the right-answer stand-in <path>, which answers each
> example with its expect and rejects each invalid input, these entries
> fail: <id>: <reason>; ... A test that fails when the code gives the
> expected answer can never pass. Fix how the acceptance reads each named
> entry (its fields as contract.json spells them), or, if the stand-in's
> answer is wrong, the stand-in.

What each run gets:

- S01: ex-015, ex-016, ex-017 refused (`KeyError: 'expect'`); 0 falsely
  refused. The :87 order check is not caught by C; it passes under the
  oracle and fails under the sealed stand-in, so it is a weak test, caught
  only by a stand-in that parses right and compares wrong (residual).
- R96: invalid-negative, invalid-oversize, inv-overflow refused; 0 falsely
  refused (already refused codeless by `codeless_outliers`).
- R97: semver-118 refused; 0 falsely refused (already refused by the
  unloaded rule, as are the other 55 own-id entries).

Reject A (blind to S01), B (falsely refuses 1 in S01 and 7 in R96), D (no
signal in output, Python-only) and E (Python's format, blind to R96).
