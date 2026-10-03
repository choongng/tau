+++
id = "000019-pursuit"
ordinal = 19
kind = "pursuit"
timestamp = "2026-10-03T09:55:23+00:00"
summary = "pursuit open T0020: R01 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: Run R01 (mimo-v2.6-9b-q4) launched via launch.sh from a clean ~/itc under the 1h cap; runs/R01/{exit.json,scorecard.json,grade.json,adapter.py} written; dev-notes/itc-runs/R01.md has a Scorecard section and a 'grader: k/n' line (0/n with MISSING ops if no ITC was built — report that rather than inventing an adapter).
decided by: sh -c 'echo "266946c887e0f64f177a3b25cd64b49a0ac0adb5abe5439113d5c489046a83d7  .beagle/checks/T0020/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0020/scored.sh R01'
budget: 100000 tokens
