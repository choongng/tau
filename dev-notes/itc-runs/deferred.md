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
