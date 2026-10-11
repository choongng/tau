---
title: Managing context
description: Keep long sessions working with automatic and manual compaction, and control model effort with thinking modes.
---

A model can only read so much text at once — its **context window**. Long coding
sessions fill it up. Tau handles this with **compaction** (summarizing older
history) and lets you tune how hard the model works with **thinking modes**.

## Seeing context usage

The compact status below the TUI prompt shows provider-anchored active context as
`used/limit`. When no valid provider usage exists yet, it shows `?/limit` instead
of presenting the fallback estimate as provider-confirmed usage. Run `/session`
to see the detailed provider basis or fallback estimate:

```text
Estimated context tokens: <count>
Context window: <count>
Context window source: configured catalog | provider live catalog
Context token breakdown: system=<count>, messages=<count>, tools=<count>
Thinking mode: <mode>
```

After a successful model response, Tau uses the provider-reported token usage as
the authoritative size of the context processed by that response, then estimates
only messages added afterward. Before the first response, immediately after
compaction, or when no valid usage is available, Tau falls back to a deterministic
estimate (roughly `characters / 4` plus small per-message and per-tool overhead).
The fallback covers the system prompt, project context (`AGENTS.md`), skill
metadata, active message history, and tool schemas.

`/session` reports `Context token basis: provider=<count>, estimated
trailing=<count>` when provider usage anchors the active count. Otherwise it shows
the fallback system/message/tool breakdown. Provider usage from errored or aborted
responses is not trusted.

This is different from the cumulative token totals in the sidebar's **usage**
section. Cumulative usage adds the provider-reported input and output tokens from every request on the active
branch, including history later replaced by compaction. Repeatedly sending the
same context therefore increases cumulative input usage, while active context
consumption describes only what Tau expects to send next. The two figures are
not expected to match.

## Automatic compaction

By default, Tau compacts automatically when the estimate gets close to the
model's context window. It checks two moments:

- when a turn is about to start — a new prompt, an extension's message that
  starts a turn, or a continue — and
- after a context-overflow error (force compaction regardless of the local estimate,
  then retry once).

Tau does not compact after a turn ends. A session waiting for your reply stays
idle: no summary request occupies the provider (which matters on a single-slot
local server shared with background subagents), and the summary is written
only once your reply to the last message exists.

When it compacts, Tau asks the model to summarize older messages, keeps a recent
suffix of the conversation, and continues. The original session file is never
edited — only the *active context* sent to the provider changes.

The summarizer is told that the conversation is chronological and that later
messages supersede earlier ones, so a requirement you changed or a plan the
agent abandoned is recorded in its final form rather than alongside the version
it replaced. If the assistant's last question to you (its last message ending in
`?` with no reply from you after it) falls in the summarized part, Tau appends it
verbatim to the summary under `## Open Question to User`, so the answer you type
next still has the question it answers. Messages that extensions inject do not
count as your reply. This applies to automatic and manual compaction alike.

The default threshold follows the model's context window minus a reserve. Providers
that advertise an explicit runtime threshold can override that default. In particular,
Codex subscription sessions discover account/rollout-specific limits from Codex's
authenticated model catalog because those limits can differ from the public OpenAI API.
You can override the resulting threshold for a run:

```bash
tau --auto-compact-threshold 100000
```

Automatic compaction is best-effort: if summarization fails, Tau logs it and keeps
the original context. During successful overflow recovery, the TUI shows compaction
and retry progress instead of presenting the intermediate provider rejection as a
terminal error. The error becomes visible only if recovery cannot complete.

## Manual compaction

Compact on demand any time:

```text
/compact
/compact focus on the database migration work
```

Optional text after `/compact` is added as extra focus for the summary. Like automatic
compaction, manual compaction summarizes an older prefix and keeps a recent suffix. If
there is not enough older context to summarize while retaining a real entry, Tau reports
that the context is too short to compact. Summary generation failures remain visible.

In the TUI, a manual compaction looks like a normal working turn: the prompt
activity indicator and terminal tab title animate while it runs, and a
turn-finished notification fires when it completes while the app is unfocused.
Press `Esc` to cancel a running compaction.

## Thinking modes

Some models can spend extra effort reasoning before answering. Tau exposes a
thinking level you can cycle:

```text
default → off → minimal → low → medium → high → xhigh → max
```

`default` hands the choice upstream: Tau uses the provider catalog's
`thinking_default` for the model, and when the catalog names none it sends no
thinking setting at all, so the API server's own default applies.

- **Shift+Tab** cycles the thinking level (default is `medium`).
- **Ctrl+T** toggles whether reasoning tokens are shown (hidden by default).
  Reasoning blocks are saved with the assistant response, so their original
  positions and visibility toggle are restored when you resume a session.

Thinking is model-aware: Tau enables it only when the active provider declares
supported levels for the active model. When it's unavailable, `/session` shows
the reason (e.g. the provider doesn't declare `thinking_levels`, or the model
isn't listed). Custom providers can opt in via `thinking_levels` in their config
— see [Configuration](/reference/configuration/#providers).

At startup Tau picks a valid level for the selected model automatically: a
remembered per-model choice wins, then `medium`, then the provider's own
default, then the first level the model supports. For example, `kimi-code:k3`
supports `low`, `high`, and `xhigh`; because `medium` is unavailable, it opens
at its `xhigh` catalog default instead of failing with "Thinking mode medium is
not available". Picking an unsupported level explicitly (via `/think` or the
thinking picker) still shows an error listing the available modes.

You can also set the startup level from the command line with `--thinking`
(`-t`), for example `tau -t high` or `tau -t max -p "explain this"`. The flag
takes precedence over remembered and catalog defaults for that run but is not
saved as a new default; requesting a level the selected model does not support
exits with an error listing the available modes. `--thinking default` is
accepted for every model, including ones with no thinking modes. Levels chosen interactively
afterwards (via `/think` or Shift+Tab) persist as usual.
