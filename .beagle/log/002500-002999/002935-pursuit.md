+++
id = "002935-pursuit"
ordinal = 2935
kind = "pursuit"
timestamp = "2026-10-14T02:34:47+00:00"
summary = "pursuit open T0562: advance tau-harness to the slice-flow tau; smoke the pairing"
metric_command = ""
drains = []
hooks = []
+++

criteria: tau-harness is detached at choong-dev's tip (holding 040a2b33, its beagle.py equal to choong-dev's); launch.sh accepts a smoke id S01 (pursuit mode, runs/S01) and a CAP_S override; a contained q35 semver smoke S01 with BEAGLE_ROOT=~/beagle-wt/contract-first (cde3fbd) founds, seals contract/slices/01-examples and commits code under src/; the report gives founding->seal and seal->first code times from the trace.
decided by: sh -c 'echo "25fde6eef6bbf881f3f0b44b5fefab4e8e1f10a9769c52a14a8d35bca0de8f3d  .beagle/checks/T0562/T0562.sh" | sha256sum -c --quiet && bash .beagle/checks/T0562/T0562.sh'
budget: 120000 tokens
