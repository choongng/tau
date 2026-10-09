"""A tool call whose arguments carry chat-template tool-call tokens is refused."""

from pathlib import Path

import pytest

from pi_event_helpers import assistant_done, assistant_start
from tau_agent import AgentTool, AgentToolResult, AssistantMessage, TextContent, ToolCall
from tau_agent.messages import assistant_content
from tau_agent.session import JsonlSessionStorage
from tau_agent.types import JSONValue
from tau_ai import FakeProvider
from tau_coding import CodingSession, CodingSessionConfig, TauResourcePaths

#: Run R36's founding statement, as gemma sent it: the tail is the reply's
#: next call and its reasoning, run into this call's last string.
R36_STATEMENT = (
    "Implement interval tree clocks in Python; the fork/event/join behaviour "
    'is tested where it varies.",user_confirmed:false,user_delegated:true}'
    "<tool_call|><|channel>thought\nNow that the pursuit is founded, I will "
    "dispatch the first task.<channel|><|tool_call>call:bash{command:"
)
#: R36's W1 descriptions ended this way, on seven calls.
R36_DESCRIPTION = (
    'Run the known-answers test.\\"}<tool_call|><|channel>thought\n'
    "<channel|><|tool_call>call:bash{command:"
)
#: The qwen form R02 and R15 left at the end of a worker's text.
QWEN_SPILL = "Report written.</tool_call>\n<tool_call>\n<function=bash>\n<parameter=command>"


def _turns(name: str, *arguments: dict[str, JSONValue]) -> list[list[object]]:
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
        for i, args in enumerate(arguments)
    ]
    turns.append(
        [assistant_start(model="fake"), assistant_done(message=AssistantMessage(content="Done"))]
    )
    return turns


def _recording_tool(ran: list[object]) -> AgentTool:
    async def record(
        tool_call_id: object, arguments: object, signal: object = None, on_update: object = None
    ) -> AgentToolResult:
        ran.append(arguments)
        return AgentToolResult(content=[TextContent(text=f"ran {len(ran)}")])

    return AgentTool(
        name="note",
        label="Note",
        description="Record a note.",
        parameters={"type": "object"},
        execute_fn=record,
    )


async def _run(session: CodingSession) -> list[str]:
    async for _ in session.prompt("Go."):
        pass
    return [m.text for m in session.messages if m.role == "toolResult"]


async def _run_note(
    tmp_path: Path, *arguments: dict[str, JSONValue]
) -> tuple[list[object], list[str]]:
    ran: list[object] = []
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(_turns("note", *arguments)),
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[_recording_tool(ran)],
        )
    )
    return ran, await _run(session)


@pytest.mark.anyio
async def test_tool_args_with_template_tokens_refused(tmp_path: Path) -> None:
    founding: dict[str, JSONValue] = {"statement": R36_STATEMENT, "user_delegated": True}
    nested: dict[str, JSONValue] = {"tasks": [{"title": "W1", "description": R36_DESCRIPTION}]}

    ran, results = await _run_note(tmp_path, founding, nested, {"text": "plain"})

    assert ran == [{"text": "plain"}]
    assert results[0].startswith(
        "Not run: its arguments carry the chat template's own tool-call tokens "
        "(`<tool_call|>` in `statement`), so the reply's next call ran into this one; "
        "send one call per reply, with the text alone. 7 more refused calls in a row "
        "stop the run."
    )
    # A string at any depth is read, and the refusals count toward the stop.
    assert "(`<tool_call|>` in `tasks[0].description`)" in results[1]
    assert "6 more refused calls in a row" in results[1]


@pytest.mark.anyio
async def test_tool_args_with_spilled_qwen_call_refused(tmp_path: Path) -> None:
    json_form = 'Done.<tool_call>\n{"name": "bash", "arguments": {"command": "ls"}}'

    ran, results = await _run_note(tmp_path, {"text": QWEN_SPILL}, {"text": json_form})

    assert ran == []
    assert "(`<tool_call>` in `text`)" in results[0]
    assert "(`<tool_call>` in `text`)" in results[1]


@pytest.mark.anyio
async def test_extension_tool_args_with_template_tokens_refused(tmp_path: Path) -> None:
    # Extension tools, and so beagle's, take the same path; a sub-agent's
    # session is a CodingSession too, so its calls do as well.
    paths = TauResourcePaths(
        root=tmp_path / "home-tau", cwd=tmp_path / "project", agents_root=tmp_path / "agents"
    )
    assert paths.cwd is not None
    paths.cwd.mkdir(parents=True)
    log = tmp_path / "ran.log"
    extensions = paths.root / "extensions"
    extensions.mkdir(parents=True)
    (extensions / "founder.py").write_text(
        f"""
from pathlib import Path

from tau_agent.tools import AgentTool, AgentToolResult


async def _run(tool_call_id, arguments, signal=None, on_update=None):
    with Path({str(log)!r}).open("a") as log:
        log.write(arguments["statement"] + "\\n")
    return AgentToolResult(content="founded")


def setup(tau):
    tau.register_tool(
        AgentTool(
            name="pursuit_found",
            label="Found",
            description="Found a pursuit.",
            parameters={{"type": "object", "properties": {{"statement": {{"type": "string"}}}}}},
            execute_fn=_run,
        )
    )
""",
        encoding="utf-8",
    )
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(
                _turns("pursuit_found", {"statement": R36_STATEMENT}, {"statement": "Clean goal."})
            ),
            model="fake",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=paths.cwd,
            resource_paths=paths,
        )
    )
    assert "pursuit_found" in [tool.name for tool in session.tools]

    results = await _run(session)

    assert log.read_text() == "Clean goal.\n"
    assert results[0].startswith("Not run: its arguments carry the chat template's own")
    assert results[1] == "founded"


@pytest.mark.anyio
async def test_tool_args_with_ordinary_angle_brackets_run(tmp_path: Path) -> None:
    ordinary: list[str] = [
        '<html><body><p class="x">a</p></body></html>',
        '<?xml version="1.0"?><config><item name="a"/></config>',
        "List<String> names = new ArrayList<>();",
        "if a < b > c: pass",
        "The tool_call field names the channel the reply came on.",
        "Qwen wraps a call in <tool_call> tags; gemma's own tokens differ.",
        "<|endoftext|> and <tool_call/> and <channel> are not the forms refused.",
    ]

    ran, results = await _run_note(tmp_path, *({"text": text} for text in ordinary))

    assert ran == [{"text": text} for text in ordinary]
    assert not any(r.startswith("Not run") for r in results)
