+++
id = "001505-pursuit"
ordinal = 1505
kind = "pursuit"
timestamp = "2026-10-10T04:11:19+00:00"
summary = "pursuit prove T0354: WITNESSED — refuses when launch.sh's `extensions=(--no-extensions)` is put back as `extensions=()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "42b7cb294dc2113ee3a7f5d70b1505c186456cd0753f56d2739fdacc8a59a624  .beagle/checks/T0354/T0354.sh" | sha256sum -c --quiet && bash .beagle/checks/T0354/T0354.sh'
refutes: refuses when launch.sh's `extensions=(--no-extensions)` is put back as `extensions=()` (proven 2026-10-10T04:10:20+00:00; refused at env GIT_AUTHOR_NAME=choong GIT_AUTHOR_EMAIL=choongx@fastfin.net GIT_COMMITTER_NAME=choong GIT_COMMITTER_EMAIL=choongx@f…)
refused after 0s of a 1s check at: env GIT_AUTHOR_NAME=choong GIT_AUTHOR_EMAIL=choongx@fastfin.net GIT_COMMITTER_NAME=choong GIT_COMMITTER_EMAIL=choongx@f…
refused with: env GIT_AUTHOR_NAME=choong GIT_AUTHOR_EMAIL=choongx@fastfin.net GIT_COMMITTER_NAME=choong GIT_COMMITTER_EMAIL=choongx@fastfin.net BEAGLE_TAU_DISPATCH_PROVIDER=bane BEAGLE_TAU_DISPATCH_MODEL=qwen3.5-9b-q4-mtp-thinking-coding systemd-run --user --scope -q --unit cobs-B99 -p MemoryMax=8G -p MemorySwapMax=0 timeout -k 30 3600 tau -p --provider bane --model qwen3.5-9b-q4-mtp-thinking-coding $'implement a modern python implementation of consistent overhead byte stuffing (COBS, reference link below). use your judgement to do the work without further discussion.\n\nhttps://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing\n'
