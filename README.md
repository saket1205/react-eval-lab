# ReAct eval lab (30-day sprint)

Closed-world Helios Corp research agent. **You implement** `run_agent`, the OpenAI-compatible provider, and the MCP JSON-RPC dispatcher. The wiki, tools, tracer, graders, and golden set are given so you can tell if the learning is real.

Frameworks are banned: no LangChain, LangGraph, CrewAI, AutoGen.

## Setup

```bash
cd /Users/saketgupta/personal/react-eval-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Week 3+: `cp .env.example .env` and `pip install -e ".[dev,openai]"`.

## How you are graded

| Layer | Command | Needs API key | What it proves |
| --- | --- | --- | --- |
| Loop correctness | `pytest tests/test_loop_scripted.py tests/test_tracer.py -q` | No | ReAct loop, stop conditions, token/tool logs |
| MCP surface | `pytest tests/test_mcp.py -q` | No | You understood tools/list and tools/call |
| Live exam | `python evals/run.py` | Yes | Real model + your ACI + complete traces |

Pass: scripted tests green, MCP tests green, live golden **≥ 5/6**, every trace complete, `notes.md` filled.

## What you implement

1. `src/react_eval_lab/loop.py` — `run_agent`
2. `src/react_eval_lab/providers/openai_compatible.py` — week 3
3. `src/react_eval_lab/mcp_server.py` — `handle_rpc` week 4
4. `notes.md` — reading responses (prompts are in [LEARNING.md](LEARNING.md))

## Layout

- `src/react_eval_lab/world.py` — fake wiki (do not fetch the internet)
- `src/react_eval_lab/tools.py` — five tools; `create_ticket` requires `confirm=true`
- `src/react_eval_lab/tracer.py` — log every token and tool call
- `evals/golden.json` — the exam
- [LEARNING.md](LEARNING.md) — 30-day reading + build sequence
