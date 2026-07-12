class RetrievalAgent:
    def __init__(self, retriever=None):
        self.retriever = retriever

    def retrieve(self, query, k=5):
        return self.retriever.get_relevant_documents(query, k=k)
