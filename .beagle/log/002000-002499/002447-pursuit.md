+++
id = "002447-pursuit"
ordinal = 2447
kind = "pursuit"
timestamp = "2026-10-12T15:50:22+00:00"
summary = "pursuit open T0480: beagle: 'pursuit contract diff' and the second-extraction coverage rule"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle (branch contract-first): 'beagle pursuit contract diff A B [--json]' compares two extractions by the source lines their entries cite (sources identified by path or command, a span covered when the other side cites an overlapping line range of the same source) and by operations, printing what only one side has, exit 0 when neither has anything the other lacks, 1 otherwise, 3 when either cannot be read; 'contract check' with [contract] second declared (and no --draft, no --file) checks the second as an extraction and refuses every span it cites that no primary entry or primary 'excluded' item (source, quote found in it, why) covers, and every operation it names that the primary does not, each problem naming the second's entry and the repair; --draft skips that rule. Covered by 5 named tests in tests/test_contract.py; the file's suite passes.
decided by: sh -c 'echo "a2478a631c8aad5066daff577ebedbdc5e86cc62ff0dbb1aa3f3bf44cf3bb294  .beagle/checks/T0480/T0480.sh" | sha256sum -c --quiet && bash .beagle/checks/T0480/T0480.sh'
budget: 300000 tokens
