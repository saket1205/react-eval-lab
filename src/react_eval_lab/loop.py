"""You implement this. Do not import LangChain, LangGraph, CrewAI, or AutoGen."""

from __future__ import annotations

from typing import Any

from react_eval_lab.providers.base import LLMProvider
from react_eval_lab.tools import TOOL_SCHEMAS, execute_tool
from react_eval_lab.tracer import Tracer
from react_eval_lab.types import Trace


SYSTEM_PROMPT = """You are the Helios internal research agent.

Rules:
- Use tools to answer. Do not rely on training data for Helios facts.
- Search, then read_page, before stating a fact.
- For arithmetic, call calculate.
- create_ticket is a write: dry-run with confirm=false unless the user asked to open a ticket.
- If the wiki does not contain the answer, say you do not know. Never invent people, pets, offices, or budgets.
- When you are done, respond with a concise final answer and no further tool calls.
"""


def run_agent(
    question: str,
    provider: LLMProvider,
    *,
    task_id: str = "adhoc",
    max_steps: int = 8,
    tools: list[dict[str, Any]] | None = None,
) -> Trace:
    """ReAct loop with native tool calling.

    while not done and step < max_steps:
        1. LLM(messages, tools) → thought and/or tool_calls   # Reason
        2. log usage on the tracer
        3. if no tool_calls: stop with content as final answer
        4. else execute each tool, append observations, continue  # Act / Observe
        5. if max_steps hit: stop with reason max_steps

    Requirements:
    - Use Tracer.span("llm", ...) and Tracer.span("tool", ...).
    - Copy provider usage onto the llm TraceEvent.
    - Put tool results in event.output["result"].
    - Never swallow tool errors; put them in the observation the model sees.
    """
    _ = (question, provider, task_id, max_steps, tools or TOOL_SCHEMAS, execute_tool)
    raise NotImplementedError("implement run_agent in src/react_eval_lab/loop.py")
