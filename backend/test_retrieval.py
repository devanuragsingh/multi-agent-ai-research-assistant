from app.rag.retriever import Retriever

retriever = Retriever()

query = (
    "What is cloud computing?"
)

results = (
    retriever.get_relevant_documents(
        query=query,
        k=3
    )
)

print(
    "\nRetrieved Chunks:\n"
)

for i, chunk in enumerate(
    results,
    start=1
):

    print(
        f"\n----- Chunk {i} -----"
    )

    print(chunk)