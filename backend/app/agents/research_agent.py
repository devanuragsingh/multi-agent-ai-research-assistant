class ResearchAgent:

    def break_down_query(
        self,
        query
    ):

        query = query.lower()

        if "compare" in query:

            parts = query.replace(
                "compare",
                ""
            ).split("and")

            return [
                part.strip()
                for part in parts
                if part.strip()
            ]

        return [query]

    def is_research_query(
        self,
        query
    ):

        query = query.lower()

        keywords = [
            "compare",
            "difference",
            "advantages",
            "disadvantages",
            "versus",
            "vs"
        ]

        return any(
            keyword in query
            for keyword in keywords
        )