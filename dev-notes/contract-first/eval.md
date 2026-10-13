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

