+++
id = "001250-pursuit"
ordinal = 1250
kind = "pursuit"
timestamp = "2026-10-09T19:01:26+00:00"
summary = "pursuit amend T0023"
metric_command = ""
drains = []
hooks = []
+++

7750daeb (trial T01, 2026-10-06) renamed test_worker_argv_thinking_off to test_worker_argv_thinking_level; it still asserts unset means --thinking off, and adds the 'default' case
was: sh -c 'echo "8a38c62c4251d3fc6e93fe05a520313706edc950f29f1205557ee6f4d412ff2a  .beagle/checks/T0023/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0023/check.sh'
  8a38c62c4251d3fc6e93fe05a520313706edc950f29f1205557ee6f4d412ff2a  .beagle/checks/T0023/check.sh
now: sh -c 'echo "473108eb846e652523c3791653cd5717401ebfc3671f87b60660ff7b1f9b5bf8  .beagle/checks/T0023/T0023.sh" | sha256sum -c --quiet && bash .beagle/checks/T0023/T0023.sh'
