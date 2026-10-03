+++
id = "000194-pursuit"
ordinal = 194
kind = "pursuit"
timestamp = "2026-10-03T18:20:38+00:00"
summary = "pursuit open T0058: refuse duplicate-abandon that stalls the parent container"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step abandon='duplicate of Tnnnn' on a leaf whose parent is a container other than the root is refused (R08: T0013/T0014 under T0011, duplicates of done T0015, left T0011 stalled for good, since beagle keeps an abandoned leaf with no successor as accountable). The refusal says the container would stall and names the move: work the task with pursuit_step and a done_when that runs the code, which closes done at once if the work is already there. Root/milestone refusals and the R06 successor-of-superseded-milestone exception are unchanged.
decided by: sh -c 'echo "6d864dcf508333c64e09a2d752c4c66a5ffa934144acc2e8472c74f0d3570a72  .beagle/checks/T0058/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0058/check.sh'
budget: 50000 tokens
