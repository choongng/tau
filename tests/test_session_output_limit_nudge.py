"""The output-limit nudge with another message queued beside it.

R38 (mimo, a tau-subagents `agent` session): the turn that hit the output limit
also ended the run with an empty message, so tau-subagents queued its report
request as steering beside the nudge. The steering went first and took the
nudge's request, and the nudge, delivered a turn late, kept one nudge queued
ahead of each cut-off: four nudges ran in a row past the bound.
"""

from pathlib import Path

import pytest

from conftest import isolate_home
from tau_agent import AssistantMessage
from tau_agent.messages import ThinkingContent
from tau_ai import FakeProvider
from tau_coding import CodingSession, OpenAICompatibleProviderConfig, ProviderSettings
from tau_coding import session as coding_session_module
from tau_coding.session import (
    LOOP_CUT_NUDGE,
    MAX_OUTPUT_LIMIT_CONTINUATIONS,
    OUTPUT_LIMIT_NUDGE,
    TIME_CUT_NUDGE,
    TURN_REASONING_SECONDS_ENV,
)
from test_session_output_limit import (
    R36_OPENING,
    R36_ROUND,
    _answers,
    _nudges,
    _session,
    _streamed_reasoning,
    _truncated,
)

REPORT_REQUEST = "Your last message was empty. Reply now with your final report."


async def _run_with_report_request(session: CodingSession) -> None:
    """Run a prompt, steering a report request in at the first turn's end."""
    requested = False
    async for event in session.prompt("Design it."):
        if getattr(event, "type", None) == "turn_end" and not requested:
            requested = True
            session.queue_steering_message(REPORT_REQUEST)


@pytest.mark.anyio
async def test_nudges_in_a_row_stay_bounded_with_a_steering_message_beside_one(
    tmp_path: Path,
) -> None:
    provider = FakeProvider([_truncated() for _ in range(8)])
    session = await _session(tmp_path, provider)

    await _run_with_report_request(session)

    # The reply to the report request is cut off while the nudge is still
    # queued: no second nudge goes in behind it, and the bound holds.
    assert len(_nudges(session)) == MAX_OUTPUT_LIMIT_CONTINUATIONS
    assert len(provider.calls) == 4


async def _thinking_session(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, main: FakeProvider, built: list[object]
) -> CodingSession:
    """A session on `main` at thinking medium that records each provider built."""
    isolate_home(monkeypatch, tmp_path)
    provider_config = OpenAICompatibleProviderConfig(
        name="local",
        models=("fake",),
        default_model="fake",
        thinking_levels=("off", "low", "medium"),
        thinking_models=("fake",),
        thinking_default="medium",
        thinking_parameter="reasoning_effort",
    )

    def create(*args: object, thinking_level: object, **kwargs: object) -> FakeProvider:
        built.append(thinking_level)
        return main

    monkeypatch.setattr(coding_session_module, "_create_runtime_provider", create)
    session = await _session(
        tmp_path,
        main,
        provider_name="local",
        provider_settings=ProviderSettings(providers=(provider_config,)),
        runtime_provider_config=provider_config,
    )
    built.clear()
    return session


@pytest.mark.anyio
async def test_nudge_after_a_steering_reply_keeps_the_session_provider(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    main = FakeProvider([_truncated(), _answers("Reported."), _answers("Acted on the nudge.")])
    built: list[object] = []
    session = await _thinking_session(monkeypatch, tmp_path, main, built)

    await _run_with_report_request(session)

    # The report request's reply goes first, then the nudge's; both go to the
    # session's provider at its thinking level, so the prompt prefix holds.
    assert [call[2][-1].text for call in main.calls] == [
        "Design it.",
        REPORT_REQUEST,
        OUTPUT_LIMIT_NUDGE,
    ]
    assert built == []
    assert session.messages[-1].text == "Acted on the nudge."
    assert session.thinking_level == "medium"


@pytest.mark.anyio
async def test_loop_cut_nudge_keeps_the_session_provider(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # R42 (dev-notes/itc-runs/R42.md, class 4): a nudge after a loop cut went
    # thinking-off, and on gemma's template that re-prefilled the prompt twice.
    looping = R36_OPENING + R36_ROUND * 40
    never_reached = AssistantMessage(content="The loop ran to its end.")
    main = FakeProvider(
        [_streamed_reasoning(looping, then=never_reached), _answers("Acted on the nudge.")]
    )
    built: list[object] = []
    session = await _thinking_session(monkeypatch, tmp_path, main, built)

    async for _event in session.prompt("Design it."):
        pass

    cut = session.messages[1]
    assert isinstance(cut, AssistantMessage)
    assert [diagnostic.type for diagnostic in cut.diagnostics or []] == ["reasoning_loop_cut"]
    assert [call[2][-1].text for call in main.calls] == ["Design it.", LOOP_CUT_NUDGE]
    assert built == []
    assert session.messages[-1].text == "Acted on the nudge."
    assert session.thinking_level == "medium"


@pytest.mark.anyio
async def test_output_limit_cut_nudge_keeps_the_session_provider(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    main = FakeProvider([_truncated(), _answers("Acted on the nudge.")])
    built: list[object] = []
    session = await _thinking_session(monkeypatch, tmp_path, main, built)

    async for _event in session.prompt("Design it."):
        pass

    cut = session.messages[1]
    assert isinstance(cut, AssistantMessage)
    assert cut.stop_reason == "length"
    assert not cut.diagnostics
    assert [call[2][-1].text for call in main.calls] == ["Design it.", OUTPUT_LIMIT_NUDGE]
    assert built == []
    assert session.messages[-1].text == "Acted on the nudge."
    assert session.thinking_level == "medium"


@pytest.mark.anyio
async def test_reasoning_past_the_turn_budget_is_cut_and_asked_to_act(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # S06 (q35): a worker reasoned 16k tokens, about 11 min, checking by hand
    # values one run settles. With a budget set, the turn is cut and its
    # reasoning kept for the nudge to build on.
    monkeypatch.setenv(TURN_REASONING_SECONDS_ENV, "5")
    ticks = iter(range(1000))
    monkeypatch.setattr(coding_session_module, "_reasoning_clock", lambda: next(ticks))
    long = " ".join(f"Byte {n} holds bits {n * 7} to {n * 7 + 6}." for n in range(40))
    never_reached = AssistantMessage(content="The reasoning ran to its end.")
    main = FakeProvider(
        [_streamed_reasoning(long, then=never_reached), _answers("Acted on the nudge.")]
    )
    built: list[object] = []
    session = await _thinking_session(monkeypatch, tmp_path, main, built)

    async for _event in session.prompt("Encode it."):
        pass

    cut = session.messages[1]
    assert isinstance(cut, AssistantMessage)
    assert cut.stop_reason == "length"
    assert [diagnostic.type for diagnostic in cut.diagnostics or []] == ["reasoning_time_cut"]
    assert [call[2][-1].text for call in main.calls] == ["Encode it.", TIME_CUT_NUDGE]
    replayed = main.calls[1][2][1]
    assert isinstance(replayed, AssistantMessage)
    assert any(isinstance(block, ThinkingContent) for block in replayed.content)
    assert session.messages[-1].text == "Acted on the nudge."


@pytest.mark.anyio
async def test_reasoning_has_no_time_budget_unless_the_run_sets_one(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv(TURN_REASONING_SECONDS_ENV, raising=False)
    ticks = iter(range(0, 100000, 100))
    monkeypatch.setattr(coding_session_module, "_reasoning_clock", lambda: next(ticks))
    long = " ".join(f"Byte {n} holds bits {n * 7} to {n * 7 + 6}." for n in range(40))
    main = FakeProvider([_streamed_reasoning(long, then=AssistantMessage(content="Done."))])
    built: list[object] = []
    session = await _thinking_session(monkeypatch, tmp_path, main, built)

    async for _event in session.prompt("Encode it."):
        pass

    assert session.messages[-1].text == "Done."
    assert len(main.calls) == 1
