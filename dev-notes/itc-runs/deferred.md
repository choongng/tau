# Deferred tau classes

These are the [tau] failure classes from run notes that have no fix merged. Each says why it waits and what would bring it back.
Since R0002 (2026-10-12), tau is frozen for R53–R70, and only outright bugs are fixed between runs.

## R51

All three [tau] classes were fixed before the freeze:
- locked unpassable cases test: T0444
- worker read guards: T0445
- killed worker's last words: T0446

## R52

- **T0005 routed tests-only** (R52.md class 1). Split into two kinds of fix:
  - **Fixed before the freeze, as outright bugs (T0452).**
    - A later empty attempt replaced the earlier attempt's report.
    - The brief's `Scope:` line named the record's scope, not the scope the guard enforces.
  - **Deferred: route redesigns.** These change behaviour rather than fix a bug, so R0002 holds them.
    - `_already_passes`'s new-test-file route also names the code the check imports.
    - The step skips a second attempt after a write the check imports was refused.
    - Already-passes is M09, which the lean arm turns off, so the full/lean pairs measure whether this route earns its place.
    - Revisit once R53–R70 are summarised.
- **Source verdict offered an input row as a result** (class 3): fixed, T0448.
- **No boundary rows in the known answers** (class 4). Deferred.
  - It would add something, and the note itself leaves it as the owner's call against the tooling-weight concern.
  - B05 wrote those rows unasked.
  - Revisit if the full and lean arms both keep missing cobs boundary cases.

## R53

- **Outright bugs, filed to land after R56 so the first pairs run on identical code:**
  - T0453: the done-by refusal points back to the offered scope.
  - T0454: the retry note no longer says a killed worker "reported back".
- **Founding comes before the references are read, so the plan never gained event** (class 1). Deferred.
  - It is a design change: bringing the reference's operations back into the plan.
  - It drove 32 of the 37 grade failures, so it is the first candidate once R53–R70 are summarised.
  - The lean arm doesn't touch founding, so the pairs say nothing about it. Compare across runs instead.
- **The head/tail report cut dropped W5's reference disagreement** (class 4, design part). Deferred.
- **The source judge held correct rule-instance cases and asked for no reference examples** (class 5). Deferred.
  - It joins R52's boundary-rows class, which also asked for no reference examples.
