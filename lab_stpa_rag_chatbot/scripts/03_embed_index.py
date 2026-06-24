from __future__ import annotations

import json
import os
from pathlib import Path

import chromadb
import sys
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.rag_core import embed_texts

load_dotenv()
CHILDREN_PATH = Path("data/parsed/children.jsonl")
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/index/chroma")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "stpa_handbook_children")
BATCH_SIZE = 64


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def batched(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def main() -> None:
    if not os.getenv("OPENAI_API_KEY") and os.getenv("ALLOW_OFFLINE_EMBED", "").lower() not in ("1", "true", "yes"):
        raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")
    if not CHILDREN_PATH.exists():
        raise FileNotFoundError("Run scripts/02_build_parent_child.py first.")
    chroma = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        chroma.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = chroma.create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    children = load_jsonl(CHILDREN_PATH)
    print(f"Indexing {len(children)} children into {COLLECTION_NAME}")
    for batch in batched(children, BATCH_SIZE):
        texts = [item["text"].replace("\n", " ").strip() for item in batch]
        vectors = embed_texts(texts)
        metadatas = []
        for item in batch:
            md = {k: (str(v) if not isinstance(v, (str, int, float, bool)) else v) for k, v in item["metadata"].items()}
            metadatas.append(md)
        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=texts,
            metadatas=metadatas,
            embeddings=vectors,
        )
        print(f"  indexed {len(batch)}; total={collection.count()}")
    print("Done. Collection count:", collection.count())


if __name__ == "__main__":
    main()
