+++
id = "002784-pursuit"
ordinal = 2784
kind = "pursuit"
timestamp = "2026-10-13T20:30:04+00:00"
summary = "pursuit open T0540: advance the run build: contract-first <- rotation-fixes (CI green), tau-harness <- choong-dev"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first contains rotation-fixes (T0536, T0537, T0541) with ci/check.sh green on a clean checkout of its tip, and ~/tautest/tau-harness is checked out at choong-dev (T0535, T0538, T0539), clean and uv-synced; done only between runs
decided by: sh -c 'echo "24918a0a042bc867b8738f73640f937eae43cc993acd23bd5a0cc099feda4b1d  .beagle/checks/T0540/T0540.sh" | sha256sum -c --quiet && bash .beagle/checks/T0540/T0540.sh'
budget: 30000 tokens
