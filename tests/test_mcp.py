import json

from react_eval_lab.mcp_server import handle_rpc


def test_tools_list():
    response = handle_rpc(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    )
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    names = {t["name"] for t in response["result"]["tools"]}
    assert names == {"search", "read_page", "list_employees", "calculate", "create_ticket"}
    search = next(t for t in response["result"]["tools"] if t["name"] == "search")
    assert "query" in search["inputSchema"]["properties"]


def test_tools_call_search():
    response = handle_rpc(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "aurora"}},
        }
    )
    text = response["result"]["content"][0]["text"]
    payload = json.loads(text)
    titles = [h["title"] for h in payload["hits"]]
    assert "Aurora project" in titles


def test_unknown_method():
    response = handle_rpc({"jsonrpc": "2.0", "id": 3, "method": "nope", "params": {}})
    assert "error" in response
