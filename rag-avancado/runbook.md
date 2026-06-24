# Runbook

Guia operacional para reproduzir o pipeline completo. Código em `../lab_stpa_rag_chatbot/`.

## Pré-requisitos

- Python 3.11+
- Chave API em `../.env` (repo root):

```env
OPEN_AI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...   # fallback se OpenAI inacessível
```

## Setup (uma vez)

```powershell
cd lab_stpa_rag_chatbot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy ..\.env.example ..\.env          # editar chaves
copy ..\\docs\\STPA_Handbook.pdf data\\raw\\   # se ausente
```

## Pipeline de ingestão e indexação

```powershell
python scripts/00_doctor.py
python scripts/01_parse_pdf.py
python scripts/02_build_parent_child.py    # → chunk_report.txt
python scripts/03_embed_index.py           # → ChromaDB
```

## Validação

```powershell
$env:PYTHONPATH="."
python scripts/04_smoke_test_retriever.py | Tee-Object smoke_output.txt
python evals/05_run_eval.py | Tee-Object eval_output.txt
```

## UI

```powershell
$env:PYTHONPATH="app"
streamlit run app/streamlit_app.py
# → http://localhost:8501
```

## Evidências (screenshots)

```powershell
python scripts/capture_screenshots.py
# → rag-avancado/development/evidence/*.png
```

## Troubleshooting

| Sintoma | Ação |
|---------|------|
| `OPENAI_API_KEY is missing` | Verificar `rag-avancado/.env` com `OPEN_AI_API_KEY` |
| OpenAI connection error | Confirmar `OPENROUTER_API_KEY`; fallback automático |
| OpenRouter 402 | Créditos insuficientes ou `max_tokens` alto — já limitado em `rag_core.py` |
| Chroma dimension mismatch | Re-executar `03_embed_index.py` após trocar modelo de embed |
| Offline dev | `ALLOW_OFFLINE_EMBED=1` + BGE-M3 + Ollama ([[design-decisions#DD-006]]) |
