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
