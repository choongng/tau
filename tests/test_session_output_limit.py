"""A turn whose reasoning loops is cut early, and the output-limit nudge."""

from collections.abc import AsyncIterator, Iterable
from pathlib import Path

import pytest

from conftest import isolate_home
from pi_event_helpers import assistant_done, assistant_start
from tau_agent import (
    AgentMessage,
    AgentTool,
    AgentToolResult,
    AssistantMessage,
    TextContent,
    ThinkingContent,
    ToolCall,
    UserMessage,
)
from tau_agent.messages import assistant_content
from tau_agent.provider_events import ThinkingDeltaEvent
from tau_agent.session import JsonlSessionStorage
from tau_ai import CancellationToken, FakeProvider
from tau_ai.events import AssistantMessageEvent
from tau_coding import (
    CodingSession,
    CodingSessionConfig,
    OpenAICompatibleProviderConfig,
    ProviderSettings,
)
from tau_coding import session as coding_session_module
from tau_coding.session import OUTPUT_LIMIT_NUDGE

# R36 driver session, turn E76 (dev-notes/itc-runs/R36.md, class 1): gemma's
# reasoning opened like this, then went round the same block until the
# 8,192-token cap with no tool call.
R36_OPENING = """\
The `pursuit_step` says "no new route" because the `done_when` and `notes` are not different enough.
I'll change the `done_when` to be very different.
I'll use a `python3 -c` command that is very different.
I'll also include the `locks`.
I'll also include the `notes`.

"""
R36_ROUND = """\
Actually, I'll just run it.
I'll also add `docs/` to the scope.
I'll also check if `tests/test_case_data.py` exists.
I'll just run the step.

Actually, I'll use a different `done_when` that is very different.
I'll use a `python3 -c` command that is very different.
I'll also include the `locks`.
I'll also include the `notes`.

"""
CALL = ToolCall(id="call-1", name="fetch", arguments={})


class ClosingStreams:
    """A fake provider that records how far each stream was read."""

    def __init__(self, streams: Iterable[Iterable[AssistantMessageEvent]]) -> None:
        self._streams = [list(stream) for stream in streams]
        self.calls: list[list[AgentMessage]] = []
        self.read: list[int] = []
        self.closed: list[bool] = []

    def stream_response(
        self,
        *,
        model: str,
        system: str,
        messages: list[AgentMessage],
        tools: list[AgentTool],
        signal: CancellationToken | None = None,
        session_id: str | None = None,
    ) -> AsyncIterator[AssistantMessageEvent]:
        self.calls.append(list(messages))
        stream = self._streams.pop(0)
        index = len(self.read)
        self.read.append(0)
        self.closed.append(False)

        async def iterator() -> AsyncIterator[AssistantMessageEvent]:
            try:
                for event in stream:
                    self.read[index] += 1
                    yield event
            finally:
                self.closed[index] = True

        return iterator()


def _fetch_tool() -> AgentTool:
    async def fetch(
        tool_call_id: object,
        arguments: object,
        signal: object = None,
        on_update: object = None,
    ) -> AgentToolResult:
        return AgentToolResult(content=[TextContent(text="fetched")])

    return AgentTool(
        name="fetch",
        label="Fetch",
        description="Fetch a document.",
        parameters={"type": "object"},
        execute_fn=fetch,
    )


def _streamed_reasoning(text: str, *, then: AssistantMessage, chunk: int = 9) -> list[object]:
    """A response that streams `text` as reasoning, then ends with `then`."""
    deltas = [
        ThinkingDeltaEvent(
            content_index=0,
            delta=text[i : i + chunk],
            partial=AssistantMessage(content=[ThinkingContent(thinking=text[: i + chunk])]),
        )
        for i in range(0, len(text), chunk)
    ]
    return [assistant_start(), *deltas, assistant_done(message=then)]


def _acts() -> list[object]:
    return [assistant_start(), assistant_done(message=AssistantMessage(content=[CALL]))]


def _answers(text: str = "Done.") -> list[object]:
    return [assistant_start(), assistant_done(message=AssistantMessage(content=text))]


def _truncated() -> list[object]:
    return [
        assistant_start(),
        assistant_done(
            message=AssistantMessage(content=[ThinkingContent(thinking="Hmm. " * 50)]),
            finish_reason="length",
        ),
    ]


async def _session(tmp_path: Path, provider: object, **config: object) -> CodingSession:
    return await CodingSession.load(
        CodingSessionConfig(
            provider=provider,  # type: ignore[arg-type]
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[_fetch_tool()],
            **config,  # type: ignore[arg-type]
        )
    )


async def _run(session: CodingSession, prompt: str = "Design it.") -> None:
    async for _event in session.prompt(prompt):
        pass


def _nudges(session: CodingSession) -> list[UserMessage]:
    return [
        message
        for message in session.messages
        if isinstance(message, UserMessage) and message.text == OUTPUT_LIMIT_NUDGE
    ]


@pytest.mark.anyio
async def test_reasoning_repetition_stops_turn_as_output_limit(tmp_path: Path) -> None:
    looping = R36_OPENING + R36_ROUND * 40
    never_reached = AssistantMessage(content="The loop ran to its end.")
    provider = ClosingStreams(
        [_streamed_reasoning(looping, then=never_reached), _acts(), _answers()]
    )
    session = await _session(tmp_path, provider)

    await _run(session)

    cut = session.messages[1]
    assert isinstance(cut, AssistantMessage)
    assert cut.stop_reason == "length"
    assert [diagnostic.type for diagnostic in cut.diagnostics or []] == ["reasoning_loop_cut"]
    # Stopped well inside the loop, and the request was closed there.
    assert 0 < len(cut.thinking_text) < len(looping) // 4
    assert looping.startswith(cut.thinking_text)
    assert provider.read[0] < len(looping) // 9 // 4
    assert provider.closed[0]
    # Handled as a cut-off at the cap: nudged, and the reply acted.
    assert provider.calls[1][-1].text == OUTPUT_LIMIT_NUDGE
    assert len(provider.calls) == 3
    assert session.messages[-1].text == "Done."


@pytest.mark.anyio
@pytest.mark.parametrize(
    "looping",
    [
        "<|channel>thought\n" * 200,  # R36 E68: one token, a line each
        "thought " * 1_000,  # the same run with no line breaks
    ],
)
async def test_degenerate_token_run_is_cut(tmp_path: Path, looping: str) -> None:
    provider = ClosingStreams(
        [_streamed_reasoning(looping, then=AssistantMessage(content="x")), _answers()]
    )
    session = await _session(tmp_path, provider)

    await _run(session)

    cut = session.messages[1]
    assert isinstance(cut, AssistantMessage)
    assert cut.stop_reason == "length"
    assert len(cut.thinking_text) < len(looping)
    assert len(provider.calls) == 2


def _varied_reasoning(lines: int) -> str:
    """Long reasoning that comes back to a short line now and then."""
    out = []
    for i in range(lines):
        out.append(f"Case {i}: a node of depth {i % 7} splits into {i * 3 + 1} and {i * 5 + 2}.")
        if i % 60 == 0:
            out.append("Let me check that again.")
        if i % 9 == 0:
            out.append("")
    return "\n".join(out) + "\n"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "reasoning",
    [
        _varied_reasoning(400),
        # A long paragraph with no line breaks, varied throughout.
        " ".join(f"step {i} gives {i * i % 97}." for i in range(1_500)),
        # A short line said a few times among varied ones, in a short reply.
        "Hmm.\nThe left half is 1.\nHmm.\nThe right half is 0.\nHmm.\nSo the id is (1, 0).\n" * 3,
    ],
)
async def test_reasoning_without_repetition_is_not_cut(tmp_path: Path, reasoning: str) -> None:
    final = AssistantMessage(content=assistant_content("", [CALL]))
    provider = ClosingStreams([_streamed_reasoning(reasoning, then=final), _answers()])
    session = await _session(tmp_path, provider)

    await _run(session)

    message = session.messages[1]
    assert isinstance(message, AssistantMessage)
    assert message.stop_reason == "toolUse"
    assert not message.diagnostics
    assert not _nudges(session)
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_output_limit_nudge_request_sends_thinking_off(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
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
    main = FakeProvider([_truncated(), _answers("Second run.")])
    off = FakeProvider([_answers("Acted on the nudge.")])
    built: list[object] = []

    def create(*args: object, thinking_level: object, **kwargs: object) -> FakeProvider:
        built.append(thinking_level)
        return off if thinking_level == "off" else main

    monkeypatch.setattr(coding_session_module, "_create_runtime_provider", create)
    session = await _session(
        tmp_path,
        main,
        provider_name="local",
        provider_settings=ProviderSettings(providers=(provider_config,)),
        runtime_provider_config=provider_config,
    )
    assert session.thinking_level == "medium"
    assert "off" not in built

    await _run(session)

    # The nudge's request went to a thinking-off provider, built for it alone.
    assert built.count("off") == 1
    assert [call[2][-1].text for call in off.calls] == [OUTPUT_LIMIT_NUDGE]
    assert session.messages[-1].text == "Acted on the nudge."
    # The session's thinking level is unchanged, and the next run's request
    # goes to its own provider again.
    assert session.thinking_level == "medium"
    assert session.provider is main

    await _run(session, "And now?")

    assert len(main.calls) == 2
    assert len(off.calls) == 1
    assert session.messages[-1].text == "Second run."


@pytest.mark.anyio
async def test_per_run_nudge_bound_skips_nudges_whose_reply_acted(tmp_path: Path) -> None:
    # Each cut-off's nudge is answered with a tool call: the model is acting,
    # not thinking itself out of room, so the per-run bound of six does not
    # end the run at the seventh cut-off.
    provider = FakeProvider([*[_truncated(), _acts()] * 8, _answers()])
    session = await _session(tmp_path, provider)

    await _run(session)

    assert len(_nudges(session)) == 8
    assert session.messages[-1].text == "Done."


@pytest.mark.anyio
async def test_in_a_row_bound_still_stops_a_model_that_never_acts(tmp_path: Path) -> None:
    provider = FakeProvider([_truncated() for _ in range(5)])
    session = await _session(tmp_path, provider)

    await _run(session)

    assert len(_nudges(session)) == 2
    assert len(provider.calls) == 3
