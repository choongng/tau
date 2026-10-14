+++
id = "002955-pursuit"
ordinal = 2955
kind = "pursuit"
timestamp = "2026-10-14T03:21:41+00:00"
summary = "pursuit open T0567: tau: a slice worker can save and name a source (S01 #1)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Under a declared contract, a Slice: task's scope is contract/ and references/ (whatever the driver passes), so its worker can save a source there; the Slice: examples text (and the slice brief tau adds, if any) says to save each source under references/ with beagle refs fetch (or by writing it) and how the contract names it before contract add; nothing requires a source (bare goal). Tests slice_scope_admits_references and slice_worker_saves_a_source pass; whole extension suite green outside beagle's venv.
decided by: sh -c 'echo "0ee789dc73a491b7693ed698e6ba4e45f2fc4f15f4c0ec7e1ec8e997ef0ff789  .beagle/checks/T0567/T0567.sh" | sha256sum -c --quiet && bash .beagle/checks/T0567/T0567.sh'
budget: 80000 tokens
