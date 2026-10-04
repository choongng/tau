+++
id = "000617-pursuit"
ordinal = 617
kind = "pursuit"
timestamp = "2026-10-04T09:19:12+00:00"
summary = "pursuit open T0147: Quote check strips a leading label before matching"
metric_command = ""
drains = []
hooks = []
+++

criteria: _quotes_reference finds a source whose verbatim quote is prefixed by a short label and colon (e.g. 'send: This operation is the atomic composition of event followed by peek.') when the text after the label is in references/*.txt, and every case of R15's cases file (at ~/itc.r15/tests/cases.json, copied into the test as a fixture) counts as quoting the reference.
decided by: sh -c 'echo "1c884585a3bbdfaa1c20a3f38a46044ad6b59afec93ec229eba2db6dac2f678c  .beagle/checks/T0147/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0147/check.sh'
budget: 40000 tokens
