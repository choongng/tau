"""The thinking-off twin an output-limit nudge's request goes to.

R38 (dev-notes/itc-runs/R38.md, class 3): a tau-subagents child session had no
runtime provider config, so the twin could not be built. The failure was
swallowed on every nudge, and each nudged request went out with thinking on
with nothing to say so.
"""

import json
from pathlib import Path

import pytest

from tau_ai import FakeProvider
from tau_coding import CodingSession, OpenAICompatibleProviderConfig, ProviderSettings, TauPaths
from tau_coding import session as coding_session_module
from tau_coding.extensions.api import NotifyLevel, StderrUiBridge
from tau_coding.session import OUTPUT_LIMIT_NUDGE
from test_session_output_limit import _answers, _nudges, _run, _session, _truncated

PROVIDER_CONFIG = OpenAICompatibleProviderConfig(
    name="local",
    models=("fake",),
    default_model="fake",
    thinking_levels=("off", "low", "medium"),
    thinking_models=("fake",),
    thinking_default="medium",
    thinking_parameter="reasoning_effort",
)


class RecordingNotifications(StderrUiBridge):
    def __init__(self) -> None:
        self.notices: list[tuple[NotifyLevel, str]] = []

    def notify(self, message: str, level: NotifyLevel = "info") -> None:
        self.notices.append((level, message))


def _count_off_builds(monkeypatch: pytest.MonkeyPatch) -> list[object]:
    """Record each attempt to build a thinking-off provider."""
    attempts: list[object] = []
    build = CodingSession._build_runtime_provider

    def counting(self: CodingSession, **kwargs: object) -> object:
        if kwargs.get("thinking_level") == "off":
            attempts.append(kwargs)
        return build(self, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(CodingSession, "_build_runtime_provider", counting)
    return attempts


def _logged_warnings() -> list[dict[str, object]]:
    path = TauPaths().agent_calls_log_path
    if not path.exists():
        return []
    entries = [json.loads(line) for line in path.read_text().splitlines()]
    return [entry for entry in entries if entry["kind"] == "warning"]


@pytest.mark.anyio
async def test_thinking_off_twin_warns_once_when_the_build_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    attempts = _count_off_builds(monkeypatch)
    # As the R38 child was built: a provider, and no runtime provider config.
    provider = FakeProvider([_truncated(), _answers("A."), _truncated(), _answers("B.")])
    session = await _session(tmp_path, provider)
    ui = RecordingNotifications()
    session.extension_runtime.set_ui_bridge(ui)

    await _run(session)
    await _run(session, "Again.")

    # Both nudges went out, with thinking on, to the session's own provider.
    assert len(_nudges(session)) == 2
    assert [call[2][-1].text for call in provider.calls].count(OUTPUT_LIMIT_NUDGE) == 2
    # The twin was tried once, not on every nudge, and the session said so once.
    assert len(attempts) == 1
    assert len(ui.notices) == 1
    level, message = ui.notices[0]
    assert level == "warning"
    assert "no runtime provider config" in message
    assert "nudges keep thinking on" in message
    [logged] = _logged_warnings()
    assert logged["phase"] == "output_limit_nudge"
    assert logged["warning"] == {"message": message}


@pytest.mark.anyio
async def test_thinking_off_twin_warning_names_a_failed_build(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    main = FakeProvider([])

    def create(*args: object, thinking_level: object, **kwargs: object) -> FakeProvider:
        if thinking_level == "off":
            raise RuntimeError("Missing provider API key. Set LOCAL_API_KEY.")
        return main

    monkeypatch.setattr(coding_session_module, "_create_runtime_provider", create)
    session = await _session(
        tmp_path,
        main,
        provider_name="local",
        provider_settings=ProviderSettings(providers=(PROVIDER_CONFIG,)),
        runtime_provider_config=PROVIDER_CONFIG,
    )
    ui = RecordingNotifications()
    session.extension_runtime.set_ui_bridge(ui)
    provider = session._harness.config.provider

    assert session._thinking_off_provider(provider) is None
    assert session._thinking_off_provider(provider) is None

    [(level, message)] = ui.notices
    assert level == "warning"
    assert "Missing provider API key. Set LOCAL_API_KEY." in message


@pytest.mark.anyio
async def test_thinking_off_twin_is_returned_when_a_runtime_config_is_present(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    main = FakeProvider([])
    off = FakeProvider([])
    built: list[object] = []

    def create(*args: object, thinking_level: object, **kwargs: object) -> FakeProvider:
        built.append(thinking_level)
        return off if thinking_level == "off" else main

    monkeypatch.setattr(coding_session_module, "_create_runtime_provider", create)
    session = await _session(
        tmp_path,
        main,
        provider_name="local",
        provider_settings=ProviderSettings(providers=(PROVIDER_CONFIG,)),
        runtime_provider_config=PROVIDER_CONFIG,
    )
    ui = RecordingNotifications()
    session.extension_runtime.set_ui_bridge(ui)
    provider = session._harness.config.provider

    assert session._thinking_off_provider(provider) is off
    assert session._thinking_off_provider(provider) is off
    assert built.count("off") == 1
    assert ui.notices == []
    assert _logged_warnings() == []
