from __future__ import annotations

import streamlit as st

from rag_core import answer_question

st.set_page_config(page_title="STPA RAG Chatbot", page_icon="📘", layout="wide")
st.title("STPA Handbook · RAG Chatbot")
st.caption("RAG customizada com PDR, ChromaDB e OpenAI API")

with st.sidebar:
    st.header("Configuração")
    filter_mode = st.selectbox(
        "Filtro de conteúdo",
        ["Sem filtro", "Somente parágrafos", "Somente tabelas", "Somente legendas/figuras"],
    )
    st.info("Use perguntas factuais. O chatbot deve citar páginas ou recusar.")

chunk_type = None
if filter_mode == "Somente parágrafos":
    chunk_type = "paragraph"
elif filter_mode == "Somente tabelas":
    chunk_type = "table"
elif filter_mode == "Somente legendas/figuras":
    chunk_type = "figure_caption"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Pergunte algo factual sobre STPA."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ex.: What is an unsafe control action?")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.status("Recuperando evidências...", expanded=False):
            result = answer_question(question, chunk_type=chunk_type)
        st.markdown(result["answer"])
        with st.expander("Fontes recuperadas"):
            for idx, source in enumerate(result["sources"], start=1):
                md = source["metadata"]
                st.markdown(
                    f"**Fonte {idx}** — `{md.get('section')}` · pp. "
                    f"`{md.get('page_start')}-{md.get('page_end')}` · parent `{source.get('parent_id')}`"
                )
                text = source["text"]
                st.text(text[:1400] + ("..." if len(text) > 1400 else ""))
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
