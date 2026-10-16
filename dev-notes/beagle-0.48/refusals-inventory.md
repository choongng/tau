# Model-facing refusals in beagle.py: inventory and rewrite plan

Source: /home/choong/tautest/tau/examples/extensions/beagle.py (17,418 lines on disk,
not ~13k). beagle: /home/choong/beagle-wt/0.48 (08e642c). Read-only pass; no
repo file was edited. Relayed-beagle counts come from the driver sessions of
R104–R131 (meta.json "session"); scope-guard counts from their worker sessions.

Classes: **A** a good next step already · **B** model-directed but tied to a
language or task (Python/pytest) · **C** relays text written for beagle users or
humans · **D** the host already knows the answer, so it could repair instead.

## 1. Ranked by expected payoff

Failures = "same refusal again" + "never recovered" (R104–R131).

| # | Class (measured) | ok/again/never | fail | Kind | Fix in one line |
|---|---|---|---|---|---|
| 1 | Write outside scope (worker guard 14880–14937) | 37/12/32 | 44 | B+D | Write the refused paths to the task log. pursuit_step lists them and offers `scope=[…, path]`. Drop the Python-only "under tests/" clause. Send report files to the final message. |
| 2 | beagle refused open/spawn, raw relay (12377, 12695, 11913, 4831) | 4/9/11 | 20 | C→D | Map the 4 observed beagle messages (§3). Two of them are pure host repairs: resolve a title to its id, and amend instead of spawn. |
| 3 | criteria missing (12453) | 4/3/2 | 5 | D | Fill criteria from the record's intent (or title) and say so in a lead line. Do not refuse. |
| 4 | pursuit_dispatch after founding (2547) | 0/0/3 | 3 | D | Run pursuit_step(task=offered, notes=brief) in its place and lead with "ran as pursuit_step". Tools stay unchanged, so the prefix cache is safe. |
| 5 | task waits on another (11331–11351) | 4/1/2 | 3 | D | When one waited-on task is workable, step it with a lead line. pursuit_step already does this for a described task (12120). |
| 6 | cases worker left no marked test (11944) | 2/0/2 | 2 | D | Resume the same cases session with a "no `beagle-case:` marker in <files>" mend. The dry-run mend loop already does this at 11918. |
| 7 | no scope given (5493 via 12495/12593) | 2/0/2 | 2 | D/A- | Build the scope from the check's run files, the record's scope and the predecessor's scope. Offer the exact `scope=[…]` call or apply it. |
| 8 | done_when names no test file (11858) | 13/1/0 | 1 | B | Recovers well, but `_cases_scope` uses `_is_test_path`, so this fires on every non-Python spec task (`go test ./...`, `cargo test`). |
| 9 | done_when is a file-exists check (5027) | 8/1/0 | 1 | A/B | The message is fine. Only `_ONE_COMMAND`'s pytest example is Python-specific (§4). |

Notes on ranking:
- #1 has the most volume. About 15% of it is report files (docs/*.md,
  report.md, REPORT.md, reports/…). About a third is the implementation module
  or `pyproject.toml` written from a tests-only scope.
- For a worker, "never recovered" is often the outcome the message asks for
  ("end the turn with your report"). The waste is that nothing carries the
  refused path to the driver's next call.
- #2 costs the most per failure: 11 driver-level dead ends. The host can map
  most of it cheaply.
- #3–#7 are small counts, but every one of them is a pure host repair with no
  model judgement.

## 2. Inventory (model-facing refusals and gates)

Raw? = whether beagle's own stdout/stderr is pasted into the result.

### 2a. pursuit_step

| Line | Trigger | Quote | Raw? | Cls | Rewrite / repair |
|---|---|---|---|---|---|
| 12035 | no goal | "no pursuit here yet; call pursuit_found first." | n | A | — |
| 12046 | `next --json` rc≠0/4 | "beagle cannot hand out work now (exit N):\n{raw}… Stop here and tell the user" | **y** | C | Fine as a stop. Map rc 4 (audit due/lock) to the call when beagle names one via `_relay_next`. |
| 12091 | abandon w/o task | "abandon names the task to drop; pass task too." | n | A | — |
| 4104–4174 | `_abandon_problem` | "{T} not abandoned — it is the root…/a milestone…" | n | A | — |
| 9160 | close abandoned rc≠0 | "`beagle pursuit close T --outcome abandoned` refused (exit N):\n{out}" | **y** | C | Pass through `_relay_next`. Add "task stays <status>; next: …" |
| 9209–9228 | infeasible w/o evidence, root, … | "{T} not closed infeasible — say why after the colon" | n | A | — |
| 9242 | close infeasible rc≠0 | "…--outcome infeasible` refused (exit N):\n{out}" | **y** | C | Same as 9160. |
| 9103/9137 | audit / audit --record rc≠0 | "`beagle pursuit audit` failed (exit N):\n{brief}" | **y** | C | Add a Next line: "call pursuit_step again; the audit is re-sent". |
| 10024–10101 | done-by close gates | "{T} not closed done by {D} — it has no check: pass done_when, ONE command…" | n | A/B | Inherits `_ONE_COMMAND` (§4). |
| 10041/12155/12410 | `show` rc≠0 | "cannot read {T} (exit N):\n{out}" | **y** | C | Almost always a bad id. Resolve the title to its id, or list the ids that exist. |
| 10129 | done-by `open` rc≠0 | "`beagle pursuit open` refused (exit N):\n{refused}" + Next | **y** | C | See §3. |
| 10154 → 10331 | done close refused | "`beagle pursuit close` refused the done close" → closed blocked, tail pasted | **y** | C | — |
| 11858 | spec task, check runs no test path | "done_when names no test file… e.g. `python3 -m pytest -q tests/test_<part>.py`" | n | **B** | "done_when must run the file the cases go in, using the test command this project already uses: `{example}`". Derive the example from bound checks (§4). |
| 11873 | source not fetched | "Fetch it with `beagle refs fetch <url>`" | n | A | — |
| 11889/11937 | cases worker died | "did not finish: {problem}… Call pursuit_step… again" | n | A | — |
| 11913 | cases dry run refused after 2 mends | "`beagle pursuit open` refused (exit N):\n{relayed}… cases… stay in {files}" | **y** | C | See §3. |
| 11944 | no `beagle-case:` marker | "left no test in {scope} with a `beagle-case:` marker…" | n | **D** | Resume the worker (`resume=run.transcript.stem`) with a marker mend, as at 11918. |
| 12248/12257/12264/12345/12353 | new_route gates | "no new route for {T} — {problem}" | n | A | — |
| 12371 | new route already passes | "…stays as it is — " + `_already_passes` (9462: pytest example) | n | B | §4 example. |
| 12377 | `spawn` rc≠0 | "`beagle pursuit spawn {T}` refused:\n{spawned}\n\n" + offer | **y** | C/**D** | See §3. "No commit since opened" means amend in place (6/24 relays). |
| 12453 | done_when w/o criteria | "criteria is missing: say what will be true…" | n | **D** | Use `record["intent"]` or the title as criteria and note it. |
| 12459–12475 | pending task, no criteria/done_when | "done_when: ONE command…, e.g. `python3 -m pytest -q tests/test_x.py`" | n | B | §4 example. |
| 12487/12499/12619 | `_scope_problem`, `_module_under_tests_problem` | "{T} not opened — {why}" | n | A/B | Module-under-tests is a Python import rule (7755). |
| 12593 → 5493 | no scope after references/ exist | "no scope given… Pass scope=[...] naming the paths this task writes" | n | **D** | Compute it from `_check_run_files(done_when)` ∪ record scope ∪ `_predecessor_scope`, or offer it verbatim. |
| 12634 | check passes before work | `passing_refusal` → 9459 "e.g. `python3 -m pytest -q tests/test_<this task>.py`" | n | B | §4. |
| 12640 | check could not run | "the check could not run: `{broke}` (exit N). Correct the command…" | n | A | — |
| 12648 | `-k` selected none | `_selected_none_refusal` | n | A (pytest-only detector) | — |
| 12670 | check killed at cap | "Call {call}." | n | A | — |
| 12689 | rank gate | "it ranks below {X}. Send {T} first…" | n | A | Already a mapped beagle refusal: the model to copy. |
| 12695 | `open` rc≠0 | "`beagle pursuit open` refused (exit N):\n{refused}" | **y** | C | See §3. |
| 12821 | rewritten check rejected | "{T}'s check not changed — {reason}{advice}" | n | A | — |
| 12835 | `amend` rc≠0 | "`beagle pursuit amend` refused the new check (exit N):\n{amended}" | **y** | C | `_relay_next`, plus "the old check `{bound}` stays bound". |
| 12887–12917 | bound check unpassable / open w/o scope | "{T} not run — … Give it a new route that names its files: {call}" | n | A | — |
| 12931 | `brief` rc≠0 | "`beagle pursuit brief {T}` failed:\n{brief}" | **y** | C | Rare. Add "call pursuit_step with no arguments". |
| 13009/13044/13421/13437 | weak check / unproven | "call instead: …e.g. `python3 -m pytest -q tests/test_<this task>.py`… must import the code" | n | **B** | "a test file that exercises the code (as `{example}` does), with the code's source in scope". |
| 13155 | worker problem | "{T} stays open — {problem}… Call pursuit_step… again" | n | A | — |
| 11869/12974 | bad `thinking` | `_bad_thinking` | n | A | — |
| 16444–16541 | pursuit_wakeup | "REFUSED — this Tau session has no interactive frontend" | n | A | — |

### 2b. pursuit_dispatch / pursuit_plan / pursuit_found / pursuit_driver

| Line | Trigger | Quote | Raw? | Cls | Rewrite / repair |
|---|---|---|---|---|---|
| 2547 | dispatch once founded | "refused, nothing was spawned… Call pursuit_step with task={T}" | n | A→**D** | 0/0/3: run the step for the model (table 1, #4). |
| 2585 | no brief | "pass: run `beagle pursuit brief <task>` and do what it says" | n | C | Pre-founding only. Fine. |
| 4740/4745 | no goal / missing args | "'task' and 'parts' are both required." | n | A | — |
| 4748–4805 | split/setup/rerun/label/repeat gates | "nothing added — {why}" | n | A | — |
| 4831 | `split`/`add` rc≠0 | "pursuit_plan: beagle refused (exit N):\n{out}" | **y** | C/**D** | 7 of the 24 relays are "no task '<goal statement or title>' in the tree" or "no parent '<title>'". Resolve the title (or goal statement) to its id before calling beagle, as pursuit_step does at 12120. |
| 4242/4253 | unconfirmed goal | "read them back… user_confirmed=true" / print-mode "user_delegated=true" | n | A | — |
| 4287/4295/4298/4311 | already founded / missing args / setup milestone | "name the milestones…" | n | A | — |
| 4354 | `add --root-task` rc≠0 | "nothing founded; … failed (exit N):\n{out}" | **y** | C | Rare. Add "correct X and call pursuit_found again". |
| 4372 | milestone split rc≠0 | "…failed (exit N):\n{out}\n\nAdd them with pursuit_plan." | **y** | A- | — |
| 16739–16750 | pursuit_driver misuse | "'command' must be 'pursuit' or 'pursuit-run'." | n | A | — |

### 2c. Tool-call guards ("Tool call blocked: " + reason)

| Line | Who | Trigger | Quote | Cls | Rewrite / repair |
|---|---|---|---|---|---|
| 14880–14937 | worker | write outside scope | "refusing to write {rel}: it is outside {T}'s scope ({scopes})… report that {rel} is needed" | A/B/**D** | The B part is 14883: "The implementation does not go under tests/ either", gated on `.py` + `_is_test_path`. Make it "do not move it to another path in scope instead". The D part is §1 #1. |
| 14893 | worker | same path again | "refused again, N times now… end the turn now with your report" | A | — |
| 14899–14910 | worker | scratch-like path | "Scratch files go in /tmp." | A | Add report-like names (`report`, `*_analysis.md`, `REPORT.md`): "your report is your final message, not a file". |
| 14916–14926 | worker | check imports rel | `_check_imports` (Python `import` → `.py`/`__init__.py`) | B | Never fired in R104–R131. Python-only detector. |
| 14880 → 14730 | worker | write under .git/beagle | "beagle's store… Put your result in your report." | A | — |
| 14672–14697 | worker | re-read past half the cap | "Query it instead, e.g. `python3 -c` over the file" | **B** | "search it instead (`grep -n '<term>' {path}`) for the line you need". |
| 14720 | worker | idle bash past 3/4 cap | "Write {scope} now… then run the check: {check}" | A | — |
| 14792/14802/14813 | worker | beagle verb / sibling tree / ruff on dirs | NO_BEAGLE_REASON, SIBLING_REASON, "Name the files instead" | A | — |
| 14451 | worker | link out of project | "Write the file where it belongs, or report it" | A | — |
| 14994 | worker | commit/claim/close | "Do not commit or claim; do the work… then end with a report" | A | — |
| 13703 | driver | edit/commit in driver | "Call pursuit_step with task={T}…; Reading and running (tests, `ruff check` without `--fix`…)" | A/B | Drop the ruff example, or say "linters without auto-fix". |
| 13690 | driver | same killed-check call | "{T} was last refused on a killed check… call {call}" | A | — |
| 13936 | driver+worker | git reset/clean/rebase | "Fix forward: `git rm --cached`…" | A | — |
| 15182 | driver | bash `beagle pursuit <verb>` | "refusing `beagle pursuit {verb}` from bash: {use}" | A | — |
| 15265–15280 | driver | read inside a stuck task's scope | "debugging its work is the sub-agent's" + escalation calls | A | — |
| 15337 | driver | read references/ | "Call pursuit_step, naming in its notes the reference" | A | — |
| 15411/15969 | driver | write .beagle/ | "put what you meant to change in its notes" | A | — |
| 15639 | driver | beagle PreToolUse hooks via bridge | "beagle {name}: {reason}" | **C** | Raw beagle hook text, written for Claude Code users. Pass it through a hook-reason → tau-call map (as `_tau_next` does), or append the steered tool from `_STEERED_VERBS`. |
| 15871/15884 | driver | agent/setup before founding | "Call pursuit_found now" | A | — |
| 16006 | driver | N off-pursuit calls | "call pursuit_step for the ready task" | A- | Name the ready task id (`_offered_task`). |

### 2d. Worker-brief retry notes (model = worker)

| Line | Note | Cls | Rewrite |
|---|---|---|---|
| 9035–9040 `_without_beagle_habits` | "(e.g. `{bound} python3 -m pytest -q tests/ > {log} 2>&1…`)" | **B** | Use the task's own bound check as the example: `{bound} {check} > {log}`. |
| 9073 `_blocked_brief` | "the check refused it ({reason}). Find what is still missing" | A | — |
| 9305 `_fix_the_work` | "Fix the work, not the check." / "names no failing case… say so" | A | `_FAILURE_NAMED` and `_pytest_collected_none` are pytest-shaped (B detector). Elsewhere it falls back to the neutral branch. |
| 9318 `_last_failure_note` | "The check failed last step (exit N). Its output ends:…" | A | — |
| 9364 `_last_close_note` | "The last close kept this task open: {demand}" | A | — |
| 13250–13270 in-step retry | no-tests lead + fix-the-work + "An earlier attempt read the references; its notes:" | A | — |
| 3137/3148 WORK_IT_OUT / CASES_WORK_IT_OUT | "by running them (`python3 -c`)" | **B** | "by running a one-line script in the project's language". |
| 11991 `_cases_mend_brief` | "beagle refused it:\n{refusal}\nMend the cases…" | C (fine) | The worker can act on beagle's cite/case text directly. Keep it. |

## 3. Relayed beagle refusals: what open/spawn/add emit, and who can map them

Observed in R104–R131 driver results (24 relays; the measured 4/9/11 = 24):

| n | Verb → tau site | beagle text (source) | Map |
|---|---|---|---|
| 6 | spawn → 12377 | "{T} has no commit of its own since it opened, so… the defect is the check's alone. Fix it in place…: `pursuit amend {T} --check-file`/`--done-when`" (pursuit.py 9856) | **Host repair.** The call already carries the new done_when, so run the amend branch (12825) and skip the spawn. Otherwise say "call pursuit_step task=T, done_when=<new> (no new_route)". |
| 7 | split/add → 4831 | "no task '<goal statement/title>' in the tree" (1961); "no parent '<title>' in the tree" (3189) | **Host repair.** Match `task` against the goal statement → root, then node titles (case/space-folded) → id. If there is no match, list ids with titles. |
| 3 | open dry run → 11913 | "cite 'X:146#0b7': #0b7 is line 136's anchor: cite 136#0b7 if…" (spec.py 232) | Already host-repaired by `_reanchor_cites` (R109 fix, 11512). Verify on the next run. |
| 3 | open → 12695/11913 | "the cases do not tie to the cited source: op=X has no invalid or limit case: add one, or `kind=gap op=X assume=…`" (spec.py 363) | Needs the worker. Host: give more mends, or end the driver text with one line: "Call pursuit_step task=T again; its cases worker gets this list". Upstream could also report the ops as data (JSON). |
| 3 | open → 12695 | "no reference 'pyproject' under references/: it holds none; `beagle refs fetch <url>` saves one" | **Host repair.** The source was "N/A", yet a cases route ran. Treat an empty or N/A `source`, or one `_named_reference` rejects, as not spec-tied before spawning a cases worker. |
| 1 | open → 11913 | "cite 'itc2008:48#e3b' names only blank lines" (spec.py 207) | Host could move to the nearest non-blank line whose anchor matches. Otherwise worker mend. |

Other open/spawn/add refusals in beagle source (pursuit.py), mapped:

- Host can map (the answer is in the tree or the call):
  - open 3544 "already open": go straight to the run.
  - open 3552 "has children": `_not_workable`.
  - open 3581 "{T} waits on {X}": step X.
  - open 3602 "ranks below": already mapped at 12689.
  - open 3656 "needs a budget": pass a default.
  - open 3668 / amend 7836 "scope takes one path per argument": split the strings.
  - open 3675 / amend 7939 "check is N characters… --check-file": write the script under .beagle/checks.
  - open 3685 "criteria are N characters": the model should split. Offer pursuit_plan.
  - spawn 9817 "pending: never opened": drop new_route and open.
  - spawn 9845 / add 3176 "attempt limit": `_spawn_limit_offer`, already done.
  - add 3195 "leaf with work of its own": handled at 4823.
  - add 3213 "already has a root": use the root as parent.
  - split 3306 "already has children": falls back to add (4828).
- Needs the model (relay is fine, with a tau-call tail):
  - open 3644 "check cannot be run as written".
  - open 3628 / spawn 9869 "INFEASIBLE recorded".
  - spawn 9882 "same approach already tried" (needs a different delta).
  - add 3158 "say what this attempt does differently".
- Needs upstream beagle:
  - Remedies phrased as beagle flags tau cannot pass: `--over`, `--approach-delta`, `--check-file`, `kind=gap assume=`.
  - The structural fix is a machine-readable refusal: a refusal code plus fields (task, missing flag, offending value) on `--json`. The host then maps code → tau call without regexing prose.
  - The 0.48 "refusals name the route" lines are written as `pursuit <verb> …` commands. `_tau_next` maps only next/audit/open/retry/spawn `next:` lines, not the inline remedies above.

## 4. Language/task-specific choke points (B)

- `_ONE_COMMAND` (5079–5082) and its siblings carry the hardcoded example
  "such as `python3 -m pytest -q tests/test_greet.py`".
  - Siblings: 4864 (tool schema), 5007, 5073, 9462, 11863, 12470, 13037, 13379,
    13421, 13437, 9038.
  - Repair: one `_example_check(root)` that uses the most recent bound
    done_when in the tree that names a test file, with that file replaced by
    `<new test file>`.
  - Before any check is bound, fall back to "the project's test command over
    one test file".
  - The tool schema should use a neutral placeholder, since it sits in the
    cached prefix.
- `_is_test_path` (7527) only knows Python layouts: `test_*`, `*_test.py`,
  `conftest.py`, and anything non-.py under `test/` or `tests/`.
  - It misses `*_test.go`, `*.test.ts`/`*.spec.js`, `__tests__/` and Rust inline
    tests. It also counts every data file under tests/ as a test.
  - It feeds `_cases_scope` (11368), so #8 refuses every non-Python spec task.
  - It also feeds `_data_task`, the "implementation does not go under tests/"
    clause, the witness rules (8586, 8631) and `_scope_problem`.
  - Repair: one `_test_path(rel, root)` predicate. It takes test files from
    what the bound checks run, and falls back to a per-ecosystem table keyed on
    the manifest present.
- Python-import machinery behind refusals:
  - `_check_imports` (14420), `_imports_unwritten`, `_pytest_node_*`
    (6051/6138), `_data_self_import` (6444), `_module_under_tests_problem`
    (7755), `_import_error_only` with `.py` witnesses (10144), and the
    `src/{base}.py`/`__init__.py` probes (8179, 5817, 6236).
  - These are Python-only detectors. They are harmless elsewhere (they do not
    fire) but give no cover either. Keep them, and do not grow more.
- Phrases: "`python3 -c`" (3139, 3148, 14693), "`ruff check`" (13707),
  "pyproject.toml" (6879 example intent).

## 5. Suggested order of work (fix-as-we-go: one patch → one q35 run)

1. pursuit_plan title→id resolution (4831). This is a pure repair and covers
   7 of the 24 relays.
2. spawn "no commit since opened" → amend in place (12377). Covers 6 of the 24.
3. Feed refused out-of-scope writes back to the driver.
   - The worker guard appends the path to `.git/beagle/logs/<T>.log`.
   - The step result names it with a concrete `scope=[…]` call.
   - Report-like names get "the report is your final message".
   - Drop the `.py`/tests clause.
4. Fill criteria from intent (12453). Run pursuit_step in place of a founded
   dispatch (2547). Step the ready dependency (11331).
5. Resume the cases worker on a missing marker (11944). Reject an N/A source
   before the cases route.
6. `_example_check(root)`, plus a project-derived `_test_path`. There are no
   measured failures yet, but this gates every non-Python task.
