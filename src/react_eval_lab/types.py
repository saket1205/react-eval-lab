from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ToolCallRequest(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class LLMResponse(BaseModel):
    content: str | None = None
    tool_calls: list[ToolCallRequest] = Field(default_factory=list)
    usage: Usage = Field(default_factory=Usage)
    raw_model: str | None = None


class TraceEvent(BaseModel):
    type: Literal["llm", "tool", "stop"]
    step: int
    name: str
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    usage: Usage | None = None
    duration_ms: float = 0
    error: str | None = None


class Trace(BaseModel):
    task_id: str
    events: list[TraceEvent] = Field(default_factory=list)
    final_answer: str | None = None
    stop_reason: str | None = None
    total_usage: Usage = Field(default_factory=Usage)

    def add(self, event: TraceEvent) -> None:
        self.events.append(event)
        if event.usage:
            self.total_usage.prompt_tokens += event.usage.prompt_tokens
            self.total_usage.completion_tokens += event.usage.completion_tokens
            self.total_usage.total_tokens += event.usage.total_tokens
