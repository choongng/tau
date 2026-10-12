+++
id = "002540-pursuit"
ordinal = 2540
kind = "pursuit"
timestamp = "2026-10-12T17:36:27+00:00"
summary = "pursuit open T0491: harness: an invented spec the weights cannot know"
metric_command = ""
drains = []
hooks = []
+++

criteria: An invented spec (Wrenfold sequence encoding r3, specs/wrenfold-r3.html) with traps: forms 1/2/3/5 bytes against a QUIC-shaped prior and a withdrawn r2 four-byte form, 63 kept out of the one-byte form by the end marker (prose only), stated rejections (no marker, truncated, trailing bytes, overlong form), count named once. grade_wrenfold.py: the reference adapter passes all cases (>=50) and exits 0; each trap adapter fails exactly its own categories (marker passes every worked example); the spec's example table equals the grader's and the reference's. launch.sh accepts wrenfold and serves specs/ at the prompts' URL for the run.
decided by: sh -c 'echo "774c9c5a24e6eb665829dc1b352687ecfc4642106f28288eeb5160a76b543661  .beagle/checks/T0491/T0491.sh" | sha256sum -c --quiet && bash .beagle/checks/T0491/T0491.sh'
budget: 150000 tokens
