class AnalysisAgent:

    def analyze_query(
        self,
        query
    ):

        query = query.lower()

        if (
            "summarize" in query
            or "summary" in query
        ):
            return "summary"

        elif (
            "source" in query
            or "citation" in query
            or "reference" in query
        ):
            return "citation"

        else:
            return "question"