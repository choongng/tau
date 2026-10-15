+++
id = "003356-pursuit"
ordinal = 3356
kind = "pursuit"
timestamp = "2026-10-15T21:46:24+00:00"
summary = "pursuit open T0650: founding-only bench runner"
metric_command = ""
drains = []
hooks = []
+++

criteria: /home/choong/tautest/itc-harness/founding_bench.sh [--dry-run] FNNN q35|g26|lfm24 itc|cobs|wrenfold|semver runs one founding with launch.sh's environment (harness tau at TAU_SRC, TAU_HOME, the beagle pin on PATH, BEAGLE_ROOT, TAU_BIN, dispatch provider/model/thinking, the exact prompt bytes, MemoryMax scope; the wrenfold spec server) in an empty ~/fb/FNNN/TASK, stops the scope once the 'pursuit: found' commit exists (or at FOUND_CAP_S, default 600), and writes runs-founding/FNNN/{meta.json, stdout.log, result.json} where result.json holds found_seconds (null if never founded), stopped_on (found|cap|exit) and grade_founding.py's grade. --dry-run prints that environment and command and creates nothing. One real smoke founding (F000) has run and recorded a graded result.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider /home/choong/tautest/itc-harness/test_founding_bench.py
budget: 200000 tokens
