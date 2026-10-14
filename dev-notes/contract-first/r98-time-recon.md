# R98: where 49.9 min went beyond the code

R98 (q35, wrenfold, 10-13 21:51:30-22:41:30 PDT) graded 54/54 in 49.9 min;
plain tau B06 graded 54/54 in 9.1 min. Source: driver session `352e9df6`
and six worker sessions in `~/.tau-harness/sessions/home-wrenfold-5b007e/`
(per-turn `timing.totalDurationMs`, tool-result timestamps), `~/wrenfold`
git log and `.beagle/tree`. Times are minutes from run start.

## Where the time went

- Model generation: 43.6 min (87%). The driver took 13.1 min over 126
  turns; six workers took 30.6 min over 167 turns.
- Beagle/tau overhead: about 3 min. Driver tool time outside workers was
  2.1 min. Dispatch and close around the six workers (check, prove, seal)
  added 0.9 min in all. Each close re-used a `pursuit prove` result ("not
  re-run") and cost 3-9 s; no standing sweep showed up as a cost.
- Workers' own tool execution: 0.4 min.
- Unattributed: 2.0 min of worker inter-turn latency, plus 0.8 min before
  the first model call (likely krang load, not beagle).
- The code itself took 15.5 min of worker time: T0010 codec 6.7, T0011
  tests 3.0, T0005 validation 1.2, T0007 rejection 4.6.

Time went to turns the model should not have needed, not to slow beagle
commands.

## Driver gap 4.7-10.5 (5.7 min): a duplicate examples milestone

- Founding (1.5) wrote a milestone T0003 "Slice: examples" next to the
  auto-inserted T0002 "Slice: examples". Both were created 04:53:41Z, with
  T0003 `after` T0002, and nothing flagged the duplicate.
- 48 turns, 4.9 min of generation (average 6.1 s, maximum 18.5 s), 22
  pursuit_step, 22 bash, 2 pursuit_plan, 1 edit. There were 21 refusals and
  6 blocked calls.
- 13 refusals gave the same reason: "`beagle pursuit contract check
  --draft` already passes, before any work". After T0002's seal the draft is
  empty, and an empty draft passes. The driver tried 13 done_when variants
  against a check that ignores done_when ("Slice: examples keeps its
  check").
- It also tried `abandon` (refused: "it is a milestone") and "done by
  T0002" (refused twice: no witness file). Bare `beagle pursuit
  close/open/bind/delete/retire` was blocked or invalid. An edit of
  `.beagle/tree/T0003.md` and `mkdir tests` were blocked.
- The exit at 9.95 was a pursuit_plan split of T0003 into T0010 codec and
  T0011 tests. That made T0003 a container: useful work under a misleading
  name.

## Driver gap 28.2-34.4 (6.0 min): late coverage, T0013, vacuous slice

- 28.3-29.5 (1.2 min): T0008 and T0009 closed "done by T0010". T0009 was
  first refused 3 times: done_when runs beagle, no `contract run`, already
  passes.
- 29.5-30.9 (1.4 min): the driver declared "All tasks done" and ran
  coverage, which found 8 of 29 normative lines. It began covering spans
  itself with `contract refs`. Its `contract add --slice` failed on
  argument parsing, and then the 8-calls-without-a-pursuit-tool limit
  blocked it.
- 30.9-31.0 (2 turns, about 10 s): pursuit_plan filed T0012 and T0013, both
  "Slice: coverage". The tool flagged T0013, and the driver abandoned it at
  once. **T0013 itself cost about 10 s.**
- 31.0-34.3 (3.3 min): T0012 was refused 7 times with the same vacuous
  "already passes" (the draft was empty again), and an `agent` call was
  blocked. The driver then added 3 exclusions and ex-009 by bash `contract
  add`; 2 adds were refused (no source, wrong anchor). The draft now failed
  ("no accept.sh"), and only that let T0012 open at 34.3.
- Window total: 49 turns, 5.1 min of generation, 13 refusals, 5 blocked
  calls.

## Smaller driver gaps (4.0 min)

- 0-1.9: 0.8 min before the first call, which had 13.9 s ttfo on a cold
  12.5k-token prefill. Then the spec read, `beagle init` and
  `pursuit_found`.
- 17.2-17.6, 20.7-21.8, 23.0-23.6 (2.1 min): T0004 and T0006 closed "done
  by T0010", each after a smoke test with `python3 -c`, and T0005 was opened
  after 2 refusals (a bare `>&`, no `contract run`). Founding planned 6
  milestones that one codec commit satisfied.
- 49.0-49.9 (0.9 min): final checks and the summary.

## Coverage slice T0012, 34.4-49.0 (14.6 min)

- 55 turns, 13.9 min of generation, 0.23 min of tools. Eight turns of 42-78
  s of thinking account for 7.0 min.
- **What it read:** the whole source twice (`contract refs --lines 1-89`),
  the draft, the sealed slice and its accept.sh, and `--help` three times.
  Two reads of codec.py were blocked (a slice reads sources, not code). It
  spent 5 more calls hunting for tilth in bash.
- **Contract add calls:** 26 calls, 18 items added, 3 items refused. ex-012
  and ex-013 used kind "excluded"; lim-001 was a limit with no
  input/expect. Most adds repeated the warning "draft has no accept.sh".
  ex-010, ex-011 and ex-016 were re-added to correct them.
- **Phase 1, 34.4-41.2 (6.8 min):** reaching 29 of 29 coverage, with 5
  coverage runs.
- **Phase 2, 41.2-49.0 (7.8 min):** making `check --draft` pass. Seven
  property entries each need a hand-written test in accept.sh. The worker
  wrote accept.sh 3 times and edited it twice, and wrote standin/ and
  oracle/ from scratch. It ran the check 8 times and accept.sh twice.
- Failures in order: properties unnamed, no stand-in, accept.sh reported 5
  of 12 entries, wrong expectations, wrong property asserts.

## Cuts, ranked by minutes saved

1. **A slice task opens on an empty draft: about 9 min (gap 1 at 5.7 and
   gap 2 at 3.3).** After a seal, `check --draft` passes vacuously, so
   every Slice open is refused as "already passes". That was 21 of the 38
   refusals in the run. Contract mode only, but it carries over directly to
   task-level spec-tying inside a standard pursuit.
2. **No unchanged repeat refusal: about 3 min, any pursuit.** After a
   second identical refusal, pursuit_step should return one working route.
   It should allow abandoning a milestone as "duplicate of Tnnnn", and
   founding should drop a milestone whose title matches an auto-inserted
   one (T0003). This overlaps cut 1 in gap 1.
3. **Generated runner and scaffolding: about 4 min, contract or
   spec-tying.** Seal could carry accept.sh, standin/ and oracle/ into the
   next draft, with accept.sh generated from contract.json so a worker
   writes only property bodies. The `contract add` refusal could show the
   shape of an exclusion.
4. **Close already-satisfied milestones together: about 2.5 min, any
   pursuit.** T0004, T0006, T0008 and T0009 closed "done by T0010" one at a
   time, after refusals. Founding fewer milestones (6 for one module) would
   also help.
5. **Plan coverage before "all done": about 1.4 min plus T0013, contract
   only.** This is moot under T0551, where done is coverage.
6. **Blocked driver hand-work: about 1.2 min, any pursuit.** 11 blocked
   calls cost one turn each, and the block text already names the route.

Decision: file (a) beagle+tau: open a Slice task on an empty draft, with no
vacuous "already passes" refusal (cut 1). (b) beagle pursuit_step: return
one working route after a repeated refusal; let a milestone be abandoned as
a duplicate; dedupe founding milestones against auto-inserted slices (cut
2, any pursuit). (c) beagle: seal carries accept.sh, standin/ and oracle/
forward, with a runner generated from contract.json (cut 3). (d) beagle
pursuit_step: batch "done by" closes for already-satisfied milestones (cut
4, any pursuit). Cuts 5 and 6 go to T0551 and are not filed.
