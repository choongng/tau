+++
id = "000760-pursuit"
ordinal = 760
kind = "pursuit"
timestamp = "2026-10-04T17:09:55+00:00"
summary = "pursuit prove T0102: WITNESSED — refuses when summary-R11-R20.md's `## Compared with R01–R10` is put back as `## Versus the first ten`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e323864559912e8b84511e587a38b1f66e1c9a66e91d418377286b8d0038e245  .beagle/checks/T0102/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0102/check.sh'
refutes: refuses when summary-R11-R20.md's `## Compared with R01–R10` is put back as `## Versus the first ten` (proven 2026-10-04T17:08:59+00:00; refused at missing ## Compared with R01–R10)
refused after 0s of a 0s check at: missing ## Compared with R01–R10
refused with: missing ## Compared with R01–R10
