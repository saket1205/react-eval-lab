# Reading notes (fill this — it is part of the exam)

## A. ReAct paper

1. In one paragraph, map Thought / Action / Observation to your `run_agent` implementation (message roles, tool_calls, tool results).

2. Why does chain-of-thought fail on HotpotQA-style questions without tools? Give a Helios analogue.

3. Name three ways ReAct can still fail even with tools.

## B. Building effective agents

1. Workflow vs agent, in your words (max 6 sentences).

2. For each golden task (`hq_location`, `aurora_lead_budget`, `travel_cost`, `laptop_ticket`, `unknown_pet`, `step_budget`): workflow or agent, and why.

3. What did you change in tool descriptions (ACI) after watching the model misuse a tool?

## C. MCP spec

1. Who is the host, client, and server in this lab?

2. Difference between tools, resources, and prompts. Which of the five Helios capabilities are tools, and would any be better as resources?

3. Where should authorization live if `create_ticket` were hitting a real IT system?

## D. Failed-eval postmortem

Task id:

What the trace shows:

Fix:

Re-run result:

## E. Would I ship this?

List remaining gaps (identity, retries, human approval UX, cost caps, prompt injection).
