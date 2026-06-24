from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader

PDF_PATH = Path("data/raw/STPA_Handbook.pdf")
OUT_PATH = Path("data/parsed/pages.json")
SAMPLE_PATH = Path("data/parsed/sample_pages.txt")


def extract_page_text(page) -> str:
    try:
        text = page.extract_text(extraction_mode="layout") or ""
    except TypeError:
        text = page.extract_text() or ""
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Missing PDF: {PDF_PATH}")
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(PDF_PATH))
    pages = []
    for page_num, page in enumerate(reader.pages, start=1):
        pages.append({"page": page_num, "text": extract_page_text(page)})
    OUT_PATH.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    sample_numbers = [1, 2, 3, min(10, len(pages)), min(20, len(pages))]
    samples = []
    for n in sorted(set(sample_numbers)):
        if 1 <= n <= len(pages):
            samples.append(f"\n\n===== PAGE {n} =====\n{pages[n - 1]['text'][:2500]}")
    SAMPLE_PATH.write_text("".join(samples), encoding="utf-8")
    empty = sum(1 for p in pages if not p["text"].strip())
    print(f"Wrote {len(pages)} pages to {OUT_PATH}")
    print(f"Empty pages: {empty}")
    print(f"Review sample text at {SAMPLE_PATH}")


if __name__ == "__main__":
    main()
