+++
id = "000679-pursuit"
ordinal = 679
kind = "pursuit"
timestamp = "2026-10-04T12:56:04+00:00"
summary = "pursuit open T0160: Data-test resend amends an open task; spawn notice survives refusal"
metric_command = ""
drains = []
hooks = []
+++

criteria: Resending a pursuit_step with the suggested data-test done_when for a task that is open amends that task instead of spawning a successor; when a new-route spawn does happen, any refusal of the successor in the same call names the spawn; and the successor keeps its predecessor's scope.
decided by: sh -c 'echo "dcf98cb32e82d797d23d4b93035a710fbe5167be7b29056d7538c425d5f8d633  .beagle/checks/T0160/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0160/check.sh'
budget: 50000 tokens
