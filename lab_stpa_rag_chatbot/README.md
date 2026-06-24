# STPA RAG Lab

Chatbot RAG com Parent Document Retrieval sobre o STPA Handbook (tutorial TE-251 Aula 11).

## Setup

```powershell
cd lab_stpa_rag_chatbot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy ..\\docs\\STPA_Handbook.pdf data\\raw\\   # if missing
copy .env.example .env                          # add OPENAI_API_KEY
```

## Pipeline

```powershell
python scripts/01_parse_pdf.py
python scripts/02_build_parent_child.py
python scripts/03_embed_index.py
$env:PYTHONPATH="."; python scripts/04_smoke_test_retriever.py
$env:PYTHONPATH="app"; streamlit run app/streamlit_app.py
$env:PYTHONPATH="."; python evals/05_run_eval.py *> eval_output.txt
```
