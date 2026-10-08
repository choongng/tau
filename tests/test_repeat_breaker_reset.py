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


def test_call_key_ignores_duplicate_list_entries() -> None:
    from tau_coding.session import _call_key

    def key(arguments: dict[str, JSONValue]) -> str:
        return _call_key(ToolCall(id="c", name="pursuit_step", arguments=arguments))

    base = key({"task": "T1", "locks": ["a.py", "b.py"]})
    assert key({"task": "T1", "locks": ["a.py", "b.py", "a.py", "a.py"]}) == base
    assert key({"task": "T1", "locks": ["a.py", "a.py", "b.py", "b.py"]}) == base
    nested = key({"opts": {"locks": ["x", "y"]}})
    assert key({"opts": {"locks": ["x", "x", "y", "x"]}}) == nested

    assert key({"task": "T1", "locks": ["b.py", "a.py"]}) != base
    assert key({"task": "T1", "locks": ["a.py"]}) != base
    assert key({"task": "T2", "locks": ["a.py", "b.py"]}) != base
    assert key({"task": "T1", "locks": ["a.py", "b.py", "c.py"]}) != base
    assert key({"flags": [1, True]}) != key({"flags": [1]})
    assert (
        _call_key(
            ToolCall(
                id="c", name="pursuit_found", arguments={"task": "T1", "locks": ["a.py", "b.py"]}
            )
        )
        != base
    )


@pytest.mark.anyio
async def test_repeated_call_quotes_sentence_holding_the_call(tmp_path: Path) -> None:
    # Run R32: the quoted head was cut before the call the refusal asked for,
    # and "It said: … closes on th" read as done.
    why = "step: T2 not changed — its data test already passes on the work on disk. " * 5
    ask = 'Send step task="T2" check="pytest -q" to close it.'
    texts = {
        "step": f"{why}{ask}\nThen go on.",
        "look": "look: " + 'the call that holds it is `step` task="T9" here. ' * 8,
    }
    ran: list[str] = []

    def tool(name: str) -> AgentTool:
        async def execute(
            tool_call_id: object, arguments: object, signal: object = None, on_update: object = None
        ) -> AgentToolResult:
            ran.append(name)
            return AgentToolResult(content=[TextContent(text=texts[name])])

        return AgentTool(
            name=name,
            label=name,
            description=f"{name} something.",
            parameters={"type": "object"},
            execute_fn=execute,
        )

    args: dict[str, JSONValue] = {"task": "T2"}
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(_turns([("step", args)] * 3 + [("look", args)] * 3)),
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[tool("step"), tool("look")],
        )
    )

    async for _ in session.prompt("Go."):
        pass

    assert ran == ["step", "step", "look", "look"]
    results = [m.text for m in session.messages if m.role == "toolResult"]
    # Cut before the call: the sentence holding it is quoted instead.
    assert f"It said: {ask} Do what that result asks" in results[2]
    assert why.strip()[:300] not in results[2]
    # A head that already holds the call is quoted as before.
    assert f"It said: {texts['look'].strip()[:300]} Do what" in results[5]
