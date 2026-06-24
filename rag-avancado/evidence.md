# Evidence

Índice de artefatos de verificação e entrega. Detalhes na [[rtm]].

## Screenshots (Streamlit UI)

| Arquivo | Cenário | REQ |
|---------|---------|-----|
| [[development/evidence/in-scope.png\|in-scope.png]] | Pergunta in-scope (UCA) + painel **Fontes recuperadas** expandido | REQ-07, REQ-10 |
| [[development/evidence/out-of-scope.png\|out-of-scope.png]] | Pergunta off-topic (capital da França) → recusa explícita | REQ-08 |

Captura: `lab_stpa_rag_chatbot/scripts/capture_screenshots.py`

## Relatórios e outputs

| Artefato | Caminho | Gerado por |
|----------|---------|------------|
| Chunk report | `lab_stpa_rag_chatbot/data/parsed/chunk_report.txt` | `02_build_parent_child.py` |
| Eval output | `lab_stpa_rag_chatbot/eval_output.txt` | `evals/05_run_eval.py` |
| Smoke output | `lab_stpa_rag_chatbot/smoke_output.txt` | `04_smoke_test_retriever.py` |

### chunk_report.txt (snapshot)

```
parents=89
children=321
chunk_types={'paragraph': 248, 'figure_caption': 72, 'table': 1}
```

### Eval (q01–q05)

| ID | Pergunta | Resultado esperado |
|----|----------|-------------------|
| q01 | Purpose of STPA | Resposta ancorada + referências |
| q02 | Unsafe control action | Resposta ancorada + referências |
| q03 | Control structure | Resposta ancorada + referências |
| q04 | Causal scenarios in STPA | Resposta ancorada + referências |
| q05 | Capital of France | Recusa explícita |

## Dados parseados

| Arquivo | Registros | Descrição |
|---------|-----------|-----------|
| `data/parsed/pages.json` | 188 páginas | Saída do parser PDF |
| `data/parsed/parents.jsonl` | 89 | Chunks pai (contexto LLM) |
| `data/parsed/children.jsonl` | 321 | Chunks filho (indexados) |

## Índice vetorial

- **Collection:** `stpa_handbook_children`
- **Count:** 321
- **Dimensão:** 1536 (`text-embedding-3-small`)
- **Path local:** `lab_stpa_rag_chatbot/data/index/chroma/` (gitignored)
