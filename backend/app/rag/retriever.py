from app.rag.embeddings import (
    create_query_embedding
)

from app.rag.vector_store import (
    search_documents
)


class Retriever:

    def get_relevant_documents(
        self,
        query,
        k=5
    ):

        query_embedding = (
            create_query_embedding(
                query
            )
        )

        documents = (
            search_documents(
                query_embedding,
                k
            )
        )

        return documents