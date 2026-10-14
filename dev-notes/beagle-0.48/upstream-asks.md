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
