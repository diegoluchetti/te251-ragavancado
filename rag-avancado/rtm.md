# Requirement Traceability Matrix

| ID | Requirement | Artifact | Evidence | Status |
|----|-------------|----------|----------|--------|
| REQ-01 | Ingest STPA_Handbook.pdf | `scripts/01_parse_pdf.py` | `data/parsed/pages.json` (188 pages) | verified |
| REQ-02 | Parent Document Retrieval | `scripts/02_build_parent_child.py` | `data/parsed/chunk_report.txt` (89/321) | verified |
| REQ-03 | Metadata chunk_type, section, pages | `children.jsonl` | chunk_types in chunk_report | verified |
| REQ-04 | text-embedding-3-small | `scripts/03_embed_index.py` + `app/rag_core.embed_texts` | Chroma count=321 (OpenAI path; MiniLM fallback dev) | verified |
| REQ-05 | Local ChromaDB | `data/index/chroma/` | smoke test | verified |
| REQ-06 | Retrieve relevant chunks | `app/rag_core.retrieve_parents` | smoke test (3 parents UCA) | verified |
| REQ-07 | Section/page in answer | system prompt + Referências | `development/evidence/in-scope.png` | verified |
| REQ-08 | Explicit refusal | prompt + CRAG + weak-retrieval guard | `development/evidence/out-of-scope.png` | verified |
| REQ-09 | Streamlit input/response | `app/streamlit_app.py` | localhost:8501 | verified |
| REQ-10 | Fontes recuperadas panel | `streamlit_app.py` expander | in-scope screenshot | verified |
| REQ-11 | Automated eval | `evals/05_run_eval.py` | `eval_output.txt` | verified |
