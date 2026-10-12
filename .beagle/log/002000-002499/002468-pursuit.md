+++
id = "002468-pursuit"
ordinal = 2468
kind = "pursuit"
timestamp = "2026-10-12T16:15:25+00:00"
summary = "pursuit open T0482: beagle: the done gate on contract acceptance"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: with [contract] declared, 'pursuit next' with nothing ready and nothing open reports the contract: unsealed or altered says so; sealed runs acceptance under [run] contain and keeps the result in .beagle/contract-acceptance.json with a fingerprint of the work outside .beagle/; failing says the goal is not met and shows the output's tail; passing lists the seal's assumptions and leaves acceptance to the user (--json: 'contract'). 'status' prints the seal and the kept result without running it. The loop-guard Stop hook, with nothing pending, objects unless a kept passing run matches the work as it stands. 4 named tests; the file passes.
decided by: sh -c 'echo "c7a9966c76f2f0fa16e67a4ebae1ac09b17f29fa7bd5f9990f201b833473cd6c  .beagle/checks/T0482/T0482.sh" | sha256sum -c --quiet && bash .beagle/checks/T0482/T0482.sh'
budget: 300000 tokens
