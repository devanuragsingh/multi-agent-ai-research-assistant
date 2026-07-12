import chromadb
import uuid

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="research_docs"
)


def add_documents(
    chunks,
    embeddings
):

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search_documents(
    query_embedding,
    k=5
):

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=k
    )

    return results["documents"][0]