# Showing each entry's test can fail once the code loads (T0549)

Read 2026-10-13 against beagle rotation-fixes at commit c3999dc
(`plugins/beagle-pursuit/tooling/beagle/src/beagle/contract.py`, shortened
below to `contract.py`), R97's `~/semver/contract/` and R96's
`~/wrenfold/contract/`. Line numbers are of the committed c3999dc file. That
worktree had uncommitted edits to contract.py from another task while this
was written, and those edits shift the lines (seal is at 1385 there).

## What R97 sealed

`~/semver/contract/accept.sh` groups entries by `operation` and imports each
one as a module (semver/contract/accept.sh:28-35). Then, per entry:

- `property`: `results.append(f"ok {eid}")` with nothing called
  (semver/contract/accept.sh:52-54); the "tested by hand" list is a comment
  (semver/contract/accept.sh:62) and nothing below it tests anything.
- `operation`: ok, unconditionally (semver/contract/accept.sh:55-56).
- `example`: `mod.Version(e["input"])`, then ok; `expect` is never read
  (semver/contract/accept.sh:42-45). The caller's "every expect is valid" is
  not quite right: 12 of 35 say `valid`; 23 are comparisons, e.g. semver-022
  input `1.0.0 < 2.0.0`, expect `less`. Those were never compared, and with a
  correct parser they would FAIL (it rejects the string `1.0.0 < 2.0.0`), so
  they could never pass. That is an inference; not run against R97's code.
- `invalid`: ok on any exception, `Exception` included
  (semver/contract/accept.sh:50), so a stub that raises passes all 26.
- 56 entries (semver-100..155) have `operation` equal to their own id
  (T0543's Reconcile copy), so the script imports a module `semver-118`. They
  can never reach the code.

Codeless, every entry fails `could not import <op>: No module named '<op>'`.
`failure_reasons` replaces the entry's operation with a placeholder
(contract.py:1600-1602), so all 131 runnable entries read as one load reason.
Nothing passed and there were no outliers, so seal went through.

Measured, in a scratch copy (not committed): a 7-line stand-in `semver.py`
whose `Version` accepts anything and answers every comparison False. Under it
52 lines print ok: 34 examples, 15 properties, 3 operations. All 26 invalid
entries FAIL, which shows the stand-in never raised. The 56 own-id entries
still FAIL `No module named`, though the stand-in loaded.

## What sealing checks now

- `seal` runs the full `check`, then `codeless_refusal`, and refuses if either
  objects (contract.py:1323-1330).
- `check` requires every property id to appear somewhere in an acceptance
  file's text (contract.py:830-845). A comment satisfies it, which is all R97
  did (semver/contract/accept.sh:5, :62). With a run prefix it also wants
  every runnable entry reported and a non-zero exit on FAIL
  (contract.py:1638-1667).
- `codeless_run` copies only the sealed files and references/ into a temp dir
  and runs the acceptance there (contract.py:1670-1688).
- `codeless_refusal` refuses any entry that passes with no code
  (contract.py:1749-1757; R94). It also refuses `codeless_outliers`: an entry
  that fails for a reason other than the shared load reason, a reason that
  must match `_LOAD_REASON` and be held by more than half the entries
  (contract.py:1697-1732; R96's prose inputs).
- `shared_failure` (contract.py:1606-1619) is advisory and only feeds
  `contract run`'s note. It does not gate the seal.
- Kinds: `CASE_KINDS` example/limit/invalid need input and expect;
  `STATED_KINDS` limit/property/operation need a statement; `EXERCISING_KINDS`
  are the runnable ones (contract.py:99-105). `operation` declares and is not
  run.
- The brief's LOADING paragraph (contract.py:2227-2236) covers how to load.
  Nothing in the brief or the checks says a verdict must depend on what the
  code returned.

All of these look at the codeless run. With no code, a sound test and an
`ok`-printer that sits behind a failing import look the same: both FAIL on
the import. So no codeless check can tell them apart.

## Options

R96 measurements use a 4-line stand-in `wrenfold.py`: encode returns `b""`,
decode `[]`, count `-1`, and nothing raises. Under it the sealed R96
acceptance printed ok for 8 entries. Three are operation declarations. The
other five are `limit-max`, which only checks `isinstance(..., bytes)`
(wrenfold/contract/accept.sh:130-135); `property-forms`, `rev2-withdrawn` and
`prop-count`, whose statements match no branch and fall through to the shared
`print(f"ok {eid}")` (wrenfold/contract/accept.sh:169); and `ex-decode-empty`,
where the stand-in's `[]` happens to equal the expected `[]`.

**(a) A stand-in that loads but answers wrongly, written by the contract
task.** It goes in `contract/standin/` (sealed with `files = ["contract/"]`)
and is the code with every answer wrong. At seal, beagle copies it to the root
of the codeless scratch copy and runs the acceptance. Beagle never reads the
stand-in, only what the acceptance prints, so this works in any language (beagle
cannot write one itself without knowing the language and API). The
seal refuses if:
1. any runnable entry passes under every stand-in;
2. any entry fails with the codeless load reason (the stand-in loaded, so that
   test never reaches the code);
3. any invalid entry passes under any stand-in. Rule 3 rules out a stand-in
   that raises everywhere, which would otherwise "fail" each example by
   raising.

Several stand-ins are allowed, to break coincidences like `ex-decode-empty`.
- Cost: 10-20 lines of code for the contract worker, and one acceptance run per
  stand-in at seal (both runs above took under a second; a compiled language
  pays a build). In the code, `codeless_run` and `failure_reasons` are reused.
- Failure modes:
  - A stand-in that does not load: every entry fails on one reason, and the
    refusal names that.
  - A stand-in that knows the inputs and raises only on example inputs. Beagle
    can refuse a stand-in whose text names the contract file, as `check` does
    for the acceptance (contract.py:826). Literal lists stay a residual risk.
  - A contract with no invalid entries can't prove the stand-in never raises.
  - A test of "must succeed" that checks no value is refused, so it has to
    check a value: a round trip or a parsed field.
- R97: refused for 34 examples, 15 properties and the 56 own-id entries.
- R96: refused for the five above.

**(b) Perturb contract.json input/expect; the verdict must move.** Works only
where the acceptance reads the entry's data: R96's examples `eval` it
(wrenfold/contract/accept.sh:46-47), its properties use literals, R97 reads
`input` but never `expect`. Codeless nothing moves, so it needs code or a
stand-in, where (a) already shows it. A perturbed value must stay parseable in
the acceptance's encoding (Python literals in R96): not language-neutral. Sound
literal tests don't move either: false refusals. R97: catches unread expects
once code passes them, not the 15 properties. R96: nothing new.

**(c) Static refusal of an ok reached without reading the code's return.**
Needs dataflow analysis per acceptance language (bash, pytest, cargo, jest);
gamed by `_ = mod.Version(x)`. Catches R97's :54/:56; :45 needs taint analysis
(result unused); R96's fall-through :169 needs path analysis over statement
matching. Rejected.

**(d) Prove discrimination at the first milestone that loads the code.** No
stand-in to write, but beagle can mutate only data, so (b)'s limits apply
(mutating code is per-language). The hole surfaces after the code exists: a
dispute and reseal mid-run (R97 sealed at 31.6 of 60 min), and the worker who
fixes the test wrote the code it judges, so the test can bend to fit it. R97:
comparison examples flagged late. R96: nothing new.

**(e) Beagle generates the example/invalid harness.** Needs a stdio adapter
protocol (`<cmd> <operation>`, JSON in/out, non-zero exit for invalid) and
expects as canonical JSON: a schema and extraction change (R97's expects are
prose like `less`; R96's are Python literals). The adapter is new code that can
swallow errors too. Properties stay hand-written, so R97's 15 property oks and
56 own-id entries are untouched: heavy, and covers half the hole.

**Properties "tested by hand".** A property with no machine test should not
seal. R97's semver-071..077 are rules for whoever publishes versions ("MUST
declare a public API"), not for the code. Each of those belongs in `excluded`
with a `why` (contract.py:729-746). A property that is about the code but
can't be machine-tested (e.g. "count does not build the list") becomes a gap
with an `assumption`. Assumptions are already carried into the seal record
(contract.py:723, :1337). Under (a), an untested property passes under the
stand-in, so it is refused, and the refusal can name these two exits. That
enforces the rule without relying on prose.

## Recommendation

Adopt (a). Sealing should require a stand-in (one or more under
`contract/standin/`, sealed with the contract) under which:
- every runnable entry fails under at least one stand-in;
- no entry fails with the codeless load reason;
- no invalid entry passes.

The refusal names each entry and says why. For a property it offers
`excluded` or a gap with an assumption as the ways out.

The brief needs one sentence next to LOADING telling the contract worker to
write the stand-in. The seal refusal, not the sentence, does the enforcing.
(a) catches R97's whole hole: the examples that never read their expect, the
15 ok-printing properties, and the 56 entries that can't reach the code. It
also catches R96's five weak entries.

Defer (b), (d) and (e), and reject (c). The residual risk is a stand-in that
knows the inputs; mitigate it by refusing stand-ins that name the contract
file.
