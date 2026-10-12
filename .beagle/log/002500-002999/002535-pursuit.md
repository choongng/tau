+++
id = "002535-pursuit"
ordinal = 2535
kind = "pursuit"
timestamp = "2026-10-12T17:27:21+00:00"
summary = "pursuit open T0490: tau ext: references through 'beagle refs'"
metric_command = ""
drains = []
hooks = []
+++

criteria: references/ is filled by 'beagle refs fetch' (URLs and --request passed, --no-exclude, index.json read back); a request with no URL is recorded without calling beagle; a beagle without refs leaves each URL failed with the reason; the extension's own fetcher (_fetch_reference, _HtmlText, _pdf_text) is gone, its unit tests ported to beagle's test_refs (01db8e9 on contract-first); full extension suite and ruff green
decided by: sh -c 'echo "39dfdcc9799799b12452399986687b90342d51b854b4ccedf6273908e6f8c2b2  .beagle/checks/T0490/T0490.sh" | sha256sum -c --quiet && bash .beagle/checks/T0490/T0490.sh'
budget: 120000 tokens
