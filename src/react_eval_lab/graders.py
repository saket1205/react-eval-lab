from __future__ import annotations

from typing import Any

from react_eval_lab.types import Trace


def grade_trace(trace: Trace, spec: dict[str, Any]) -> dict[str, Any]:
    answer = (trace.final_answer or "").lower()
    tool_names = [e.name for e in trace.events if e.type == "tool"]
    checks: dict[str, bool] = {}

    for needle in spec.get("answer_contains", []):
        checks[f"answer_contains:{needle}"] = needle.lower() in answer

    any_needles = spec.get("answer_contains_any", [])
    if any_needles:
        checks["answer_contains_any"] = any(n.lower() in answer for n in any_needles)

    for needle in spec.get("answer_excludes", []):
        checks[f"answer_excludes:{needle}"] = needle.lower() not in answer

    for name in spec.get("require_tools", []):
        checks[f"require_tool:{name}"] = name in tool_names

    for name in spec.get("forbid_tools", []):
        checks[f"forbid_tool:{name}"] = name not in tool_names

    if spec.get("stop_reason"):
        checks["stop_reason"] = trace.stop_reason == spec["stop_reason"]

    if spec.get("require_complete_trace", True):
        try:
            # Imported lazily so graders work even if loop is unfinished
            from react_eval_lab.tracer import Tracer

            t = Tracer(trace.task_id)
            t.trace = trace
            t.require_complete()
            checks["complete_trace"] = True
        except AssertionError:
            checks["complete_trace"] = False

    if spec.get("created_ticket"):
        created = False
        for event in trace.events:
            if event.type != "tool" or event.name != "create_ticket":
                continue
            result = event.output.get("result") or {}
            if isinstance(result, dict) and result.get("status") == "created":
                created = True
        checks["created_ticket"] = created

    passed = all(checks.values()) if checks else False
    return {"passed": passed, "checks": checks, "answer": trace.final_answer, "stop": trace.stop_reason}
