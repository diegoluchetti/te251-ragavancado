from __future__ import annotations

import json
import re
from pathlib import Path

PAGES_PATH = Path("data/parsed/pages.json")
PARENTS_PATH = Path("data/parsed/parents.jsonl")
CHILDREN_PATH = Path("data/parsed/children.jsonl")
REPORT_PATH = Path("data/parsed/chunk_report.txt")
PAGES_PER_PARENT = 2
CHILD_WORDS = 280
OVERLAP_WORDS = 45
MIN_CHILD_WORDS = 80
SECTION_HINTS = [
    ("unsafe control action", "Unsafe Control Actions"),
    ("control structure", "Control Structure"),
    ("causal scenario", "Causal Scenarios"),
    ("loss", "Losses"),
    ("hazard", "Hazards"),
    ("constraint", "Safety Constraints"),
]


def load_pages() -> list[dict]:
    return json.loads(PAGES_PATH.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_space(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def guess_section(text: str) -> str:
    first_lines = "\n".join(text.splitlines()[:12])
    match = re.search(r"\b(\d+(?:\.\d+){0,3}\s+[A-Z][A-Za-z0-9 ,\-/()]{4,90})", first_lines)
    if match:
        return match.group(1).strip()
    lower = text.lower()
    for needle, label in SECTION_HINTS:
        if needle in lower:
            return label
    return "Unknown section"


def detect_chunk_type(text: str) -> str:
    pipe_lines = sum(1 for line in text.splitlines() if "|" in line)
    spaced_columns = sum(1 for line in text.splitlines() if re.search(r"\S\s{3,}\S", line))
    lower = text.lower()
    if pipe_lines >= 2 or spaced_columns >= 4:
        return "table"
    if "figure" in lower or "fig." in lower:
        return "figure_caption"
    return "paragraph"


def word_windows(text: str) -> list[str]:
    words = text.split()
    if len(words) <= CHILD_WORDS:
        return [text] if len(words) >= MIN_CHILD_WORDS else []
    chunks = []
    step = CHILD_WORDS - OVERLAP_WORDS
    for start in range(0, len(words), step):
        part = words[start : start + CHILD_WORDS]
        if len(part) >= MIN_CHILD_WORDS:
            chunks.append(" ".join(part))
    return chunks


def main() -> None:
    pages = load_pages()
    parents, children = [], []
    for i in range(0, len(pages), PAGES_PER_PARENT):
        group = pages[i : i + PAGES_PER_PARENT]
        text = normalize_space("\n\n".join(p["text"] for p in group if p["text"].strip()))
        if len(text.split()) < MIN_CHILD_WORDS:
            continue
        page_start = group[0]["page"]
        page_end = group[-1]["page"]
        section = guess_section(text)
        parent_id = f"stpa_p{page_start:03d}_{page_end:03d}"
        parent_md = {
            "parent_id": parent_id,
            "section": section,
            "page_start": page_start,
            "page_end": page_end,
            "source": "STPA_Handbook.pdf",
        }
        parents.append({"id": parent_id, "text": text, "metadata": parent_md})
        for idx, child_text in enumerate(word_windows(text), start=1):
            child_id = f"{parent_id}_c{idx:02d}"
            children.append(
                {
                    "id": child_id,
                    "text": child_text,
                    "metadata": {
                        **parent_md,
                        "child_id": child_id,
                        "chunk_type": detect_chunk_type(child_text),
                        "word_count": len(child_text.split()),
                    },
                }
            )
    write_jsonl(PARENTS_PATH, parents)
    write_jsonl(CHILDREN_PATH, children)
    by_type: dict[str, int] = {}
    for child in children:
        t = child["metadata"]["chunk_type"]
        by_type[t] = by_type.get(t, 0) + 1
    REPORT_PATH.write_text(
        f"parents={len(parents)}\nchildren={len(children)}\nchunk_types={by_type}\n",
        encoding="utf-8",
    )
    print(REPORT_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
