import pytest

from react_eval_lab.loop import run_agent
from react_eval_lab.providers.scripted import ScriptedLLM, call_tool, thought
from react_eval_lab.tools import TICKETS
from react_eval_lab.types import LLMResponse, Usage


def setup_function() -> None:
    TICKETS.clear()


def test_search_read_then_answer():
    provider = ScriptedLLM(
        [
            call_tool("search", {"query": "headquarters"}, thought_text="Need wiki."),
            call_tool("read_page", {"title": "Helios overview"}, call_id="call-2"),
            thought("Headquarters are in Seattle, Washington."),
        ]
    )
    trace = run_agent("Where is HQ?", provider, task_id="hq_location", max_steps=8)
    assert trace.stop_reason == "final_answer"
    assert "seattle" in (trace.final_answer or "").lower()
    names = [e.name for e in trace.events if e.type == "tool"]
    assert names == ["search", "read_page"]
    llm_events = [e for e in trace.events if e.type == "llm"]
    assert all(e.usage and e.usage.total_tokens > 0 for e in llm_events)
    tool_events = [e for e in trace.events if e.type == "tool"]
    assert all("result" in e.output for e in tool_events)
    assert provider.calls == 3


def test_create_ticket_blocked_without_confirm_then_writes():
    provider = ScriptedLLM(
        [
            call_tool("list_employees", {"query": "Raj Patel"}),
            call_tool(
                "create_ticket",
                {
                    "title": "Replace laptop",
                    "body": "hardware failure",
                    "employee_id": "emp-2219",
                    "confirm": False,
                },
                call_id="call-2",
            ),
            call_tool(
                "create_ticket",
                {
                    "title": "Replace laptop",
                    "body": "hardware failure",
                    "employee_id": "emp-2219",
                    "confirm": True,
                },
                call_id="call-3",
            ),
            thought("Opened ticket tck-0001 for Raj Patel."),
        ]
    )
    trace = run_agent("Open a ticket for Raj's laptop", provider, task_id="laptop_ticket")
    assert trace.stop_reason == "final_answer"
    statuses = []
    for event in trace.events:
        if event.type == "tool" and event.name == "create_ticket":
            statuses.append(event.output["result"]["status"])
    assert statuses == ["blocked", "created"]
    assert TICKETS[0]["employee_id"] == "emp-2219"


def test_max_steps_stops_and_logs():
    provider = ScriptedLLM(
        [
            call_tool("search", {"query": "helios"}, call_id=f"c{i}")
            for i in range(6)
        ]
    )
    trace = run_agent("research forever", provider, task_id="step_budget", max_steps=3)
    assert trace.stop_reason == "max_steps"
    assert len([e for e in trace.events if e.type == "llm"]) == 3
    assert provider.calls == 3


def test_tool_error_is_observed_not_raised():
    provider = ScriptedLLM(
        [
            call_tool("calculate", {"expression": "import os"}),
            thought("The calculator rejected that expression. I cannot compute it."),
        ]
    )
    trace = run_agent("run python in calculate", provider, task_id="calc_err")
    calc = next(e for e in trace.events if e.type == "tool")
    assert "error" in calc.output["result"]
    assert trace.stop_reason == "final_answer"


def test_out_of_script_means_you_did_not_stop():
    provider = ScriptedLLM(
        [
            LLMResponse(
                content="partial",
                tool_calls=[],
                usage=Usage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
            )
        ]
    )
    # If implementation forgets to stop on empty tool_calls, ScriptedLLM raises.
    try:
        trace = run_agent("hi", provider, max_steps=5)
    except NotImplementedError:
        pytest.fail("implement run_agent")
    except RuntimeError:
        pytest.fail("loop did not stop after a final message with no tool calls")
    else:
        assert trace.stop_reason == "final_answer"
