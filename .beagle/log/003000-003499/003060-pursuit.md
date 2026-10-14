+++
id = "003060-pursuit"
ordinal = 3060
kind = "pursuit"
timestamp = "2026-10-14T06:12:21+00:00"
summary = "pursuit open T0587: beagle: a slice task opens on an empty draft (no vacuous 'already passes before any work' refusal); founding does not seed a duplicate of an auto-inserted slice"
metric_command = ""
drains = []
hooks = []
+++

criteria: A slice task (Slice: …) opens when the contract draft is empty, with no 'already passes before any work' refusal; other tasks keep that refusal; founding does not seed a model-written slice that duplicates an auto-inserted one; tests *empty_draft_slice_open*; ci green; README count updated
decided by: sh -c 'echo "ccac0f26ecf46518190bab3ed7cbff23d575dff36c2e25c9dff8b42bad90f349  .beagle/checks/T0587/T0587.sh" | sha256sum -c --quiet && bash .beagle/checks/T0587/T0587.sh'
budget: 150000 tokens
