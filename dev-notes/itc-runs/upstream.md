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
