+++
id = "000674-pursuit"
ordinal = 674
kind = "pursuit"
timestamp = "2026-10-04T12:49:29+00:00"
summary = "pursuit open T0159: Known-answers open/amend accepts a check passing on own uncommitted work"
metric_command = ""
drains = []
hooks = []
+++

criteria: An open or amend whose check passes only because of uncommitted files inside the task's scope is accepted (the close's witness judges those files), while a check that passes on the committed tree alone is still refused; and the not-opened text never prescribes a data-test done_when that already passes.
decided by: sh -c 'echo "a79832bf144ae099c96c56063552f2be8bc63a5b573124f8d5f2ba79b68fffc3  .beagle/checks/T0159/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0159/check.sh'
budget: 60000 tokens
