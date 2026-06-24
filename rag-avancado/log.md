# Log

## [2026-06-24] wave-1 | Scaffold + ingestion

- Criado `lab_stpa_rag_chatbot/` com requirements, .gitignore, .env.example.
- Copiado `STPA_Handbook.pdf` → `data/raw/`.
- `01_parse_pdf.py`: 188 páginas, 0 vazias.
- `02_build_parent_child.py`: parents=89, children=321, chunk_types paragraph=248, figure_caption=72, table=1.
- Evidência: `data/parsed/chunk_report.txt`.
- Vault: index, rtm, design-decisions, log iniciados.

## [2026-06-24] wave-2 | Index + RAG core

- `03_embed_index.py`: Chroma collection `stpa_handbook_children` count=321.
- `00_doctor.py`: OK (PDF, packages, env).
- Smoke test: 3 parents para UCA.

## [2026-06-24] wave-3 | UI + eval + evidências

- `streamlit_app.py` com Fontes recuperadas e filtros chunk_type.
- `evals/05_run_eval.py` → `eval_output.txt` (q01–q05).
- Screenshots: `development/evidence/in-scope.png`, `out-of-scope.png`.
- RTM: todos REQ verified.

## [2026-06-24] wave-4 | CRAG inline

- `judge_retrieval()` em `app/rag_core.py` — classifica correct/ambiguous/incorrect antes da geração.

## [2026-06-24] wave-5 | OpenAI + OpenRouter (produção)

- Chave OpenAI em `rag-avancado/.env` (`OPEN_AI_API_KEY`); `app/env_config.py` carrega root antes de lab overrides.
- Fallback OpenRouter em `rag_core.py` (chat + embed) quando OpenAI falha e `OPENROUTER_API_KEY` está definida.
- `ALLOW_OFFLINE_EMBED=0` para teste real; offline (BGE-M3 + Ollama) só com flag explícita.
- **Bloqueio:** `api.openai.com` inacessível neste host (WinError 10013); `openrouter.ai` OK. Re-index/eval/screenshots pendentes de `OPENROUTER_API_KEY` no root `.env`.

## [2026-06-24] wave-5b | OpenRouter test + evidências (concluído)

- `OPENROUTER_API_KEY` em `rag-avancado/.env`; fallback chat+embed via OpenRouter (`openai/gpt-4.1-mini`, `openai/text-embedding-3-small`).
- Fix `max_tokens` no chat OpenRouter (evita erro 402 por créditos).
- Re-index Chroma: 321 children, dim=1536 (OpenRouter embed).
- Eval q01–q05 OK; q05 recusa off-topic corretamente → `eval_output.txt`.
- Screenshots atualizados: `development/evidence/in-scope.png`, `out-of-scope.png`.

## [2026-06-24] wave-6 | Vault + repo polish

- Vault: `requirements`, `architecture`, `evidence`, `runbook`; RTM e index atualizados.
- Removidos duplicatas (Welcome.md, plan copies).
- README principal reescrito; `.env.example` no root.
