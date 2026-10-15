# Contract-first setup (R0003, R0004)

## Why

The R53–R60 q35 runs left one dominant lesson. Setup decides the session.
- In the two runs that scored 42/44 on cobs, the model saw the reference's whole example set before planning.
- In every low run, it planned first: founding enumerated inputs from memory, the checks covered only what founding enumerated, and "done" meant "the checks I wrote pass".
  - R53: event was never planned.
  - R58: "up to 253".
  - R59: an invented API.

Owner's framing (R0004): for most interesting problems, the weights will not hold the knowledge. So reliability comes from three things:
- getting the knowledge in from outside (documents, the repo, experiments, the user);
- recording where each piece came from;
- judging the work against that record, not against the model's belief.

Setup becomes **gather → contract → plan**.

Where the code lives: the shared mechanics go in beagle (branch `contract-first` in `~/beagle-wt/contract-first`), so Claude Code gets them too. tau's extension keeps only what is about running sessions.

## The contract (beagle)

`pursuit.toml` gets an optional `[contract]` table. It is read by a never-raising reader like `[run]`; `[goal]` stays strict.

```toml
[contract]
path = "tests/contract.json"            # the acceptance inventory
second = "tests/contract.second.json"   # optional: an independent extraction it must cover
acceptance = "python3 -m pytest -q tests/test_contract.py"  # runs every entry against the code
files = ["tests/test_contract.py"]      # sealed with the contract
```

### The contract file

The file is JSON, so any language's tests can read it:

```json
{
  "sources": {
    "S1": {"path": "references/cobs.txt", "url": "https://…"},
    "S2": {"path": "include/frame.h"},
    "E1": {"command": "printf 'a' | ./ref-encoder | xxd -p", "output": "026100"}
  },
  "entries": [
    {"id": "C1", "kind": "example",   "operation": "encode", "input": "00", "expect": "010100",
     "source": "S1", "quote": "00 → 01 01 00"},
    {"id": "C2", "kind": "limit",     "operation": "encode", "statement": "a block holds at most 254 data bytes",
     "input": "01…FE", "expect": "FF01…FE00", "source": "S1", "quote": "…"},
    {"id": "C3", "kind": "invalid",   "operation": "decode", "input": "0500", "expect": {"error": "truncated"},
     "source": "S1", "quote": "…"},
    {"id": "C4", "kind": "property",  "operation": "decode", "statement": "decode(encode(x)) == x",
     "source": "S1", "quote": "…"},
    {"id": "C5", "kind": "operation", "operation": "event", "statement": "…", "source": "S1", "quote": "…"}
  ],
  "gaps": [
    {"id": "G1", "question": "what does decode do on a zero inside a block?",
     "assumption": "raise ValueError"}
  ]
}
```

### What each piece does

- **`beagle pursuit contract check [--file F] [--draft] [--rerun]`** checks, and writes nothing:
  - the schema;
  - that every quote appears verbatim in its source, after normalising whitespace, quotes, dashes and line-end hyphens;
  - that an experiment's quote appears in its recorded output, and with `--rerun` that the command still prints that output;
  - that every `operation` entry is exercised by an example, invalid, limit or property entry;
  - that every gap carries an assumption or an answer;
  - that the acceptance files exist, load the contract, and name each property by id;
  - without `--draft`, that `second` exists, is valid, and that every span it cites is covered by a span the primary cites.
- **`contract diff A B`** compares two extractions by the source lines they cite, and by their operations.
- **`contract seal`** runs the full check, then records the sha256 of every contract file in `.beagle/contract-seal.json` and commits the record.
- **`contract status [--json]`** reports one of: `none`, `draft`, `ready`, `sealed` or `altered`. It also gives counts and assumptions.
- **`contract run`** runs `acceptance` under `[run] contain`.

### Gates

- **Order:** with `[contract]` declared and no seal, `open` refuses a task unless its scope lies within the contract files and `references/`. `--before-contract "<why>"` lets reconnaissance through, and the reason is logged.
- **Drift:** once sealed, a change to a sealed file refuses the done close of any task that is not contract work. `status` names it as ALTERED. Re-seal through a contract task.
- **Done:** when `next` has nothing ready and nothing is open, it reports one of three things:
  - the contract state, if unsealed;
  - the acceptance result: failing means the goal is not met, so add work;
  - a pass, with the recorded assumptions listed, after which acceptance is the user's.

  The `loop-guard` Stop hook does the same.
- **Hook:** a new PreToolUse `contract-guard` (Edit|Write|MultiEdit|NotebookEdit) refuses an edit to a sealed file unless an open task's scope holds it.
- **Briefs:** `pursuit brief` adds the inventory instructions for contract work, or a one-line "the contract is sealed; it is what done means" otherwise.

### Other beagle changes

- **`beagle refs fetch URL… | find WORDS…`** ports the extension's reference fetcher, so references are in one on-disk format for every host:
  - HTML and PDF are converted to text;
  - files go to `references/<name>.txt`, with an `index.json` index.
- **`open` refuses a check that reads whole-tree git status** (`git status --porcelain`, `git diff --quiet` with no pathspec). beagle's own record dirties the tree during a task, so such a check cannot pass (R59: 29.9 min).
- **Skill text:** `/pursuit` §1.5 and §3, `/pursuit-run` and `beagle-setup`, plus the commands table, the upgrade notes and version 0.47.0.

## The inventory wording (the contract brief)

> Before anything is planned, read the sources and list what they pin down. Sources are the references, the repo's docs, tests, types and callers, a named standard, and experiments you run and record. List:
> - every worked example (input and exact output);
> - every limit or boundary they state;
> - every input they call invalid, and what must happen to it;
> - every operation they define.
>
> Where no example exists, state a property the output must satisfy. Each entry quotes its source. What no source settles is a gap: ask, or record an assumption. Never guess it into an entry.
>
> Done is every entry passing, not the tests you wrote passing.

## tau extension

- **Founding:**
  - writes `[contract]`;
  - seeds `Contract::…` (extract), then `Second extraction::…` (independent, then reconcile);
  - the plan of the code is split after the seal.
- **Driver criteria** point at the contract. `DRIVER_STEERS_NOTE` stays: the driver still does not read.
- **`pursuit_step`:**
  - seals when `contract status` says `ready`;
  - takes beagle's done gate;
  - turned the cases-first refusals, the source judge and the lock store off when `[contract]` was declared;
  - they were deleted in T0493 (d3bc903f).
- **References** come through `beagle refs`.

## Evaluation

- A spec invented for the test, which no model has seen, with traps:
  - a boundary rule;
  - a stated error case;
  - an operation mentioned once.

  It needs its own grader and adapter.
- q35 on that spec, itc and cobs.
- A 9B smoke run, so small models do not regress.
