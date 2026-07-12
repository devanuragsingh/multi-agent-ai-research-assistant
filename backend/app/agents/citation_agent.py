class CitationAgent:

    def extract_citations(
        self,
        documents,
        max_sources=3
    ):

        citations = []

        for i, doc in enumerate(
            documents[:max_sources]
        ):

            citations.append({
                "chunk": i + 1,
                "text": doc[:100]
            })

        return citations