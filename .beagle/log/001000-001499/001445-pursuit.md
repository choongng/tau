+++
id = "001445-pursuit"
ordinal = 1445
kind = "pursuit"
timestamp = "2026-10-10T02:37:32+00:00"
summary = "pursuit open T0343: Scorecard splits workers that ended without a reply by cause"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/scorecard.py's workers block keeps timed_out and splits it into wall_timeouts, stopped_by_refusals (tau's 8-refusal stop) and cap_killed (last event within a minute of the run's cap), so R39 scores 6 = 1 + 4 + 1.
decided by: sh -c 'echo "31598f802db9cff7992c852730e7c1ab9e54baa42038c8fe4c2b371ad013fcab  .beagle/checks/T0343/T0343.sh" | sha256sum -c --quiet && bash .beagle/checks/T0343/T0343.sh'
budget: 12000 tokens
