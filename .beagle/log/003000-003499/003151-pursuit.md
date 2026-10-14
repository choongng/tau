+++
id = "003151-pursuit"
ordinal = 3151
kind = "pursuit"
timestamp = "2026-10-14T22:50:48+00:00"
summary = "pursuit open T0605: rotation R100-R103 (wrenfold, semver bare goal, itc, cobs) and the before/after table in eval.md"
metric_command = ""
drains = []
hooks = []
+++

criteria: The 0.48 rotation ran on the port: R100 wrenfold, R101 semver (bare goal), R102 itc, R103 cobs, each q35, ended and graded on beagle 0.48.0 with clean tau, each with an eval.md row and section, fixes between runs only to what sank one; eval.md has a before/after table (plain B04-B07, contract R95-R99, 0.48 R100-R103).
decided by: sh -c 'echo "501fceb2a2962796b9ed5021a58e9583a19504ea372e865dba15852b790cc674  .beagle/checks/T0605/T0605.sh" | sha256sum -c --quiet && bash .beagle/checks/T0605/T0605.sh'
budget: 500000 tokens
