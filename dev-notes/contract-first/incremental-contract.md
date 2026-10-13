# Incremental contract: slices sealed just ahead of the work (T0552)

Design for T0551. Read 2026-10-13 against beagle rotation-fixes at aee1707
(`plugins/beagle-pursuit/tooling/beagle/src/beagle/`: contract.py,
pursuit.py, hooks.py; `commands/pursuit.md`) and tau choong-dev at cb041830
(`examples/extensions/beagle.py`, below beagle.py). In the working tree,
T0550 shifts beagle.py by two lines after line 11378. Read only: T0548 and
T0550 are editing both files.

Today, three sealed stages come before any code: Contract, Second
extraction and Reconcile (beagle.py:340-357, seeded ahead of the milestones
at beagle.py:4251). `open` refuses all other work until the seal
(contract.py:1532-1547). On q35 the seal took 14.5 min on wrenfold
(eval.md:573). On semver it took 31.6 min, and the run then reached 58/76
at the cap; plain tau scored 75/76 in 8.1 min (eval.md:613, eval.md:629).
The ethos says to add detail at the last responsible moment
(pursuit.md:58-63). This design keeps §1.5's lesson that runs which planned
from memory scored low (pursuit.md:339-345), by reading the examples first,
and drops the rest of the up-front stage.

## The flow

1. **Found** as today, plus `[contract] slices`; one contract task,
   `Slice: examples`, goes ahead of the milestones.
2. **Slice 1: worked examples only.** A fresh sub-agent adds every worked
   example, cited by anchor, via `contract add`, with the slice's
   acceptance and a stand-in; then it is sealed. No limits, no properties,
   no second read.
3. **Work opens** after the first seal. A milestone is checked with
   `contract run --operation <op>` over entries sealed so far, as tau
   already tells the driver (beagle.py:4975-4986).
4. **Later slices as the work reaches them.** Before a milestone whose
   operation has no sealed limit or invalid entry, the driver plans `Slice:
   <op> limits and invalid inputs`; properties where no example exists. A
   wait edge makes each slice seal before the task it gates.
5. **Re-reads only on evidence** (below): one section, a fresh reader, the
   result a slice.
6. **Coverage closes it.** `contract coverage` lists normative lines no
   entry cites; a last slice cites or excludes each. Done is that slice
   sealed and every live entry passing.

**A bare goal with no source.** The driver fetches a source with `beagle
refs fetch`; R97's driver saved semver.org by itself (eval.md:632). If
nothing can be fetched, slice 1 holds experiments, sources with a command
and output (contract.py:514-520), and gaps with assumptions
(contract.py:773-799). Coverage then has nothing to measure, and `status`
says so. It does not claim coverage is complete. The done gate puts the
assumptions to the user, as it already does (contract.py:2042).

**Floor cost.** On semver, R97's Contract task wrote its 78 own entries
(35 examples) in 11 min. Slice 1 is about 5 min plus 1-2 for stand-in and
seal: code starts at about 6-7 min, not 31.6. Second extraction and
Reconcile (18.4 min) are gone; invalid and precedence slices come later at
2-4 min each; coverage closes in 10 spans. About 13-15 min of contract in
all, still not B07's 8.1, as expected below the owner's ~100k-token bar.

Where the others would spend: **wrenfold** almost all in slice 1 (its
table is lines 46-64 of an 89-line spec), then re-reads at the traps R96
missed (63; a missing end marker). **cobs** at the example table, the
254-byte group limit and about 12 coverage spans. **itc** in coverage:
R95's 201 entries cite 24% of itc2008's normative lines, leaving about 46
spans, nearly all formal definitions, the same place its code fails. The
cost lands where the difficulty is.

## Slices and the seal

**Data.** `[contract] slices = "contract/slices"`, `draft =
"contract/draft"`. The open slice is written in `contract/draft/`, which
holds `contract.json` (this slice's entries, gaps and excluded items),
`accept.sh` (prints `ok <id>` or `FAIL <id>: why`, contract.py:1630) and
`standin/`. `contract seal --slice <name>` checks the draft and moves it to
`contract/slices/NN-<name>/`. It records each file's sha256 as `seal`
already does (contract.py:1411). `contract run` runs every sealed slice's
`accept.sh` from the root and concatenates the output. A draft never runs,
so code work goes on while a slice is written. A later slice may import
slice 1's loader but never edit it.

**Append-only, enforced mechanically.** A sealed slice's files never
change. `altered` already finds a changed sealed file
(contract.py:1373-1383), and the contract-guard hook refuses the edit
itself (hooks.py:1140-1160). What changes: a file under `draft/` is not
altered, and after a seal `contract add` writes to the draft, where today
it refuses (contract.py:1167-1170).

**The dispute route stays as built** (beagle c3999dc, tau 122d1231).
`dispute --brief` gives an independent judge the entry, its cite and the
acceptance lines (contract.py:2171), and `--record` keeps the verdict
(contract.py:2241). What changes: a `wrong` verdict retires the entry
instead of reopening its file, and the fix is a new id with `"supersedes":
"<old id>"` in the next slice. The seal refuses a `supersedes` whose target
has no `wrong` verdict. The done gate judges live entries by their verdict
lines (contract.py:1639), not the exit code (contract.py:1980-1982), so a
retired entry's FAIL does not count. Retired with it: re-sealing with a
reason (contract.py:1417-1422), tau's `_amend_reason` (beagle.py:12394) and
the altered branch of `_seal_when_ready` (beagle.py:431).

**What a slice seal checks**, over all slices plus the draft: the full
`check` (contract.py:932-1014), ids unique across slices; T0548's refusals
of an entry id used as an operation and of a duplicate statement
(contract.py:622-696); `codeless_refusal` on the draft's acceptance
(contract.py:1812-1848); the stand-ins (below); and every earlier slice
file still matching its recorded sha. A slice of only excluded items and
gaps runs no acceptance.

**How open and close gate on the slices so far.** `order_refusal`
(contract.py:1532) keys on the first slice: once it is sealed, code opens
(pursuit.py:3384-3387). New: `open` refuses a done_when of `contract run
--operation X` when `judge` (contract.py:1864) finds no sealed entry of X,
naming the slice to plan; this keeps each slice ahead of its work.
`drift_refusal` at close (pursuit.py:6316-6319) holds over sealed slices.

**The slice writer** is a fresh sub-agent scoped to `contract/` and
`references/`. In tau, the worker read guard (beside beagle.py:17802)
refuses it any other path the pursuit changed since founding. Beagle alone
(Claude Code) cannot tell a sub-agent's task, so there the brief asks it;
the stand-in rule makes reading the code no help in any case.

## Coverage: what done means

**The rule.** A non-blank source line is normative if it holds an RFC
2119 keyword in capitals; a code span (backticks or `<code>`); a table row
(`^\s*\|.*\|` or `x | y`); a formula (`::=`, `→`, `≤`, `≥`, `∧`, `∨`, `λ`,
` = `, `==`, `f(a, b)`); or a digit left once page numbers (`^\d+$`), `[12]`
citations, years and leading section numbers are stripped. HTML is read
as its text with tags stripped, outside head, script and style. The
owner's first cut (no formula test, raw digits) failed on the papers: 249
of the 251 itc2008 lines it marked were digit-only (page numbers,
references), and without digits it marked nothing in either itc source.

**Measured.** Span counts assume cites of at most 12 lines, the current
`MAX_CITE_LINES` (contract.py:119).

| Source | non-blank | normative | sealed contract cites | spans to close |
|---|---|---|---|---|
| semver-2.0.0.txt | 308 | 94 (31%) | (R97 cited the .html) | — |
| semver-2.0.0.html | 384 | 94 (24%) | R97: 76/94 (81%) | 10 |
| wrenfold-r3.txt | 56 | 29 (52%) | R96: 24/29 (83%) | 3 |
| Consistent_Overhead_Byte_Stuffing.txt | 166 | 68 (41%) | R94: 36/68 (53%) | 12 |
| itc2008.txt | 514 | 197 (38%) | R95: 48/197 (24%) | 36 |
| interval-tree-clocks.txt | 131 | 34 (26%) | R95: 10/34 (29%) | 10 |

Neither R96 nor R97 would have met the rule: neither has a single
`excluded` item. R97 cites every keyword, code and table line and misses
only version history and FAQ lines, all excludable. R96 misses lines 3-4,
"nothing written by revision 2 with that form is valid revision 3": a real
rule about invalid input, which coverage finds.

**Done.** `DoneGate.met` (contract.py:1980) also needs every normative line
covered. A line is covered by an entry's cite or by an `excluded` item with
a `why` (contract.py:801-817), computed by `uncovered`
(contract.py:820-822). `contract coverage` prints the uncovered lines
grouped into citable spans, so writing the last slice is mechanical.

## Stand-ins

This is T0549's option (a) (discriminate-recon.md:83-97,
discriminate-recon.md:154-167), applied to each slice. Each slice ships
`standin/`: the code with every answer wrong, in the slice's language,
loadable under the names the goal imports. At seal, beagle copies each
stand-in into the codeless scratch root (contract.py:1747-1767) and runs
that slice's acceptance. It refuses (1) a runnable entry that passes
under every stand-in, (2) an entry that fails for the load reason
(contract.py:1769), (3) an invalid entry that passes under any stand-in,
(4) a stand-in whose text names a contract file. Rule 1 catches an
untested property; the refusal offers `excluded` or a gap with an
assumption (discriminate-recon.md:142-150). A stand-in answers only the
slice's operations: 10-20 lines, under a second to run.

## Re-reads on evidence

No second extraction runs up front. A re-read covers one section (one
heading's span) and is done by a fresh sub-agent that has not seen the
contract. It writes a listing (ids, kinds, operations, cites), as the
second extraction does now (`is_listing`, contract.py:919). Beagle compares
the listing to the entries with `uncovered`, confined to that range. Any
line the listing cites and no entry does goes into the next slice.

A re-read is due only on **resistance** (one entry FAILs on 3
acceptance runs over distinct trees; today beagle keeps only the last run,
contract.py:1928-1960), on **an upheld dispute** (a `wrong` verdict,
contract.py:2241, puts the entry's cited section up), or on
**disagreement** (two live entries with one operation and one input but
different expects, which `check` refuses, naming both cites).
`contract status` prints `REREAD due: <source> <lines> (<trigger>)`. The
second extraction is retired as a stage: `second` (contract.py:141) and
`_second_problems` (contract.py:825-846). Its listing check is kept for
re-reads.

## What changes in beagle

- `ContractSettings` gains `slices` and `draft`. `load`, `judge`,
  `dispute_entry` and `brief_lines` (contract.py:2316) read entries merged
  across sealed slices and the draft. `add` writes to the draft.
- `seal --slice NAME`: the checks above, the move, per-file shas; `--reason`
  is retired in slice mode. `check` refuses an unearned `supersedes` and
  conflicting expects. `codeless_refusal` gains the stand-in run.
- New: the normative rule, `contract coverage`, an acceptance run history.
  `DoneGate.met` needs coverage and judges verdict lines.
- `order_refusal` keys on the first slice; `open` refuses an `--operation`
  check with no sealed entry.
- The brief gives each slice its kind's inventory (examples; one
  operation's limits and invalid inputs; properties; re-read; coverage), not
  INVENTORY's all-at-once list (contract.py:2267-2279).
- Legacy single-file pursuits (`path`, `second`, one seal) keep working,
  out of the docs.

## What changes in tau

- `CONTRACT_TABLE` (beagle.py:326-332) declares slices, no second;
  `CONTRACT_MILESTONES` (beagle.py:340-357) shrinks to `Slice: examples`;
  `CONTRACT_CRITERION` (beagle.py:334) adds "and covers its sources".
- `CONTRACT_STEPS` (beagle.py:360-367) becomes a rule for any `Slice:`
  title: scope `contract/`, check `contract check --draft`, applied whatever
  the driver passes (beagle.py:13454).
- `_seal_when_ready` (beagle.py:417) seals the draft as the slice its task
  names. `_settle_after_seal` (beagle.py:452-470), R85's Reconcile
  workaround, is retired.
- `_contract_verdict` (beagle.py:473) words coverage short, re-read due and
  retired entries. On beagle's `--operation X` refusal, the driver is told
  to plan `Slice: X limits and invalid inputs`.
- An upheld dispute (beagle.py:16148-16158, beagle.py:12443-12470) opens a
  superseding slice, not an amend; a due re-read becomes `Slice: reread
  <source> <lines>`.
- `CONTRACT_FIRST_NOTE` (beagle.py:19943) is rewritten. It is in the system
  prompt from load (beagle.py:20044), so it changes only between runs; new
  behaviour starts at each slice's sub-agent boundary, and the driver's
  tools do not change.

## Build tasks

In order, beagle first. Beagle's tests go in `tests/test_contract.py`,
tau's in tests/test_beagle_example_extension.py.

1. **beagle: slices, append-only seal, gating** (rotation-fixes). Data
   model, `add` to draft, `seal --slice`, merged reads, `supersedes`,
   first-slice `order_refusal`, the `--operation` open refusal; retires
   `seal --reason` in slice mode. Check: `test_seal_slice_moves_draft`,
   `test_sealed_slice_edit_altered`, `test_add_after_seal_writes_draft`,
   `test_supersedes_needs_wrong`, `test_open_refuses_unsealed_operation`,
   `test_duplicate_statement_across_slices`.
2. **beagle: stand-ins at the slice seal** (rotation-fixes). T0549 (a),
   rules 1-4. Check: `test_standin_pass_refused`,
   `test_standin_load_reason_refused`, `test_standin_invalid_pass_refused`,
   `test_standin_naming_contract_refused`, and an R97 fixture refused for
   its 34 examples and 15 properties.
3. **beagle: coverage and the done gate** (rotation-fixes). The rule,
   `contract coverage`, `met` with coverage and verdict lines. Check:
   `test_normative_rule_lines` (keyword, table row, formula, page number,
   `[12]`, year, `6. Changes`), `test_coverage_counts_excluded`,
   `test_done_gate_needs_coverage`, `test_retired_entry_fail_ignored`,
   `test_coverage_wrenfold_fixture` (29 of 56 lines).
4. **beagle: re-reads on evidence** (rotation-fixes). Acceptance history,
   the three triggers, the range-confined listing; retires `second` as a
   stage. Check: `test_reread_due_after_three_trees`,
   `test_reread_due_on_upheld_dispute`, `test_conflicting_expects_refused`,
   `test_reread_listing_outside_range_refused`.
5. **beagle docs: pursuit.md §1.5 and the brief** (rotation-fixes).
   Rewrite §1.5 (pursuit.md:339-430) as gather, examples slice, work,
   later slices, coverage; an ethos-table row (yield by sealing late, kept
   honest by append-only, stand-ins, coverage); a brief per slice kind.
   Check: `test_brief_slice_inventory_by_kind`, a grep that pursuit.md
   names no "Second extraction", the markdown format gate.
6. **tau: founding and step flow on slices** (choong-dev, after 1-5 land
   on contract-first). Table, milestones, steps, draft sealed as a slice,
   verdict wording, the plan-a-slice reply; retires `_settle_after_seal`,
   Second extraction and Reconcile. Check:
   `test_founding_seeds_examples_slice_only`,
   `test_slice_step_scope_and_check_fixed`,
   `test_close_seals_draft_as_slice`, `test_operation_refusal_offers_slice`.
7. **tau: slice-writer isolation, re-read and dispute routing**
   (choong-dev). The read guard, `REREAD due` as a slice, an upheld
   dispute as a superseding slice; retires the amend path. Check:
   `test_slice_worker_refused_code_read`, `test_reread_due_offers_slice`,
   `test_upheld_dispute_supersedes`.

Then R98, q35 on wrenfold, then semver, recording time to first code
beside R96 and R97 in eval.md.
