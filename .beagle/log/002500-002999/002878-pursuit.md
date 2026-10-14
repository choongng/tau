+++
id = "002878-pursuit"
ordinal = 2878
kind = "pursuit"
timestamp = "2026-10-14T00:52:07+00:00"
summary = "pursuit prove T0561: WITNESSED — refuses when README.md's `1. A second baseline, from a pursuit, against` is put back as `1. A second baseline, from a pursuit, against (…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "974196dccb808ccfdc90c09874436345a92822b0ad9a2deaa41e194f04a16487  .beagle/checks/T0561/T0561.sh" | sha256sum -c --quiet && bash .beagle/checks/T0561/T0561.sh'
refutes: refuses when README.md's `1. A second baseline, from a pursuit, against` is put back as `1. A second baseline, from a pursuit, against (…` (proven 2026-10-14T00:52:05+00:00; refused at contract-first is dirty)
refused after 0s of a 2m11s check at: contract-first is dirty
refused with: contract-first is dirty
