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
- Nota: OpenAI API bloqueada neste host (WinError 10013); `ALLOW_OFFLINE_EMBED=1` usa MiniLM + Ollama para dev.
- `00_doctor.py`: OK (PDF, packages, .env).
- Smoke test: 3 parents para UCA (pp. 13-14, 23-26).

## [2026-06-24] wave-3 | UI + eval + evidências

- `streamlit_app.py` com Fontes recuperadas e filtros chunk_type.
- `evals/05_run_eval.py` → `eval_output.txt` (q01–q05).
- Screenshots: `development/evidence/in-scope.png`, `out-of-scope.png`.
- RTM: todos REQ verified.

## [2026-06-24] wave-4 | CRAG inline

- `judge_retrieval()` em `app/rag_core.py` (OpenAI path; skip em offline dev).
- Guarda weak-retrieval (distance > 0.5) + overlap lexical para recusa off-topic.
