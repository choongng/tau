+++
id = "000562-pursuit"
ordinal = 562
kind = "pursuit"
timestamp = "2026-10-04T07:24:01+00:00"
summary = "pursuit open T0135: Founding milestones are known answers, not read-and-design"
metric_command = ""
drains = []
hooks = []
+++

criteria: FOUND_FIRST_NOTE and the system-prompt founding line name the first milestone as known answers from the reference (cases data and its test), not reading the reference or choosing a design; at founding, _repair_milestones retitles a milestone that only reads the reference or chooses a design (R15's 'Read the reference material ... and choose a design.') as 'Known answers from the reference', saying so in the founding result.
decided by: sh -c 'echo "9c4f4c7f0a9e6da89db5d6be3287835ee5cd5a5ecfc7a87afcdd44240b06d469  .beagle/checks/T0135/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0135/check.sh'
budget: 60000 tokens
