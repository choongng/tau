# Lift-12: twelve turns of q35 wrenfold on beagle 0.48 (T0610)

2026-10-14. These are q35 smokes on wrenfold with a 30-minute cap, starting from the port to beagle
0.48 (tau ecb438ea). A turn is one fix landed and proven, or one run made, graded and read; the
owner's rule was one patch, then one run. There were 13 turns. The bar is plain tau: B06 got
wrenfold to 54/54 in 9.1 min.

## Turns

| # | Turn | Result |
|---|------|--------|
| 1 | R100 run | 54/54 on the working tree, green at 14.6 min (reconstructed), but no task closed. The code worker corrected cases that read the spec wrong, and the changed pin refused the close. |
| 2 | Fix 1, T0611 | Cases assert only what their cited lines say. |
| 3 | Fix 2, T0612 | A code worker corrects a pinned case only with a `CASE <id>: "<source words>"` line. Tau then amends, or puts the case back. |
| 4 | S03 run | 0/54. Sound cases under markers beagle couldn't read: the cite sat where the name goes, then a `cite=` had no name. Nothing opened. |
| 5 | Fix 3, T0613 | Repair markers with the cite in the id slot. |
| 6 | Fix 4, T0614 | The cases brief spells out the marker and whose scope is whose; unnamed markers get a name. |
| 7 | S04 run | 45/54 at the cap, first code at 23 min. T0002 opened tied at 12.9 min, markers right first time. Two workers each lost about 11 min to a 16k length stop. |
| 8 | Fix 5, T0616 | Workers run arithmetic rather than reason it out; cases don't stub the code. |
| 9 | S05 run | 0/54. Founding made "Project scaffolding" a sourced milestone, whose cases were cited to the spec's title line. It ate the run. |
| 10 | Fix 6, T0617 | Founding folds a layout-only milestone into the first work, ahead of that part's `Source:`. |
| 11 | S06 run | Code at 49/54 by 20 min, never closed. One wrong pinned case was put back three times. One 16k stop in the cases worker. |
| 12 | Fix 7, T0618 | A worker turn reasoning more than 240 s without acting is cut. Its reasoning is kept, and it is asked to act. |
| 13 | Fix 8, T0619 | A CASE line counts by test name and by its first quoted span, checked against the cited paragraph. |

Score across the smokes: 0, 45, 0 and 49 of 54. None closed the goal. T0002 opened tied at 12.9 min
in S04 and 17.2 min in S06. In the two runs that reached code, the code was right within minutes
of a code worker starting.

## What we learned

1. **The format between workers and tau is where q35 runs fail.** The code is not the problem.
   S03 (markers), R100 and S06 (the case-correction line) and S02 (driver-written values) each
   failed on how a correct result was written down. The fixes that paid off made tau's reading
   lenient in ways that keep the meaning: repairing markers, matching ids, using the quoted span,
   checking the cited paragraph. Stricter briefs paid off less. *Read what a small model means;
   don't make it say it exactly.*

2. **Long reasoning turns are the main cost in time.** At about 25 tok/s, a 16k length stop costs
   about 11 min. In S04 and S06 the workers were working out bytes by hand. Of 355 worker turns,
   95% reasoned for at most about 2k tokens; the 8 longest went past about 5k, and 6 of those hit
   length stops. Asking in prose to "run it" (T0616) did not stop this, so T0618 caps reasoning
   time, which carries across models and decode rates. S07 tests it.

3. **Case values written before any code exists are the weakest link.** Spec examples give a form
   ("63 is 0x40 0x3F") rather than the full output (`encode([63])` adds the end marker). With no
   code there is nothing to run. Correcting a case from the source is the right valve, so it has
   to work on the first try (T0619).

4. **A founding needs every milestone to be checkable work.** Folding design-only and layout-only
   parts into the next real part (T0617) gave S06 a clean three-milestone tree.

5. **Beagle accepts anchors that have nothing to do with the case.** S05 cited the spec's title line
   for "the module exists", and `open --cases` took it. This is an upstream ask (see below).

6. **After repeated failure, the step guidance points to a split.** S06 split a task whose code
   already worked, over one pinned case. When the only red is a case that was put back, the route
   should be that case's correction, not a split. This is a candidate next fix.

7. **Harness hygiene.** A worker `pip install -e .`'d the project into the user site to satisfy
   `python3 -m pytest`, and that shadowed the graded snapshots. `curve.py` now runs with
   `PYTHONNOUSERSITE=1`.

## Where the time goes (S06)

- Founding: 5.5 min.
- Cases worker to tied open: 11.7 min, including one 16k stop.
- Code worker to right code: about 3 min.
- Correction loop until the cap: 10 min.

T0618 and T0619 target the second and the last. Without them, closing near 15 min looks possible.
Beating plain tau's 9.1 min also needs a faster cases step, for example running the cases worker
alongside the code worker, or a lighter cases brief.

## Next

- **S07:** q35 wrenfold on choong-dev 8f721639, with fixes 7 and 8. Watch for:
  - `reasoning_time_cut` diagnostics;
  - CASE amends being accepted;
  - time to T0002 tied, and time to the first closed task.
- **The rotation widens to more models** after the inference restart: gemma 26b and lfm 24b. Each
  fix must hold across them too.
- **Candidate fixes, one per run:**
  - make a case's correction the route when that case is the only red;
  - say in the cases brief that setup text in the task is for the code worker;
  - parallel cases and code workers.
- **Upstream asks for the beagle topic branch:**
  - `open --cases` should refuse a cite that doesn't bear on the case;
  - move validated asks 10 and 11 into rule 2e.
- **T0615:** the standing drift from the strip (T0335, T0360, T0386, T0496, T0508, T0526, T0529),
  which names deleted contract-era tests and a removed beagle worktree.
