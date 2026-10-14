+++
id = "003044-pursuit"
ordinal = 3044
kind = "pursuit"
timestamp = "2026-10-14T05:31:17+00:00"
summary = "pursuit open T0582: beagle+tau: a milestone's operation needs its sealed <op> limits-and-invalid slice before contract run --operation passes (design incremental-contract.md:32-34)"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle: contract run --operation X (and the milestone gate that uses it) is refused while no sealed slice holds a limit or invalid entry for X, unless a sealed slice records a gap for X's malformed input; the refusal names the slice to plan ('Slice: X limits and invalid inputs'); the examples-slice-only case of R98 is a test. tau: _slice_due / the driver note plan that slice from the refusal before the milestone, and its tests pass. Tests named *limits_slice_gate* in both; beagle ci green; tau's extension suite fully passes.
decided by: sh -c 'echo "db33143e31029074c4ccc257d2b8d9099f688837f2ed1a6cb83e0aae3dfea64c  .beagle/checks/T0582/T0582.sh" | sha256sum -c --quiet && bash .beagle/checks/T0582/T0582.sh'
budget: 120000 tokens
