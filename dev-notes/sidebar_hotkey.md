# Sidebar show/hide hotkey

## Problem

`/sidebar` toggles the session sidebar, but no key does. In a normal TUI
session the prompt owns every keystroke, so hiding the sidebar (for example to
gain width while a long tool result is on screen) means leaving the keyboard
flow and typing a slash command.

The toggle behavior already exists — it only needs a keybinding wired to it.

## Where the toggle lives today

- `src/tau_coding/commands.py:388` registers `/sidebar`; its handler
  `_sidebar_command` (line 767) returns
  `CommandResult(handled=True, sidebar_toggle_requested=True)`.
- The TUI consumes that flag at `src/tau_coding/tui/app.py:4421`, calling
  `TauTuiApp._toggle_sidebar_visibility()` (`app.py:6892`). That flips
  `self._sidebar_visibility_override`, then `_apply_sidebar_position()` and
  `_update_responsive_layout()` toggle the `-hide-sidebar` class
  (`app.py:3264`, `app.py:6874`).
- The override is deliberately session-only and never persisted
  (`app.py:3950`). `sidebar_position` in `~/.tau/tui.json` stays the durable
  setting; `/sidebar` and the new hotkey share the same transient semantics.
- Print mode already rejects the command as interactive-only (`cli.py`), and a
  hotkey is TUI-only by construction, so nothing is needed there.

## Keybinding plumbing

Mirror `toggle_tool_results` (Ctrl+O), the closest existing analogue: a
display-only toggle that must work while the prompt has focus.

1. **`src/tau_coding/tui/config.py:50`** — add a field to `TuiKeybindings`:

   ```python
   toggle_sidebar: str = "ctrl+b"
   ```

   and include it in `TuiKeybindings.to_json()`. Nothing else is required for
   persistence: `_keybindings_from_json` builds its values from
   `defaults.to_json()`, so omitted-key defaults, forward compatibility with
   newer key names, and `_reject_duplicate_keys` all come for free.

2. **`app.py:7425 _app_bindings()`** — add

   ```python
   Binding(keybindings.toggle_sidebar, "toggle_sidebar", "Sidebar"),
   ```

   so the key works when focus is not in the prompt.

3. **`app.py:7545 _hidden_prompt_bindings()`** — add
   `(keybindings.toggle_sidebar, "toggle_sidebar")` to the `candidates` tuple.
   The prompt (`PromptInput`) holds focus almost always, and these widget-level
   `priority=True` bindings are what actually fire while typing.

4. **`app.py:638`** — add a delegating `PromptInput.action_toggle_sidebar()`
   calling `self._completion_target().action_toggle_sidebar()`, and declare the
   action on the `CompletionActionTarget` Protocol (`app.py:510`).

5. **`app.py:829`** — add the explicit branch in `PromptInput.on_key`, next to
   the `toggle_tool_results` branch. Tau registers both a binding and an
   `on_key` branch for these toggles; stay consistent.

6. **`app.py:5979`** — add the app action beside `action_toggle_tool_results`:

   ```python
   def action_toggle_sidebar(self) -> None:
       """Toggle sidebar visibility for this session."""
       self._toggle_sidebar_visibility()
   ```

### Minimal alternative

Steps 1, 2 (with `priority=True`), and 6 alone work: Textual checks app-level
priority bindings in `App.on_event` before forwarding the key to the focused
widget, so the prompt cannot swallow it. Rejected because that variant also
fires while a modal screen is on the stack, and it breaks the convention every
other display toggle follows.

### Default key

`ctrl+b` is the conventional sidebar key, and a sweep of `TextArea` bindings,
`App.BINDINGS`, the `TuiKeybindings` defaults, and every `Binding(...)` literal
in `app.py` leaves it free. The one collision worth a docs line is tmux: `ctrl+b`
is the default prefix, so a tmux user's first press never reaches Tau and only
`ctrl+b ctrl+b` (tmux's `send-prefix`) toggles the sidebar; docs point those
users at remapping `toggle_sidebar` in `tui.json`.

Alternatives considered, all verified against the same sweep:

- `ctrl+y` — Textual's `TextArea` redo. The prompt's `on_key` branch consumes it
  first (a pilot `ctrl+z` then `ctrl+y` leaves the prompt empty and only hides
  the sidebar), so it would silently kill prompt redo.
- `ctrl+f` / `ctrl+l` — free while typing, but bound in the session-tree picker
  (`toggle_labeled_only`, `toggle_label_timestamps`).
- `ctrl+g`, `ctrl+n` — genuinely free everywhere and terminal-safe; rejected as
  non-mnemonic, and available as the documented escape hatch for tmux users.
- `ctrl+i` / `ctrl+m` / `ctrl+h` / `ctrl+j` — arrive as Tab / Enter / Backspace /
  newline, all already bound.
- `ctrl+1` — Textual defines the key, but legacy terminals send `\x01` for it,
  which decodes to `ctrl+a` (`cursor_line_start`); no kitty CSI-u path in the
  xterm parser to distinguish it.
- `alt+<letter>`, `ctrl+shift+<letter>` — free in-app, unreliable over legacy
  terminals (collapsing, and macOS Option producing glyphs).
- `ctrl+w` / `ctrl+u` — `TextArea` word/line deletion.

`_reject_duplicate_keys` raises `TuiConfigError` on any collision, so a bad
default fails loudly at startup instead of silently shadowing another action.

## Also update

- `/hotkeys` output list: `commands.py:508`.
- Docs: `website/content/reference/keybindings.md` (Output & session table),
  `website/content/reference/configuration.md:386` (keybindings JSON sample),
  `website/content/guides/tui.md:309`, and the bundled
  `src/tau_coding/data/docs/tui.md:26` `/sidebar` section.
- Tests: `tests/test_tui_config.py:168` (keybinding serialization) and a pilot
  test in `tests/test_tui_app.py` modeled on
  `test_tui_app_uses_configured_command_palette_keybinding` (line 7161),
  asserting `app.has_class("-hide-sidebar")` flips (pattern at lines 3248 and
  3416).

## Out of scope

Persisting the visibility choice. `_sidebar_visibility_override` stays
session-only, consistent with `/sidebar`; a durable change remains
`sidebar_position` in `~/.tau/tui.json` (written today through
`_replace_tui_settings`/`save_tui_settings`, `app.py:5402`), which would need
`sidebar_position`-style left/right/off handling rather than a boolean toggle.
