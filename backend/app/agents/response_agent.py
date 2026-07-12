class ResponseAgent:

    def combine(
        self,
        answer,
        sources,
        intent
    ):

        return {
            "intent": intent,
            "answer": answer,
            "sources": sources
        }