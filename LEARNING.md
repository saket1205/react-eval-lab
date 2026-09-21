# 30-day learning log

Work in this repo. After each reading block, write answers in [notes.md](notes.md). Do not paste paper summaries; answer the prompts.

## Canonical sources

### 1. ReAct (required, days 1–4)

- Paper: https://arxiv.org/abs/2210.03629 (PDF: https://arxiv.org/pdf/2210.03629)
- Project page with trajectories: https://react-lm.github.io/

Read the HotpotQA example closely. Reason-only invents facts. Act-only retrieves but cannot synthesize. ReAct interleaves both.

Production mapping: `Thought` ≈ `message.content` before tools; `Action` ≈ `tool_calls`; `Observation` ≈ tool result appended to messages.

### 2. Building effective agents (required, days 8–10)

- https://www.anthropic.com/engineering/building-effective-agents

Steal three principles: keep the design simple; show the plan (your traces); invest in the agent-computer interface (tool names, descriptions, argument shapes) as much as the prompt.

Patterns to be able to sketch from memory: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, vs a true agent loop.

### 3. MCP specification (required, days 22–26)

- Spec index (2026-07-28): https://modelcontextprotocol.io/specification/2026-07-28
- Architecture: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
- Server concepts (tools / resources / prompts): https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts
- Tools: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- Spec blog for what changed: https://blog.modelcontextprotocol.io/posts/2026-07-28/

MCP is how hosts talk to tool servers. It is not an agent runtime. Your loop stays yours.

## Supporting (skim, do not rabbit-hole)

- LLM agents overview: https://lilianweng.github.io/posts/2023-06-23-agent/
- OpenAI function calling: https://platform.openai.com/docs/guides/function-calling
- Anthropic tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs
- Karpathy, intro to LLMs (for token intuition): https://www.youtube.com/watch?v=zjkBMFhNj_g

## Day-by-day

### Days 1–2 — Tokens and one API call

Call any OpenAI-compatible chat API once in a scratch script (not in this repo's loop yet). Print `usage`. Send one tool schema. Confirm you can parse `tool_calls`.

### Days 3–4 — ReAct paper

Fill notes.md section A. Sketch the loop on paper before coding.

### Days 5–7 — Implement `run_agent` against ScriptedLLM

`pytest tests/test_loop_scripted.py tests/test_tracer.py`

You are done with week 1 when those pass.

### Days 8–10 — Anthropic article

Fill notes.md section B. For each golden task, decide workflow vs agent.

### Days 11–14 — Harden ACI

Tighten tool descriptions in `tools.py` if needed. Add nothing that hardcodes golden answers. The scripted tests must still pass.

### Days 15–18 — Real provider + live eval

Implement `OpenAICompatibleProvider`. `python evals/run.py`. Iterate on prompt/tools, not on secretly special-casing task ids.

### Days 19–21 — Read traces

Pick a failed golden task. Write a short postmortem in notes.md section D: which event went wrong, what you changed, before/after.

### Days 22–26 — MCP

Read the spec pages above. Implement `handle_rpc`. `pytest tests/test_mcp.py`. Optionally route `run_agent` tool execution through `call_tool`.

### Days 27–30 — Freeze

Re-run evals. Confirm traces always have tokens. Write section E: what you would still not ship to production.

## Cheating that fails the sprint

- Importing an agent framework
- Hardcoding answers per `task_id`
- Skipping token usage and filling in fake numbers
- Using live web search instead of the Helios wiki
