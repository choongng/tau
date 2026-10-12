+++
id = "002483-pursuit"
ordinal = 2483
kind = "pursuit"
timestamp = "2026-10-12T16:33:38+00:00"
summary = "pursuit open T0485: beagle: 'beagle refs fetch|find'"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle contract-first: 'beagle refs fetch URL… [--request TEXT]' writes references/<name>.txt (HTML without script/nav/footer, table cells ' | ', PDF via pdftotext -layout, newline-only breaks) and references/index.json {request, fetched{name:url}, failed{url:why}} in tau's founding shape; a failure is recorded and exits 1; a file on disk is kept unless --refresh; references/ goes to .git/info/exclude unless ignored or --no-exclude. 'refs find TERM…' prints references/NAME:LINE: text for lines holding every term (case/space-insensitive), exit 1 on none. 4 named tests; the file passes; CI green.
decided by: sh -c 'echo "d03e65a39b3e167af61d1fa91c4be41fbfe0ec01c0a9218c7bda9e586cb15efe  .beagle/checks/T0485/T0485.sh" | sha256sum -c --quiet && bash .beagle/checks/T0485/T0485.sh'
budget: 200000 tokens
