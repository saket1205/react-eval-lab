from __future__ import annotations

import ast
import operator
from typing import Any, Callable

from react_eval_lab import world

TICKETS: list[dict[str, Any]] = []

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _eval_calc(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_calc(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_BINOPS:
        return float(_ALLOWED_BINOPS[type(node.op)](_eval_calc(node.operand)))  # type: ignore[operator]
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        return float(_ALLOWED_BINOPS[type(node.op)](_eval_calc(node.left), _eval_calc(node.right)))
    raise ValueError("only +, -, *, / on numbers are allowed")


def tool_search(query: str) -> dict[str, Any]:
    return {"hits": world.search_pages(query)}


def tool_read_page(title: str) -> dict[str, Any]:
    return world.read_page(title)


def tool_list_employees(query: str) -> dict[str, Any]:
    return {"employees": world.find_employees(query)}


def tool_calculate(expression: str) -> dict[str, Any]:
    tree = ast.parse(expression, mode="eval")
    return {"expression": expression, "value": _eval_calc(tree)}


def tool_create_ticket(
    title: str,
    body: str,
    employee_id: str,
    confirm: bool = False,
) -> dict[str, Any]:
    if not confirm:
        return {
            "status": "blocked",
            "reason": "refusing write without confirm=true. Re-call with confirm=true if the user asked to create the ticket.",
        }
    ticket = {
        "id": f"tck-{len(TICKETS) + 1:04d}",
        "title": title,
        "body": body,
        "employee_id": employee_id,
        "status": "open",
    }
    TICKETS.append(ticket)
    return {"status": "created", "ticket": ticket}


TOOL_IMPLS: dict[str, Callable[..., Any]] = {
    "search": tool_search,
    "read_page": tool_read_page,
    "list_employees": tool_list_employees,
    "calculate": tool_calculate,
    "create_ticket": tool_create_ticket,
}

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Keyword search over the Helios internal wiki. Returns titles and snippets. "
                "Use this before answering factual questions. Then call read_page on a title."
            ),
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": (
                "Read a wiki page by exact title from search hits "
                "(Helios overview, Offices, Aurora project, Travel policy, Laptop support)."
            ),
            "parameters": {
                "type": "object",
                "properties": {"title": {"type": "string"}},
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_employees",
            "description": "Lookup employees by name fragment, role, or id (emp-####).",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a numeric expression with + - * /. Use for money and counts. Do not guess arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": (
                "Create an IT ticket. This is a WRITE. First call with confirm=false is a dry-run. "
                "Only call with confirm=true when the user clearly asked to open the ticket and you have employee_id."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "employee_id": {"type": "string"},
                    "confirm": {"type": "boolean"},
                },
                "required": ["title", "body", "employee_id", "confirm"],
            },
        },
    },
]


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name not in TOOL_IMPLS:
        return {"error": f"unknown tool: {name}"}
    try:
        return TOOL_IMPLS[name](**arguments)
    except TypeError as exc:
        return {"error": f"bad arguments for {name}: {exc}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
