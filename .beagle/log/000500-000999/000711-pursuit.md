+++
id = "000711-pursuit"
ordinal = 711
kind = "pursuit"
timestamp = "2026-10-04T14:13:55+00:00"
summary = "pursuit open T0167: Founding folds a design milestone into the next when known answers exist"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_found's milestones include one naming known answers, a read/design-only milestone (as _read_or_design_only reads it) is not kept as its own task: it is dropped and its text joins the following milestone's intent, with a note saying it was folded in; R17's docs milestone (deliverable words) is still kept.
decided by: sh -c 'echo "2cedd2c99bc400c549aeaeb75e87ea5f1bc4f3059380a6453358ab4a88a9eb1e  .beagle/checks/T0167/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0167/check.sh'
budget: 30000 tokens
