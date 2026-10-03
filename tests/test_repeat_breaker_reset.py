"""The repeat breaker forgets what a call gave once the workspace has changed."""

from __future__ import annotations

from pathlib import Path

import pytest

from pi_event_helpers import assistant_done, assistant_start
from tau_agent import AgentTool, AgentToolResult, AssistantMessage, TextContent, ToolCall
from tau_agent.messages import assistant_content
from tau_agent.session import JsonlSessionStorage
from tau_agent.types import JSONValue
from tau_ai import FakeProvider
from tau_coding import CodingSession, CodingSessionConfig


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _tool(name: str, ran: list[str]) -> AgentTool:
    async def execute(
        tool_call_id: object, arguments: object, signal: object = None, on_update: object = None
    ) -> AgentToolResult:
        ran.append(name)
        return AgentToolResult(content=[TextContent(text=f"{name}: same result")])

    return AgentTool(
        name=name,
        label=name,
        description=f"{name} something.",
        parameters={"type": "object"},
        execute_fn=execute,
    )


def _turns(calls: list[tuple[str, dict[str, JSONValue]]]) -> list[list[object]]:
    turns: list[list[object]] = [
        [
            assistant_start(model="fake"),
            assistant_done(
                message=AssistantMessage(
                    content=assistant_content(
                        "Calling.", [ToolCall(id=f"call-{i}", name=name, arguments=args)]
                    ),
                    stop_reason="toolUse",
                )
            ),
        ]
        for i, (name, args) in enumerate(calls)
    ]
    done = [assistant_start(model="fake"), assistant_done(message=AssistantMessage(content="Done"))]
    return [*turns, done]


@pytest.mark.anyio
async def test_repeat_breaker_resets_after_workspace_change(tmp_path: Path) -> None:
    # Run R02: a third `beagle pursuit commit` was refused as "would give it
    # again" after two pursuit_steps had rewritten the file it failed on.
    ran: list[str] = []
    commit: dict[str, JSONValue] = {"command": "beagle pursuit commit T0003 .gitignore"}
    step: dict[str, JSONValue] = {"task": "T0003"}
    calls = [("bash", commit), ("bash", commit), ("pursuit_step", step), ("bash", commit)]
    calls += [("bash", commit), ("bash", commit)]
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(_turns(calls)),
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[_tool("bash", ran), _tool("pursuit_step", ran)],
        )
    )

    async for _ in session.prompt("Go."):
        pass

    # Call, call, step, call, call all run; only the third after the step,
    # with the same result twice since the change, is a repeat.
    assert ran == ["bash", "bash", "pursuit_step", "bash", "bash"]
    results = [m for m in session.messages if m.role == "toolResult"]
    assert results[5].text.startswith("Not run: this `bash` call ran 2 times")


@pytest.mark.anyio
async def test_repeat_refusal_quotes_earlier_result(tmp_path: Path) -> None:
    # Run R03: pursuit_found refused a setup milestone, and its fourteen repeats
    # were each told only "use the result you already have".
    head = "pursuit_found: nothing written — 'setup' is not part of the goal's work. " * 6
    ran: list[str] = []

    async def execute(
        tool_call_id: object, arguments: object, signal: object = None, on_update: object = None
    ) -> AgentToolResult:
        ran.append("pursuit_found")
        return AgentToolResult(content=[TextContent(text=f"{head}\nLeave it out.")])

    found = AgentTool(
        name="pursuit_found",
        label="pursuit_found",
        description="Found a pursuit.",
        parameters={"type": "object"},
        execute_fn=execute,
    )
    args: dict[str, JSONValue] = {"milestones": ["setup", "impl"]}
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(_turns([("pursuit_found", args)] * 3)),
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[found],
        )
    )

    async for _ in session.prompt("Go."):
        pass

    assert ran == ["pursuit_found", "pursuit_found"]
    refusal = [m for m in session.messages if m.role == "toolResult"][2].text
    assert refusal.startswith("Not run: this `pursuit_found` call ran 2 times")
    assert f"It said: {head.strip()[:300]}" in refusal
    assert head.strip()[:301] not in refusal and "Leave it out." not in refusal
