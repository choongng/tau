+++
id = "000315-pursuit"
ordinal = 315
kind = "pursuit"
timestamp = "2026-10-03T20:20:16+00:00"
summary = "pursuit open T0073: a worker stopped by the breaker reports the call it repeated"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a worker's event stream shows tau's breaker stop ('Not run, and the run is stopped: …' as a tool result) before it ends on an error, its final_report says the sub-agent was stopped for repeated refused calls and quotes the last refusal's reason (the 'Not run: <problem>' before the stop), instead of '(worker error: Provider stream ended …)'. A worker that ends on a provider error without the stop still reports the worker error. R09: W12 and W13 ended this way and came back as 'worker error'.
decided by: sh -c 'echo "1ffa47c5e7cc5de8211cc132b1bf20c475019ee98b32715ba6ecfe412a6b5447  .beagle/checks/T0073/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0073/check.sh'
budget: 25000 tokens
