+++
id = "003033-pursuit"
ordinal = 3033
kind = "pursuit"
timestamp = "2026-10-14T04:52:49+00:00"
summary = "pursuit open T0580: beagle: contain run must not pass beagle's own venv (VIRTUAL_ENV, UV_PROJECT_ENVIRONMENT, PATH) into the contained command"
metric_command = ""
drains = []
hooks = []
+++

criteria: A command run by beagle contain run (and by the check runner when [run] contain is unset) does not inherit VIRTUAL_ENV, UV_PROJECT_ENVIRONMENT, UV_RUN_RECURSION_DEPTH or beagle's own venv bin dir on PATH from beagle's process, while the caller's own values of those (set before beagle was invoked) are kept; tests matching *contain_env* show it, including a contained 'env' listing. ci/check.sh green; README count updated.
decided by: sh -c 'echo "f7e941ec54345407779e1769c97ec558ec88831b89cc641f6fe44cc56b859392  .beagle/checks/T0580/T0580.sh" | sha256sum -c --quiet && bash .beagle/checks/T0580/T0580.sh'
budget: 60000 tokens
