# Upstream (beagle) items from the ITC runs

Items for beagle itself, which is the user's to change. Tau-side fixes live
in the per-run notes.

## R01

- **`beagle pursuit brief` could resolve a task by its unique title
  prefix.** In R01 the 9B driver wrote "run `beagle pursuit brief Read the
  reference materials`" twice (driver session 5f19264c L21, L83). The verb
  takes only a `Tnnnn` id, so the worker got a usage error, or skipped the
  call. Resolving an unambiguous title prefix, or printing "did you mean
  T0002?" on a miss, would turn the brief's first command into a useful one.
  It is low priority: tau's pursuit_step writes the brief with the id.

## R02

- **`beagle pursuit brief` could omit its commit steps on request.** Every
  brief has "Before you report back, commit Tnnnn in the two steps below"
  (`pursuit claim` + `pursuit commit`). In tau the step tool commits on
  close, and workers are refused those verbs, so R02's workers spent about
  20 refused calls on them. They then ran raw `git add`/`git commit` and, once,
  a nested sub-agent for the claims (R02 W1 L52–56, W11 L35–41, W12 L20–27).
  A `--no-commit` flag (or a `[dispatch] commits = "host"` setting) that
  drops the section would let tau stop cutting it out by string match.
- **`prove` has no route for a data-only known-answers task.** A cases task
  whose scope is only `tests/cases.json` and `tests/test_cases.py` has no
  source file to take away. Its WITNESS must sit "never in a test file", so
  it can never close done (R02 T0003: six "no defect could be put back"
  results). Treating a declared data file (cases.json) as removable for
  prove, or a documented witness mode for locked known-answer files, would
  give the cases-first pattern a close. Low priority until tau binds that
  task itself.

## R04

- **`prove` has no route for a data-only known-answers task (R02 item,
  now the whole run).** R04's driver followed tau's cases-first recipe
  exactly (driver L10: scope tests/cases.json, tests/test_case_data.py,
  tests/test_cases.py). The check passed by t 6.6, and the task never
  closed in 59.5 min: no witness may sit in a test file, and there is no
  source file to take away. Proposal: a witness kind for a declared data
  file, `prove T --mutate-data tests/cases.json --needle … --replacement …`,
  where the check must fail when one expected value is changed. Or let
  `[close]` exempt tasks whose scope is all locked known-answer files.
  Priority: high, because it blocks the pattern tau recommends.
- **The needle refusal comes before the test-file refusal.** At L189 a
  WITNESS in tests/test_case_data.py was refused with "--needle occurs 2
  time(s)". The worker learned to lengthen the needle, not that a test file
  can never be a witness. Checking the path rule first would give the more
  useful message. Low priority, since tau will filter it.
- **`beagle pursuit list` does not exist** (driver L137). The model reached
  for it as an alias of `tree`/`status`. An alias, or "did you mean
  `pursuit tree`?", would save a turn. Low priority.
- Good: the container-abandon refusal (L143) named the live parts and what
  to do. Keep it.

## R05

- Nothing for beagle: the stall was in tau's `pursuit_found` wrapper, not in beagle's founding.

## R06

- **The `depend --hard` cycle check does not follow superseded tasks to
  their heirs.** In R06 (driver L72–73) `depend T0008 --hard T0003` was
  accepted. T0003 waited on T0002, which was superseded by T0008, so the
  edge closed a cycle. `Tree.reaches` (pursuit.py ~L1796) walks only
  `after`, but the scheduler (`dep_standing`/`_heir`) and `Order` resolve
  heirs. The very next `tree` printed "order: cycle via T0008", and the
  run deadlocked. Proposal: resolve `_heir` in `reaches`, the same way the
  scheduler does. `depend --help` already promises that hard edges "are
  checked for cycles". Priority: high.
- **`tree` flags the cycle but not the way out.** "order: cycle via T0008"
  could print the edges in the cycle and the command that drops one
  (`depend T0008 T0003 --drop --reason …`). The R06 driver tried
  retire, unretire, unbind and abandon, and never found `--drop`.
  Priority: medium.
- **The `open` refusal for criteria drift on a fresh successor does not
  say what to pass.** At L35, L53 and L69 a successor that never had
  criteria was refused three times: "criteria differ from those of T0002".
  The message could quote T0002's criteria and the exact
  `--criteria-delta` form, or a successor that has never been open could
  take the predecessor's criteria by default. Priority: medium.
- **The brief's "Working habits" line tells workers to run
  `beagle contain run`.** Hosts that keep workers off beagle (tau since
  T0041) then refuse it (W2 L49, W4 L41). A dispatch setting that leaves
  the habit out, or a way to mark it host-optional, would stop the brief
  contradicting its host. Priority: low.
- **`retire` on a pending task could point somewhere useful.** "only a
  done task's check can be retired" (L88, L115) could add "to remove a
  wait, use `depend … --drop`; to give up the task, close it abandoned".
  Priority: low.

## R07

Nothing for beagle. The run never reached beagle: tau's founding tool refused a milestone list that was only setup (tau T0054).

## R08

- **An abandoned part leaves its container stalled for good, and a wait
  on it never resolves.** At L88 and L98, T0013 and T0014 were abandoned
  as duplicates of their done sibling T0015, after their checks already
  passed. T0011 became stalled, and its own check passed (L101). But
  `_refuse_container_close` (pursuit.py ~L5816) never closes a container
  done, and `dep_standing` (~L1846) never satisfies a wait on a stalled
  heir. T0007 waited from 52.9 min to the end. Proposal: a container whose
  undone parts are all abandoned as duplicates of a done sibling may close
  done on its own check. Or `tree` prints, under a stalled container, the
  waits it blocks and the `depend W N --drop` command for each.
  Priority: high.
- **Closing a container abandoned does not release waits that reach it
  through a superseded predecessor's heir.** At L306, T0011 closed
  abandoned, and T0007 still "waits T0011 (for T0006)", because the edge
  is on T0006. Proposal: `close --outcome abandoned` lists those waiters,
  or drops them as it does for direct ones. Priority: medium.
- **The wait text shows the row status, not the subtree state.** For
  T0011, "handed to T0011: pending" was shown while `tree` drew "✗
  stalled" (L99, L107). Showing "stalled" in the heir's standing would
  have told the driver the wait is dead. Priority: low.
- **`beagle init` does not say its files need committing.** The
  workspace-clean gate was red from the first close (T0002) to the end
  of the run. `init` could print "commit .beagle/*.toml, memory-rubric.md
  and .gitignore", or the gate could ignore beagle's own config until
  the first commit. Priority: low.
- **`close --outcome abandoned` has no way to name the task that holds the work.** tau now refuses "duplicate of Tnnnn" abandons of a container's part (T0058), because beagle keeps an abandoned leaf with no successor as accountable and the container stalls for good. A `--duplicate-of T` that records T as the heir (as `spawn` does) would let a true duplicate be dropped without stalling its container. Priority: medium.

## R09

- **A part whose work a done sibling already holds cannot be closed.**
  T0007 was split into T0009 (move the code) and T0010 ("re-run the
  test and confirm"), and both had the same check. After T0009 closed
  done, T0010's check already passed before any work, so tau would not
  open it. Abandoning it as a duplicate would stall T0007 (see R08's
  `--duplicate-of`). With T0010 the only ready task, the run ended on the
  breaker. Proposal: `close T0010 --outcome done --covered-by T0009`
  records the part as done on T0009's witness when the bound checks are
  identical. Or `split`/`add --parent` refuses a child whose done_when
  equals a sibling's. Priority: medium. (The `--duplicate-of` proposal
  from R08 would also cover it.)
- **Splitting an open task leaves its uncommitted work to whichever
  child's scope covers it.** T0007 had written tests/cases.json and its
  test, uncommitted, when it became a container. T0009's `tests/` scope
  took them into the code commit, unlocked. Proposal: `split`/`add
  --parent` on an open leaf with changes in its scope lists them, and
  either commits them as the split task's WIP or names them on the first
  child. Priority: low. tau can list them too; R09.md has that as a tau
  Action.

Nothing else for beagle: the other R09 failures are in tau's texts,
guards and buffers, or in the model.

### Between R09 and R10 (driver)
- `beagle contain run` passes beagle's own venv (`UV_PROJECT_ENVIRONMENT`, `VIRTUAL_ENV`, PATH) into the job, so a project check that runs `uv run --no-sync` inside the container imports from beagle's venv and fails (`ModuleNotFoundError: tau_agent`). The T0078 worker hit it; it unset the variables to run the check. Suggest: the launcher strips beagle's own environment before exec.

## R10

- **`beagle init` writes another project's rulings as this one's, inside
  long essays.** The skills.toml it placed in ~/itc already declares
  ffi-bindings "not-applicable" because it is "pure Python, no native
  bindings anywhere in the tree". It declines repo-hygiene because "this
  one is thirty files at five commits", and both are stamped `ruled_at =
  2026-08-11`. The other templates run to 18.5 KB (gates.toml), 12 KB
  (cadences.toml) and 11 KB (track.toml), mostly measured-rationale
  comments. R10's 9B driver took them as config to finish. It spent 53
  calls and about 54 K chars of a 32K-token window reading and editing
  them (R10.md, Answer 3), until compaction. Proposal: `init` writes
  dispositions commented out, or with `status` left for the project to
  set (doctor already reports "no recorded disposition"), and puts the
  rationale in the skill docs, with a one-line pointer in each file. Or
  add an `init --terse` that a host bridge can ask for. Priority: medium.
- **`beagle pursuit next` names `beagle pursuit open` as the next
  command, even under a host that refuses that verb.** At E142 its "Next:
  beagle pursuit open T0002 --criteria '…' --done-when '…'" became the
  call the driver sent 11 times into tau's guard. Proposal: a
  `[run] next_hint` (or an env var a host bridge sets) that replaces the
  CLI line, e.g. "call pursuit_step". Priority: low. tau can also guard
  `next` (R10.md, fourth tau class).
- **`doctor`'s one FAIL sits mid-output, and the summary gives only a
  count.** "[FAIL] gates .beagle/gates.toml does not load" was line 35 of
  113. A host that keeps the tail (tau keeps the last 60 lines) shows
  only "41 check(s): … 1 FAILED". Proposal: repeat each FAIL line in the
  closing summary, as the "Not checked" lists already are. Priority: low.

Nothing else for beagle: the run's main failure is tau's setup-milestone
detector (R10.md, first tau class).
- `pursuit open` refused a check script because a *comment* in it read "…Setup beagle pursuit infrastructure…": the self-modifying-check scan matched `beagle pursuit <word>` in a comment. Suggest: skip comment lines, or only match known pursuit verbs.

## R12

- **`pursuit split` of an open leaf leaves its uncommitted, in-scope
  work with no owner.** T0005 was split with tests/test_comprehensive.py
  passing but uncommitted. beagle's split recorded nothing about the
  file. From the first part's close on, workspace-clean was red, flagged
  "untracked-not-ignored", with no task named (R12.md, fourth tau class).
  This is the same as R09's tests/cases.json. tau now prints a note, but
  beagle holds the tree. Proposal: `split` lists the open task's
  uncommitted in-scope paths in the result and on the parent record
  (`carried = [...]`), and workspace-clean's FAIL line names the task
  whose scope holds each untracked path. Priority: medium.
- **`pursuit prove`'s tests-only route is easy to miss.** For a task
  that changed only tests, `--mutate` of the module the test imports is
  accepted without `--predates-because`. This is in `--help` only. tau
  (and R02/R04's notes) assumed a tests-only task could be proven only
  by taking a data file away, and R12's T0008 died on that assumption.
  Proposal: when `prove` is given no `--mutate`/`--absent` and the scope
  is tests-only, its error names the modules the scoped tests import as
  candidate `--mutate` targets. Priority: low (tau's first class is the
  fix on the host side).

Nothing else for beagle: the event-tree loss is tau's ordering and checks
(R12.md, second tau class) and the model's invented design.

## R13

- **The open rehearsal does not recognise git's usage error.** R13's
  T0002 was opened on `git diff --stat: references/NOTES.md`; beagle ran
  it at open (T0002.md `check_seconds = 1`), and it exited 129 with
  `error: invalid option: --stat:` and git's `usage:` block. `usage_error`
  (pursuit.py ~L4664) misses it twice: `_USAGE_EXITS` is (2, 4, 64), not
  129, and `_USAGE_ERROR` needs `<prog>: error:` or `Error:`, not git's
  bare lowercase `error:`. So the open printed no warning, and two workers
  ran on a check no work could pass (R13.md, first tau class). Proposal:
  add 129 to `_USAGE_EXITS` and accept a line-initial `error: `; for git,
  whose unknown option is never what the work adds, refuse rather than
  warn. Priority: low (tau's first class is the fix on the host side).
- R23/T0216: beagle pursuit amend has no --scope; a task's scope cannot be
  changed after open, so tau reports the mismatch to the driver instead
  (T0223).
