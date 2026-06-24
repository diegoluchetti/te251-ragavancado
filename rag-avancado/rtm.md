# Requirement Traceability Matrix

> Última verificação: wave-5b (2026-06-24) — OpenRouter production path.

| ID | Requirement | Artifact | Evidence | Status |
|----|-------------|----------|----------|--------|
| REQ-01 | Ingest STPA_Handbook.pdf | `scripts/01_parse_pdf.py` | `data/parsed/pages.json` (188 pages) | verified |
| REQ-02 | Parent Document Retrieval | `scripts/02_build_parent_child.py` | `data/parsed/chunk_report.txt` (89 parents / 321 children) | verified |
| REQ-03 | Metadata chunk_type, section, pages | `children.jsonl`, `parents.jsonl` | chunk_types in chunk_report | verified |
| REQ-04 | text-embedding-3-small | `scripts/03_embed_index.py`, `app/rag_core.embed_texts` | Chroma count=321, dim=1536 (OpenAI / OpenRouter) | verified |
| REQ-05 | Local ChromaDB | `data/index/chroma/` | smoke test, collection `stpa_handbook_children` | verified |
| REQ-06 | Retrieve relevant chunks | `app/rag_core.retrieve_parents` | smoke_output.txt (3 parents UCA) | verified |
| REQ-07 | Section/page in answer | system prompt + Referências | [[development/evidence/in-scope.png]] | verified |
| REQ-08 | Explicit refusal | CRAG `judge_retrieval()` + prompt | [[development/evidence/out-of-scope.png]] | verified |
| REQ-09 | Streamlit input/response | `app/streamlit_app.py` | localhost:8501 | verified |
| REQ-10 | Fontes recuperadas panel | `streamlit_app.py` expander | in-scope screenshot | verified |
| REQ-11 | Automated eval | `evals/05_run_eval.py` | `eval_output.txt` (q01–q05) | verified |

## Mapping FR → REQ

| FR (see [[requirements]]) | REQ |
|-----------------------------|-----|
| FR-01 … FR-03 | REQ-01, REQ-02, REQ-03 |
| FR-04, FR-05 | REQ-04, REQ-05 |
| FR-06 … FR-08 | REQ-06, REQ-07, REQ-08 |
| FR-09 … FR-11 | REQ-09, REQ-10 |
| FR-12 | REQ-11 |
| DEL-01 … DEL-04 | REQ-02, REQ-07/10, REQ-08, REQ-11 |
