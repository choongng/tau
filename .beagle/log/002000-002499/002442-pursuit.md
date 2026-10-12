+++
id = "002442-pursuit"
ordinal = 2442
kind = "pursuit"
timestamp = "2026-10-12T15:44:23+00:00"
summary = "pursuit open T0479: beagle: contract record and 'pursuit contract check'"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle (branch contract-first): pursuit.toml's optional [contract] table (path, second, acceptance, files) is read by a never-raising reader; 'beagle pursuit contract check [--file F] [--draft] [--rerun]' validates a JSON contract: sources (path or command+output), entries of kind example/limit/invalid/property/operation each with id, operation, source and a quote found verbatim (whitespace, dash, quote-mark and line-break-hyphen insensitive, case-sensitive) in its source, input+expect for example/limit/invalid, statement for limit/property/operation; every operation entry exercised by another entry; every gap carrying an assumption or answer; the acceptance files exist, load the contract and name each property id. Exit 0 on a clean contract, 1 on problems, each problem a sentence naming the entry and the repair. Covered by 9 named tests in tests/test_contract.py; the beagle suite file passes.
decided by: sh -c 'echo "c244693c7ec0943da1e34d90b0d59bba7617538d68e05166219ff0f358f49ccd  .beagle/checks/T0479/T0479.sh" | sha256sum -c --quiet && bash .beagle/checks/T0479/T0479.sh'
budget: 400000 tokens
