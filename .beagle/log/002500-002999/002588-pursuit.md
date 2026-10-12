+++
id = "002588-pursuit"
ordinal = 2588
kind = "pursuit"
timestamp = "2026-10-12T22:23:31+00:00"
summary = "pursuit open T0507: tau ext: a contract worker reads the references by contract refs, uncounted"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker on the contract (scope contract/, [contract] declared) is briefed to read each reference by 'beagle pursuit contract refs NAME --lines A-B / --grep WORD' with its name, not by page reads; its contract refs calls (R79's 'cd … && beagle pursuit contract refs itc2008 2>&1 | head -20' included) do not count toward the nothing-written refusals and are not refused late; a refused read of a reference names contract refs; non-contract workers' briefs and refusals are unchanged.
decided by: sh -c 'echo "57a41e253892417ccb72581c8133a5d05be737cff1a869e0d790ed888b070ce2  .beagle/checks/T0507/T0507.sh" | sha256sum -c --quiet && bash .beagle/checks/T0507/T0507.sh'
budget: 30000 tokens
opened over T0493: R79 stopped on it; the anchor eval waits on it
