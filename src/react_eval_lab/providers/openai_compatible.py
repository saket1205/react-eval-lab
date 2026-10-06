from __future__ import annotations

import json
import os
from typing import Any

from react_eval_lab.providers.base import LLMProvider
from react_eval_lab.types import LLMResponse, ToolCallRequest, Usage


class OpenAICompatibleProvider(LLMProvider):
    """Thin adapter: OpenAI-compatible chat.completions → LLMResponse."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4.1-mini")
        self.api_key = os.environ.get("LLM_API_KEY")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            if not self.api_key:
                raise RuntimeError("Set LLM_API_KEY in the environment (see .env.example)")
            from openai import OpenAI

            self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return self._client

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        completion = self._get_client().chat.completions.create(**kwargs)
        message = completion.choices[0].message

        tool_calls: list[ToolCallRequest] = []
        for tc in message.tool_calls or []:
            fn = tc.function
            tool_calls.append(
                ToolCallRequest(
                    id=tc.id,
                    name=fn.name,
                    arguments=parse_tool_arguments(fn.arguments),
                )
            )

        raw_usage = completion.usage
        usage = Usage(
            prompt_tokens=(raw_usage.prompt_tokens if raw_usage else 0) or 0,
            completion_tokens=(raw_usage.completion_tokens if raw_usage else 0) or 0,
            total_tokens=(raw_usage.total_tokens if raw_usage else 0) or 0,
        )
        if usage.total_tokens <= 0 and (usage.prompt_tokens or usage.completion_tokens):
            usage.total_tokens = usage.prompt_tokens + usage.completion_tokens

        return LLMResponse(
            content=message.content,
            tool_calls=tool_calls,
            usage=usage,
            raw_model=completion.model,
        )


def parse_tool_arguments(raw: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    return json.loads(raw or "{}")
