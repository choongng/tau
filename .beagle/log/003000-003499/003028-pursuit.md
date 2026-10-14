+++
id = "003028-pursuit"
ordinal = 3028
kind = "pursuit"
timestamp = "2026-10-14T04:47:03+00:00"
summary = "pursuit open T0581: tau ext: the examples slice and contract-first note tell the worker to write contract/draft/oracle/"
metric_command = ""
drains = []
hooks = []
+++

criteria: The examples slice title text (CONTRACT_MILESTONES) asks for contract/draft/oracle/ beside standin/: laid out the same, a literal table answering each example's input with its expect and rejecting each invalid input; CONTRACT_FIRST_NOTE names it beside the stand-in; a test matching *oracle_standin* pins both; ruff clean.
decided by: sh -c 'echo "d11bcdedf57a2830c9697fe6bbea59e619486929196eafa5660ad4631e17a2aa  .beagle/checks/T0581/T0581.sh" | sha256sum -c --quiet && bash .beagle/checks/T0581/T0581.sh'
budget: 40000 tokens
opened over T0580: R98 needs it: without it every slice seal is refused once for a missing oracle
