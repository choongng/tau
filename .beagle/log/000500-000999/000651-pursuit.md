+++
id = "000651-pursuit"
ordinal = 651
kind = "pursuit"
timestamp = "2026-10-04T11:25:56+00:00"
summary = "pursuit open T0154: pytest exit 5 explained in results"
metric_command = ""
drains = []
hooks = []
+++

criteria: When the bound check is pytest and exits 5, the not-done result and the retry note lead with: pytest collected no tests from <file>: it defines no test_ function; adding them is the work.
decided by: sh -c 'echo "9609505b9f4927b6ef4d8e1e2a0e477231a7c7b18b668cb9bde750ef4376f0b9  .beagle/checks/T0154/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0154/check.sh'
budget: 40000 tokens
