from __future__ import annotations

import json
import os
from typing import Any

from react_eval_lab.providers.base import LLMProvider
from react_eval_lab.types import LLMResponse, ToolCallRequest, Usage


class OpenAICompatibleProvider(LLMProvider):
    """Fill this in during week 3. Keep it thin: map API → LLMResponse, including usage."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4.1-mini")
        self.api_key = os.environ.get("LLM_API_KEY")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        # TODO(week3): call chat.completions (or Responses) with tools.
        # Must copy usage.prompt_tokens / completion_tokens into LLMResponse.usage.
        # Map tool_calls into ToolCallRequest (arguments are JSON strings on the wire).
        raise NotImplementedError("wire OpenAICompatibleProvider.complete in week 3")


def parse_tool_arguments(raw: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    return json.loads(raw or "{}")
