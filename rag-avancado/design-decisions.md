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

## DD-005 — Vault Obsidian

- **Decisão:** Vault em `rag-avancado/` com `index`, `requirements`, `architecture`, `evidence`, `runbook`, `rtm`, `design-decisions`, `log`, `history/`, `development/`.
- **Status:** aceito.

## DD-006 — Fallback offline (dev only)

- **Decisão:** Produção: OpenAI (`text-embedding-3-small` + chat OpenAI) com chave em `rag-avancado/.env` (`OPEN_AI_API_KEY`). Se OpenAI inacessível, fallback OpenRouter (`OPENROUTER_API_KEY`, modelos `openai/*`). Dev offline opcional: `ALLOW_OFFLINE_EMBED=1` → BGE-M3 + Ollama.
- **Status:** aceito.
