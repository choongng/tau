+++
id = "001035-pursuit"
ordinal = 1035
kind = "pursuit"
timestamp = "2026-10-05T10:47:04+00:00"
summary = "pursuit prove T0252: WITNESSED — refuses when R28.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "19b32420aff2b51aaac8598fdbff4c1acd5f32727cac38e98202b87b4ea6ad61  .beagle/checks/T0252/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0252/check.sh'
refutes: refuses when R28.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T10:46:08+00:00)
refused after 0s of a 0s check
