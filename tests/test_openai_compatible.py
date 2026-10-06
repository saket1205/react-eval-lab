from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from react_eval_lab.providers.openai_compatible import OpenAICompatibleProvider, parse_tool_arguments


def test_parse_tool_arguments():
    assert parse_tool_arguments('{"query": "hq"}') == {"query": "hq"}
    assert parse_tool_arguments({"query": "hq"}) == {"query": "hq"}
    assert parse_tool_arguments("") == {}


def test_complete_maps_response_and_usage():
    provider = OpenAICompatibleProvider(model="test-model")
    provider.api_key = "sk-test"

    mock_fn = SimpleNamespace(name="search", arguments='{"query": "aurora"}')
    mock_tc = SimpleNamespace(id="call-1", function=mock_fn)
    mock_message = SimpleNamespace(
        content="Looking up Aurora.",
        tool_calls=[mock_tc],
    )
    mock_usage = SimpleNamespace(prompt_tokens=100, completion_tokens=20, total_tokens=120)
    mock_choice = SimpleNamespace(message=mock_message)
    mock_completion = SimpleNamespace(
        choices=[mock_choice],
        usage=mock_usage,
        model="test-model",
    )

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion

    with patch.object(provider, "_get_client", return_value=mock_client):
        response = provider.complete(
            [{"role": "user", "content": "hi"}],
            [{"type": "function", "function": {"name": "search"}}],
        )

    assert response.content == "Looking up Aurora."
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].name == "search"
    assert response.tool_calls[0].arguments == {"query": "aurora"}
    assert response.usage.prompt_tokens == 100
    assert response.usage.completion_tokens == 20
    assert response.usage.total_tokens == 120
    assert response.raw_model == "test-model"

    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "test-model"
    assert "tools" in call_kwargs
