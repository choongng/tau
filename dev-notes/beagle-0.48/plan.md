# Tau on beagle 0.48: retire the contract mode, carry task-level spec-tying

## Overview

Beagle 0.48.0 (`~/beagle` main 08e642c, 2026-10-14) ported the
recommendation "fold contract mode back into standard pursuit as task-level
spec-tying". It has no `contract` verbs. A task opts into spec-tying with
`pursuit open --cites/--cases`, and coverage is now a report. Tau's extension
still runs the incremental contract unconditionally, so tau cannot use the beagle
on PATH. This plan moves tau onto 0.48 in four steps: take the contract mode out
of the extension, carry the new verbs, and take tau's copies of beagle policy
back to `pursuit brief` and the verbs' `next:` lines. It then re-runs the
four-task q35 rotation as the before/after the owner asked for.

## Goals

- Tau's extension runs against unmodified beagle 0.48 (pinned, not a moving
  checkout), with no contract mode. A pursuit founded on a bare goal has no
  ceremony before the first milestone.
- A milestone built from a cited source can opt into spec-tying. The driver
  passes `--cites/--cases` and the worker writes `beagle-case:` cases first.
  Tau holds no copy of the rule text: it comes from `beagle pursuit brief` and
  the verbs' refusals and `next:` lines.
- The rotation re-run is q35, 60-min cap, one run each of wrenfold, semver
  (bare goal), itc and cobs. The bars come from the recommendation:
  - itc: at least 22/42, with more than 8 min of code time.
  - wrenfold, semver, cobs: the same score as plain tau, and wall time
    approaching plain tau's (B06 9.1, B07 8.1, B05 48.8 min).
  - Each run reports time to first code commit and its refusal count, split as
    in `r98-time-recon.md`.
- The extension shrinks. Contract-only code is deleted, not flagged off: the
  owner wants few modes.
- Constraints:
  - The prefix-cache rule: driver prompt and tool schemas fixed per session.
    Different behaviour goes behind a sub-agent boundary.
  - "Beagle decides, hosts carry".
  - Fixes must hold across models.
  - Never edit what a live run uses.

## Current State

- **Beagle.** 0.48.0 is installed (`~/.local/bin/beagle`). Its main is
  local-only ahead of GitHub. `urd` fetch fails with an access error this
  session. Relevant to tau:
  - `open --cites <ref>:<anchor> --cases <files>`, `beagle-case:` markers,
    `pursuit coverage <ref>`, `beagle refs show|find`. Find lines now read
    `references/x.txt:12#a1f: …`.
  - `stopped_at_open`: a check that never reached the work is told apart from
    the work failing. This is the import seam that sank R94, S01 and R99.
  - `open --reads`, `recheck --affected`, and `BEAGLE_CHECK_PHASE`.
  - `prove` is refused beside a live worker. `prove --isolated` proves in a
    copy.
  - Every verb ends on a `next: <command>` line, and `next --json` carries
    `"next"`.
  - `amend --scope/--check-timeout`.
  - `close --outcome abandoned --duplicate-of`, and the repeated-refusal route
    (both were T0588's ask).
- **Tau.**
  - `choong-dev` (e07caf80) is 168 commits ahead of `urd/choong-dev`.
    `examples/extensions/beagle.py` is 17,166 lines. Founding always emits
    `CONTRACT_FIRST_NOTE` and plans `Slice: examples`.
  - The harness runs from `~/tautest/tau-harness` (detached at f061aa4a) with
    `BEAGLE_ROOT=~/beagle-wt/contract-first`.
  - Workers still run `~/.local/bin/tau`, the editable dev checkout (T0593).
- **Last results** (q35, contract mode):
  - R95 itc 22/42 capped.
  - R96 wrenfold 50/54 capped.
  - R97 semver 58/76 capped.
  - R98 wrenfold 54/54 in 49.9 min.
  - R99 semver capped at 60 min with nothing committed. Its untracked
    `Version` class grades 75/76, B07's score, which plain tau committed in
    8.1 min. 53 min went to founding plus the examples slice.
- **Tree.**
  - T0588 is open, its scope `~/beagle-wt/rotation-fixes`. Its work shipped in
    0.48 (542049a, 5280959).
  - 13 tasks are ready.
  - Contract-only pending tasks: T0542/T0545 (dispute), T0590, T0591, T0595.
  - Containers whose leaves have all ended: 52, mostly the R01–R44 run
    containers.
  - The working tree has uncommitted `.beagle/` edits from opening T0588.

## Design

**Where this goes, and what it hides.**

- Beagle owns the rules and their text:
  - which cases a cited task needs (`pursuit rules 2e`);
  - the refusals at `open`;
  - the worker brief (`pursuit brief`);
  - the next move (`next:` / `next --json`).
- Tau's extension owns only what a host must carry: tools, dispatch, sub-agent
  roles and scopes, wakeups, and prompt pinning.
- A spec-tied milestone is one `pursuit_step`. The step:
  1. dispatches a **cases worker**: role `cases`, scope the test files, told to
     run `beagle pursuit rules 2e` and write cases for the milestone. Its stop
     condition is `beagle pursuit open <T> … --cites … --cases … --dry-run`
     passing.
  2. opens the task for real.
  3. dispatches the code worker with `beagle pursuit brief <T>`.
- The driver sees one step and one result. It never sees anchors, case kinds or
  the dry-run loop. Plain milestones, and every task on a bare goal, skip step 1
  entirely.

**The approach that lost.**

- *Cases as their own tree task.* The milestone would wait on a `cases: X` leaf.
  This is closest to how R98's slices worked. It lost on time: every extra task
  is a driver turn, and R98's recon put 12 min of its 49.9 in driver gaps.
  It also puts back the "nothing opens until the cases are sealed" ordering the
  owner just retired.
- *Revert the extension to its pre-contract state* (before T0478) and re-apply
  the mode-independent fixes. It lost on risk: about 160 commits sit on top,
  including the cut-off, wall, prove and witness fixes, and the 0.48 changes
  have to be carried either way.

**The interface.**

- The driver's `pursuit_plan` milestone entry gains one optional field:
  `source`, a reference name such as `itc2008`, or `itc2008` plus the topic
  words. The cases worker finds the anchors with `beagle refs find` and cites
  them. The extension takes `--cites` from the `cite=` of the markers the
  worker wrote (0.48 prints no accepted ties; upstream-asks.md 3), and the real
  `open` re-judges them.
- Anchors never pass through the driver, so a small driver cannot mistype them.
  This is the measured R94–R99 failure class, in a new place.
- The cost: coverage of the whole source moves from a gate to
  `pursuit coverage`, a report the driver reads when planning. That is what
  beagle 0.48 chose.

**What the next change touches.**

- The likeliest next change is another beagle refusal or rule for cited tasks.
  It touches beagle only: tau relays the refusal and the `next:` line. Today the
  same change touches both repos (T0581, T0582).
- The second likeliest is the cases worker's model or role. That touches one
  dispatch-role entry in `dispatch.toml`, from the 0.46 role/provider split.

**Errors defined away.**

- The import seam (R94, S01, R99): cases run through the project's own tests,
  and `stopped_at_open` tells "never reached the work" from "the work failed".
- Ceremony before code on a bare goal: no founding-time slice exists, so there
  is nothing to wait for.
- Tau/beagle drift in rule text: tau keeps no copy of the text.
- A worker seeing a prove's planted defect: `prove --isolated`.

## Changes Required

Line numbers are for `examples/extensions/beagle.py` at e07caf80. They come
from a scout's sift on 2026-10-14, so spot-check each region before deleting
it.

### 1. Delete the contract-only regions (about 990 lines)

| Lines | What |
|---|---|
| 314-387 | `CONTRACT_*` constants, `SLICE_PREFIX`, `CONTRACT_MILESTONES`, `CONTRACT_BUILD_MILESTONE`. Keep `REFERENCES_DIR`. |
| 394-587 | `_contract_declared`, `_contract_work`, `_slice_name`, `_contract_step`, `_slice_dirs`, `_seal_when_ready`, `_rereads_due`, `_contract_verdict`. Keep `_lean`. |
| 2859-2957 | Slice planning and the limits gate (`_plan_slice_call` … `_slice_due`) |
| 3298-3305 | `_reference_lines`. The anchors are now `beagle refs show`'s. |
| 4248-4273 | `_after_the_contract` |
| 4976-5156 | Check rules under a contract (`CONTRACT_CHECKS` … `_uncontracted_check_problem`) |
| 7555-7570 | `CONTRACT_WITNESS_NOTE` |
| 9238-9494 | Dispute and supersede of sealed entries (`_judge_dispute`, `_supersede_task`, …) |
| 13511-13586 | Contract read-verb allowlist. Its `refs` half is reshaped in §3. |
| 13780-13790, 14072-14096 | Slice worker guards (`_slice_refs_fetch`, `_code_read`) |
| 16530-16554 | `CONTRACT_FIRST_NOTE` |

### 2. Unpick the entangled branches (about 140 lines)

- **`make_found_tool`** (4313-4424): no `CONTRACT_CRITERION`, no
  `CONTRACT_TABLE` in the goal, no `CONTRACT_MILESTONES` prepended to the split,
  no `CONTRACT_FIRST_NOTE`. Founding goes back to what it was before
  T0478: the goal, criteria and milestones, plus the references fetch, which
  stays.
- **`make_step_tool`** (11705-13233): remove the contract branches at 11745,
  11785, 11858-11866, 12027, 12252, 12347, 12574, 12583, 12690, 12737-12752,
  12875-12882, 12920-12940 and 13189. Each is an `if contract…:` arm. The
  other arm stays.
- **Small call sites:**
  - `_repair_milestones` (7294-7309): a lone read or design milestone gets the
    pre-contract repair.
  - `_references_brief` (3246-3296): drop its `contract=` parameter.
  - `_check_problem` 5185-5191 and `_scope_problem` 5539-5540.
  - done-by 10380-10385, `_pursuit_write_verb` 13530-13537.
  - `NO_BEAGLE_NOTE`, the orientation guard 13854, the write-size hint 14224,
    `_free_reference_call` 14355, `_reread_refusal` 14400 and
    `_idle_bash_refusal` 14456.
  - `make_worker_scope_guard` 14559-14575.
- **Wording only:** `FOUND_PARAMETERS`, `FOUND_FIRST_NOTE`,
  `_unfounded_section`, `DRIVER_PROCEDURE` and the found tool's
  `prompt_guidelines`.
- **Tests:** delete the 37–39 contract tests and their helpers
  `_contract_project`, `_sealed_contract` and `_disputed_project`
  (19899-20458). Re-check that the founding tests assert the plain split, not
  the contract-seeded one.

### 3. The spec-tied step (new)

```python
# NEW, beside make_step_tool's open path. One step: cases, then open, then work.
def _open_spec_tied(task: str, source: str, criteria: str, check: str, root: Path) -> StepOutcome:
    cases = _dispatch(role="cases", scope=_test_paths(root), task=task,
                      prompt=f"Run `beagle pursuit rules 2e`. Write the cases for {task} "
                             f"from {source} in the project's tests. You are done when "
                             f"`beagle pursuit open {task} --criteria … --done-when … "
                             f"--cites <your cites> --cases <files> --dry-run` passes.")
    if not cases.ok:
        return StepOutcome.failed(cases.report)  # relayed to the driver as any worker failure
    cites, files = _marker_ties(cases.changed, root)  # cite= of each beagle-case: marker
    return _open(task, criteria, check, extra=["--cites", *cites, "--cases", *files])
```

- `cases` is a dispatch role, so `dispatch.toml` can give it its own model
  (0.46).
- Its scope is test files and `references/`. It never gets the source
  directory, which keeps "a worker that will not write the code".
- `_marker_ties` reads the `cite=` of each `beagle-case:` marker in the files
  the cases worker changed. 0.48's `open --dry-run` prints only the check's
  run, not the ties it accepted, `open` has no `--json`, and `coverage` counts
  done tasks only (probed 10-14). Reading the markers copies beagle's marker
  grammar into tau, so it is interim: upstream-asks.md 3 asks `open` to take
  the cites from the markers. The real open re-judges them either way, so a
  misread is a refusal, not a wrong tie.

### 4. `pursuit_plan` milestones take `source`

- The schema gains an optional string `source` per milestone. It is the
  prefix-cache-safe change: fixed for every session on this build.
- The founding note gains one sentence: name a `source` for a milestone whose
  behaviour a file in `references/` states.

### 5. Worker allowlist and guards

- Workers may run `beagle refs find|show`, `beagle pursuit rules [section]`,
  `beagle pursuit coverage <ref>` and `beagle pursuit open … --dry-run` (the
  cases role only).
- The read guard's "references/ re-read" counting moves from `contract refs` to
  `refs show`.

### 6. Adopt 0.48's outputs

- **`prove`:** pass `--isolated` whenever another dispatch is live. This
  replaces tau's own put-back logic from df30f428 where 0.48 covers it.
- **`_json_out`** (1539): it runs strict `json.loads` on output that includes
  stderr. A `next:` or notes line would empty a scope silently. Switch it to
  `_json_reply`'s first-`{` parse, and log a non-JSON remainder rather than
  dropping it.
- **Next moves:** where the extension writes its own "Next: …" for a beagle
  verb's outcome, relay the verb's `next:` line, mapped to the tool call that
  does it. Keep the extension's own "Next: pursuit_step" lines, which are about
  tau's tools, not beagle's verbs.

## Testing Plan

The extension's unit tests run against a fake `beagle` script
(`tests/test_beagle_example_extension.py:179`). That is why all 726 pass today
against 0.48, which has no `contract` verb. They cannot show that the
integration works, so this plan adds two more layers.

```bash
# 1. Unit: the extension's tests, with the contained beagle venv stripped
#    from PATH (T0550)
cd ~/tautest/tau
PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '/beagle/venv' | paste -sd:) \
  uv run python -m pytest -q tests/test_beagle_example_extension.py

# 2. Contract with the real CLI: a few tests that run the pinned 0.48 beagle
#    (not the fake) through found -> plan -> a spec-tied step's dry-run open ->
#    close, in a tmp git repo with a three-line reference. They are marked so
#    they can be run alone.
uv run python -m pytest -q -m real_beagle tests/test_beagle_example_extension.py

# 3. Live smoke on the harness: q35, a short cap, the run id S-prefixed.
cd ~/tautest/itc-harness && CAP_S=1500 ./launch.sh S02 q35 wrenfold
```

The rotation re-run (R100–R103) is the acceptance test. Grade each run with
`grade_<task>.py --adapter runs/RNN/adapter.py --json`. Each run gets an
`eval.md` row and section with time to first code commit, refusal count, and
the `r98-time-recon.md` split (model generation against overhead).

## Implementation Order

0. **Close out the contract era**, in tau's tree and the harness only:
   - Commit T0588's open record. Close T0588 abandoned: 0.48 shipped it
     (542049a, 5280959).
   - Close T0584 done with `Decision: replace`. The owner decided on
     2026-10-14 and 0.48 implements it.
   - Close T0542, T0545, T0590, T0591 and T0595 abandoned, as contract-only.
   - Settle the 52 containers whose leaves have all ended.
   - Record R99 in `eval.md`: 75/76 on untracked code, capped, no commit.
   - Do T0593: `launch.sh` sets `TAU_BIN` to the harness tau and records it.
   - Pin beagle: `git -C ~/beagle worktree add --detach ~/beagle-wt/0.48
     08e642c`, which becomes `launch.sh`'s default `BEAGLE_ROOT`. Record the
     rev in `meta.json` as now.
1. **Strip the contract mode** on branch `beagle-0.48` off `choong-dev`:
   - Delete contract-only code and its tests.
   - Unpick the entangled functions the scout listed.
   - The unit tests must stay green, and the extension must shrink by about
     the contract-only line count.
2. **Carry 0.48.** In order:
   1. The spec-tied step: cases worker, `--dry-run` loop, real open, code
      worker.
   2. The `source` field on `pursuit_plan` milestones.
   3. Worker read-only access to `beagle refs find|show`,
      `pursuit rules`, and `pursuit coverage`.
   4. `prove --isolated` whenever another worker is live.
   5. Relay of `next:` lines and `next --json`'s `"next"` in place of the
      extension's own "Next:" prose, where beagle's says the same thing.
   6. The real-beagle tests from layer 2.
3. **Hand policy text back (T0586, scoped).** List every instruction or rule
   text in the extension that 0.48's `brief`, `rules` or refusals now carry,
   and delete tau's copy. What beagle lacks becomes an upstream ask in
   `dev-notes/beagle-0.48/upstream-asks.md`, not a tau copy. The first ask: a brief for the
   cases worker before `open`, which `pursuit brief` refuses since the task is
   not open. A full decide/carry move of the extension's other policy waits
   for the rotation's evidence.
4. **Smoke S02** (q35 wrenfold, 25 min). Fix what sinks it, on the branch.
5. **Rotation R100–R103:** wrenfold, semver (bare goal), itc, cobs. Fix only
   what sinks a run, between runs, never in what a live run uses. Merge
   `beagle-0.48` into `choong-dev` (merge, not rebase) after S02, and move
   `tau-harness` to the merge.
6. **Judge** against the Goals' bars, and write the before/after table
   (plain B04–B07, contract R95–R99, 0.48 R100–R103) in `eval.md`. Report it
   to the owner.

## Files Modified

| File | Change |
|------|--------|
| `examples/extensions/beagle.py` | Contract mode deleted. Spec-tied step, `source` field, read allowlist, `prove --isolated`, `next:` relay |
| `tests/test_beagle_example_extension.py` | Contract tests deleted. Spec-tied step tests, `real_beagle` marked tests |
| `dev-notes/contract-first/eval.md` | R99, S02, R100–R103 rows and sections, before/after table |
| `dev-notes/beagle-0.48/plan.md` | This plan |
| `dev-notes/beagle-0.48/decide-carry.md` | New: Phase 3's list of what was handed back, and the asks |
| `~/tautest/itc-harness/launch.sh` | `TAU_BIN` (T0593), default `BEAGLE_ROOT` = `~/beagle-wt/0.48` |
| `.beagle/` (tau tree) | Phase 0 closes, the new tasks for Phases 1–6 |

## Definition of Done

- [ ] The extension has no reference to `contract` verbs, slices, seal, oracle
      or `CONTRACT_FIRST_NOTE`. `grep -c contract` reaches 0 or near it, each
      remaining hit explained.
- [ ] Unit tests and `real_beagle` tests pass against the pinned 0.48.
- [ ] Founding on a bare goal plans no task before the first milestone.
- [ ] S02 and R100–R103 graded, with rows and sections in `eval.md`.
- [ ] The before/after table is written and judged against each bar in Goals.
- [ ] `beagle-0.48` merged to `choong-dev`, and `tau-harness` moved to it.
- [x] Upstream asks filed in `dev-notes/beagle-0.48/upstream-asks.md` (3, 10-14).

## Open Questions

1. **Who picks the cites.** Proposed: the cases worker, from a `source` the
   driver names. The alternative is the driver passing anchors, which keeps
   `open`'s "every cite has a case" check meaningful. It also puts anchors
   through the model with the worst record on exact strings.
2. **When the extension uses spec-tying.** Proposed: only where the driver
   names a `source`, and the founding note says to name one when `references/`
   holds the task's source. The alternative is automatic when `references/`
   is non-empty, with no driver choice: simpler for small models, but it would
   tie a performance-grind task too.
3. **Beagle-side changes: settled with the owner on 2026-10-14.**
   - Beagle work starts from 0.48, with no rebase.
   - The old lineage is kept under `~/beagle` `refs/archive/*`, 52 commits on
     0.46:
     - the tip is `rotation-fixes-T0588-partial-2026-10-13` (5f76e43);
     - two side tips;
     - 126b4a7, a pursuit-run doc from 09-29.
   - 45 of the 52 are contract mode and stay unmerged. The 6 mode-independent
     ones and T0588 are already in 0.48.
   - New beagle changes go on topic branches off main 08e642c, for the owner to
     take upstream.
4. **One run per task or two.** The memory notes R56 42 vs R58 29 on repeats.
   One run each matches the recommendation's protocol. A second semver and
   cobs run would cost about 2 h of krang time.

## Out of Scope

- Moving the rest of the extension's policy into beagle (full T0586) beyond
  the text 0.48 already carries. It follows the rotation, on its evidence.
- Claude Code parity runs on the same four tasks. They are wanted, but are the
  next round.
- Upstreaming tau changes (`upstream/*` branches) and pushing `choong-dev`.
- The right-answer oracle (T0572). 0.48 left it out pending measurement.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Unit tests stay green while the real CLI disagrees, because they use a fake beagle | `real_beagle` tests against the pinned rev, and the S02 smoke, before any R-run |
| Beagle `main` moves under a run (another agent is working there) | Runs pin `~/beagle-wt/0.48` detached. A new beagle is an explicit re-pin, recorded in `meta.json` |
| The cases worker loops on `--dry-run` refusals | Cap its turns. 0.48 names a route after the second identical refusal. Its stop is relayed to the driver as an ordinary step failure |
| Spec-tying costs time on wrenfold, semver and cobs, as the contract did | No founding ceremony. Cited milestones only. Any stall before first code is a defect, per the recommendation |
| Deleting about 5k entangled lines drops a mode-independent fix | Delete by the scout's region map, and keep each entangled function's other half. Re-run the unit tests after each region |
| The `urd` remote is unreachable, so 0.48 is local-only | Pin by sha, not by remote branch |
