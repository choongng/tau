+++
id = "001866-pursuit"
ordinal = 1866
kind = "pursuit"
timestamp = "2026-10-12T00:46:18+00:00"
summary = "pursuit open T0445: R51 fix: worker read guards let a known-answers worker read and search the references once"
metric_command = ""
drains = []
hooks = []
+++

criteria: In a worker whose scope holds only tests and data, the call guards do not count toward the nothing-written refusal a first read of each reference window (limit <= 60) or a search confined to the references; a repeat read of the same window is still refused; a read refusal that offers a search is never followed by a bash refusal of that search. q35 R51. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "7a035fffab63f905bdb591b1e5f2c9f4585beeab58f47ba9ba5d50826dd91cf2  .beagle/checks/T0445/T0445.sh" | sha256sum -c --quiet && bash .beagle/checks/T0445/T0445.sh'
budget: 150000 tokens
