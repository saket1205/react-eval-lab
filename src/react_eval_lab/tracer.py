from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from react_eval_lab.types import Trace, TraceEvent, Usage


class Tracer:
    """Every LLM call and tool call must go through this. Graders fail incomplete traces."""

    def __init__(self, task_id: str) -> None:
        self.trace = Trace(task_id=task_id)

    @contextmanager
    def span(
        self,
        type: str,
        name: str,
        step: int,
        input: dict[str, Any] | None = None,
    ) -> Iterator[TraceEvent]:
        event = TraceEvent(
            type=type,  # type: ignore[arg-type]
            name=name,
            step=step,
            input=input or {},
        )
        started = time.perf_counter()
        try:
            yield event
        except Exception as exc:  # noqa: BLE001 — we want the failure in the trace
            event.error = str(exc)
            raise
        finally:
            event.duration_ms = (time.perf_counter() - started) * 1000
            self.trace.add(event)

    def stop(self, reason: str, step: int, final_answer: str | None) -> Trace:
        self.trace.stop_reason = reason
        self.trace.final_answer = final_answer
        self.trace.events.append(
            TraceEvent(type="stop", name=reason, step=step, output={"answer": final_answer})
        )
        return self.trace

    def require_complete(self) -> None:
        llm_events = [e for e in self.trace.events if e.type == "llm"]
        if not llm_events:
            raise AssertionError("trace has no llm events")
        for event in llm_events:
            if event.usage is None:
                raise AssertionError(f"llm event {event.step} missing usage")
            if event.usage.total_tokens <= 0 and event.usage.prompt_tokens <= 0:
                raise AssertionError(
                    f"llm event {event.step} has zero tokens — log prompt+completion usage"
                )
        for event in self.trace.events:
            if event.type == "tool" and "result" not in event.output:
                raise AssertionError(f"tool {event.name} at step {event.step} missing result")
