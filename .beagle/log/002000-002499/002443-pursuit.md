+++
id = "002443-pursuit"
ordinal = 2443
kind = "pursuit"
timestamp = "2026-10-12T15:49:56+00:00"
summary = "pursuit prove T0479: WITNESSED — refuses when contract.py's `if found is None: return [f\"{where}'s quote is …` is put back as `if found is None and False: return [f\"{where}'s…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c244693c7ec0943da1e34d90b0d59bba7617538d68e05166219ff0f358f49ccd  .beagle/checks/T0479/T0479.sh" | sha256sum -c --quiet && bash .beagle/checks/T0479/T0479.sh'
refutes: refuses when contract.py's `if found is None: return [f"{where}'s quote is …` is put back as `if found is None and False: return [f"{where}'s…` (proven 2026-10-12T15:48:59+00:00; refused at FAILED tests/test_contract.py::test_contract_check_refuses_a_quote_not_in_its_source)
refused after 1s of a 1s check at: FAILED tests/test_contract.py::test_contract_check_refuses_a_quote_not_in_its_source
refused with: 3 failed, 6 passed in 0.46s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
