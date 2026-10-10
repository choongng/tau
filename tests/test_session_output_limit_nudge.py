"""The output-limit nudge with another message queued beside it.

R38 (mimo, a tau-subagents `agent` session): the turn that hit the output limit
also ended the run with an empty message, so tau-subagents queued its report
request as steering beside the nudge. The steering went first and took the
nudge's thinking-off request, and the nudge, delivered a turn late, kept one
nudge queued ahead of each cut-off: four nudges ran in a row past the bound.
"""

from pathlib import Path

import pytest

from conftest import isolate_home
from tau_ai import FakeProvider
from tau_coding import CodingSession, OpenAICompatibleProviderConfig, ProviderSettings
from tau_coding import session as coding_session_module
from tau_coding.session import MAX_OUTPUT_LIMIT_CONTINUATIONS, OUTPUT_LIMIT_NUDGE
from test_session_output_limit import _answers, _nudges, _session, _truncated

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


@pytest.mark.anyio
async def test_thinking_off_request_is_the_nudges_not_a_steering_reply(
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
    main = FakeProvider([_truncated(), _answers("Reported.")])
    off = FakeProvider([_answers("Acted on the nudge.")])

    def create(*args: object, thinking_level: object, **kwargs: object) -> FakeProvider:
        return off if thinking_level == "off" else main

    monkeypatch.setattr(coding_session_module, "_create_runtime_provider", create)
    session = await _session(
        tmp_path,
        main,
        provider_name="local",
        provider_settings=ProviderSettings(providers=(provider_config,)),
        runtime_provider_config=provider_config,
    )

    await _run_with_report_request(session)

    # The report request's reply goes with the session's thinking level; the
    # nudge's own request, sent after it, is the one with thinking off.
    assert [call[2][-1].text for call in main.calls] == ["Design it.", REPORT_REQUEST]
    assert [call[2][-1].text for call in off.calls] == [OUTPUT_LIMIT_NUDGE]
    assert session.messages[-1].text == "Acted on the nudge."
