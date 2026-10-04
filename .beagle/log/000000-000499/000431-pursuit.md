+++
id = "000431-pursuit"
ordinal = 431
kind = "pursuit"
timestamp = "2026-10-04T01:46:22+00:00"
summary = "pursuit open T0111: scope guard: catch writes through os.system/subprocess in inline scripts"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker scope guard reads the shell command string passed to os.system/os.popen/subprocess.* inside an inline script (python3 -c, heredoc) through the bash write-target parser, so R12 W10's python3 -c "import os; os.system('sed -i … src/interval_tree_clock.py')" under scope tests/test_cases.py is blocked naming the out-of-scope path; a script that shells out with no readable path is refused when an out-of-scope project path appears literally; the same write inside scope is allowed. Named tests pass, extension test file passes, ruff clean.
decided by: sh -c 'echo "9903479c441c8080c522a1ee3c971ce54805a6de361441ac64b82947e66e2299  .beagle/checks/T0111/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0111/check.sh'
budget: 100000 tokens
