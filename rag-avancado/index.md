# STPA RAG Lab — Vault Index

> Documentação de engenharia do laboratório TE-251 Aula 11: chatbot RAG ancorado ao *STPA Handbook* com Parent Document Retrieval, ChromaDB, CRAG e Streamlit.

## Navegação

| Área | Nota | Descrição |
|------|------|-----------|
| Requisitos | [[requirements]] | Requisitos funcionais e de entrega (fonte: Starting Prompt) |
| Arquitetura | [[architecture]] | Pipeline, componentes e fluxo de dados |
| Decisões | [[design-decisions]] | DD-001 … DD-006 |
| Rastreabilidade | [[rtm]] | Matriz REQ → artefato → evidência |
| Evidências | [[evidence]] | Screenshots, eval, chunk_report, smoke |
| Runbook | [[runbook]] | Como executar o pipeline localmente |
| Histórico | [[log]] | Log append-only por wave |

## Histórico e prompts

- [[history/Starting Prompt]] — brief original do projeto
- [[history/Cursor 1st Implementation Plan]] — plano de implementação (Cursor)
- [[development/prompts/2026-06-24-implementation-plan]] — prompt da sessão de build

## Repositório

| Caminho | Conteúdo |
|---------|----------|
| `../lab_stpa_rag_chatbot/` | Código, scripts, dados parseados, eval |
| `../docs/` | PDFs de referência (Handbook, tutorial, Aula 11) |
| `../README.md` | Entrada principal do repositório GitHub |

## Status do projeto

**Entrega completa** — todos os REQ-01 … REQ-11 verificados ([[rtm]]).

- **Ingestão:** 188 páginas → 89 parents / 321 children
- **Índice:** ChromaDB `stpa_handbook_children` (321 vetores, dim 1536)
- **LLM path:** OpenAI → fallback OpenRouter → offline opcional (BGE-M3 + Ollama)
- **Evidências:** [[evidence]]
