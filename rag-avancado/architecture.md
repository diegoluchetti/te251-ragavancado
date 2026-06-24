# Architecture

## Visão geral

```mermaid
flowchart TB
    subgraph ingest [Ingestion]
        PDF[STPA_Handbook.pdf]
        P01[01_parse_pdf.py]
        P02[02_build_parent_child.py]
        PDF --> P01 --> pages[pages.json]
        pages --> P02
        P02 --> parents[parents.jsonl]
        P02 --> children[children.jsonl]
        P02 --> report[chunk_report.txt]
    end

    subgraph index [Embedding and Storage]
        P03[03_embed_index.py]
        embed[embed_texts]
        chroma[(ChromaDB)]
        children --> P03 --> embed --> chroma
    end

    subgraph rag [RAG Core]
        retrieve[retrieve_parents]
        judge[judge_retrieval CRAG]
        answer[answer_question]
        chroma --> retrieve
        parents --> retrieve
        retrieve --> judge --> answer
    end

    subgraph llm [LLM Providers]
        openai[OpenAI API]
        orouter[OpenRouter fallback]
        offline[BGE-M3 + Ollama dev]
        embed --> openai
        embed -.-> orouter
        embed -.-> offline
        answer --> openai
        answer -.-> orouter
        answer -.-> offline
    end

    subgraph ui [UI]
        st[streamlit_app.py]
        st --> answer
    end

    subgraph eval [Evaluation]
        ev[05_run_eval.py]
        ev --> answer
    end
```

## Parent Document Retrieval (PDR)

1. **Children** (321) — chunks pequenos indexados no ChromaDB para busca semântica.
2. **Parents** (89) — seções completas em `parents.jsonl`; retornadas ao LLM como contexto.
3. **Query flow:** embed query → top-k children → deduplicate by `parent_id` → fetch parent text → format context.

## CRAG (Corrective RAG)

`judge_retrieval()` classifica a recuperação como `correct`, `ambiguous` ou `incorrect` antes de gerar a resposta. Se `incorrect`, uma segunda busca (n_results=16) é tentada; persistindo incorreto → mensagem de recusa.

## Configuração de ambiente

Carregamento em `app/env_config.py`:

1. `lab_stpa_rag_chatbot/.env` (overrides locais)
2. `rag-avancado/.env` (chaves API — **prevalece**)

Variáveis principais: `OPEN_AI_API_KEY`, `OPENROUTER_API_KEY`, `ALLOW_OFFLINE_EMBED`.

## Stack

| Camada | Tecnologia |
|--------|------------|
| PDF parsing | pypdf |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | ChromaDB (cosine, persistent) |
| Chat | OpenAI `gpt-4.1-mini` |
| UI | Streamlit |
| Fallback | OpenRouter (`openai/*` models) |

Sem LangChain ([[design-decisions#DD-002]]).
