+++
id = "001606-pursuit"
ordinal = 1606
kind = "pursuit"
timestamp = "2026-10-10T18:45:36+00:00"
summary = "pursuit open T0379: R42 fix: scorecard tells loop cuts from output-limit cut-offs"
metric_command = ""
drains = []
hooks = []
+++

criteria: scorecard.py counts loop_cuts (assistant turns whose diagnostics hold reasoning_loop_cut) for the driver and the workers, apart from output-limit cut-offs, and driver_reprocess_seconds (time to first output of the driver turns after a thinking switch, i.e. a nudge reply and the turn after it). On R42: 10 driver loop cuts, over 300 s of re-prefill. R41's T0371 counts (12 reasoning cut-offs, 6 cut-off kills) are unchanged. Existing fields keep their meaning.
decided by: sh -c 'echo "905ce9d88f1343034ce22464ea663f97e4b7368bb8398c7a84b557c8c0a16cb8  .beagle/checks/T0379/T0379.sh" | sha256sum -c --quiet && bash .beagle/checks/T0379/T0379.sh'
budget: 30000 tokens
