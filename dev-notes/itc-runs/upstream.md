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
