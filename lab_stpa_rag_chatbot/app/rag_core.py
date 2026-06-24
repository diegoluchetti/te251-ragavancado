from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any

import chromadb
from openai import OpenAI

from app.env_config import load_project_env

load_project_env()

EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
OPENROUTER_BASE = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_CHAT_MODEL = os.getenv("OPENROUTER_CHAT_MODEL", "openai/gpt-4.1-mini")
OPENROUTER_EMBED_MODEL = os.getenv("OPENROUTER_EMBED_MODEL", "openai/text-embedding-3-small")
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/index/chroma")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "stpa_handbook_children")
MAX_PARENTS = int(os.getenv("MAX_PARENTS", "3"))
PARENTS_PATH = Path("data/parsed/parents.jsonl")
REFUSAL_MESSAGE = "Informação não encontrada no STPA Handbook recuperado."
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "gemma4:latest")
OFFLINE_EMBED_MODEL = os.getenv("OFFLINE_EMBED_MODEL", "BAAI/bge-m3")

_openai_client: OpenAI | None = None
_openrouter_client: OpenAI | None = None
_offline_embedder = None


def _allow_offline() -> bool:
    return os.getenv("ALLOW_OFFLINE_EMBED", "").lower() in ("1", "true", "yes")


def _get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is missing. Check repo root .env or lab .env.")
        _openai_client = OpenAI(api_key=key)
    return _openai_client


def _get_openrouter_client() -> OpenAI:
    global _openrouter_client
    if _openrouter_client is None:
        key = os.getenv("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is missing.")
        _openrouter_client = OpenAI(base_url=OPENROUTER_BASE, api_key=key)
    return _openrouter_client


def _ollama_chat(messages: list[dict[str, str]], num_predict: int = 1024) -> str:
    payload = json.dumps(
        {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0, "num_predict": num_predict},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("message", {}).get("content", "")


def _chat_complete(messages: list[dict[str, str]], *, num_predict: int = 1024) -> str:
    if _allow_offline():
        return _ollama_chat(messages, num_predict=num_predict)
    try:
        response = _get_openai_client().chat.completions.create(
            model=CHAT_MODEL,
            temperature=0,
            max_tokens=num_predict,
            messages=messages,
        )
        return response.choices[0].message.content or ""
    except Exception as exc:
        if not os.getenv("OPENROUTER_API_KEY"):
            raise
        print(f"OpenAI chat failed ({exc}); using OpenRouter ({OPENROUTER_CHAT_MODEL}).")
        response = _get_openrouter_client().chat.completions.create(
            model=OPENROUTER_CHAT_MODEL,
            temperature=0,
            max_tokens=num_predict,
            messages=messages,
        )
        return response.choices[0].message.content or ""


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
    global _offline_embedder
    if _offline_embedder is None:
        from sentence_transformers import SentenceTransformer

        print(f"offline: loading embedder {OFFLINE_EMBED_MODEL}")
        _offline_embedder = SentenceTransformer(OFFLINE_EMBED_MODEL)
    batch_size = int(os.getenv("OFFLINE_EMBED_BATCH_SIZE", "8"))
    return _offline_embedder.encode(
        texts,
        normalize_embeddings=True,
        batch_size=batch_size,
        show_progress_bar=len(texts) > 32,
    ).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    if _allow_offline():
        return _offline_embed(cleaned)
    try:
        response = _get_openai_client().embeddings.create(model=EMBED_MODEL, input=cleaned)
        return [item.embedding for item in sorted(response.data, key=lambda d: d.index)]
    except Exception as exc:
        if os.getenv("OPENROUTER_API_KEY"):
            print(f"OpenAI embed failed ({exc}); using OpenRouter ({OPENROUTER_EMBED_MODEL}).")
            response = _get_openrouter_client().embeddings.create(
                model=OPENROUTER_EMBED_MODEL,
                input=cleaned,
            )
            return [item.embedding for item in sorted(response.data, key=lambda d: d.index)]
        if _allow_offline():
            print(f"OpenAI embed failed ({exc}); falling back to {OFFLINE_EMBED_MODEL}.")
            return _offline_embed(cleaned)
        raise RuntimeError(f"OpenAI embed failed and no fallback is configured: {exc}") from exc


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


def judge_retrieval(question: str, context: str) -> str:
    if not context.strip():
        return "incorrect"
    prompt = (
        "Classifique a recuperação.\n"
        "Retorne apenas uma palavra: correct, ambiguous ou incorrect.\n"
        f"Pergunta: {question}\n"
        f"Contexto: {context[:6000]}"
    )
    verdict = _chat_complete([{"role": "user", "content": prompt}], num_predict=32).strip().lower()
    for token in verdict.replace("*", " ").replace(",", " ").split():
        if token in ("correct", "ambiguous", "incorrect"):
            return token
    return "incorrect"


def answer_question(question: str, chunk_type: str | None = None) -> dict[str, Any]:
    hits = retrieve_parents(question, where=build_where_filter(chunk_type))
    if not hits:
        return {"answer": REFUSAL_MESSAGE, "sources": [], "retrieval_verdict": "incorrect"}

    context = format_context(hits)
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
    if REFUSAL_MESSAGE.lower() in (answer or "").lower():
        return {"answer": REFUSAL_MESSAGE, "sources": hits, "retrieval_verdict": verdict}
    return {
        "answer": answer or REFUSAL_MESSAGE,
        "sources": hits,
        "retrieval_verdict": verdict,
    }
