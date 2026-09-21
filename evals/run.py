from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dotenv import load_dotenv

from react_eval_lab.graders import grade_trace
from react_eval_lab.loop import run_agent
from react_eval_lab.providers.openai_compatible import OpenAICompatibleProvider
from react_eval_lab.tools import TICKETS


def main() -> int:
    load_dotenv()
    if not os.environ.get("LLM_API_KEY"):
        print("Set LLM_API_KEY in .env (see .env.example)", file=sys.stderr)
        return 2

    specs = json.loads((ROOT / "golden.json").read_text())
    out_dir = ROOT.parent / ".eval_runs"
    out_dir.mkdir(exist_ok=True)

    passed = 0
    provider = OpenAICompatibleProvider()
    results = []
    for spec in specs:
        TICKETS.clear()
        trace = run_agent(spec["question"], provider, task_id=spec["id"], max_steps=8)
        grade = grade_trace(trace, spec)
        results.append({"id": spec["id"], **grade, "usage": trace.total_usage.model_dump()})
        (out_dir / f"{spec['id']}.json").write_text(trace.model_dump_json(indent=2))
        mark = "PASS" if grade["passed"] else "FAIL"
        if grade["passed"]:
            passed += 1
        print(f"{mark} {spec['id']}: {grade['checks']}")
        print(f"  answer: {trace.final_answer!r}  stop={trace.stop_reason} tokens={trace.total_usage.total_tokens}")

    print(f"\n{passed}/{len(specs)} passed (need ≥5/6)")
    (out_dir / "summary.json").write_text(json.dumps(results, indent=2))
    return 0 if passed >= 5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
