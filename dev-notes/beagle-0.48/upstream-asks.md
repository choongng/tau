# Beagle 0.48 — upstream asks from the tau port

Asks for beagle found while fitting tau's extension to 0.48 (plan.md). Each
was reproduced on the pinned 0.48.0 (`~/beagle-wt/0.48`, 08e642c) on
2026-10-14. Beagle changes go on topic branches off main 08e642c, for the
owner to upstream; nothing here is patched in tau.

## 1. An all-done container refuses its abandon with an empty list

```
$ beagle pursuit close T0545 --outcome abandoned --reason probe
beagle: T0545 is a container with parts still live (). Closing it would strand
them: close or abandon each part first, and then the container if the decision
is to stop there.
```

T0545's leaves have all ended, and `tree` shows it settled (✓ all-done). The
refusal names no live part, and its route (close each part first) has
nothing to act on. Either a container whose parts have all ended is no
longer refused, or the refusal says it is already settled by its leaves and
needs no close. Found closing out the contract era's tasks in tau's tree.

## 2. A brief for the worker who writes a task's cases, before the open

`pursuit brief` is for an open task only:

```
$ beagle pursuit brief T0605
beagle: T0605 is pending; a brief is for an open task, since only `open` binds
the criteria and the check. Run `beagle pursuit open T0605` first.
```

Spec-tying puts the cases before the open: `open --cites --cases` refuses
unless the case files exist and tie to the source. So the worker who writes
them works on a pending task and gets no brief, and the host writes that
worker's instructions itself (rules 2e, the marker grammar, the dry run as
the stop condition). That is policy a host should carry, not author.

Ask: `pursuit brief <task> --cases-from <ref>` (or a `rules 2e`-backed
section in `brief` for a pending task) that briefs the cases worker: the
source, the marker grammar, the case kinds, the gap rule, and the dry-run
command that says when it is done.

## 3. Let `open` take the cites from the cases' markers

Every `beagle-case:` marker already carries its `cite=`. `open` still needs
`--cites` listed by hand, and neither `open --dry-run` nor `coverage` (done
tasks only) prints the ties it accepted; `open` has no `--json`. A host that
dispatches a cases worker and then opens the task must therefore re-parse
the markers itself, which copies beagle's marker grammar into the host, or
trust the worker to report its cites, which a small model gets wrong.

Ask, either: `open --cases <files>` with no `--cites` takes the cites from
the markers (listing them in its output), or `open --dry-run` prints the
accepted cites and cases in a form a host can read (a `--json`, or one
`ties:` line). Tau's interim: read `cite=` from the markers and let
`--dry-run` judge them (plan.md Changes Required 3).

## 4. A dispatch role for the cases worker

Spec-tying (rules 2e) adds a worker that writes a task's cases before its
open, but `dispatch model` knows only three roles:

```
$ beagle dispatch model --for cases
usage: beagle dispatch model [-h] --for {executor,scout,reviewer} [--json]
                             [--host HOST] [--root ROOT] [--config CONFIG]
beagle dispatch model: error: argument --for: invalid choice: 'cases' (choose from 'executor', 'scout', 'reviewer')
```

So a project cannot pin the cases worker apart from the executor, though the
two do different work: one reads the source and writes tests that must fail,
the other writes code until they pass. Tau sends its cases worker on the
executor's pin until beagle has a dispatch role for it (found in T0601).

Ask: a `cases` dispatch role (`dispatch model --for cases`, a `[cases]` line
in `dispatch.toml`), inheriting the executor's pin when none is set.

## 5. The orchestrator does not read the reference or work out the design

The core rules say the orchestrator does not do the work, and that a fact
nobody has read is a reconnaissance leaf:

```
$ beagle pursuit rules | sed -n '11p;19,20p'
- The orchestrator does not do the work. Dispatch a worker with "run
- Criteria you cannot state mean `split`. A check that rests on a fact nobody
  has read makes that fact a reconnaissance leaf, not inline research (§3).
$ beagle pursuit rules | grep -ciE 'the reference'
0
```

A small driver does not read "the work" as including reading the reference
or thinking through the algorithm: in every ITC trial a 9B driver fetched
the paper and reasoned past its output limit (30K characters, then nothing)
before it dispatched anything. Tau says it in its own words
(`DRIVER_STEERS_NOTE`): do not fetch or read the reference, do not work out
the design; a question you would have to think hard about is a task, sent
with the reference and the one question in its notes; keep turns short.

Ask: a core line saying so, in terms of the reference and the design, not
only "the work", so every host's driver gets it from `rules` and
`loop-report`.

## 6. Found first, before reading the reference or designing

`rules 1` says founding is an interview for the goal and the criteria, and
nothing about what not to do before it:

```
$ beagle pursuit rules 1 | grep -ciE 'reference|design'
0
```

Asked to set beagle up and build something, a small model reads the
reference and designs the solution first, then founds with a "design"
milestone, or with criteria for the wrong thing (R02 and R03 founded on
interval trees for interval tree clocks). Tau steers it
(`FOUND_FIRST_NOTE`): found first; workers read the references as each task
needs them; the design is part of the implementation, not a milestone of its
own; name the reference in the milestones.

Ask: §1 (and its core line) says the founding comes before any reading of
the reference or design, and that a design is not a milestone.

## 7. A working habit for a hard part: cases first, one piece per turn

The brief's habits say to run code rather than trace it by hand:

```
$ beagle pursuit brief T0603 | sed -n '/^Working habits/,/^- Report/p' | sed -n '4p'
- Write the code, then run it or the check and read what fails, before you work a case through by hand. A case traced in your head costs a whole reply, and a reply that runs out before it acts leaves nothing in the tree.
```

That names the failure (a reply that runs out) but not the way round it
when the code cannot be written yet because the rule is not known: a small
worker then tries to solve the algorithm whole in one reply and loses it.
Tau's worker prompt (`PIECE_BY_PIECE_NOTE`) gives the steps: write the
smallest cases and their expected results to a file first; in a new turn
find the rule that produces them and write it down; run the cases and fix
from the first failure; going round the same question, write down what is
known and the one open question; stay inside the task.

Ask: a brief habit for a task that needs real working out, with those
steps, so the habit reaches every host's worker.

## 8. Prose in a shell argument

Every pursuit verb that records prose (`add --intent`, `spawn --reason`,
`close --reason`, `--approach-delta` on `add` and `spawn`, `audit --record
--note`, `commit --why`) takes it as a shell argument, and nothing a driver
reads says how to quote it:

```
$ beagle pursuit rules | grep -ciE 'quot|heredoc'
0
$ grep -ciE 'heredoc|single quotes' ~/beagle-wt/0.48/plugins/beagle-pursuit/commands/pursuit-run.md
0
```

Only `owe add --help` warns that prose through a shell heredoc is a quoting
failure waiting to happen. A model that writes a reason in double quotes has
its backticks run as commands and its `$` expanded. Tau's host mapping says
it (prose goes in a quoted heredoc, a file, or single quotes, never double
quotes).

Ask: a line in `rules` (or `pursuit-run.md`) on passing prose to a verb,
or a `--*-file` form for each prose flag, as `owe add --from` has.

## 9. `open --cases` accepts a check that does not run the cases

Rule 2e says "the check runs the cases through the project's own test
command", but `open` doesn't hold a spec-tied task to it. On the pinned 0.48
(a scratch pursuit whose tests/test_add.py carries two marked cases):

```
$ beagle pursuit open T0002 --criteria "add returns the sum" \
    --done-when 'python3 -c "from calc import add; assert add(1, 1) == 3"' \
    --cites spec:2#a82 spec:3#975 --cases tests/test_add.py --dry-run
T0002 would open — add returns the sum; nothing was bound
  decided by: python3 -c "from calc import add; assert add(1, 1) == 3"
exit 0
```

The ties are checked, and then decide nothing: the bound check never runs a
case. Run S02 (q35, wrenfold) did exactly this. The driver wrote a `python3
-c` of ten asserts it worked out itself, six wrong against the spec. The cases
worker copied those values under correct cites, and both workers spent a full
16k-token turn reconciling the spec with a check it contradicts. Tau now
refuses such a step itself (T0609); a host shouldn't have to.

Ask: `open --cases` refuses unless the check runs the case files, at least
when it names none of them or no test command. It could also say so where
rule 2e is printed: "the check is the test command over the case files; the
expected values live in the cases, not the check".
