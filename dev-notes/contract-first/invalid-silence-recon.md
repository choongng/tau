# Invalid input the sources leave unsaid (T0517)

R84 (cobs) graded 39/44 and lost exactly the five malformed-input cases. The
Wikipedia reference says nothing about malformed input, so the contract held
no invalid entry and no gap, and nothing asked the reader what the source
leaves unsaid (eval.md:212-216). This note reads whether the incremental
contract (T0554-T0560) now turns that silence into a gap or a question, and
what R98 (wrenfold, q35, live at the time of reading) did with invalid input.

Read against beagle contract-first 395d806
(`plugins/beagle-pursuit/tooling/beagle/src/beagle/contract.py`, cited as
contract.py) and tau choong-dev d7b110ad (`examples/extensions/beagle.py`,
cited as beagle.py).

## What the design promised

Step 4 of the design: "Before a milestone whose operation has no sealed
limit or invalid entry, the driver plans `Slice: <op> limits and invalid
inputs`" (incremental-contract.md:32-34). Coverage then closes the contract
over normative lines (incremental-contract.md:38-40).

## What the code enforces

1. **The limits slice is due only when an operation has no entry at all.**
   `operation_refusal` (contract.py:1973) collects the ops whose
   `judge(...)` returns a string (contract.py:1982). `judge` returns a
   string only when no sealed entry of any kind names the op: "no sealed
   slice holds an example, limit, invalid input or property"
   (contract.py:2573). One sealed example satisfies it. tau mirrors this:
   `_UNSEALED_OPERATION` matches only that refusal (beagle.py:2861-2863),
   `_slice_due` (beagle.py:2866) then plans `Slice: <op> limits and invalid
   inputs` (beagle.py:2873), and the driver's note says the slice is due for
   "an operation no sealed slice holds yet" (beagle.py:4986). The design's
   "no sealed limit or invalid entry" was implemented as "no entry".
2. **The limits slice asks only for what the sources state.** Its inventory
   is "every limit or boundary the sources state for {op}, and every input
   they call invalid for it" (contract.py:3429-3433). Where the sources say
   nothing, the slice is correctly empty of invalid entries, and no line
   tells the reader to record a gap. A gap exists as a shape
   (`{"id", "question", "answer" or "assumption"}`, contract.py:3518) and an
   unsettled one is refused (contract.py:1590-1596), but nothing requires
   one.
3. **Coverage cannot see silence.** `uncovered` (contract.py:1001) measures
   normative source lines no entry cites; `DoneGate.met` needs none
   uncovered (contract.py:2796-2799). A rule that is not in the source has
   no line, so an R84-style source passes coverage with zero invalid
   entries. Coverage does catch a stated rule left out (R96's revision-2
   line, incremental-contract.md:142-146), but only at the end.

So for R84's case the incremental contract is not covered: silence still
yields no invalid entry, no gap and no question.

## R98 (wrenfold): stated invalid input, never contracted

The wrenfold source states invalid input for both operations: an encoder
given a value outside 0..2^38-1 "must fail rather than write anything"
(references/wrenfold-r3.txt:16-17), and a decoder "must reject" input that
ends early, has bytes after the end marker, or is not in shortest form,
with four worked rejected inputs (references/wrenfold-r3.txt:68-79).

What R98 sealed (git log and contract/ only):

- One slice, `01-examples` (`.beagle/contract-seal.json` slices:
  `['01-examples']`), from T0002 (4953f26). It holds 8 entries, all
  `example` of `encode`; no `decode` entry, no limit, no invalid, no gap.
  The examples inventory excludes invalid inputs by design ("No limits,
  invalid inputs or properties", contract.py:3423-3427), so the four worked
  rejected inputs could not enter it.
- No `Slice: <op> limits and invalid inputs` was planned or sealed: the log
  has no such task, and the only later slice is `Slice: coverage` (T0012
  open, its duplicate T0013 abandoned at d59f466). The draft holds 1 encode
  example and 3 excluded items.
- `T0005: Encoder: validation` (6cd88fa) and `T0007: Decoder: rejection`
  (5f4347a) closed done with checks `beagle pursuit contract run --operation
  encode && python3 -m pytest -q tests/test_codec_*.py`. The decoder
  milestone ran `--operation encode` too, as did T0008 and T0009. Encode
  had sealed examples, so `operation_refusal` never fired, and `decode` was
  never named, so its absence was never seen. Both milestones were judged by
  the worker's own tests, not by the contract.

The observation is confirmed: both milestones closed done while only the
examples slice was sealed, and no limits/invalid slice was planned. Under
the design (incremental-contract.md:32-34) one was due before T0005; under
the code (contract.py:1982, contract.py:2573) none was required. Coverage
(T0012) would force lines 16-17 and 68-79 into entries or exclusions before
done, but after the milestones that build them have closed.

## Two holes, one per run

- R84 (silent source): nothing asks for a gap. Point 2 above.
- R98 (stated source): nothing makes the limits slice due once an example
  exists, and nothing checks that a milestone's `--operation` is the
  operation it builds. Point 1 above.

## Smallest change

beagle (contract.py):

1. `operation_refusal` also refuses an op with no sealed slice named
   `<op>-limits` in the seal's `slices` (written at contract.py:1792; tau
   names the slice `encode-limits` from the title, beagle.py:412). Keep the
   refusal's opening words "no sealed slice holds an entry of X, so
   `contract run --operation X`" or widen `_UNSEALED_OPERATION`
   (beagle.py:2861) to match, so tau's `_slice_due` plans the slice as now.
2. The `limits` inventory (contract.py:3429-3433) adds: where the sources
   say nothing of malformed or out-of-range input to {op}, add a gap whose
   question asks what {op} must do with it and whose assumption the work
   will make. The seal of a limits slice refuses one holding neither a
   limit/invalid entry of {op} nor a gap. The done gate already puts gap
   assumptions to the user (DoneGate.assumptions, contract.py:2753).

tau (beagle.py): the note at beagle.py:4986 says "an operation with no
sealed limits slice". Not in the smallest change, left for later: refusing
a milestone whose title names an operation (`Decoder: ...`) its check does
not run, R98's `--operation encode` on a decoder milestone.

Decision: build
