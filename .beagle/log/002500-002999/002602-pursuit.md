+++
id = "002602-pursuit"
ordinal = 2602
kind = "pursuit"
timestamp = "2026-10-13T00:41:02+00:00"
summary = "pursuit open T0513: beagle contract: entries are added one at a time by `contract add`, each checked as it lands (cite, shape, id), so a draft is never written whole"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle pursuit contract add takes one JSON item or a list (entry, gap, excluded passage, experiment) on stdin or as an argument, checks each as contract check would (cite against its source first) and writes only those that pass, naming each refusal's repair; an id added again replaces; an unlisted references/ stem becomes a source; a sealed contract is refused. tau lets a contract worker run it and counts it as writing; beagle's brief SHAPE, tau's Contract milestone and CONTRACT_FIRST_NOTE name it, and a cut-off write of contract.json is told to add instead. beagle CI green, tau extension suite green. (Work was begun before this open: the check was written after; prove shows it refuses.)
decided by: sh -c 'echo "888dca7d3fefe7ea904e65b07699f76e6228aa3cc4b45b3b52fef734fb9741ed  .beagle/checks/T0513/T0513.sh" | sha256sum -c --quiet && bash .beagle/checks/T0513/T0513.sh'
budget: 60000 tokens
opened over T0493: the owner chose ideas 1 and 2 (contract-stage cost) first, 10-12
