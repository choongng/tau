+++
id = "002623-pursuit"
ordinal = 2623
kind = "pursuit"
timestamp = "2026-10-13T03:43:35+00:00"
summary = "pursuit open T0516: contract: the second extraction is independent — founding scopes it to contract.second.json, and a worker on one extraction is refused reading or writing the other (R83, R84)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Founding seeds Contract, Second extraction and Reconcile; pursuit_step gives each its scope and check whatever the driver passes (the second: its own file, checked with check --file); a worker on the second extraction is refused reading contract.json, contract diff, and add/check without --file on the second; any other worker is refused writing or adding to the second; beagle's brief tells the second its own check and that reconciling is a later task, tells the Contract worker not to write the second, and the full check's missing-second message says it is another task's. Tau tests and beagle CI pass.
decided by: sh -c 'echo "01a3a078eee3e10c686fa1b08ed5226b035e3196832872578dcd71033b83fe8a  .beagle/checks/T0516/T0516.sh" | sha256sum -c --quiet && bash .beagle/checks/T0516/T0516.sh'
budget: 150000 tokens
opened over T0493: the owner said continue after R83/R84, 10-12
