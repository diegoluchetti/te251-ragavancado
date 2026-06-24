# Design Decisions

## DD-001 — PDR baseline (tutorial)

- **Decisão:** Parent Document Retrieval com children indexados no Chroma e parents em JSONL.
- **Alternativa:** chunk fixo + top-k ingênuo.
- **Status:** aceito.

## DD-002 — Sem LangChain

- **Decisão:** `openai` + `chromadb` + `pypdf` apenas, conforme tutorial.
- **Status:** aceito.

## DD-003 — GraphRAG deferido

- **Decisão:** GraphRAG não implementado nesta entrega; PDR + CRAG cobrem Q&A factual STPA (Aula 11).
- **Status:** aceito.

## DD-004 — CRAG inline em rag_core.py

- **Decisão:** `judge_retrieval()` no mesmo módulo, sem `app/crag.py` separado (ponytail).
- **Status:** aceito.

## DD-005 — Obsidian mínimo

- **Decisão:** `index.md`, `rtm.md`, `log.md`, `design-decisions.md`, `development/prompts/` — sem árvore verification/ separada.
- **Status:** aceito.

## DD-006 — Fallback offline (dev only)

- **Decisão:** `ALLOW_OFFLINE_EMBED=1` → MiniLM local + Ollama chat quando OpenAI inacessível; produção usa `text-embedding-3-small` + chat OpenAI sem flag.
- **Status:** aceito.
