+++
id = "003071-pursuit"
ordinal = 3071
kind = "pursuit"
timestamp = "2026-10-14T06:48:39+00:00"
summary = "pursuit open T0588: beagle+tau: after the same refusal twice, the refusal names one route that works; a milestone can be abandoned as a duplicate of another"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle open refusing the same task for the same reason a second time adds one line naming a route that works for that refusal's cause (split, amend, abandon as duplicate, ...); a milestone can be closed abandoned when it names a live task it duplicates; tests *repeated_refusal_route*; ci green; README count updated
decided by: sh -c 'echo "c8bacb0a7bb54e8ac41bdcd71753fbd99309e4d9ca793f353f2d6c91087888d8  .beagle/checks/T0588/T0588.sh" | sha256sum -c --quiet && bash .beagle/checks/T0588/T0588.sh'
budget: 150000 tokens
opened over T0593: T0593 edits itc-harness launch.sh, which the live R99 bash is still reading; it goes in after R99 ends
