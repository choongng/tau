# Contract-first eval (T0492)

Setup is gather → contract → plan (T0478). Runs launch with
`BEAGLE_ROOT=~/beagle-wt/contract-first`; `meta.json` records the beagle root,
branch and sha. Grades come from `grade_<task>.py` over `runs/RNN/adapter.py`;
`progress.py` lists them.

| Run | Model | Task | Beagle | Grade | Earlier on the same model and task |
|---|---|---|---|---|---|
| B06 | q35 | wrenfold | none (plain tau, no extensions) | 54/54 | — (baseline for R71) |
| R71 | q35 | wrenfold | contract-first 01db8e9 | 0/54 | B06 54/54 in 9.1 min |
| R72 | q35 | cobs | contract-first c4bc1a5 | 0/44 | R60 42/44 (cases-first); B05 plain 41/44 |
| R73 | q35 | itc | contract-first c4bc1a5 | 0/42 | B04 plain 0/42; R53–R61 cases-first: see below |
| R74 | qwen 9B | cobs | contract-first 01db8e9 | 11/44 | qwen cobs best 7/44 (R22 3, R43 5); B01 0/44 |
| R81 | q35 | itc | contract-first fce5dac (anchors) | 0/42 | R73 0/42; R57 lean cases-first 23/42 |
| R82 | q35 | cobs | contract-first fce5dac (anchors) | 0/44 | R72 0/44; R60 42/44 (cases-first) |
| R83 | q35 | itc | contract-first a80193c (add, listing, bare names) | 18/42 | R81 0/42; R57 lean cases-first 23/42 |
| R84 | q35 | cobs | contract-first a80193c (add, listing, bare names) | 39/44 | R82 0/44; R60 42/44; B05 plain 41/44 |
| R85 | q35 | cobs | contract-first 6e25585 (independent second, T0516) | 0/44 | R84 39/44; B05 plain 41/44 |
| R86 | q35 | cobs | contract-first 6e25585 (T0516, T0518, T0519) | 42/44 | R84 39/44; B05 plain 41/44 in 48.8 min |
| R87 | q35 | itc | contract-first 6e25585 (T0516, T0518, T0519) | 0/42 | R83 18/42; B04 plain 0/42 |
| R88 | q35 | cobs | contract-first eccdcac (T0509, T0510, T0520, T0522) | — (OOM-killed at 23 min, in Contract) | R86 42/44; B05 plain 41/44 |
| R89 | q35 | cobs | contract-first 676ffd1 (T0524) | 2/44 in 49.8 min (ended, not capped) | R86 42/44; B05 plain 41/44 in 48.8 min |
| R90 | q35 | cobs | contract-first 271a767 (T0524, T0525) | 39/44 at the 60 min cap (working tree; 31/44 committed) | R86 42/44; R89 2/44; B05 plain 41/44 in 48.8 min |
| R91 | q35 | cobs | contract-first 6ff1dd0 (T0524–T0526) | 5/44 at the 60 min cap (encode never closed) | R90 39/44; R86 42/44; B05 plain 41/44 in 48.8 min |
| R92 | q35 | cobs | contract-first 1684138 (T0529); tau 7cb40c5e (T0527, T0528) | void: another session switched ~/tautest/tau's branch at 18 min, removing the beagle extension | — |
| R93 | q35 | cobs | the same, tau pinned in ~/tautest/tau-harness | 0/44 at the 60 min cap (contract not sealed) | R92 sealed at 30.6 min; R91 5/44; R90 39/44; B05 plain 41/44 in 48.8 min |
| R94 | q35 | cobs | contract-first e02f316 (T0529, T0530); tau 7cb40c5e pinned | 13/44 at the 60 min cap (working tree; encode 11/11, decode 0/11) | R93 0/44; R90 39/44; B05 plain 41/44 in 48.8 min |
| R95 | q35 | itc | contract-first e02f316 (T0529, T0530); tau 7cb40c5e pinned | 22/42 at the 60 min cap (working tree; uncommitted) | R87 0/42; R83 18/42; R57 lean cases-first 23/42; B04 plain 0/42 |
| R96 | q35 | wrenfold | contract-first e02f316 (T0529, T0530); tau 7cb40c5e pinned | 50/54 at the 60 min cap (working tree; package ~/wrenfold/wrenfold, uncommitted) | R71 0/54; B06 plain 54/54 in 9.1 min |
| B07 | q35 | semver (bare goal) | none (plain tau, no extensions) | 75/76 in 8.1 min, ended on its own | — (baseline for the bare-goal pursuit runs) |
| R97 | q35 | semver (bare goal) | contract-first 24bd167 (T0536, T0537, T0541); tau e66018d7 pinned | 58/76 at the 60 min cap (working tree; T0006 Core Version class open, uncommitted) | B07 plain 75/76 in 8.1 min |
| S01 | q35 | semver (smoke, 25 min cap) | contract-first cde3fbd (incremental contract, T0554-T0560, T0566); tau 2ea8cd1b | not graded: capped at 1500 s mid-milestone; first code at 14.0 min (R97 31.6) | B07 plain 75/76 in 8.1 min |
| R98 | q35 | wrenfold | contract-first 395d806 (incremental contract + S01 fixes T0567-T0581, oracle stand-in T0572); tau df13db3e | 54/54 in 49.9 min, ended on its own (codec.py committed) | R96 50/54 capped; B06 plain 54/54 in 9.1 min |
| R99 | q35 | semver (bare goal) | contract-first 009c2b8 (R98 + bounded `run --operation`, caller env in contain); tau f061aa4a | 75/76 at the 60 min cap (working tree: src/ untracked, nothing committed; graded through runs/R99/adapter.py) | R97 58/76 capped; B07 plain 75/76 in 8.1 min |
| S02 | q35 | wrenfold (smoke, 25 min cap) | beagle 0.48.0 08e642c (spec-tying, no contract); tau beagle-0.48 fb3823e5 | 0/54: capped at 1500 s with T0002 (Encoder) open, no code written; the driver's done_when asserted wrong bytes (6 of 10), so both workers spent a 16k-token turn reconciling it with the spec | R98 54/54 in 49.9 min; B06 plain 54/54 in 9.1 min |
| R100 | q35 | wrenfold | beagle 0.48.0 08e642c; tau ecb438ea (T0609) | 54/54 on the working tree, stopped at 35.6 min when runs went to a 30 min cap; nothing committed, no task done. The code was green at 14.6 min (reconstructed from the worker session) | S02 0/54; R98 54/54 in 49.9 min; B06 plain 54/54 in 9.1 min |
| S03 | q35 | wrenfold (smoke, 30 min cap) | beagle 0.48.0 08e642c; tau 3cf73fa3 (fix 1, T0611: cases quote) | 0/54: capped at 30 min with no task opened and no code; both T0002 cases workers wrote sound cases under markers beagle could not read (cite where the name goes; then `cite=` with no name) | R100 54/54 green at 14.6 min; B06 plain 54/54 in 9.1 min |
| S04 | q35 | wrenfold (smoke, 30 min cap) | beagle 0.48.0 08e642c; tau 602750d9 (T0611-T0614: cases quote, case-correction route, marker naming) | 45/54 at the cap, first at 23 min; T0002 opened tied at 12.9 min (markers right first try), code worker still fixing 63 and the end-marker refusal at the cap | S03 0/54; R100 green at 14.6 min; B06 plain 9.1 min |
| S05 | q35 | wrenfold (smoke, 30 min cap) | beagle 0.48.0 08e642c; tau 5cd51a62 (T0616: work arithmetic out by running it; cases don't stub the code) | 0/54 at the cap: founding made 'Project scaffolding' a sourced milestone; its cases (cited to the title line) opened at 19.6 min, closed done at 25.5 min; the encoder never opened | S04 45/54; B06 plain 9.1 min |
| S06 | q35 | wrenfold (smoke, 30 min cap) | beagle 0.48.0 08e642c; tau 352f48e9 (T0617: fold a layout-only milestone) | 49/54 from 20 min to the cap, never closed: founding 5.5 min with scaffolding folded into Encoder; T0002 opened tied at 17.2 min; one wrong case (`encode([63])` without the end marker) put back three times, as the worker's CASE line named the test and the cite only the sentence's last line | S05 0/54; S04 45/54; B06 plain 9.1 min |
| R104 | q35 | wrenfold (round 1, 30 min cap) | beagle 0.48.0 08e642c; tau 8f721639 (T0618 reasoning time cap, T0619 CASE line) | 12/54 at the cap, first at 22 min: encoding closed (T0002 at 18.5 min, T0003 at 21.3), decoding never reached; founding 1.7 min into 6 milestones; T0002's cases worker took 11.5 min, one 241 s turn cut by T0618 | S06 49/54 unclosed; B06 plain 9.1 min |
| R105 | g26 | semver (round 2, 30 min cap) | beagle 0.48.0 08e642c; tau 4cf54474 (T0620) | 0/76 at the cap: founding's 'Environment setup' milestone took 18.5 min (13 of re-routing a check no defect could fail); T0003's source was the unfetched URL https://semver.org/, its first cases worker found no reference; the second was writing cases at the cap | B07 plain q35 75/76 in 8.1 min |
| R106 | lfm24 | itc (round 3, 30 min cap) | beagle 0.48.0 08e642c; tau 79652f00 (T0621) | 0/42, ended at 11 min: the driver sent T0002's description as pursuit_step's task (criteria, done_when, scope right), was told to call with no arguments, then tried to write src/itc.py itself until the 8-refusal breaker stopped the run; no worker ran | — |
| R107 | q35 | cobs (round 4, 30 min cap) | beagle 0.48.0 08e642c; tau b8f57402 (T0622, T0623) | 37/44, ended on its own at 27.8 min with all 6 tasks closed (T0002 at 23.6 min); no milestone named a source, so no cases worker ran: empty encode and the 5 malformed-decode cases fail | — |
| R108 | g26 | wrenfold (round 5, 30 min cap) | beagle 0.48.0 08e642c; tau 65aee9aa (T0624) | 0/54 at the cap, no code: T0002 scoped to its test file alone; tau's data-test refusal made a second cases worker (cases committed at 17.5 min, cites right) and the code worker, refused wrenfold.py, rewrote the tests | — |
| R109 | lfm24 | semver (round 6, 30 min cap) | beagle 0.48.0 08e642c; tau fe94622d (T0625) | 0/76 at the cap, no code: six refused pursuit_plan calls, then three cases workers whose cites all carried #0b7 beside the right line numbers; open refused each | — |
| R110 | q35 | itc (round 7, 30 min cap) | beagle 0.48.0 08e642c; tau a3eb469a (T0626) | 17/42 at the cap: T0002 tied at 11 min, code 22/24 of its cases by 23:16; three forced gap cases contradicted the paper, and two code workers' corrections were put back (CASE words were the docstring; the paper's words were in backticks beside) | — |
| R111 | g26 | cobs (round 8, 30 min cap) | beagle 0.48.0 08e642c; tau 93cf761e (T0627) | 3/44 at the cap: cases tied at 15 min (15 cases); the code worker's three 240 s turns in a row reasoned COBS out by hand and never acted, the bound of two nudges ended it; a second worker wrote a placeholder cobs.py just before the cap | — |
| R112 | lfm24 | wrenfold (round 9, 30 min cap) | beagle 0.48.0 08e642c; tau 0280f1b5 (T0628) | 0/54 at the cap, no code: T0002 never opened; cases worker 1 cut off three times; the driver's next call had no scope, refused only after its cases worker ran 6 min; worker 3 still writing cases at the cap | — |
| R113 | q35 | semver (round 10, 30 min cap) | beagle 0.48.0 08e642c; tau 5e458e36 (T0629) | 75/76 at 4 min (snapshot t04), all-done at 16 min, ended on its own; the miss is `1.2.3\n` accepted (`$`, not `\Z`) | B07 plain q35 75/76 in 8.1 min |
| R114 | g26 | itc (round 11, 30 min cap) | beagle 0.48.0 08e642c; tau 4fc29568 (T0629) | 0/42 at the cap, no code: founding's first task was a reading task ('Examine practical implementation patterns'); its step scoped references/ and was refused only after a 5 min cases worker; two more were refused at the open for no invalid/limit case per op (none ran the dry-run its brief names); the fourth was running at the cap | — |
| R115 | lfm24 | cobs (round 12, 30 min cap) | beagle 0.48.0 08e642c; tau 61255dbc (T0630) | 0/44 at the cap, no code: T0002's first cases worker ran 12.5 min, never ran its dry run, and the open refused it (a `kind=encode` marker with no op or cite; no invalid case for encode); the second worker ran the dry run itself and was still mending at the cap | — |
| R116 | q35 | wrenfold (round 13, 30 min cap) | beagle 0.48.0 08e642c; tau 72cc8154 (T0633) | **54/54 at 21 min** (plain 9.1; R98 49.9); T0002 encoder closed at 12.5 min and T0003 decoder at 26 min, each on one call; the cap fell during T0004 (examples) | — |
| R117 | g26 | semver (round 14, 30 min cap) | beagle 0.48.0 08e642c; tau 66af91e5 (T0634) | **75/76 at 14 min** (plain 8.1; R113 q35 4); the one miss, `1.2.3\n`, is accepted through `$`, as in R113; T0002 closed at 23.6 min, and T0003 (comparison) was open at the cap | — |
| R118 | lfm24 | itc (round 15, 30 min cap) | beagle 0.48.0 08e642c; tau 5973453f (T0635) | **0/44**; founding kept 'Setup complete: beagle init written, pursuit founded …' as T0002, and the whole run went to that empty task; the itc.py one of its workers wrote models ids as integer pairs, not trees | — |

## B06 — the invented spec was not hard

Plain `tau -p` with no extensions, on the same prompt without the beagle
instructions, finished on its own in 9.1 minutes and passes every case,
the end-marker trap (63 → `40 3F`), the overlong-form rejection and `count`
included. Knowledge outside the weights is not by itself what makes a task
hard: a short, clear spec read once is enough for q35. Wrenfold therefore
measures overhead, not rescue. Where contract-first could pay is a long or
ambiguous source (the ITC paper: B04 plain q35 itc 0/42).

## R71 — q35 wrenfold: the hour went to the contract

Capped at 3600 s, still in T0002 (Contract). Driver founded in one call at
10:41, then stepped T0002 four times; seven workers ran on it until the cap.
The draft passed `contract check --draft` at about 11:38 with 28 entries: all
8 worked examples, all 4 stated decode rejections plus out-of-range encode,
`count` (named once in the spec), and 62 in the one-byte form. It had no
entry for 63 → `40 3F`, the end-marker trap the spec states only in prose.

Where the time went:

- **Quote length (fixed, T0497, beagle c4bc1a5).** A table row such as
  `0 | 00 3F` folds to 6 characters, under `MIN_QUOTE` = 8. The refusal said
  "quote the whole line", and the whole line was refused too. The workers
  padded the rows with the prose around the table, the padding was refused as
  not in the source, and that churn ran from 10:48 to 11:38. A short quote
  that is the whole of exactly one source line now passes.
- **Reasoning-only cut-offs.** Two workers (10:49, 11:08; ~24 min together)
  ended on `length` with 115k–132k reasoning chars; the next workers ran
  thinking-off (the off-on-retry rule worked).
- **Turn cap.** Three workers ended at the 31-turn cap mid-edit; two of
  those last replies were tool calls written as text, which the existing
  nudge would have caught but the cap came first.
- **Scope.** Workers on the contract task wrote `wrenfold.py` and
  `wrenfold/__init__.py`; neither is in the final tree.

## R74 — qwen 9B cobs: the contract schema was out of reach

Capped at 3600 s, still in T0002. The draft has 25 entries, but the 9B wrote
operations as prose sentences and examples and invalid entries with no
`input`/`expect`, so the draft check refused it to the end. The only code is
`contract/cobs.py`, a helper a worker wrote inside the contract directory; it
grades 11/44 (roundtrip, decode and malformed cases fail), above qwen's
earlier best on cobs, but no pursuit task produced it.

## R73 — q35 itc: the contract closed, at 55 minutes

Capped at 3600 s. First run with T0497's short-quote rule. Five workers ran
the contract task from 11:50 to 12:43, four of them to the 30–31-turn cap;
T0002 closed done at 12:44 with 67 entries and 5 listed gaps. The seal task
(T0003) had one worker, which was reconciling the second extraction when the
cap came: it named the `fork` and `join` equations, join's commutativity and
the event-tree shape as passages the contract cites nowhere, and two
operations the contract lacks. Those are real omissions — the cross-check
did its job — but no code was written, so every grader op is MISSING.

Quote refusals no longer stalled it; the cost is volume. A 67-entry contract
over a 20-page paper takes q35 about five worker contexts to write and check.

## R72 — q35 cobs: the driver gave up on the contract

Capped at 3600 s. The contract task T0002 failed its check and was retried
as T0008; two workers timed out and two dispatches were refused by tau. At
13:41 the driver closed T0008 abandoned — "The contract check tool is too
strict for sub-agents to satisfy — it requires exact verbatim quotes from the
reference … I will write the contract myself and move on" — and wrote to
`contract/` itself, which the orchestrator rules forbid. No code. The tree
then showed T0003 (Second extraction) as ready with no contract to check
against.

## What the five runs say

- Plain q35 (B06) passes the invented spec in 9 minutes; q35 cases-first
  (R60) and plain (B05) reach 41–42/44 on cobs. Contract-first q35 scored 0
  on all three tasks: every run spent its hour in setup.
- The cost sits in authoring the contract by hand, and most of it in
  quoting: short table rows (R71, fixed by T0497), quotes retyped from
  memory (R73), PDF text whose symbols cannot be retyped (`⇐⇒`, `t` for ⊔),
  and a driver that abandoned the task over verbatim quotes (R72).
- The checks themselves worked: R73's second extraction found real
  omissions (the fork and join equations, join's commutativity).
- The 9B (R74) could not produce the schema at all.

Next: cite by line anchor instead of quote (`beagle pursuit contract refs`
prints `83#a1f| text`; an entry cites `itc2008:83#a1f[-85#c02]`; beagle
checks the hash and fills in the quote), then re-run q35 on cobs and itc.
Open beyond that: a driver that does the work itself after abandoning, a
seal task that is ready with no contract, and the per-worker turn cap on
long contract tasks.

## Line anchors: R75–R82 (T0504, T0506, T0508)

Cites became `N#hhh` line anchors (beagle 809d194, fce5dac): `contract refs`
prints each reference line with its anchor, and the check refuses an anchor
whose hash is wrong or a bare line number, naming the right one. Three runs
were stopped before grading, each by a tau guard that kept the workers from
the anchors, and each guard was fixed before the next run:

- **R75** (stopped): a worker sent with no task could not run `contract`
  verbs (T0502, tau 0de5e0b7).
- **R77** (stopped): a worker sent on a task met the "do not run beagle"
  orientation guard, and invented anchors (T0505, tau 8633f50a).
- **R79** (stopped): the brief offered 12 `read` calls at 60 lines, the worker
  paged the references with `read`, and the call budget then refused
  `contract refs`; 71 of 76 anchors were invented, copying the brief's example
  (T0507, tau eab231f1: references are read by `contract refs`, uncounted).

## R81 — q35 itc: the contract sealed; the code ignored it

Capped at 3600 s, 5 of 9 tasks done. The first contract-first run to seal.
The contract worker ran `contract refs` 38 times; its first draft had 34 bad
cites of 76, and the check's refusals took that to 0. T0002 closed at 16:02
(95 entries), the second extraction sealed it at 16:13, and Scaffolding, Core
types, Split and Merge took the last 15 minutes.

The contract states the paper's model (id and event trees, `split(1) =
((1,0),(0,1))`), but `itc/clock.py` is a float interval per named node, so
every grader case fails. Nothing held the code to the contract: `accept.sh`
names `contract.json` only in a comment and runs 16 hand-written tests against
a `src/itc/stamp.py` that was never built, none of the 58 example ids, and
beagle's acceptance check reads the script's text only. Milestones closed on
their own tests. Follow-ups: T0509 (the acceptance run must report every
entry id before the contract seals), T0510 (a milestone is held to the
contract entries for its operations).

Where the hour went: contract 45 min (first draft 14, of which one 51 KB
whole-file write was cut off and redone in parts; fixing cites and coverage
17; second extraction 11), implementation 15. The contract workers wrote
about 100k output tokens; the contract is 46 KB and was written about 2.5
times.

## R82 — q35 cobs: two problems the check would not explain

Capped at 3600 s, never sealed, no code. By 17:12 the draft had 31 entries,
0 bad cites and 3 problems: no second extraction yet, and `op-encode` and
`op-decode` "defined and nothing exercises it". Those two are beagle's: the
operation entries name `encode(data: bytes) -> bytes`, the 13 examples name
`encode`, and the check matches the two strings exactly without saying so.
The worker spent its last minutes adding property links to the operation
entries; the retry worker (T0009) re-read every file and ran out of time.

## What R81–R82 say

- Anchors work once the workers can reach them: 0 bad cites in both runs,
  fixed from the check's own refusals.
- Sealing is not enough. R81 sealed a correct contract and built something
  else, because acceptance was text and milestones were not held to it.
- The contract stage is still most of the hour (45 min on itc), mostly in
  writing JSON: whole-file writes, fixes, and a second full extraction.
- A refusal has to say what would satisfy it (R82's exact name match).

Next: T0509, T0510, the operation-name match, and a cheaper contract stage
(entries added one at a time and checked as they go; a second extraction
that lists anchors rather than rewriting entries).

## A cheaper contract stage: R83–R84 (T0515)

Both ran on beagle a80193c and tau 96b9beb9 or later. Changes since R81–R82:
`contract add` (T0513), a second extraction that lists anchors only (T0514),
and operations matched by bare name (T0512). Both runs hit the 60-minute cap.
Both contracts sealed, and both runs produced code that grades.

| | R81 itc | R83 itc | R82 cobs | R84 cobs |
|---|---|---|---|---|
| Founding to seal | 45 min | 30 min | never | 19 min |
| First Contract worker | 14 min (51 KB written whole, cut off, redone) | 8.5 min, 71 added, 17 refused | — | 5 min, 26 added, 7 refused |
| Second extraction | 11 min, 39 KB | written by a Contract worker (below) | — | 14 min over two workers, 25 listing entries |
| Implementation time | 15 min | 26 min | 0 | 39 min |
| Grade | 0/42 | 18/42 | 0/44 | 39/44 |

- Every Contract worker used `contract add`, and no run wrote `contract.json`
  whole. Refused entries were fixed in the same turn they were refused, so
  there was no separate fixing pass like R81's 17 minutes.
- R83's code is a real ITC (id and event trees on tuples). It passes the
  per-operation cases and fails the traces and the paper's worked run. It is
  uncommitted in the working tree: the scaffolding task was still open at the
  cap.
- R84 fails only the five malformed-input cases. The Wikipedia reference says
  nothing about malformed input, so the contract has no invalid entries and
  no gap for it. That is knowledge the source does not hold, the regime this
  series is for. Nothing asked the reader what the source leaves unsaid about
  invalid input.

### The second extraction was not independent

- R83: the second Contract worker read `contract.json` and ran the full check.
  The check said "second extraction does not exist yet: have a reader who has
  not seen contract.json write it", and the worker wrote it itself, as full
  entries (20 KB). The Second extraction task then closed in a minute on that
  file.
- R84: both second-extraction workers began with `cat contract/contract.json`.
  The listing has the first's ids and cites, minus one.
- Cause: tau's founding note tells the driver to give both tasks the scope
  `contract/`. Beagle recognises a second extraction only when its scope is
  the second file (plus references), so these workers got the Contract brief.
  "Without reading the first" reached them only as criteria text the driver
  wrote.

## What R83–R84 say

- With `add`, the stage still costs time, but less of it: about a third to a
  half of the hour, down from all of it.
- Independence is not held by anything yet. The fix belongs in the scope
  founding gives the second extraction, and in a refusal when a worker reads or
  writes the other extraction.
- Invalid input the sources do not state needs to become a gap the reader is
  asked about, not silence.

## An independent second extraction: R85 (T0516, T0518, T0519)

R85 ran on beagle 6e25585 and tau 22b198e8 (T0516). Founding seeds three contract
milestones (Contract, Second extraction, Reconcile), and pursuit_step gives each
its scope and check itself. The guard keeps the second's worker from
`contract.json` and every other worker from the second.

- Independence held. T0003's worker had the scope `contract/contract.second.json`.
  Its one attempt to read the first (`cat contract/contract.json`) was refused,
  and it built 22 entries from the reference with `contract add`. The first had
  25. The full check passed on the two, so the contract sealed when T0003
  closed, at 18.5 min (R84: 19 min).
- Then the run stopped itself at 31.1 min with no code: 0/44. Reconcile's check,
  `contract check`, already passed, so it could not be opened. Tau offered a
  done-by close with `done_when="beagle pursuit contract check"`. The driver
  bound `--draft`, which still passes with the second taken away, so the close
  was not proven and T0004 closed blocked. A milestone cannot be abandoned. Every
  later route was refused as "already passes", and eight refusals in a row
  stopped the run.
- Fix (T0519, 7a77a357): a close that seals the contract closes each pending
  contract milestone done by the task that sealed it, proven on the milestone's
  own check with that task's work taken away. A done-by close of a contract
  milestone takes the milestone's fixed scope and check, whatever the driver
  passes.

### R84's last 25 minutes (T0518)

R84's code graded 39/44 at about 35 min. The rest went to T0004 "Project
structure", bound to `python -m pytest -q --co -q`. `python` is not on PATH
here, and `systemd-run` reports a missing program as exit 1, not 127. So the
check read as failing rather than as unable to start. One worker was killed at
its 900 s budget and a second ran on; together they took 32 minutes. The driver
then made a host symlink `~/.local/bin/python -> /usr/bin/python3` (removed after
R85, which ran with it). T0518 (24d24895) looks a check's first word up before
running it, and refuses one that is not a program here. The refusal names
`python3` or `.venv/bin/python` when they are there.

## R86 — q35 cobs: 42/44, sealed at 14 min, capped in Tests

Tau d1704881 (T0518, T0519), beagle 6e25585. Capped at 60 min. The code grades
42/44 and fails only the two malformed-input cases. That is the best
contract-first cobs grade, and above plain tau's 41/44 (B05). The code was
committed with T0006 at about 44 min. The run did not finish: Tests was open at
the cap, with Package and a gate fix pending, so it does not beat B05's 48.8 min.

| Stage | Minutes | |
|---|---|---|
| Founding | 0–1.8 | |
| Contract T0002 | 1.8–7.8 | 19 added, 2 refused |
| Second extraction T0003 | 8.0–10.4 | 20 added, 2 refused; did not read the first |
| Reconcile T0004 | 10.6–13.6 | 3 added; then sealed |
| Core encoding T0006 | 14.0–44 | three workers, below |
| Decoding T0007 | 44 | done by T0006, no worker |
| Tests T0008 | 44–59 | worker killed at its 900 s budget; open at the cap |

- The contract stage took 14 min (R84: 19). Reconcile had real work this time,
  so it was a worker, not T0519's close at the seal.
- T0518 refused the driver's first T0006 check (`python -c …`): "no `python` on
  PATH; python3 is". The driver corrected it in one call.
- T0006's first worker read the reference and the contract, then spent 10 min
  writing the encoder in its reasoning. It was cut off at the 16K output limit
  twice and ended with no file written.
- T0006's check was the driver's own `python3 -c` assertions, and they
  contradicted each other: `encode(b'') == b'\x01'` with no delimiter, but
  `encode(b'\x00') == b'\x01\x01\x00'` with one. The second worker's code met
  the contract and failed the check. The driver amended the check, and a third
  worker ran (35.6–42.7 min). About 9 min went to a check the contract would not
  have written.
- The goal's criteria include a pytest suite and packaging, which the contract
  does not cover. Tests took the rest of the hour.

What it says: the contract stage is now about 14 min on cobs. After the seal,
the time goes to checks the driver writes by hand, and to milestones the
contract's acceptance could decide. The next step is to bind those milestones
to `beagle pursuit contract run`, or a per-operation part of it.

## R87 — q35 itc: 0/42, the Contract task's check replaced (T0522)

Capped at 3600 s in Core data structures, with `src/itc/__init__.py` holding Protocol stubs and
functions whose bodies are `pass`.

| stage | closed at |
|---|---|
| Contract T0002 | 37.6 min |
| Second extraction T0003 | 42.7 min |
| Reconcile T0004 (110 entries) | 52.6 min |
| Project scaffolding T0005 | 56.6 min |

About 20 of the Contract's 37 minutes were lost to one gap. The task opened on its own check,
`contract check --draft`, and two workers left it failing on properties no acceptance file named.
The driver's next `pursuit_step` passed notes with a `done_when` of its own (`test -f ... &&
assert len(entries) > 0`), and that amended the check: T0516 kept the contract milestones'
check only at open. The worker's 15 minutes closed on a check `prove` showed could not refuse;
the driver's next guess asked for at least 50 entries, and the worker padded the contract from
30 to 56. T0522 keeps the check on an open task too and tells the driver its `done_when` is not
used.

Even without it, itc's contract stage is long: Second extraction and Reconcile took 15 minutes
after the Contract closed, against 14 minutes for cobs's whole stage in R86.

## R88 — q35 cobs: killed at 23 min by an acceptance that ran itself (T0524)

Not graded: the kernel's OOM killer took the run's scope at 23 min, with
T0002 Contract still open and no code written.

- T0522 held: the driver's first `pursuit_step` passed its own done_when, and
  was told Contract keeps `contract check --draft`.
- The first Contract worker spent 1.9–9.6 min reading the reference with no
  writes, then wrote the contract as a JSON list (refused: an object is wanted)
  and rebuilt it through `contract add` by 14.4 min. The 6 properties then
  wanted an acceptance file naming each.
- At 17.4 min the driver's notes said "accept.sh should use `beagle pursuit
  contract run`". The next worker wrote accept.sh as
  `exec beagle pursuit contract run`; the acceptance is
  `sh contract/accept.sh`, so each started the other. Two worker runs hit their
  4G cap on `bash contract/accept.sh`; then the driver itself ran
  `beagle pursuit contract run` at 22.2 min, inside the whole run's scope.
- T0524 (beagle 676ffd1): the acceptance beagle runs is marked
  (BEAGLE_CONTRACT_ACCEPTANCE), and one run from inside it is refused, exit 2;
  `contract check` names an acceptance file that runs beagle's contract
  before anything runs it.
- Not answered by R88: whether accept.sh prints ok/FAIL lines at the seal, and
  whether milestones use `contract run --operation`. R89 repeats it on 676ffd1.

## R89 — q35 cobs: 2/44, the encode milestone could not pass (T0525)

The contract sealed at 13.8 min (R86: 14). Stages closed at:

| Stage | Closed at |
|---|---|
| Contract (28 entries) | 9.2 min |
| Second extraction | 11.9 min |
| Reconcile (sealed) | 13.8 min |
| T0005 Core encoding | open at the end, 49.8 min |

- accept.sh prints one `ok <id>` / `FAIL <id>: why` line per entry (T0509/T0510
  hold), and T0005's check was `beagle pursuit contract run --operation encode`
  (T0520 holds).
- 18 of the 28 entries could not be replayed: EX-7..EX-11 kept the source
  table's elision (`01 02 03 ... FD FE`), and all 10 limits were descriptions
  (`any input`, `n data bytes`). The acceptance FAILs them on parsing, so
  `--operation encode` could not pass whatever the code did. R84, R85 and R86
  sealed the same elided rows; before T0509 nothing judged a milestone by its
  entries, so it cost nothing.
- The T0005 worker spent its 900 s wall reasoning about a contract it read as
  "intentionally contradictory", hit the output limit, and left a cobs.py whose
  encode raises IndexError on `00`. The driver, refused the reference, worked
  the algorithm in its head: three replies in a row ended at the 16k output
  limit (5 min each), and tau ends a session on the third
  (MAX_OUTPUT_LIMIT_CONTINUATIONS = 2). The run ended at 49.8 min, not capped.
- T0525 (beagle 271a767): an example, limit or invalid whose input or expect
  elides (`...`, `…`) or opens as a description (any/every/all/each/some/n …)
  is a contract problem; a bound with no case of its own is pointed at kind
  property. Over past contracts it flags R84–R89 cobs and one prose example
  each in itc R77/R83, none in R73/R75/R79/R81/R87.
- Open: the driver's output-limit spiral when a milestone stalls. R90 repeats
  on 271a767.

## R90 — q35 cobs: 39/44 at the cap; Reconcile lost 13 min to a name (T0526)

Capped at 60 min. Graded on the working tree, 39/44; the committed tree, whose
decode the last worker was still fixing, 31/44. All five failures are malformed
input that decode returns instead of raising (B05 and R86 fail two of these);
the reference states no rule for it, so no contract entry holds it.

| Stage | Closed at |
|---|---|
| Contract (25 entries) | 13.8 min |
| Second extraction | 16.9 min |
| Reconcile (sealed) | 30.3 min |
| T0010 Encode | 53.3 min |
| T0011 Decode | open at the cap |

- T0525 holds: every case is concrete (EX-7 is 254 bytes in, 256 out, in
  full hex) and every bound became a property with a `prop-*.sh` test. accept.sh
  prints `ok`/`FAIL` lines; Encode's check was `contract run --operation
  encode` and it passed.
- Reconcile took 13 min (17.0–30.2). The contract named its reference by
  `cat references/…txt` with the file's text as output, the second named it by
  path, and spans were compared by ident: `contract check` reported all 22 of
  the second's entries as cited by no entry of the first. The worker matched
  cites by hand, added entries, tried to rewrite the second (refused), and the
  next worker switched the contract's source to the path form, which passed.
  T0526 (beagle contract-same-document 6ff1dd0): a file matches any source of
  the same lines, hashed in comparison form; two experiments are still told
  apart by command. On R90's two files: 22 problems to 0 (`diff` 26/22 to 0/0).
- The first Encode worker (31.7–42.6) hit q35's 16k output limit thinking the
  algorithm through, three replies running, and tau ended it with nothing
  written; the second wrote it in 10 min. The same spiral ended R89's driver.
- T0005, the goal's first milestone, was titled "T0001: Build contract …": the
  driver's seeding repeated the contract stage as a milestone. Refused an
  abandon (a milestone is the goal's), it split it into encode, decode and
  tests, which worked, at a minute's cost.
- Open: the output-limit spiral (q35 max_tokens 16384 in the krang catalog;
  B05 ran under the same limit), and a repeat of R90 on T0526.

## R91 — q35 cobs: 5/44 at the cap; five encode workers, none closed it

Repeat of R90 on 6ff1dd0. The contract sealed at 20.6 min (R90: 30.3), 36
entries, all concrete; Reconcile took 3.9 min (R90: 13) and added 8 entries
the second extraction had and the first lacked. T0526 holds.

| Encode worker | Minutes | How it ended |
|---|---|---|
| dde44317 | 20.9–21.8 | tool calls written as text without `<tool_call>`, twice |
| 5befdf85 | 21.8–22.2 | the same |
| 8d863128 | 22.4–34.6 | two replies at the 16k output limit (5 min each), then the 900 s wall |
| 9e04ae2e | 34.6–41.8 | wrote encode/decode; IndexError, overhead bound failed |
| 4dea9856 | 42.8–56.8 | the 900 s wall, its last reply at the output limit |

At the cap ~/cobs/cobs/__init__.py was uncommitted, with no decode: 5/44.

- The cut-off replies were hand traces: 43k and 45k characters of reasoning
  stepping the C encoder byte by byte, and tracing EX-10 (255 bytes in) to
  decide whether the contract's expected output was right, without running
  either. At ~55 tokens/s a 16k reply takes 5 min, so two end a worker at its
  900 s wall. Plain tau's one session has no wall: B05 had two length stops
  and went on. R89 and R90 each lost a worker the same way; here it was two.
- The driver, refused the code, wrote "the correct COBS encoding algorithm"
  into the notes without having read the reference, and at 58 min "Do NOT do
  any reasoning or testing. Here is the exact code to write".
- Open: the worker wall against reasoning-length replies; the text-written
  tool calls (R37's class, unparsed by the server when the opening tag is
  missing).

## R92 — void: the tau checkout under the run changed at 18 min

The first run of T0527–T0529. At 08:29 another session checked
`upstream/tui-stream-cpu` out in ~/tautest/tau, which the harness's `tau` and
`~/.tau/extensions/beagle.py` both pointed into: every worker after that ran
without the beagle extension. Stopped at 08:46. Before then the contract
sealed at 30.6 min with 32 entries, and a contract worker wrote and ran code
rather than hand-tracing (T0529), but built a COBS implementation inside
`contract/accept.sh`. The two contract workers that ended on tool calls
written as text had hit the 30-turn cap first: the markup was their reply to
"no more tool calls", not the template failure R91 saw.

Runs now use a tau pinned for them: launch.sh puts `~/tautest/tau-harness` (a
detached worktree with its own venv) on PATH and sets
`TAU_HOME=~/.tau-harness`, whose `extensions/beagle.py` points into it and
whose other entries link to ~/.tau.

## R93 — q35 cobs: 0/44 at the cap; the contract task took 51 min

T0002 (Contract) ran from 0.2 to 52.5 min over four workers; T0003 (Second
extraction) took 3 min; Reconcile was mid-way at the cap. No code.

| Contract worker | Minutes | How it ended |
|---|---|---|
| 1d1b61b6 | 1.5–10.0 | 31-turn cap: 41 entries and accept.sh, 19 properties unnamed by it |
| 392cdfc0 | 10.0–27.8 | the 837 s wall, not counting a 318 s reply cut at the output limit |
| 33eca536 | 30.4–42.8 | 31-turn cap: wrote a JSON input/expect per property, then grepped beagle's binary for the rule |
| fc87b9e2 | 42.8–52.6 | added `"property": "<id>"` to each JSON file; draft check passed |

- What held the contract was one rule: `contract check` printed "no
  acceptance file names property X: a property has no input to replay, so a
  test must encode it, naming its id" once for each of 19 properties. Workers
  read "encode it" as the COBS operation and gave each property an input and
  expect, in the entry and then in `contract/prop-*.json` files named after
  the ids (`files = ["contract/"]`, so the JSON files were read, and they did
  not name the id in their text). Beagle 711abcb (branch
  property-acceptance-message) prints one problem listing the unnamed ids and
  the files it read, says the id goes in that file's text beside the test,
  and that a file named after the id or an input on the entry does not count.
- The check passed on a name, not a test: fc87b9e2 wrote each id into its
  JSON file, and accept.sh names none of the 19. A data file holding the id
  satisfied the rule; beagle e02f316 (same branch, T0530) counts an id only in
  an acceptance file that is not a JSON document.
- T0528 seen once: 392cdfc0's reply at the output limit (49.6k reasoning
  chars) was replayed, and the next reply acted, writing a Python COBS to
  compute expected outputs (T0529). Its wall left out the 318 s.
- No tool calls written as text, no loop cuts.
- The driver's own criterion `len(encode(b"a"*300)) <= 301` is wrong for COBS
  (300 non-zero bytes need two code bytes); nothing graded it here.

## R94 — q35 cobs: 13/44 at the cap; the contract sealed at 18.5 min

T0530 held: one contract worker (1.1–10.2 min) closed T0002 at 9.6 min, the
second extraction closed at 13.4 and Reconcile at 18.4, 39 entries (R93 never
sealed; R91 20.6 min; R90 30.3). T0005 closed on T0004's commit. Then T0006
(Core COBS encoding) was open from 19 min to the cap over four workers:

| Encode worker | Minutes | How it ended |
|---|---|---|
| cfcce259 | 20.1–32.0 | 31-turn cap (one reply at the output limit, 347 s, not counted against its wall) |
| 5505d769 | 32.1–41.0 | 31-turn cap: "install the cobs package in the Python that `contract run` uses" |
| 31a1381e | 42.4–57.3 | the 900 s wall, fixing decode |
| a2bd3074 | 57.8– | the cap |

- The acceptance hid its own failure. `contract/accept.sh` imports
  `from cobs import encode, decode` under `except ImportError:` and prints
  `FAIL <id>: cobs module not found` for every entry. The encode milestone ran
  before decode existed, so every entry failed with that line though
  `cobs/__init__.py` imported fine. The driver spent its eight bash calls on
  pip, uv, sys.path and grepping beagle for the message, and a worker reported
  the fix as installing the package. Two general fixes: the contract brief
  asks the acceptance to load each operation on its own and print the
  exception it caught; and `contract run` can say when every entry failed
  with one identical reason that the acceptance itself is failing, not the
  cases.
- At the cap: encode passes the grader's 11 Wikipedia cases; decode
  appends a zero after a 0xFF group and fails all 11. Acceptance 30 ok.
- Three acceptance properties ("output contains no zero byte") test the
  encoded frame with its delimiter, so a correct encoder fails them: the
  contract's delimiter convention and its properties disagree, and the seal
  did not catch it.
- Turn cap: 3 of 7 workers ended at it (R93: 3 of 6), the next worker
  re-reading the tree for 5–8 turns each time.

## R95 — q35 itc: 22/42 at the cap, the best contract-first itc yet

Best contract-first q35 itc so far (R83 18/42, R87 0/42; lean cases-first
R57 23/42; plain B04 0/42). Contract closed at 13.6 min, Second extraction at 18.6,
then Reconcile took 29 min: the contract sealed at 46.5 min, 201 entries.
The code was written in the last 8 min (11:46–11:53) by two workers on the
scaffolding and data-model tasks: ~/itc/src/itc/clock.py (529 lines),
uncommitted. Graded through its tree functions (split, event,
sum_id/join_event, leq, normalize_*): paper 7/7, norm 6/6, leq 5/5, join
4/4, trace-canon 0/10, trace-causal 0/10. The traces fail on join: event
trees come back with negative counters (`(3, 3, (-1, …))`), so `join_event`
lifts and sinks wrong on unequal bases.

- Reconcile (T0004): the first worker hit the 900 s wall mid-merge; the
  second found the check already passing, changed nothing and gave no
  witness, so prove could not refuse and the task stayed open; the driver
  spawned T0010 with a delta, which closed at 46.5 min. Beagle has a route
  for a check that passes before the work ("abandon: done by T000N"), but
  not for one that the previous, killed attempt made pass.
- The contract stage cost 46.5 of 60 min; coding got 13. 201 entries is
  ~5x cobs's.

## R96 — q35 wrenfold: 50/54 at the cap; the acceptance, not the code, held it

R71 was 0/54 on this prompt; plain B06 was 54/54 in 9.1 min. The contract
sealed at 14.5 min (Contract 6 min, Second extraction 2, Reconcile 5; 44
entries), the fastest seal yet. The encoder milestone (T0006) then had 45
min and never closed, though by +29 min its worker had written
~/wrenfold/wrenfold/encoder.py (191 lines, encode/decode/count) that grades
50/54 through `from wrenfold import ...`. It misses: encode([63]) drops
the end marker after `40 3f`; decode accepts input with no end marker
(empty, `05`, `01 02`).

Where the 45 min went, all on the sealed accept.sh:

- It loads the code by path, `spec_from_file_location("wrenfold",
  "wrenfold.py")`, while the founding criteria import `from wrenfold` and
  the driver scoped T0006 to `wrenfold/`. Workers 1-2 (+15 to +36 min)
  built the package and could not write the root `wrenfold.py` the
  acceptance reads; every entry failed `module 'wrenfold' has no attribute`.
  The driver then wrote the shim itself (+52 min); it was gone at the cap.
- Its test for `prop-marker-inside` (a property: "inside a two-, three- or
  five-byte form 0x3F is an ordinary byte") invents an input and a wrong
  answer: `decode(81 3f 00) == [319]`. `0x81` opens the three-byte form, so
  the spec gives 81664, which the code returns. Worker 3 spent its 900 s
  wall (+37 to +52 min) concluding "there might be an error in the
  contract. But the contract is sealed" — and there is no route for that.
- Three `invalid` entries (invalid-negative, invalid-oversize,
  inv-overflow) carry prose for input (`invalid syntax`, `name 'integer'
  is not defined` when accept.sh evals them): they can never pass,
  whatever the code does.

Run against the final code through a shim, accept.sh prints 33 ok and 7
FAIL: three prose inputs, prop-marker-inside twice (Reconcile left it in
twice), and the one real miss twice, `decode(05)` not raising.

- The fixes this calls for are beagle's, at seal: an acceptance that
  imports the code by name, as the goal does; a codeless run in which an
  entry that fails for any reason other than the missing code is named as
  the acceptance's own defect; and a recorded route for a worker to
  dispute a sealed entry's test against its cited source.

## B07 — plain q35 on the bare-goal semver prompt: 75/76 in 8.1 min

The control for the bare-goal rotation (criterion 8): one sentence, "implement
a modern python library for parsing, validating and comparing semantic
versions", no spec link. Plain tau (`--no-extensions`) ended on its own after
8.1 min with ~/semver/src/semver (a frozen SemVer dataclass, regex parse,
precedence by key, 102 tests of its own). Graded through an adapter over
`SemVer.parse`, its comparison operators and `from_parts`/`str`: 75/76. The
one miss: `parse("1.2.3\n")` is accepted (`re.match` with `$`, which matches
before a trailing newline).

What a bare-goal pursuit run must beat: 75/76 in 8 min, on a problem the
model already knows. There are no sources to read, so the contract stage
has nothing to cite but what the driver saves; the runs say whether beagle
still pays its way when the spec is the model's own memory.

## R97 — q35 semver, bare goal: 58/76 at the cap; a sealed acceptance that could not fail

The first bare-goal pursuit run (criterion 8). The driver founded from the
one-line prompt, saved semver.org's 2.0.0 page itself into contract/, and
sealed a 134-entry contract at 31.6 min (Contract 11 min, Second extraction
7.4, Reconcile 11). Scaffolding took 11 min, and the Core Version class worker
was still open at the cap. Graded through an adapter over `Version(s)`, its
`<` and `str`: 58/76. The misses are 15 precedence cases (prerelease
identifiers compare equal), one build case, and two inputs with surrounding
whitespace (`Version` strips them).

Time went to:

1. **An acceptance that passes whatever the code does.** accept.sh prints
   `ok` for every `property` and `operation` entry unconditionally ("tested
   by hand" is a comment), and checks examples only for not raising, passing each input
   whole to `Version(...)`: 12 of 35 examples expect `valid`, and the other
   23 are comparisons such as `1.0.0 < 2.0.0` → `less`, which no comparison
   ever reached (T0549). Precedence, the spec's own example chain
   included, is a property, so nothing ever asked the code to compare two
   versions. Sealing let it through: without code every entry fails to
   import, one shared load reason, so T0541's outlier test sees no outlier
   and T0536's codeless test sees no pass.
2. **Reconcile copied the second extraction in whole.** 56 of the 134
   entries came from contract.second.json with `operation` set to the
   entry's own id (`semver-100` … `semver-155`), 13 statements duplicate
   another's. The milestone check is `contract run`, whose acceptance
   imports each operation as a module, so the T0006 worker wrote a meta-path
   finder that makes `semver-NNN` importable and a `Version(s)` that
   evaluates `"1.0.0 < 2.0.0"`. Both are code shaped to the acceptance, not
   to the goal.
3. **Scaffolding dispatched twice.** The first worker passed the
   file-existence check in 1.2 min; a second worker on the same task, with
   the work already done, spent 9.5 min, twice hitting the output limit,
   deciding what WITNESS a scaffold could have. The extension sent it
   because its prove gave up on the first worker's mutation, which the
   file-existence check passed, before trying the removal of the new
   files (T0550 fixed that).
4. **The contract stage on a known problem.** 31.6 min before any code,
   against B07's 8.1 min for the whole job. The owner's bar is problems
   above ~100k tokens, which semver is not; the bare-goal runs are here to
   show beagle still works without a spec, and R97 shows it found and cited
   one by itself.

Fixes filed under T0531: the contract check refuses an operation that is
its own entry's id and a statement that duplicates another; sealing must
show each entry's test can fail once the code loads; and why a
task whose check passed was dispatched again is read before it is fixed.


## S01 — q35 semver smoke of the incremental contract: code at 14.0 min, 12 findings

A 1500 s smoke (T0562), not a numbered trial. Founding at 1.3 min seeded one
`Slice: examples` ahead of five milestones, as built. The slice sealed 17
entries as `contract/slices/01-examples` at 10.9 min, and the first code
commit came at 14.0 min, against R97's 31.6 and the design's 6-7. The cap
fell inside the version-parsing milestone, so nothing was graded.

Where the 9.6 min of the slice went: its worker could not save the spec
(references/ is outside the slice's contract/ scope) and was refused
`contract --help`, so it wrote `contract.json` by hand; `contract status`
then said ready while the slice's check refused, the worker ran out of
turns, and the slice was dispatched a second time.

What sealed and should not have: `accept.sh` reads the input's `expect` for
the comparison entries (a KeyError) and compares an order with itself, and
the stand-in "failed" those entries too. Its root path is right only in
`contract/draft`. The seal was not committed, so the workspace gate went red
and the driver's repair was refused three times. Milestones were checked by
pytest, not `contract run --operation`. The run's python came from
tau-harness's venv.

Fixes filed as T0567-T0575 (source saving, read-only verbs, status vs
check, acceptance root, committed seal, a crashing test under the stand-in,
milestones on `contract run`, the venv on PATH, `run --operation` noise).

## R98 — q35 wrenfold on the incremental contract: 54/54 in 49.9 min

The first full run of the incremental contract after the S01 fixes, and
the first full score on wrenfold under beagle (R96 50/54 capped, R71
0/54). It ended by itself, every file committed. Plain tau (B06) also
scores 54/54, in 9.1 min, so on this task the contract bought
reliability plain tau already had, at 5.5 times the time.

Timeline (worker sessions, minutes from launch):

| From | To | What |
|---|---|---|
| 0.0 | 1.9 | founding |
| 1.9 | 4.7 | `Slice: examples`: 8 encode examples, accept.sh, standin/, oracle/; sealed at 4.8 |
| 4.7 | 10.5 | driver planning (5.8 min, no worker) |
| 10.5 | 17.2 | codec.py (first code commit 22:09, 17.6 min) |
| 17.6 | 28.2 | tests, encoder validation, decoder rejection |
| 28.2 | 34.4 | driver (6.2 min; a duplicate coverage slice T0013 filed and abandoned) |
| 34.4 | 49.0 | `Slice: coverage`: 12 entries, 29/29 normative lines cited or excluded |

What went right: the slice worker saved the spec and sealed in under 3
minutes, with the right-answer stand-in written first time (T0572,
T0581); the acceptance root, committed seal and source saving held
(T0567-T0571).

What it shows:
- The examples slice is no longer the cost. Coverage is (14.6 min, 29%
  of the run), then driver time between workers (12 min, 24%).
- No limits-and-invalid slice was planned. The validation and rejection
  milestones closed on `contract run --operation encode` and the
  worker's own pytest, with nothing sealed for decode until coverage
  (T0517's read: the gate checks "any sealed entry", not "a sealed limit
  or invalid entry"). The code was right anyway; the contract only caught
  up at the end. -> T0582, T0583.
- First code at 10.5 min (worker start) / 17.6 min (commit), against
  S01's 14.0 and R97's 31.6.

## R99 — q35 semver, the last contract-mode run: 75/76, uncommitted

The last run on the contract-first lineage before beagle 0.48 retired the
contract verbs (beagle reported itself as 0.47.0 at 009c2b8; no 0.47 was
released). Capped at 3600 s (exit 124). Founding and the examples slice
(T0002, the only slice sealed) took about 53 of the 60 minutes; the code
was written after that and never committed: `src/` is untracked in
~/semver.

Graded 75/76 through runs/R99/adapter.py, which wraps the run's
`Version.parse` (prerelease and build split on ".", format from `repr`),
the same score as plain tau (B07, 75/76 in 8.1 min) and up from R97's
58/76. The code is right; the mode spent the hour before it.

This closes the contract era's runs. The port to beagle 0.48 (task-level
spec-tying, no contract) is dev-notes/beagle-0.48/plan.md, and its runs
start at R100.


## S02 — q35 wrenfold smoke on beagle 0.48: 0/54, a check the spec contradicts

The first live run of the port (tau beagle-0.48 fb3823e5, beagle 0.48.0).
Capped at 1500 s (exit 124) with T0002, Encoder, open and no code written.

**The spec-tied path ran end to end.** Founding planned Encoder, Decoder,
Validation and Tests. The driver gave Encoder the source
`references/wrenfold-r3.txt`, and the cases worker wrote 13 marked cases.
`open --dry-run` and the real `open --cites --cases` accepted them, and the
cases were committed (183beb0, 14.4 min). The code worker started at 14.5 min.

**What sank it: the driver wrote the expected values.** T0002's done_when was
a `python3 -c` with ten `assert encode([…]) == bytes([…])` lines the driver
computed in its head. Six are wrong against the spec. For example, 63 is
`40 3F` plus the end marker (spec lines 33–35), but the driver asserted
`bytes([64, 63])`, and it put 64 in the three-byte form. Then:

- The cases worker cited the right spec lines but copied the done_when's
  values. 0.48 accepted the ties, because `open` checks that each cite is
  there, not what the case asserts.
- The check never ran the case files, although rule 2e says "the check runs
  the cases through the project's own test command". `open` doesn't enforce
  that.
- Each worker hit the 16,384-token output limit in one turn, reconciling the
  spec with the check. The cases worker took 30k chars of thinking, about
  4.6 min; the code worker took 39k chars, about 4.7 min, ending on "But the
  acceptance criteria says bytes([64, 63])".

**Time:**

- 0–4.1 min: the driver's first turn (160 output tokens on a 12.5k prompt).
  This is most likely krang loading the model; the workers' first turns took
  under a minute on the same size of prompt.
- 4.5 min: founded.
- 5.6–14.4 min: the cases worker, 4.6 min of it in the length-stopped turn.
- 14.5–25 min: the code worker, which had written nothing at the cap.

Graded 0/54 through runs/S02/adapter.py (`No module named 'wrenfold'`).

**Fixes before R100:**

- Tau (T0609): `pursuit_step` refuses a done_when for a task with a source
  unless it runs a test file. The refusal and the next-task prompt say to use
  the project's test command over the case file, with no expected values in
  it: the cases are read from the source.
- Upstream ask 9: `open --cites --cases` should refuse a check that does not
  run the case files.

## R100 — q35 wrenfold on beagle 0.48: green at 14.6 min, then 21 min of bookkeeping

Stopped at 35.6 min (exit 143) when runs went to a 30 min cap. Graded 54/54 on the untracked
`wrenfold.py` (runs/R100/snap, adapter.py). Only the T0002 code worker ever wrote it.

| min | what |
|---|---|
| 0–1.3 | founding: 4 milestones (Encoder, Decoder, Count, Tests), the spec as source |
| 1.5 | T0609 fired: the driver's `python3 -c` asserts were refused; 0.4 min later it sent `pytest -q test_wrenfold.py` |
| 2.0–7.3 | cases worker, T0002: 13 cases, 3 of them with expected bytes it worked out for inputs the spec gives no example of, all 3 wrong (63, 16384, 4194304) |
| 7.3–15.3 | code worker, T0002: 5.6 min (one 16k length stop) to its one write of the whole module (encode, decode, count) at 12.9; it corrected the 3 wrong cases in test_wrenfold.py at 14.1; 17/17 at 14.6 |
| 15.3 | prove refused: the bound check file changed since open. T0002 stays open |
| 15.6–16.5 | the driver re-sent its old `python3 -c` check as a new route (T0006, refused by T0609), abandoned T0006 as a duplicate, then found T0002 superseded and tried to abandon the root |
| 17.3–35.3 | two cases workers for T0003 (Decoder) over the same file: `open` refused the first ("op=encode has no invalid or limit case") at 20.4; the second spent 14.6 min, 42k output tokens, on markers |

What it shows:

1. **The spec-tied path can win the first 15 min.** Code that passes every hidden test at
   14.6 min, against B06's 9.1 min for plain tau. The rest was ceremony after the work was done.
2. **The cases worker computes bytes no better than the driver.** S02's failure moved one step:
   every case that quoted a spec example was right, and every case it worked out itself was wrong.
3. **A correct fix to a case has no channel.** The code worker was right to fix the cases, but
   editing the bound check makes the task unprovable, and the driver could not recover it.
4. **Milestones per function multiply the cases ceremony.** One module, one spec: the code
   worker wrote all three functions at once, and the Decoder/Count milestones then had nothing to do
   but write cases for code that already passed.

From R100 on, runs cap at 30 min, and launch.sh copies the project each minute it changes to
runs/RNN/snaps/tMM; `curve.py RNN` grades every snapshot and gives time-to-green.

## S03 — q35 wrenfold smoke on fix 1: the markers, not the cases, cost the run

Capped at 30 min (exit 124) with T0002 never opened and no module written: 0/54. Fix 1 (T0611)
held: this time the cases asserted the form a bound gives (`len(encode_single(16384)) == 3`), not
bytes worked out. What failed was the marker line around them.

| min | what |
|---|---|
| 0–2.0 | setup and founding: 5 per-function milestones, the spec as source |
| 2.3–5.0 | cases worker 1, T0002: 17 sound cases, every marker `# beagle-case: wrenfold-r3:25#019 kind=… op=…` (the cite where the case's name goes); it also tried to write `wrenfold/`, reading the dry run's `--scope` as its own. Tau found no tied marker and opened nothing |
| 5.5–24.9 | cases worker 2, T0002: a 16k-token turn (50k chars of thinking) and a 15.7k-char one; the dry run said "no cite=", it moved to `beagle-case: cite=…`, the dry run said "no id"; killed at the 900 s wall |
| 26.6–30 | a third round of cases, cut by the cap |

What it shows:

1. **Rule 2e's marker example doesn't say what its first word is.** q35 read `fork-seed` in
   `# beagle-case: fork-seed cite=itc2008:367#95b` as part of the cite, and the "no id" refusal
   didn't tell it otherwise. Beagle-side ask: say the first word is the case's own name.
2. **Malformed but sound markers cost a whole round.** Tau can name them mechanically; beagle
   still checks every tie.

Fixes before S04: T0612 (a corrected pinned case is amended when it quotes its cited lines, else
put back), T0613 (unnamed markers are named before ties are read), T0614 (the cases brief gives
the marker's fields with the source's ref, and says the dry run's `--scope` is the code's).

## S04 — q35 wrenfold smoke on T0611–T0614: tied on the first try, then two 16k-token turns

Capped at 30 min (exit 124): 45/54 on the untracked package `wrenfold/` (runs/S04/snap). The curve
(curve.py) is 0/54 until t23, then 45/54. The 9 misses are two defects: 63 written in the one-byte
form (0x3F is the end marker), and decode/count accept input with no end marker. Both have failing
cases in S04's own test file, so the code worker was on them when the cap hit.

| min | what |
|---|---|
| 0–2.2 | setup and founding: 4 milestones (integer encoding, sequence encoding, decoder, count) |
| 2.2–12.9 | cases worker, T0002: one 16k-token turn cut at the output limit; 30 cases with markers beagle read on the first try (`# beagle-case: zero-is-one-byte cite=wrenfold-r3:52#397 kind=example op=encode`); it stubbed `wrenfold` (first a conftest.py, then a try/except in the case file) because the file would not import before the code existed |
| 12.9 | T0002 opened tied, cases committed |
| 12.9–30 | code worker: a 16k-token first turn of bit layouts by hand ("15 zeros + 23 bits = 38"), wrong; one `python3 -c` then settled it; module written by t23; its `uv run -- pytest` saw the stub, not its code, until it set PYTHONPATH |

What it shows:

1. **T0613/T0614 worked**: the markers tied on the first try, against S03's whole run lost to them.
2. **The 16k-token turn is now the biggest cost**: about 8 min in each worker, 16 of the 30 min. In
   the code worker it was arithmetic a single run settles. R100's code worker had the same turn.
3. **A cases worker stubs what will not import** unless told the import failure is the one expected.

Fix before S05: T0616 (both worker briefs: work arithmetic and expected outputs out by running them;
the cases brief: the import failure is expected, do not stub the code).

## S05 — q35 wrenfold smoke on T0616: a sourced scaffolding milestone eats the run

Capped at 30 min, 0/54: `wrenfold/` holds only `__init__.py`. The founding (7.6 min) made four
milestones: Project scaffolding, Encoder and Decoder, each with the spec as its source, then Tests.
T0609 refused the scaffolding step's import-only check twice, so the driver named
`tests/test_scaffold.py`. A cases worker spent 10.8 min looking in the spec for pyproject.toml, uv
and ruff, then tied "the module exists" to the spec's title line and "it is a package" to its scope
sentence. Beagle accepted both: an anchor is checked for being valid, not for bearing on the case.
T0002 closed done at 25.5 min, and the encoder never opened.

What it shows:

1. **A layout-only part has nothing to cite and nothing but an import to check.** S04's founding
   had no such part. Its code worker made the package within the encoder task.
2. **No length stop in either worker** (largest turns 9.8k and 2.6k tokens), against two 16k stops
   in S04. T0616's note is the only change, but these tasks were trivial, so this is weak evidence.
3. **No stub**: the scaffolding cases import `wrenfold` plainly.

Fix before S06: T0617. Founding folds a layout-only milestone into the next part's intent, ahead
of that part's `Source:`. The design fold had the same latent bug of writing after the source. The
setup refusal now says to name the package layout in the first part's intent.

## S06 — q35 wrenfold smoke on T0617: right code at 20 min, held open by one wrong case

Capped at 30 min. The code graded 49/54 from the 20-min snapshot to the cap; the 5 misses are 3
malformed inputs and 2 `count` cases, a later milestone. The founding took 5.5 min and made three
sourced milestones, with T0617 folding the scaffolding into Encoder. A cases worker opened T0002
tied at 17.2 min. On the way it had one 16k length stop (about 11 min of decode), checking the
spec's worked examples by hand, so T0616's note did not prevent it.

The cases pinned `encode([63]) == b"\x40\x3f"`. The spec gives 63's two-byte form, but `encode`
also appends the 0x3F end marker. The code worker corrected the case three times, at 22.8, 25.4
and 27.5 min, and each correction was put back:

1. It wrote `CASE test_sixty_three_two_byte: …`, naming the test function. The case's id is
   `sixty-three-two-byte`.
2. Then it named the right id but added commentary after the quote, and the whole tail was
   checked as the quote.
3. Neither form could have passed. The cite named line 35, `0x40 0x3F.`, which ends a sentence
   begun on line 33, and the quote was that sentence.

After three steps the step guidance offered a split, and the driver split Encoder into scaffold,
impl and tests. That throws away a task whose code already worked.

Grading note: a code worker ran `pip install --break-system-packages -e .` so that its check,
`python3 -m pytest`, could import from `src/`. That put `~/wrenfold/src` on every python3's path
through the user site and shadowed each snapshot, so every minute graded 49/54. The install was
removed, and `curve.py` now grades with `PYTHONNOUSERSITE=1`.

What it shows:

1. **The pinned-case correction path is the bottleneck once the code is right.** The code was done
   about 3 min into the code worker's run. Everything after was the correction ritual failing on
   form, not substance.
2. **The cases worker's values still come from reading, not running.** No code exists yet, and the
   spec's worked example gives a form, not the full output.
3. **Time to T0002 is still 12–17 min** (S04 12.9, S06 17.2), against plain tau's whole run of 9.1.

Fixes before S07:

- **T0618:** a worker turn that reasons for 240 s without acting is cut and asked to act; its
  reasoning is kept.
- **T0619:** a CASE line counts by the test's name, keeps only its first quoted span, and is
  checked against the cited lines' paragraph (up to 4 lines either side).

## R104 — round 1, q35 wrenfold: the first closed tasks, at one milestone in six

Capped at 30 min, 12/54. All 12 encode cases pass; decoding was never written. The founding took
1.7 min and made six milestones: integer encoding, sequence encoding, integer decoding, sequence
decoding, error handling, tests. T0002 closed done at 18.5 min, the first close of the smokes, and
T0003 closed at 21.3 min. The T0004 cases worker ran from 21.6 to 28.6 min.

- **T0618 fired once and worked.** The T0002 cases worker's turn was cut at 241 s (38.7k
  reasoning chars) and the next turn wrote the case file. Without the cut it would have run to
  the 16k limit, about 4 more minutes.
- **What that turn was weighing:** a contradiction in the cases brief. T0616's shared note said to
  work out expected outputs by running them, and T0611 said to assert no output you work out. The
  worker had run a reference encoder to get the limit values, then went back and forth on whether
  it could assert them.
- **T0619 had no case correction to handle.** The cases were right.
- **Cost per milestone:** the cases worker takes 2–11.5 min and the code worker 1–5 min. Six
  milestones at that cost don't fit in 30 min, and plain tau writes the whole thing in 9.1.

Fix before round 2: T0620. The cases brief now has its own note: check arithmetic by running it,
but expected values still come from the cited lines. Next to look at is milestone granularity:
"error handling" and "tests" as their own milestones, and integer versus sequence as separate
milestones.

## R105 — round 2, g26 semver: a setup milestone and an unfetched source

This was gemma4-26b's first pursuit. Its tool calls parsed cleanly, it thinks briefly (most turns
under 2k chars), and it had one length stop in the driver. The run scored 0/76 at the cap, because
no semver code was written.

- **Founding** made 'Environment setup:: uv, ruff, pytest' the first milestone, T0002. T0617's
  layout fold missed it: 'environment' was in neither word list.
  - A worker did the setup under `grep -q ruff pyproject.toml`, but no defect could be put back, so
    the task stayed open.
  - The driver then went 13 min through `ls`, `exit 1`, `test -f non_existent_file`, `grep` on a
    missing line, and new routes. Every one was refused, correctly.
  - It closed at 18.5 min under a `tests/test_non_existent.py` that reads pyproject.toml.
- **T0003** came with `Source: https://semver.org/`, but no reference was on disk.
  - The cases worker searched the empty `references/` for 5 min; its `refs fetch` was blocked by
    the worker guard.
  - The driver fetched the page only after that worker's report.
  - The second cases worker cited correctly, apart from one stale anchor, and was writing cases
    when the cap came.

Fix before round 3: T0621 (fix 10). Founding folds an environment, tooling or dependency milestone
into the first work. Queued as fix 11, after a round that doesn't need it: a URL source is fetched
by the host before the cases worker runs.

## R106 — round 3, lfm24 itc: the task id slot

This was lfm2.5-24b's first pursuit. It reasons at length (up to 16k chars a turn), and its tool
calls parsed until the breaker. The `<function=` text-call bug (llama.cpp #30490) never showed:
tau's breaker stopped the run at the 8th refusal in a row, about where the bug reportedly starts.

- **Founding** was sound: three tasks, with both reference URLs named.
- **First step:** it asked for an assert-less `python3 -c` check, and was refused, correctly.
- **The task id slot:** twice it sent a correct step (criteria, done_when `python3 -m pytest -q
  tests/test_itc.py`, scope, notes) with T0002's description in `task`. Tau answered "is not a
  task to work now ... Call pursuit_step with no arguments", which threw the good fields away.
- **What followed:**
  - `task: ""` calls without criteria;
  - a `pursuit_dispatch`, refused;
  - writes to `src/itc.py` from the driver, refused;
  - the same refused heredoc six times.
  The breaker then ended the run at 11 min, with exit 0, no worker run, and 0/42.

Fixes before round 4. This is two patches, each from its own run, in unrelated code:
- **T0623 (fix 12):** with one task workable and `task` not a task id, that task is the one meant.
  The description joins the notes, and the reply says so.
- **T0622 (fix 11, from R105):** a URL source is fetched by the host before the cases worker runs.
  An unfetchable one refuses the step, with beagle's reason.

## R107 — round 4, q35 cobs: the first pursuit to close every task

Every task closed and the run ended on its own at 27.8 min, scoring 37/44.

- **Timeline:**
  - founding took 2 min;
  - T0002's code worker ran from 21:07, with two 240 s reasoning cuts (T0618), each followed by a
    concrete step;
  - T0002 committed and closed at 23.6 min;
  - T0003–T0006 closed in the next 4 min on the driver's `python3 -c` and `ruff` checks, against
    code T0002 had already written.
- **Why the 7 failures:**
  - Founding fetched the Wikipedia link only after the milestones were split.
  - The `source` guidance asked for "a file in references/", which was empty at that moment, so
    q35 named no source.
  - With no source, no cases worker ran, and the driver set every expected value itself. One of
    them was a wrong criterion: "Empty input encodes to a single zero byte" (the spec says `01 00`).
  - That left empty encode and all five malformed-decode cases failing.
  - The code was 37/44 from its first snapshot.

Fix before round 5: **T0624 (fix 13)**. The milestone guidance and the `source` description now
also offer "a link in the user's request"; T0622 fetches it before the cases worker runs.

## R108 — round 5, g26 wrenfold: a tests-only scope met a known-answers-era route

Gemma named the URL as T0002's source, and the source was fetched; its title was "Wrenfold encoding
specification". The driver read T0002 as "write the tests" and scoped it to
`tests/test_wrenfold_spec.py` alone.

1. **First cases worker (6 min).** Its cases imported `wrenfold`, so `scope_refusal` sent the
   driver down the known-answers-era data-test route: "check runs the data test only
   (`tests/test_case_data.py`)".
2. **Second cases worker (10 min).** It ran on that check and wrote good cases (right cites,
   committed at 17.5 min). The cases still imported `wrenfold`.
3. **Code worker.** Refused `wrenfold.py` as out of scope, it rewrote the tests and stripped the
   import from the cases file. A third worker was still running at the cap: 0/54.

Fix before round 6: **T0625 (fix 14).** Once a source task's cases are written, a module they
import that no path in scope creates is added to the scope as `<m>.py` and `<m>/` (under `src/`
when the project has one), and the reply says so. The task opens with its cases and goes to the
code worker. The data-test route stays for tasks without a source.

## R109 — round 6, lfm24 semver: right lines, one anchor for all

The founding (22:19:05) went well. Then lfm24 made six `pursuit_plan` calls in a row, all refused:
first it split T0002 into parts that carried T0002's own title, then into parts labelled "T0002".
After that it stepped T0002 itself, with the fetched `semver.org` as its source.

1. **Three cases workers ran, finishing at 22:31, 22:36 and 22:46.** Each wrote sound cases in
   `tests/test_parse.py`, and every marker cited the right line numbers (146, 149, 177, 188, 206,
   403). But every marker used the same anchor, `#0b7`, which is line 136's anchor.
2. **Each open was refused** with "cite 'semver.org:146#0b7': #0b7 is line 136's anchor: cite
   136#0b7 if line 136 is the one meant, or 146#d11 for line 146". The route handed the refusal
   back to the next cases worker, and each worker left the anchors the same.
3. lfm24 also tried `pursuit_dispatch` (refused) and an edit of `.beagle` (blocked). The `<function=`
   text bug was still not seen.

The run reached the cap with only the founding commit: 0/76.

Fix before round 7: **T0626 (fix 15).** After a cases worker, each case cite whose anchor is not
its line's is given that line's anchor by `beagle refs show <ref> --from N --to N`. The fix is
made in the case files and in the open's `--cites`, and the step's reply names the change. A
worker points at a line; a three-hex anchor that happens to match another line is chance. On
R109's own test file, all six cites re-anchor correctly (146#d11, 149#ef3, 177#a09, 188#474,
206#70f, 403#a65).

## R110 — round 7, q35 itc: the paper's words were there, beside the CASE line

This is the first itc score since the port: 17/42 at the cap. `leq` was never written, and the
event-tree join was left un-normalised. The founding happened at 22:57. T0002, "Core ITC data
structure", with the paper as its source, opened tied at 23:07, 11 min in. It was the run's only
task.

1. **The cases worker wrote 21 cases. Beagle's open dry run asked for an invalid, limit or gap
   case for create, fork and join.** The worker added three `kind=gap` cases assuming that a null
   id is refused. The paper says otherwise: `split(0) = (0, 0)` (line 366) and `sum(0, i) = i`
   (line 386). They also contradict the worker's own `fork-split-zero` case, so no code could
   pass all 24.
2. **Code worker 1 (23:14) and the fix-up worker (23:16)** found the contradiction and rewrote
   the three tests. Each quoted the paper in backticks on the line naming the test:
   `i ::= 0 | 1 | (i1, i2)`, `split(0) = (0, 0)`, `sum(0, i) = i`. But each `CASE` line held the
   case's own docstring, so tau put the tests back both times.
3. **The driver then read the put-back as a verdict that the tests were right.** Its third worker
   (23:24) made the code refuse null ids, which broke `fork-split-zero`. The run reached the cap
   with 22 of 24 cases green.

Fix before round 8: **T0627 (fix 16).** When a pinned case is changed, its source words can come
from the `CASE` line, or from a quoted span on a report line that names the case or its test.
Spacing around brackets and commas is ignored, so the paper's `(i1 , i2 )` matches a worker's
`(i1, i2)`. A `kind=gap` case claims the source is silent, so source words anywhere in
references/ refute it. Other kinds keep to their cited paragraph. Replayed on R110's real
report, all three corrections are accepted.

An upstream lead: beagle's demand for a malformed-input case per op pushed the worker into
inventing refusals the source contradicts.

## R111 — round 8, g26 cobs: three time cuts in a row, no action

The run ended at the cap with 3/44: `decode` was missing and `encode` was a placeholder. The
three passing checks hold for any output (empty input, no zero byte, overhead bound). The
founding happened at 23:36, and the cases worker ran from 23:37 to 23:51. It wrote 15 cases,
and the task opened tied at 23:51, 15 min in.

1. **Code worker 1 (23:51 to 00:04) never made a tool call.** Each of its three turns reasoned
   for 240 s, about 29k characters each, tracing COBS frames byte by byte. Each was cut at the
   reasoning budget and nudged. After the bound of two nudges in a row, the worker's run ended
   with nothing written: 13 min gone.
2. **A second worker started at 00:05 and wrote a placeholder `cobs.py`** just before the cap.
3. **Across all sessions, the reply to a time cut's nudge acts or doesn't, by model.** Qwen
   acted on 6 of 6. Gemma acted on 4 and was cut again on 4.

I probed the cut worker's own prompt on krang (max_tokens 7000):

- **Replayed reasoning makes no difference to gemma.** Its chat template drops a
  reasoning-only assistant turn, so the prompts with and without the replayed reasoning render
  byte-identical (22,066 characters). So the nudge's "Your reasoning so far is kept above" is
  not true there.
- **On that one prompt, gemma acted in 5 of 10 samples.** Each acting reply came within 23 s:
  `ls cobs.py`, a test run, or writing `cobs.py`. The other 5 reasoned to the limit (129 to
  142 s).
- **Showing the reasoning's last 3,000 characters as visible text did worse.** Gemma acted in
  1 of 6.
- **`tool_choice: "required"` did not help.** The reply still reasoned to the limit with no
  call.

Fix before round 9: **T0628 (fix 17), in tau core.** A reply that will act does so early, so
retries are cheap if they are short. The reply to a time cut's nudge gets a quarter of the turn
budget (60 s of 240), and time cuts allow four nudges in a row instead of two. Worst case is
240 + 4 × 60 = 480 s, against 720 s before. At gemma's 1-in-2 rate, four tries all failing is
about 1 in 16. The prompt is the same, so there is no prefix-cache cost. Other length stops keep
the bound of two.

Still open: the nudge text claims the reasoning is kept, which is false on gemma's template.

## R112 — round 9, lfm24 wrenfold: a missing scope, found after the worker

The run ended at the cap with 0/54 and no code: T0002 ("Integer encoding") never opened. The
founding happened at 00:45. Lfm wrote no `<function=` text this run.

1. **The driver's first call put its own asserts in done_when** (`python3 -c "... assert
   encode_int(0) == b'\x00' ..."`). It was refused at 00:46, as designed. Three calls then
   left out the criteria and were refused (00:47).
2. **Cases worker 1 ran from 00:47 to 00:59.** It wrote markers without `cite=`, then was cut
   off three times at the output limit (one reasoning-time cut, two output-limit stops).
   The step refused: no marker of the cited form.
3. **The driver's next call (01:00:25) had criteria but no scope.** Cases worker 2 ran for 6
   min. It wrote 12 cited cases and corrected one cite. Only then did the step refuse: "no
   scope given". The scope check came after the cases worker.
4. **The call with scope (01:06:22) started cases worker 3.** It found worker 2's file and
   rewrote it, tried twice to write `wrenfold/__init__.py` outside its scope, and was still
   going at the cap.

Fix before round 10: **T0629 (fix 18).** A spec-tied step with no scope, and no predecessor
scope to carry, is refused "no scope given" before its cases worker runs. In R112 that would
have saved worker 2's 6 min, and worker 3 would not have been needed.

Still open: the driver's slow recovery from refusals (four calls before it sent criteria and a
plain test command), and the first worker's three cut-offs.

## R113 — round 10, q35 semver: plain's score in half plain's time

This is the first round-robin run to beat plain tau's bar. It scored 75/76 by the 4-minute
snapshot; plain q35 (B07) took 8.1 min. The earlier pursuit semver runs were R97 (58/76 at the
60-min cap) and R99 (75/76 at the cap). The only miss is the same one B07 had: `1.2.3\n` is
accepted, because the regex ends on `$` rather than `\Z`.

The founding happened at 01:23:33. T0002 ("Version parsing") closed at 01:26, 4 min in, with
`parse_version` and a `Version` that has total ordering. The rest added no score:

- **T0003 ("Validation"), 3 min.** It was refused six times between 01:26 and 01:29:
  - two checks with no assert;
  - one whose asserts were in a list comprehension;
  - two with a `try:` on one line (SyntaxError);
  - one that already passed.
  The driver then closed it as done by T0002, with the check that already passed.
- **T0004 to T0006, 01:29 to 01:38.** These were comparison operators, `bump_version`, and a
  114-test suite. They added no score, but the run ended on its own at 16 min.

The source-less path held up: T0002 was not spec-tied (bare goal), so no cases worker ran.

No fix this round. The refusals were right, and the time after 4 min went to what the goal's
own criteria asked for.

## R114 — round 11, g26 itc: a wrong scope found after the worker, and skipped dry runs

The run ended at the cap with 0/42 and no code. Only `tests/test_itc_properties.py` was ever
written. The founding happened at 01:40.

1. **The founding's first task was a reading task.** T0002 was "Examine practical implementation
   patterns and ID subdivision from ferd.ca/…". Its intent glued two sources together
   (`…interval-tree-clocks.txt; Analyze the algorithm…::Source: references/itc2008.txt`). A later
   `pursuit_plan` that tried the same split was refused as reading-only. The founding was not.
2. **The first spec-tied call (01:41:43) scoped `references`.** Its cases worker ran until
   01:46:59. Only then did the step refuse: "scope names references … ignored by git". Fix 18
   had moved only the no-scope check ahead of the worker. This is the same class of waste.
3. **Two cases workers (01:47 to 01:51, 01:52 to 01:57) were refused at the open.** The open
   wanted an invalid or limit case for each op (initial_id, fork, join; then split, sum, join).
   Each brief names `beagle pursuit open … --dry-run`, but none of the four workers ran it.
4. **The fourth cases worker was still running at the cap.**

Fix before round 12: **T0630 (fix 19).** It widens T0629: a scope refused on its own is refused
before the cases worker. That covers no scope, `references/`, and `.beagle/`. The 10-15 audit
of T0629 found its predecessor-scope clause untested, so T0630 pins that too.

The audit also replaced T0605 (it named runs R101 to R103, which were never run) with T0631, a
before/after table after the round robin. T0632 holds the untested clauses it found in T0616,
T0617, T0624 and T0625.

Next candidate: the cases worker's dry run is in its brief, and gemma skips it. The host could
run the dry run itself when the worker ends, and hand a refusal back to the same worker. Its
context, and prefix cache, still holds the source.

## R115 — round 12, lfm24 cobs: a cases worker refused after it ended

The run ended at the cap with 0/44. Only `tests/test_cobs.py` was written, and no `cobs.py`.

1. **Founding, 02:21.** The first `pursuit_plan` named the goal's statement as its task and
   was refused. The driver then took T0002 from `pursuit_step`.
2. **Two refusals for `2>/dev/null`.** That is a bare '>' and the refusal is right. The driver
   sent the same `done_when` again after the second refusal (02:41:32).
3. **The first cases worker ran from 02:21:56 to 02:34:24.** It wrote the cases, then wrote
   `cobs.py` (outside its scope), and ended without the `open --dry-run` its brief names. The
   host's open then refused the cases: one marker read `kind=encode` with no op or cite, and
   encode had no invalid or limit case. All 12.5 minutes went back to the driver as one
   refusal.
4. **The driver spent 02:35 to 02:40 on a 4.8 min turn cut at the output limit.** It then tried
   to write `cobs.py` itself and was blocked.
5. **The second cases worker started at 02:41:43.** It ran the dry run itself three times and
   was still mending at the cap.

Fix before round 13: **T0633 (fix 20).** When a cases worker ends, tau runs the open's dry run
on its cases. A refusal over the cases resumes that same worker session (`tau -p --session`)
with the refusal, at most twice and with a 5 min wall each. The source is already in that
worker's context, and in its prefix cache. The real open runs only after a dry run passes.
R114 (two refusals at the open) and R115 are the same class.

## R116 — round 13, q35 wrenfold: green at 21 min, one witness borrowed

The run graded 54/54 at the t21 snapshot and held it to the cap. That beats R98's 49.9 min. Plain
tau took 9.1 min.

1. **Founding at 03:07, with two blocked writes and one refused plan.** The driver tried to write
   `pyproject.toml`, and its "project setup" part was refused. It put the setup in T0002's notes.
2. **T0002 (encoder), 03:08:14 to 03:18:51.**
   - The cases worker ran its own dry run twice. The host's dry run (fix 20) passed, so nothing
     was mended.
   - The first code worker's encoder was right, but the check `python -m pytest` could not
     import `wrenfold` from `src/`. A second worker added `tests/conftest.py`, which took 1.6
     min.
3. **T0003 (decoder), 03:19:41 to 03:32:04.**
   - The first code worker's code was right, but it named T0002's witness (an encoder line)
     with a new replacement. The decoder's check does not catch that line, so the witness
     survived.
   - A second worker ran for 5 min and was stopped once for reasoning without acting.
   - The WITNESS block reached T0003's brief through T0002's close body, which beagle shows
     under "Established by the finished tasks this one waits on".
4. **The `workspace-clean` gate was red from T0002 on**, because `uv.lock` was untracked. The
   driver added T0006 for it. That is noise, not a failure.

Fix before round 14: **T0634 (fix 21).** A done close's body leaves out the WITNESS block;
`prove` has already recorded it.

## R117 — round 14, g26 semver: 75/76 at 14 min, 10 min spent on a witness

The run reached 75/76 at the t14 snapshot and stayed there. The miss is `invalid_trailing_newline`:
`re.match` with `$` accepts `"1.2.3\n"`. R113's q35 run missed the same case. The spec says
nothing about it, and no case covered it.

1. **Founding, 03:43 to 03:46.** The driver's `uv init` was blocked. It then sent four
   `done_when` checks that only test whether a file exists, and the tool refused each one.
2. **T0002 (parsing), 03:46:05 to 04:06:40.**
   - The cases worker ran from 03:46:07 to 03:52:47.
   - The code worker started at 03:52:51 and its check passed at 03:56:51; its code already
     graded 75/76.
   - It then spent almost 10 minutes on the WITNESS:
     - 1.5 min shell-quoting a regex needle for `grep`;
     - a 125 s turn of reasoning;
     - a 240 s turn cut by the worker reasoning budget. That turn rewrote the final report again
       and again, re-checking the 4-line, 280-char regex needle byte by byte, then looped on
       "Final, final, … check: I'm done." 69 times.
   - The nudged reply reported in 13 s, and `prove` passed on the first try.
   - The reasoning-loop guard missed it: distinct lines never fell below 30 of 64, because the
     filler lines were interleaved with varied re-checks. A rule that fires when one line
     dominates the window would have fired only at line 502 of 552, and on 31,724 past turns
     it misfires on code fences.
3. **T0003 (comparison)** was opened at 04:07:29. Its first worker was still running at the cap.

Fix before round 15: **T0635 (fix 22).** When the check passes but `prove` refuses the witness,
the next attempt resumes the same worker session with the refusal, instead of starting a fresh
brief. The brief now asks for a NEEDLE that is part of one line, and says the host checks it and
asks again. A worker loses nothing by naming a short needle without checking it, and a refused
witness costs one turn rather than a new worker (R116 T0003: 5 min).

## R118 — round 15, lfm24 itc: 0/44, the run spent on a setup milestone

`pursuit_found` was called at 04:24:53 with three milestones:

- "Setup complete: beagle init written, pursuit founded with goal and criteria"
- "Core ITC implementation: …"
- "Pursuit structure: beagle pursuit file with milestones and acceptance criteria"

`_setup_milestone` reads only a title, and the first title is "Setup complete", so the milestone
survived. "Pursuit structure" was folded into the core milestone as layout.

The run then went like this:

1. **T0002 (the setup milestone).** Its `done_when` checks were refused: first one over
   `.beagle/`, then a scope that named `.beagle`.
2. **The driver tried to write the files itself.** It wrote `docs/setup-verification.md` and
   then a test for it, and both writes were blocked.
3. **A worker made the check pass, but nothing could be put back to prove it.** That worker ran
   from 04:25:37 to 04:28:27.
4. **The step escalated twice:** a new route, then another worker (04:29:30 to 04:38:40).
5. **The task was superseded by T0004 at 04:46:30,** and T0004 had the same setup check. T0003
   (the core) was never reached.

The `itc.py` on disk came from a T0002 worker. Its ITC class has an `(int, int)` id and a
counter, not the paper's trees, so none of the grader's operations map onto it.

Fix before round 16: **T0636 (fix 23).** A milestone is setup when its title holds a setup act,
other than a generic verb like create or start, and its text names beagle or the pursuit. Over
610 past founding milestones, the rule drops only R118's one more.

