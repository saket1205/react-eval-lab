from react_eval_lab.tracer import Tracer
from react_eval_lab.types import Usage


def test_require_complete_needs_tokens_and_tool_results():
    tracer = Tracer("t")
    with tracer.span("llm", "scripted", step=1) as event:
        event.usage = Usage(prompt_tokens=10, completion_tokens=4, total_tokens=14)
        event.output = {"content": "think"}
    with tracer.span("tool", "search", step=1, input={"query": "hq"}) as event:
        event.output = {"result": {"hits": []}}
    tracer.require_complete()


def test_require_complete_fails_without_usage():
    tracer = Tracer("t")
    with tracer.span("llm", "scripted", step=1) as event:
        event.output = {"content": "oops"}
    try:
        tracer.require_complete()
    except AssertionError as exc:
        assert "usage" in str(exc).lower() or "token" in str(exc).lower()
    else:
        raise AssertionError("expected incomplete trace to fail")
