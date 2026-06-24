from app.rag_core import answer_question, retrieve_parents

QUESTION = "What is an unsafe control action in STPA?"
hits = retrieve_parents(QUESTION)
print(f"Retrieved parents: {len(hits)}")
for idx, hit in enumerate(hits, start=1):
    md = hit["metadata"]
    print(f"{idx}. {md.get('section')} | pp. {md.get('page_start')}-{md.get('page_end')} | distance={hit['distance']:.4f}")
print("\nAnswer:\n")
print(answer_question(QUESTION)["answer"])
