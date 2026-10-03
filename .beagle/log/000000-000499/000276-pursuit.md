+++
id = "000276-pursuit"
ordinal = 276
kind = "pursuit"
timestamp = "2026-10-03T19:59:35+00:00"
summary = "pursuit open T0075: scorecard: label the breaker's stop and count only raw reports tau passed through"
metric_command = ""
drains = []
hooks = []
+++

criteria: scorecard.py (itc-harness) reports last_stop_by: 'breaker' when the driver's last error is tau's breaker stopping the run (R09's 'Provider stream ended without a terminal event' came from tau, per the call log), else 'provider'; and counts as workers.raw_tool_call_reports only raw tool-call reports the driver actually saw, with raw_reports_replaced for those tau replaced (R09: 0 and 4). R08's scorecard still builds.
decided by: sh -c 'echo "f37f602d157de2ba7ba7806c8e1abbf3f21aa1f0704053001e1d336ee332d282  .beagle/checks/T0075/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0075/check.sh'
budget: 30000 tokens
