+++
id = "000546-pursuit"
ordinal = 546
kind = "pursuit"
timestamp = "2026-10-04T06:19:54+00:00"
summary = "pursuit open T0132: Refuse a known-answers check that imports unwritten code"
metric_command = ""
drains = []
hooks = []
+++

criteria: Opening or amending a task with a check that runs a test importing a module that does not exist and that no path in the task's scope would create is refused, naming the module and the data-only test to bind instead (R15 E9's amend is refused). A not-done result on pytest exit 4 for a missing in-scope test file treats it as missing work and offers no new done_when. CASES_FIRST_NOTE says to open the cases file beside the test with Path(__file__).with_name; a not-done result whose check output shows FileNotFoundError for a bare data name names that fix.
decided by: sh -c 'echo "ebc0ae53ee320858be4cd540a075794f1a7fc5d96adade08a78daa9f0ecb7145  .beagle/checks/T0132/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0132/check.sh'
budget: 100000 tokens
