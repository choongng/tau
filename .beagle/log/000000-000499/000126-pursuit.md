+++
id = "000126-pursuit"
ordinal = 126
kind = "pursuit"
timestamp = "2026-10-03T15:28:34+00:00"
summary = "pursuit open T0044: Founding in print mode does not wait on an absent user"
metric_command = ""
drains = []
hooks = []
+++

criteria: Without a UI, pursuit_found's unconfirmed refusal says print mode has no user to answer, quotes the opening of the user's prompt, and leads with calling again with user_delegated=true when the prompt delegates (else stop and say what is needed). With a UI the refusal is unchanged. In print mode, a turn that ends with no goal after such a refusal gets one stop-gate follow-up saying the same; a founded or interactive session gets none.
decided by: sh -c 'echo "74d183e355a25a79c0eda551ba2ee43b6acc65c4a7531fd7ab703907c9f336e2  .beagle/checks/T0044/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0044/check.sh'
budget: 40000 tokens
