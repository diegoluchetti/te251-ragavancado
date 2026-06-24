Role: You are an experienced AI Engineering.

You are using Cursor + Composer 2.5 to develop the following tool:

"""
You need to develop a Corrective RAG/Graph RAG to work as a backend for a conversation chat anchored to STPA_Handbook.pdf.
The idea is to consume the plan from Tutorial_RAG_Customizada_STPA_Streamlit_2026-1.pdf and develop the project lab_stpa_rag_chatbot as describe in the tutorial pdf. 
"""
### Functional Requirements

- The Ingestion Subsystem shall ingest the STPA_Handbook.pdf file from a designated local input directory.
    
- The Ingestion Subsystem shall segment the ingested document utilizing a Parent Document Retrieval chunking strategy.
    
- The Ingestion Subsystem shall assign chunk_type, section, and pages metadata tags to each generated parent and child chunk.
    
- The Embedding and Storage Subsystem shall generate vector embeddings for each document chunk using the OpenAI text-embedding-3-small model.
    
- The Embedding and Storage Subsystem shall index and store all generated vector embeddings within a local ChromaDB instance.
    
- The RAG Core shall query the local ChromaDB database to retrieve the most relevant document chunks based on a user’s query.
    
- The RAG Core shall extract and include the corresponding section and page numbers from the retrieved metadata within the generated answer.
    
- The RAG Core shall output an explicit refusal message when the retrieved document chunks contain insufficient evidence to answer the user query.
    
- The UI Subsystem shall provide an interactive text input interface to receive user queries.
    
- The UI Subsystem shall present the generated RAG Core response to the user.
    
- The UI Subsystem shall display retrieved source metadata (section and pages) within an expandable user interface panel labeled "Fontes recuperadas".
    
- The Evaluation Subsystem shall execute automated test queries against the RAG Core using the evals/05_run_eval.py script.
    

### Design Constraints and Non-Functional Requirements

- The system shall run entirely on a local workstation environment.
    
- The UI Subsystem shall be implemented using the Streamlit framework.
    
- The Streamlit interface shall be served and accessible on a web browser via localhost:8501.
    
- The software shall run using a Python-based execution runtime environment.
    

### Verification and Delivery Requirements

- The developer shall generate a text report named data/parsed/chunk_report.txt by executing the 02_build_parent_child.py script to verify parent and child chunk creation.
    
- The developer shall capture a screenshot of the local Streamlit UI (running at localhost:8501) demonstrating a valid query, the system response, and an expanded "Fontes recuperadas" panel displaying section and page details.
    
- The developer shall capture a screenshot of the local Streamlit UI demonstrating an out-of-scope query and the system's corresponding explicit refusal.
    
- The developer shall generate the file eval_output.txt by redirecting the terminal output from the execution of python evals/05_run_eval.py (or equivalent command with set PYTHONPATH).


# Instructions

- As mandatory develop a requirement list, spec list, design decisions, verification, validation, requirement traceability matrix *.mds and capture that into obsidian structured well-organized folders.
- The initial plan must occur in waves and iterations. After a wave completion, the obsidian vault must be updated with the results of the validation of the requirements and the evidences. After every integration and validation complete a commit in github must be done and pushed to the repository https://github.com/diegoluchetti/te251-ragavancado
- Obsidian vault must also contains the prompts used in this conversation, in a folder called /development/prompts



------------------------------------------------------------------

# Cursor initial start prompt

You are an experienced AI engineer. Read @rag-avancado/Starting Prompt.md and the documentation on @docs to start building a implementation plan.

For now, after every interaction you must read the obsidian docs first located at folder @rag-avancado 