+++
id = "003006-pursuit"
ordinal = 3006
kind = "pursuit"
timestamp = "2026-10-14T04:21:19+00:00"
summary = "pursuit prove T0490: WITNESSED — refuses when beagle.py's `def _references_index(root: Path) -> dict[str, …` is put back as `def _pdf_text(data: bytes) -> str: return \"\" de…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "59d759e6e96533b54fbb7ec0aa9b9c501471b3014c46fac62af504be1053fc91  .beagle/checks/T0490/T0490.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0490/T0490.v2.sh'
refutes: refuses when beagle.py's `def _references_index(root: Path) -> dict[str, …` is put back as `def _pdf_text(data: bytes) -> str: return "" de…` (proven 2026-10-14T04:21:19+00:00; refused at the extension still has a fetcher of its own)
refused after 1s of a 26s check at: the extension still has a fetcher of its own
refused with: the extension still has a fetcher of its own
