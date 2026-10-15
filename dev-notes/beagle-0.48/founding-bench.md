# Founding bench — baseline (T0651, 2026-10-15)

Founding measured alone: `itc-harness/founding_bench.sh` starts a run exactly as
`launch.sh` does (harness tau `9c06d5a6`, beagle pin 0.48, the task prompt bytes)
and stops it at the `pursuit: found` commit. `grade_founding.py` grades the founded
plan; `founding_summary.py` regrades every F-run with today's rubric. 24 foundings:
q35/g26/lfm24 × itc/cobs/wrenfold/semver × 2, grouped by model. The harness tau
predates T0654 (near-miss reference names), so this is founding before it.

Every founding finished, in 44–92 s (mean 60–67 s per model): founding is not
where a round's 30 minutes go.

## Which flags mean anything

A flag is a diagnosis only once it is tied to how rounds ended. Against
R104–R129's grader categories (`runs/RNNN/grade.json`):

| flag | tied to failure? | evidence |
|---|---|---|
| MISSING | **yes** | R120 left out count and failed exactly the 6 count cases (48/54); R122 no fork → "lacks fork"; R110, R126 no comparison → "lacks leq" |
| UNSOURCED, on an operation milestone | **plausibly** | the only cobs rounds with wrong answers (not missing code) are R107 and R123, both unsourced; R107's own test asserts `encode(b"") == b"\x00"`, from memory |
| UNSOURCED, on a tests/conventions milestone | no evidence | R110's only unsourced milestone was "Tests"; it failed on unbuilt leq |
| IDLE | not shown | R105, R127 0; R123 35/44 with one. Would need the idle task's minutes |
| COUNT | no evidence | never alone (R104 with MISSING, R121 with IDLE) |

And the rounds' dominant failure is not founding: 23/26 capped, mostly
"adapter lacks X"; clean foundings still scored 0 (R109, R115 lfm24; R119 q35
cobs; R111 g26 3/44).

## Baseline, by the flags that are tied to failure

| model | founding defects tied to failure | which |
|---|---|---|
| q35 | **0/8** | — (its 5 flags are COUNT 6 and unsourced "Tests") |
| g26 | 4/8 | F009 no work milestone; F010 MISSING all of itc's ops; F011, F012 unsourced encode/decode |
| lfm24 | 2/8 | F017, F018 MISSING leq |

So founding is consistent for q35. q35's round failures are execution time
(R104 capped at "lacks decode", R119 capped at "lacks encode" with a clean plan),
and the next lever for q35 is there, not in founding.

## What each defect is, from the call the model sent

- **F011, F012 (g26 cobs): the link is in the part, not in `source`.** E.g.
  `{"part": "COBS encoding::Implement … based on https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing"}`.
  The reference is named; tau only reads it from `source`, so no milestone
  carries `Source:` and the cases worker gets none (the R123 path). Fix
  candidate: lift a request link or references/ name out of the part into
  `Source:`. Deterministic, model-independent.
- **F009 (g26 itc): the plan was one study milestone**, "Analyze the
  mathematical specification … ::<paper link>". Tau's repair turned it into
  "Known answers from the reference", leaving a plan with no implementation
  milestone. The rubric under-reports it (MISSING leq only: "Fork-Event-Join"
  matched three operations).
- **F010 (g26 itc): "Core ITC operations implementation"** names none of them.
  Sources resolved (`itc2008.txt`).
- **F017, F018 (lfm24 itc): no comparison.** Both name fork/join/event (F018
  as `tick`), neither leq/compare — the R110/R126 failure. All three itc
  MISSING cases above are comparison or vague-ops: T0653's target.
- **F021 (lfm24 wrenfold): "0: Setup and goal"** kept as T0002: it carried a
  source, which the setup repair does not fold. IDLE is not shown to cost a
  round, so this is filed, not ranked.
- **F000 (q35 cobs smoke): a source spelled `ConsistentOverheadByteStuffing.txt`**
  for `Consistent_Overhead_Byte_Stuffing.txt`; fixed in T0654 (`eb34ba7c`).
- Seen, not graded: lfm24 sends keys tau drops — F018 `description`, F019
  `title` beside `part` — so the descriptive text of those milestones is lost.

Rubric fixes found by this bench, applied before the tables here: "tree/data
structure" is product, not layout (F001); `tick` is ITC's event (F018).

## All runs

| run | model | task | founded | verdict | flags | milestones |
|---|---|---|---|---|---|---|
| F001 | q35 | itc | 68s | FLAGGED | UNSOURCED Tests — verify all operations against the paper's worked examples and edge cases; COUNT 6 | Data model and serialization — Interval, / Comparison — causal ordering: precedes,  / Fork — split a node's interval into two  / Join — merge two ITCs combining their in / Event — increment counter for the curren / Tests — verify all operations against th |
| F002 | q35 | itc | 60s | FLAGGED | UNSOURCED Tests and validation | Core ITC data structure / Core operations: comparison / Core operations: fork, join, event / Dynamic membership support / Tests and validation |
| F003 | q35 | cobs | 68s | PASS |  | Encoding / Decoding / Edge cases / Tests |
| F004 | q35 | cobs | 76s | FLAGGED | COUNT 6 | COBS encode / COBS decode / Inverse correctness / Zero-free guarantee / Edge cases / Test suite |
| F005 | q35 | wrenfold | 54s | FLAGGED | UNSOURCED Tests | Integer encoding forms / Sequence encoder / Sequence decoder / Count function / Tests |
| F006 | q35 | wrenfold | 62s | FLAGGED | COUNT 6 | Encoder / Decoder / Shortest-form validator / Truncation and trailing-byte rejection / Count / Edge cases |
| F007 | q35 | semver | 62s | PASS |  | Version model / Parser / Validator / Comparison / Tests |
| F008 | q35 | semver | 52s | PASS |  | Version parsing / Version validation / Version comparison / Version range support / Tests |
| F009 | g26 | itc | 74s | FLAGGED | MISSING leq; UNSOURCED Known answers from the reference | Known answers from the reference |
| F010 | g26 | itc | 70s | FLAGGED | MISSING fork, event, join, leq | Core ITC operations implementation / Dynamic membership support / Comprehensive testing and verification |
| F011 | g26 | cobs | 48s | FLAGGED | UNSOURCED COBS Core Logic: Implement the encoding and decoding algorithms based on https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing., Verification: Implement and run tests to ensure correct packet framing and recovery. | COBS Core Logic: Implement the encoding  / Verification: Implement and run tests to |
| F012 | g26 | cobs | 66s | FLAGGED | UNSOURCED COBS encoding, COBS decoding | COBS encoding / COBS decoding |
| F013 | g26 | wrenfold | 64s | PASS |  | Encoding and decoding logic / Validation and count implementation |
| F014 | g26 | wrenfold | 62s | PASS |  | Core implementation / Implementation of count function / Comprehensive testing |
| F015 | g26 | semver | 46s | PASS |  | Core Semver Data Model / Comparison and Validation / Public API and Packaging / Testing and Documentation |
| F016 | g26 | semver | 50s | PASS |  | Core Implementation: Parsing and Validat / Comparison Logic: Implementation of comp / Test Suite: Comprehensive testing agains |
| F017 | lfm24 | itc | 92s | FLAGGED | MISSING leq | Core operations: fork(), join(), event() / Concurrent operations: concurrent_event( / Verification: tests demonstrating fork/j |
| F018 | lfm24 | itc | 44s | FLAGGED | MISSING leq | Implement core ITC operations (tick, for / Write unit tests for ITC semantics / Verify against the paper's examples |
| F019 | lfm24 | cobs | 58s | FLAGGED | UNSOURCED pure-python | encode / decode / pure-python / round-trip |
| F020 | lfm24 | cobs | 70s | PASS |  | cobs.py / cobs.py / test_cobs.py - pytest tests for encode/d |
| F021 | lfm24 | wrenfold | 58s | FLAGGED | IDLE 0: Setup and goal | 0: Setup and goal / 1: Encoder — shortest-form encoding of i / 2: Decoder — read integers until end mar / 3: count() without list construction / 4: Tests and verification against refere |
| F022 | lfm24 | wrenfold | 70s | PASS |  | Encoder: encode each integer in the shor / Decoder: read integers until end marker, / Count reader: return number of integers  / Module wiring and tests for the full imp |
| F023 | lfm24 | semver | 52s | PASS |  | Parsing implementation: parse() function / Validation implementation: validate() fu / Comparison implementation: compare() fun / Tests and documentation: pytest suite +  |
| F024 | lfm24 | semver | 90s | PASS |  | Parse: parse_semver() function that retu / Validate: validate_semver() function tha / Compare: compare_versions() function tha / Documentation: README with usage example / Tests: pytest test suite |

| model | itc | cobs | wrenfold | semver | pass | IDLE | MISSING | UNSOURCED | COUNT | mean found |
|---|---|---|---|---|---|---|---|---|---|---|
| q35 | 0/2 | 1/2 | 0/2 | 2/2 | 3/8 | 0 | 0 | 3 | 3 | 63s |
| g26 | 0/2 | 0/2 | 2/2 | 2/2 | 4/8 | 0 | 2 | 3 | 0 | 60s |
| lfm24 | 0/2 | 1/2 | 1/2 | 2/2 | 4/8 | 1 | 2 | 1 | 0 | 67s |
