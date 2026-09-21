from __future__ import annotations

from typing import Any, Iterable

from react_eval_lab.providers.base import LLMProvider
from react_eval_lab.types import LLMResponse, ToolCallRequest, Usage


class ScriptedLLM(LLMProvider):
    """Deterministic stand-in so you can unit-test the loop with zero API spend."""

    def __init__(self, script: Iterable[LLMResponse]) -> None:
        self._script = list(script)
        self.calls = 0
        self.messages_seen: list[list[dict[str, Any]]] = []

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        self.messages_seen.append(messages)
        if self.calls >= len(self._script):
            raise RuntimeError("ScriptedLLM ran out of responses — your loop is not stopping")
        response = self._script[self.calls]
        self.calls += 1
        return response


def thought(text: str, prompt_tokens: int = 40, completion_tokens: int = 20) -> LLMResponse:
    return LLMResponse(
        content=text,
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
        raw_model="scripted",
    )


def call_tool(
    name: str,
    arguments: dict[str, Any],
    thought_text: str = "",
    call_id: str = "call-1",
    prompt_tokens: int = 40,
    completion_tokens: int = 12,
) -> LLMResponse:
    return LLMResponse(
        content=thought_text or None,
        tool_calls=[ToolCallRequest(id=call_id, name=name, arguments=arguments)],
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
        raw_model="scripted",
    )
