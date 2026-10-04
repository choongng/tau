+++
id = "000768-pursuit"
ordinal = 768
kind = "pursuit"
timestamp = "2026-10-04T21:53:33+00:00"
summary = "pursuit open T0198: R21 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R21 (mimo-v2.6-9b-q4, itc_prompt.txt) launched by launch.sh from a clean ~/itc under the 1h cap on a clean tau commit; scorecard.json and grade.json made; dev-notes/itc-runs/R21.md has the header (model, prompt, tau sha), the grader line and the Scorecard block agreeing with scorecard.json.
decided by: sh -c 'echo "910e3ea87c57f49e0137daffa2197ac6d2aa630ee7c89c8ac7b14766cc5fff7c  .beagle/checks/T0198/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0198/check.sh'
budget: 40000 tokens
