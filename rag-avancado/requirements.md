# Requirements

Fonte canônica: [[history/Starting Prompt]]

## Functional Requirements

| ID | Subsystem | Requirement |
|----|-----------|-------------|
| FR-01 | Ingestion | Ingest `STPA_Handbook.pdf` from local input directory |
| FR-02 | Ingestion | Segment document using Parent Document Retrieval (PDR) |
| FR-03 | Ingestion | Assign `chunk_type`, `section`, and `pages` metadata to each parent and child |
| FR-04 | Embedding | Generate embeddings with OpenAI `text-embedding-3-small` |
| FR-05 | Embedding | Index and store vectors in local ChromaDB |
| FR-06 | RAG Core | Retrieve relevant chunks from ChromaDB for user query |
| FR-07 | RAG Core | Include section and page numbers in generated answer |
| FR-08 | RAG Core | Refuse explicitly when retrieved evidence is insufficient |
| FR-09 | UI | Streamlit text input for user queries |
| FR-10 | UI | Display RAG response to user |
| FR-11 | UI | Expandable panel **Fontes recuperadas** with section/page metadata |
| FR-12 | Evaluation | Automated test queries via `evals/05_run_eval.py` |

## Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | Run entirely on local workstation |
| NFR-02 | UI implemented with Streamlit |
| NFR-03 | Streamlit served at `localhost:8501` |
| NFR-04 | Python-based runtime |

## Delivery & Verification

| ID | Artifact | Script / action |
|----|----------|-----------------|
| DEL-01 | `data/parsed/chunk_report.txt` | `scripts/02_build_parent_child.py` |
| DEL-02 | In-scope screenshot | Streamlit: valid query + expanded Fontes recuperadas |
| DEL-03 | Out-of-scope screenshot | Streamlit: refusal on off-topic query |
| DEL-04 | `eval_output.txt` | `python evals/05_run_eval.py` |

## Traceability

Cada requisito de entrega mapeia para REQ na [[rtm]].
