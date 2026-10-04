+++
id = "000755-pursuit"
ordinal = 755
kind = "pursuit"
timestamp = "2026-10-04T17:00:15+00:00"
summary = "pursuit open T0175: Test that the design fold keeps R17's docs milestone when known answers exist"
metric_command = ""
drains = []
hooks = []
+++

criteria: A test runs founding's milestone repair on R17's docs milestone beside a known-answers milestone and an implement milestone, and asserts the docs milestone is kept whole and no fold note is written, so a fold that swallowed it would fail.
decided by: sh -c 'echo "9febfcaae5d738364c7ae50f35691eb3daf49e60c6223cbe9780f01d066c76a5  .beagle/checks/T0175/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0175/check.sh'
budget: 15000 tokens
