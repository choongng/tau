+++
id = "002759-pursuit"
ordinal = 2759
kind = "pursuit"
timestamp = "2026-10-13T20:11:06+00:00"
summary = "pursuit open T0539: founding: criteria leave exact values to the contract"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the founding criteria are drafted by the driver (user_delegated), the extension's founding guidance (pursuit_found's criteria parameter and its prompt guidelines) tells it to state what must pass and leave exact values, sizes, bounds and worked examples to the contract read from the sources, since a value written from memory can contradict it; test *found_criteria_leave_values_to_the_contract asserts that wording reaches the driver
decided by: sh -c 'echo "750b66eae20c913164e45b5cea1502fce44aac12877e6176b89dd31f51064315  .beagle/checks/T0539/T0539.sh" | sha256sum -c --quiet && bash .beagle/checks/T0539/T0539.sh'
budget: 60000 tokens
