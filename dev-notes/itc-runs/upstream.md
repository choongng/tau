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
