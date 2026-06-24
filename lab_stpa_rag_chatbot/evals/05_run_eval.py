from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag_core import answer_question

for line in Path("evals/eval_questions.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    item = json.loads(line)
    result = answer_question(item["question"])
    print("\n===", item["id"], item["question"])
    print(result["answer"])
    print("Sources:")
    for src in result["sources"]:
        md = src["metadata"]
        print(" -", md.get("section"), md.get("page_start"), md.get("page_end"))
