+++
id = "002811-pursuit"
ordinal = 2811
kind = "pursuit"
timestamp = "2026-10-13T21:36:40+00:00"
summary = "pursuit prove T0543: WITNESSED — refuses when eval.md's `| R97 | q35 | semver (bare goal)` is put back as `| R9x | q35 | semver (bare goal)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c4f8c82a0bf5b63ded95712a32e06705eaab8ca8161134f8f98b397f1919f725  .beagle/checks/T0543/T0543.sh" | sha256sum -c --quiet && bash .beagle/checks/T0543/T0543.sh'
refutes: refuses when eval.md's `| R97 | q35 | semver (bare goal)` is put back as `| R9x | q35 | semver (bare goal)` (proven 2026-10-13T21:36:40+00:00; predates the task: the eval row was committed (f42f2827) just before open; the grade is a point-in-time write-up of a finished run; refused at no R97 row wit
refused after 0s of a 0s check at: no R97 row with 58/76 in eval.md
refused with: no R97 row with 58/76 in eval.md
