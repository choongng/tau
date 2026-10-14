+++
id = "002854-pursuit"
ordinal = 2854
kind = "pursuit"
timestamp = "2026-10-13T23:50:13+00:00"
summary = "pursuit prove T0540: WITNESSED — refuses when README.md's `<a href=\"https://github.com/huggingface/tau/iss…` is put back as `<a href=\"https://github.com/huggingface/tau/iss…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "81105354969dad39b565c53d4fe29becad43cca5550a9781caff62d52a5f0185  .beagle/checks/T0540/T0540.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0540/T0540.v2.sh'
refutes: refuses when README.md's `<a href="https://github.com/huggingface/tau/iss…` is put back as `<a href="https://github.com/huggingface/tau/iss…` (proven 2026-10-13T23:50:13+00:00; refused at tau-harness is dirty)
refused after 0s of a 1m37s check at: tau-harness is dirty
refused with: tau-harness is dirty
