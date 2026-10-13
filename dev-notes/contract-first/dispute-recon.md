# Disputing a sealed acceptance entry: reconnaissance (T0544)

Read 2026-10-13 against beagle contract-first
(`plugins/beagle-pursuit/tooling/beagle/src/beagle/`, shortened below to the
file name) and tau choong-dev `examples/extensions/beagle.py`. Line numbers are
of that day.

The case (R96, ~/wrenfold): entry `prop-marker-inside` is a property whose
statement is right ("inside a two-, three- or five-byte form it is an ordinary
byte of the value", contract/contract.json:348). The sealed contract/accept.sh
invented a concrete case for it, `decode(81 3f 00) == [319]`
(accept.sh:151-154), which the cited spec words contradict (0x81 opens a
three-byte form: 81664). The code returned 81664; the worker burned its
900 s wall deciding that the contract was wrong but sealed. The entry was
right; its test was not.

## What exists

- The seal: `seal()` runs the full check, then `codeless_refusal`, then writes
  each sealed file's sha256 and a `seals` counter to .beagle/contract-seal.json
  (contract.py:1308, contract.py:1324, contract.py:1334). It keeps no reason:
  the record has no field for why, and the CLI logs only the file list
  (cli.py:7951, cli.py:7956).
- `codeless_refusal` runs the acceptance with no project code and refuses
  entries that pass, or fail for a reason other than the code's absence
  (contract.py:1725). It cannot see a wrong expected value: R96's test failed
  on the missing import like every other entry, so it sealed.
- The sha check: `altered()` lists sealed paths whose sha differs
  (contract.py:1296); `status()` then says `altered`, never `ready`
  (contract.py:1366). `drift_refusal` refuses a done close over an altered
  contract unless the task's scope is contract work, which is told to seal
  again (contract.py:1463, contract.py:1481); the close calls it at
  pursuit.py:6318. `contract add` refuses a sealed file (contract.py:1090).
- Amend and re-seal exist in principle: a task scoped to contract/ and
  references/ is contract work (contract.py:1429), its brief says a change is
  sealed again before it closes (contract.py:2093), and pursuit.md:927 says a
  fact found after the seal goes in through a contract task that re-seals.
  There is no verb, record or field for a dispute, and no judge.
- What a worker is told: every non-contract brief ends "If an entry looks
  wrong, stop and report it with the source; changing the contract is a task
  of its own" (contract.py:2107). That is the whole route today. It names no
  report form, so nothing downstream can recognise a dispute.
- tau: the worker brief is `beagle pursuit brief <task>` (beagle.py:15458), so
  it carries that sentence. The worker cannot run beagle; pursuit_step closes
  (beagle.py:49). Its report reaches the driver as text inside the step
  result, "Last report:" when not done (beagle.py:15878) or "Sub-agent
  report:" when done (beagle.py:16274). Nothing parses it for a dispute.
- tau seals only on `state == "ready"` (beagle.py:417, beagle.py:428). After
  an amendment the state is `altered` (contract.py:1366), so tau never
  re-seals, and the amend task's close is refused by drift_refusal. Under tau
  the documented route is therefore broken end to end, not merely unused.
- Contract milestones: Contract, Second extraction, Reconcile get fixed scope
  and check (beagle.py:361); there is no amend milestone.
- A precedent at the right boundary: `_audit` (beagle.py:12208) takes its
  brief from a beagle verb (`pursuit audit`), runs a fresh sub-agent pinned to
  REVIEWER_ROLE, reads a verdict from the report's last line (AUDIT_NOTE,
  beagle.py:12199), and records it with `audit --record`. The known-answers
  route for a wrong locked test (beagle.py:11916) is retired under a contract
  (beagle.py:400), so nothing replaced it.

## Where a dispute enters

At the worker's report, which is the one channel a tau worker has
(beagle.py:15878). The brief sentence (contract.py:2107) should name a form:
end the report with `DISPUTE <entry-id>` and stop. The id, not prose, is the
dispute: the rest of the worker's argument is not passed on.

pursuit_step acts on it only when all hold, so a confused worker cannot open
one: the id is an entry of the sealed contract, the task's check failed, and
the acceptance reported `FAIL <id>` (`entry_verdicts`, contract.py:1552). One
dispute per entry per contract seal; a second report on a held entry is just
a not-done step. The brief change lands at a sub-agent's start, not mid-session.

## Who judges it

A fresh sub-agent, as `_audit` is run, pinned to REVIEWER_ROLE (a cross-model
pick through dispatch.toml where one is set, beagle.py:12228). Its brief is
built by beagle, not by the worker or driver, and holds exactly:

- the entry as sealed (id, kind, operation, statement or input/expect);
- the cited source lines, resolved from `source` and `cite` as `contract refs`
  prints them (contract.py:526);
- the acceptance's lines for that id (the block that prints `FAIL <id>`).

Not the worker's code, report or output. The question is closed: does the test
check what the cited words say? Last line `TEST WRONG: <what the words give>`
or `TEST RIGHT`. A right test cannot be softened because the judge never sees
the code it would be softened toward, and on TEST RIGHT the contract is not
touched; the worker's task stays open with notes saying the entry was upheld.
Model-agnostic: it uses only an id, a citation and a verdict line.

## Smallest change

1. beagle contract.py:2107: name the form, "end your report with
   `DISPUTE <entry-id>`".
2. beagle: `pursuit contract dispute <id> --brief` prints the judge's brief
   above; `--record --verdict wrong|right --reason ... --task T` appends to
   .beagle/contract-disputes.jsonl and the ledger. Refuses an id the last
   acceptance run did not FAIL.
3. beagle `seal()`: take `--reason` (or read open upheld disputes) and keep it
   in the record beside `seals` (contract.py:1328), so a re-seal says why.
4. tau pursuit_step, before `_not_done`: on a valid `DISPUTE`, run the judge as
   `_audit` does. On TEST WRONG, spawn an amend task scoped to contract/
   (contract work), brief carrying the entry, the cited words and the judge's
   line, check `beagle pursuit contract check`; block the disputing task on it.
5. tau `_seal_when_ready` (beagle.py:428): also seal on `altered` when the
   closing task is contract work with an upheld dispute, passing its reason.

The amend is still held: `seal()` reruns the full check and `codeless_refusal`
(contract.py:1324), so the new test must fail without code. A softened test
(one accepting both 319 and 81664) would pass that, so the amend task's check
should also run the acceptance for that id against the value the judge named.
Not verified here: how accept.sh blocks map to ids beyond R96's own file; a
generic slice may need the acceptance's `FAIL <id>` line and its enclosing
block.
