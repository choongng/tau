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

## R54

- **Outright bugs, landing after R56:**
  - T0455: already-passes offers no done-by or abandon that its own rules refuse.
  - T0456: the locked-test refusal's advice doesn't name the call it refused.
  - T0457: prove's out-of-scope witness, and its retry asking for a write the scope refuses.
  - R54 also hit T0453's scope-less refusal and T0454's "reported back" sentence again.
- **Known answers stop at the reference's short rows** (class 1). Deferred; this is the same class as R52's boundary rows and R53's founding.
  - It accounts for 12 of 17 grade failures, its second full-arm miss after R52.
  - Its revisit condition ("both arms keep missing cobs boundary cases") is decided by R56.
- **The locked-test binding route left no way to open a task with code in scope** (class 3, route part). Deferred, as with R52's tests-only route.
  - M14 locks are off in the lean arm, so R56 measures this.

## R55

- **Outright bugs, landing after R56:**
  - T0458: lean still promises locks.
  - T0459: the drop-import brief removed an import the criteria require.
  - T0460: the import-only prove asks for a new check, and the spawn-limit refusal contradicts itself.
  - T0461: raw tool-call markup reached the driver as a report.
- **The source judge held W1's correct event case** (class 5). Deferred; joins R53's classes 1 and 5.
  - M15 is on in both arms, so the pairs don't measure it.

## R56

- **Outright bugs, landing at the R57–R60 boundary:**
  - T0463: the source judge misses results under encoded_hex/decoded_hex keys.
  - T0464: the cut-off kill note says "without acting" after the worker made calls, and a second wording says a killed attempt "reported".
- **T0004's check could not pass on any route it was given** (class 3). Deferred.
  - The src layout was not importable by the system python3, the wrong example 11 was outside every later scope, and no verdict named either cause.
  - It joins the "check can't pass, no verdict says why" family.
  - Candidate test: test_step_result_names_a_src_layout_module_the_check_cannot_import.
- **R54's revisit-if condition is not met.** It said to revisit if both arms keep missing cobs boundary cases. R56 got the boundary rows only because the driver read the reference before founding.

## R57

- **Outright bugs, landing at the R57–R60 boundary:**
  - T0465: under lean, the ruff refusal names locked tests.
  - T0466: an amended check passing on disk briefs the old close demand.
  - T0467: a new route held at close reaches no worker.
- **No task's check ran a founding criterion** (class 4). Deferred.
  - A witness-by-absence close committed the whole implementation as scaffolding.
  - It joins the "check can't pass / check passes over nothing" family (R56 class 3).
- **A defect a worker finds outside its scope has no route to the task that owns the code** (class 5). Deferred.
  - W4 found the leq bug, the scope guard refused its fix, and the finding died.
- **The source judge held the cases task four times** (19.2 min) and removed the cases nearest the bugs (class 6). Deferred; joins R53/R55 class 5.
