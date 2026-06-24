from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/index/chroma")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "stpa_handbook_children")
MAX_PARENTS = int(os.getenv("MAX_PARENTS", "3"))
PARENTS_PATH = Path("data/parsed/parents.jsonl")
REFUSAL_MESSAGE = "Informação não encontrada no STPA Handbook recuperado."
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:1b")

_client: OpenAI | None = None
_offline_model = None


def _allow_offline() -> bool:
    return os.getenv("ALLOW_OFFLINE_EMBED", "").lower() in ("1", "true", "yes")


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")
        _client = OpenAI(api_key=key)
    return _client


def _chat_complete(messages: list[dict[str, str]]) -> str:
    try:
        response = _get_client().chat.completions.create(
            model=CHAT_MODEL,
            temperature=0,
            messages=messages,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        if not _allow_offline():
            raise
        payload = json.dumps({"model": OLLAMA_MODEL, "messages": messages, "stream": False}).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(f"ponytail: OpenAI chat failed ({exc}); using Ollama {OLLAMA_MODEL}.")
        return data.get("message", {}).get("content", "")


def load_parents() -> dict[str, dict[str, Any]]:
    parents = {}
    for line in PARENTS_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            parents[item["id"]] = item
    return parents


PARENTS = load_parents()


def get_collection():
    return chromadb.PersistentClient(path=CHROMA_PATH).get_collection(COLLECTION_NAME)


def _offline_embed(texts: list[str]) -> list[list[float]]:
    global _offline_model
    if _offline_model is None:
        from sentence_transformers import SentenceTransformer

        _offline_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _offline_model.encode(texts, normalize_embeddings=True).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    try:
        response = _get_client().embeddings.create(model=EMBED_MODEL, input=cleaned)
        return [item.embedding for item in sorted(response.data, key=lambda d: d.index)]
    except Exception as exc:
        if not _allow_offline():
            raise
        print(f"ponytail: OpenAI embed failed ({exc}); using local MiniLM for dev only.")
        return _offline_embed(cleaned)


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]


def build_where_filter(chunk_type: str | None = None) -> dict | None:
    if chunk_type and chunk_type != "any":
        return {"chunk_type": chunk_type}
    return None


def retrieve_parents(question: str, n_results: int = 10, where: dict | None = None) -> list[dict[str, Any]]:
    result = get_collection().query(
        query_embeddings=[embed_query(question)],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )
    hits, seen = [], set()
    for metadata, distance, child_text in zip(
        result["metadatas"][0], result["distances"][0], result["documents"][0]
    ):
        parent_id = metadata["parent_id"]
        if parent_id in seen:
            continue
        seen.add(parent_id)
        parent = PARENTS.get(parent_id)
        if parent:
            hits.append(
                {
                    "parent_id": parent_id,
                    "distance": distance,
                    "matched_child": child_text,
                    "text": parent["text"],
                    "metadata": parent["metadata"],
                }
            )
        if len(hits) >= MAX_PARENTS:
            break
    return hits


def format_context(hits: list[dict[str, Any]]) -> str:
    blocks = []
    for i, hit in enumerate(hits, start=1):
        md = hit["metadata"]
        ref = (
            f"Fonte {i}: {md.get('source')} | seção: {md.get('section')} | "
            f"páginas: {md.get('page_start')}-{md.get('page_end')} | parent_id: {hit['parent_id']}"
        )
        blocks.append(f"[{ref}]\n{hit['text']}")
    return "\n\n---\n\n".join(blocks)


_STOPWORDS = {
    "what", "when", "where", "which", "that", "this", "with", "from", "have",
    "does", "about", "would", "could", "should", "there", "their", "they",
    "them", "then", "than", "into", "your", "will", "also", "been", "were",
}


def _lexical_overlap(question: str, context: str) -> int:
    words = {w for w in re.findall(r"[a-z]{4,}", question.lower()) if w not in _STOPWORDS}
    if not words:
        return 0
    ctx = context.lower()
    return sum(1 for w in words if w in ctx)


def judge_retrieval(question: str, context: str) -> str:
    if not context.strip():
        return "incorrect"
    # ponytail: skip LLM judge when offline; system prompt + empty hits handle refusal
    if _allow_offline():
        return "correct"
    prompt = (
        "Classifique a recuperação.\n"
        "Retorne apenas uma palavra: correct, ambiguous ou incorrect.\n"
        f"Pergunta: {question}\n"
        f"Contexto: {context[:6000]}"
    )
    verdict = _chat_complete([{"role": "user", "content": prompt}]).strip().lower()
    if verdict.startswith("correct"):
        return "correct"
    if verdict.startswith("ambiguous"):
        return "ambiguous"
    return "incorrect"


def answer_question(question: str, chunk_type: str | None = None) -> dict[str, Any]:
    hits = retrieve_parents(question, where=build_where_filter(chunk_type))
    if not hits:
        return {"answer": REFUSAL_MESSAGE, "sources": [], "retrieval_verdict": "incorrect"}

    context = format_context(hits)
    weak_retrieval = min(h["distance"] for h in hits) > 0.5
    if _allow_offline() and (_lexical_overlap(question, context) == 0 or weak_retrieval):
        return {"answer": REFUSAL_MESSAGE, "sources": hits, "retrieval_verdict": "incorrect"}

    verdict = judge_retrieval(question, context)

    if verdict == "incorrect":
        hits = retrieve_parents(question, n_results=16, where=build_where_filter(chunk_type))
        context = format_context(hits)
        verdict = judge_retrieval(question, context)
        if verdict == "incorrect":
            return {"answer": REFUSAL_MESSAGE, "sources": hits, "retrieval_verdict": verdict}

    system = (
        "Você é um assistente técnico para consulta ao STPA Handbook. "
        "Responda em português claro, com precisão factual, usando somente o CONTEXTO. "
        f"Se o contexto não contiver a resposta, diga exatamente: '{REFUSAL_MESSAGE}' "
        "Não use conhecimento externo. Sempre termine com uma seção 'Referências' "
        "listando fonte, seção e páginas."
    )
    user = f"PERGUNTA:\n{question}\n\nCONTEXTO:\n{context}"
    answer = _chat_complete(
        [{"role": "system", "content": system}, {"role": "user", "content": user}]
    )
    return {
        "answer": answer or REFUSAL_MESSAGE,
        "sources": hits,
        "retrieval_verdict": verdict,
    }
