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

