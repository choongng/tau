+++
id = "002780-pursuit"
ordinal = 2780
kind = "pursuit"
timestamp = "2026-10-13T20:29:33+00:00"
summary = "pursuit prove T0534: WITNESSED — refuses when eval.md's `| B07 | q35 | semver (bare goal) |` is put back as `| B07? | q35 | semver (bare goal) |`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0e05d1982d381c9affd5e860cecccd001da498055b77ca4b0686eeef3fba5a03  .beagle/checks/T0534/T0534.sh" | sha256sum -c --quiet && bash .beagle/checks/T0534/T0534.sh'
refutes: refuses when eval.md's `| B07 | q35 | semver (bare goal) |` is put back as `| B07? | q35 | semver (bare goal) |` (proven 2026-10-13T20:28:35+00:00; refused at no B07 row with 75/76 in eval.md)
refused after 0s of a 0s check at: no B07 row with 75/76 in eval.md
refused with: no B07 row with 75/76 in eval.md
standing checks red: T0519
