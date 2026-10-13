+++
id = "002712-pursuit"
ordinal = 2712
kind = "pursuit"
timestamp = "2026-10-13T16:50:42+00:00"
summary = "pursuit open T0530: Contract check: property naming that workers can act on, and that a data file cannot satisfy"
metric_command = ""
drains = []
hooks = []
+++

criteria: contract check reports every property no acceptance test names in one problem that names the files read and does not say 'encode it'; an id found only in a JSON acceptance file does not count; beagle CI green
decided by: sh -c 'echo "6914e4ab5e3ffce300286c93c4ff9aee42b0ee2b0673caca2b09982fa54905f5  .beagle/checks/T0530/T0530.sh" | sha256sum -c --quiet && bash .beagle/checks/T0530/T0530.sh'
budget: 60000 tokens
opened over T0493, T0517: 7cb40c5e9edd0e7de2b181cce031708b1545bfbd
