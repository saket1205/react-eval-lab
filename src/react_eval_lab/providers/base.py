from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from react_eval_lab.types import LLMResponse


class LLMProvider(ABC):
    @abstractmethod
    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> LLMResponse:
        """One model turn. Must populate usage.prompt_tokens and usage.completion_tokens."""
